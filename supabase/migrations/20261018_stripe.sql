-- iTOEFL: pagamento pelo Stripe, planos Mensal, 60 dias, 90 dias e Anual (2026-10-18)
--
-- ESTE ARQUIVO FOI ESCRITO E NUNCA EXECUTADO. Rodar SQL no Supabase exige
-- autorização explícita do dono (AGENTS.md). Ordem e passo a passo em
-- docs/publicar.md. Depende de 20261008_planos.sql já aplicado. O mesmo
-- conteúdo está no fim de supabase/schema.sql, para quem monta do zero.
--
-- Pode ser rodado mais de uma vez: tudo é "if not exists", "create or
-- replace", "drop ... if exists" ou "on conflict".
--
-- O que muda:
--   payments        ganha period_end: marca a fatura da assinatura e diz até onde ela pagou
--   apply_payment() ganha p_period_end (opcional; o mp-webhook não muda)
--   recompute_entitlement() passa a entender pagamento de assinatura
--   billing         tabela nova: cliente e assinatura do Stripe de cada conta
--   apply_billing() grava a situação da assinatura, ignorando aviso atrasado
--   stripe_events   tabela nova: eventos do Stripe já processados
--
-- A REGRA continua uma só: `entitlements` é recalculada do extrato em
-- `payments`. O que entra de novo:
--   6. Planos de pagamento único (60 dias, 90 dias, Anual de 365 dias), no
--      cartão pelo Stripe ou no Pix pelo Mercado Pago: linha com days e sem
--      period_end. Seguem a regra 1: os dias somam ao fim do acesso que a
--      conta ainda tem, então comprar outro plano antes de vencer não perde
--      nenhum dia.
--   7. Fatura paga da assinatura Mensal: linha com days = duração do período
--      pago (28 a 31 dias) e period_end. Entra na MESMA soma da regra 1, então
--      quem assina o Mensal com dias sobrando de outro plano não perde nada.
--      Se a última linha que contou for de assinatura, o acesso ganha 1 dia
--      de tolerância (a renovação é cobrada logo depois do fim do período e o
--      aviso do Stripe pode levar alguns minutos). A mesma fatura avisada
--      duas vezes não vira dois meses: a chave é o id da fatura.
--   8. Cancelar a assinatura não tira nada: o acesso vai até o fim do que já
--      foi pago. Só reembolso tira (regra 4), e aí o pagamento sai da conta.
--   9. Linha sem days continua valendo como acesso sem prazo: só existe para
--      compras antigas (Premium e legado). Nenhum plano novo grava assim.
--
-- Ids gravados em payments.mp_payment_id (o nome da coluna ficou do Mercado
-- Pago; trocar exigiria reescrever as funções e o histórico):
--   número puro     pagamento do Mercado Pago (Pix de um plano de dias)
--   stripe:in_...   fatura paga da assinatura Mensal
--   stripe:pi_...   pagamento único de um plano de dias no cartão

-- ============ payments: período pago da assinatura ============

alter table payments add column if not exists period_end timestamptz;

comment on column payments.period_end is
  'Fim do periodo pago por esta fatura (assinatura Mensal). null nos pagamentos unicos. Os dias da fatura estao em days.';
comment on column entitlements.plan is
  'Plano do ultimo pagamento que contou: mensal, 60dias, 90dias, anual; ou sprint, standard, premium, legado (antigos).';

-- ============ recalcular o acesso de uma conta a partir do extrato ============

create or replace function public.recompute_entitlement(p_user uuid)
returns void
language plpgsql
security definer set search_path = public
as $$
declare
  r record;
  v_any boolean := false;
  v_lifetime boolean := false;
  v_expires timestamptz := null;
  v_plan text := null;
  v_first timestamptz := null;
  v_last_id text := null;
  v_sub_last boolean := false;
begin
  -- uma conta por vez: dois avisos simultâneos para o mesmo aluno não podem
  -- ler o extrato pela metade
  perform pg_advisory_xact_lock(hashtext(p_user::text));

  for r in
    select * from payments
    where user_id = p_user and status = 'approved'
    order by approved_at, mp_payment_id
  loop
    v_any := true;
    v_first := coalesce(v_first, r.approved_at);
    v_last_id := r.mp_payment_id;
    if r.days is null then
      -- compra antiga sem prazo (Premium, legado)
      v_lifetime := true;
      v_plan := r.plan;
    elsif not v_lifetime then
      -- plano de dias ou mês da assinatura: soma ao fim do prazo que ainda
      -- valia; se já tinha vencido (ou é o primeiro), conta da data do pagamento
      v_expires := greatest(coalesce(v_expires, r.approved_at), r.approved_at)
                   + make_interval(days => r.days);
      v_sub_last := r.period_end is not null;
      v_plan := r.plan;
    end if;
  end loop;

  if not v_any then
    update entitlements
      set paid = false, plan = null, expires_at = null, updated_at = now()
      where user_id = p_user;
    return;
  end if;

  insert into entitlements (user_id, paid, paid_at, mp_payment_id, plan, expires_at, updated_at)
  values (p_user, true, v_first, v_last_id, v_plan,
          case when v_lifetime then null
               when v_sub_last then v_expires + interval '1 day'  -- tolerância da renovação
               else v_expires end, now())
  on conflict (user_id) do update set
    paid = true,
    paid_at = excluded.paid_at,
    mp_payment_id = excluded.mp_payment_id,
    plan = excluded.plan,
    expires_at = excluded.expires_at,
    updated_at = now();
end;
$$;

-- ============ registrar um pagamento (ou o reembolso dele) ============
-- Chamada pelo stripe-webhook e pelo mp-webhook. p_status: 'approved' ou
-- 'refunded'. Repetir a chamada com os mesmos dados não muda nada.
-- A versão antiga, sem p_period_end, sai: com as duas no banco, a API não
-- saberia qual chamar.

drop function if exists public.apply_payment(text, uuid, text, int, numeric, text, timestamptz);

create or replace function public.apply_payment(
  p_payment_id text,
  p_user uuid,
  p_plan text,
  p_days int,
  p_amount numeric,
  p_status text,
  p_approved_at timestamptz,
  p_period_end timestamptz default null
)
returns void
language plpgsql
security definer set search_path = public
as $$
declare
  v_user uuid;
begin
  if p_status not in ('approved', 'refunded') then
    raise exception 'status invalido: %', p_status;
  end if;

  if p_status = 'refunded' then
    -- reembolso de pagamento que nunca foi registrado: nada a desfazer
    update payments set status = 'refunded', updated_at = now()
      where mp_payment_id = p_payment_id
      returning user_id into v_user;
    if v_user is null then
      return;
    end if;
  else
    -- o que foi gravado na primeira vez não é reescrito por aviso repetido,
    -- e pagamento já reembolsado não volta a valer por aviso atrasado
    insert into payments (mp_payment_id, user_id, plan, days, amount, status, approved_at, period_end)
    values (p_payment_id, p_user, p_plan, p_days, p_amount, 'approved', coalesce(p_approved_at, now()), p_period_end)
    on conflict (mp_payment_id) do nothing;
    select user_id into v_user from payments where mp_payment_id = p_payment_id;
  end if;

  perform public.recompute_entitlement(v_user);
end;
$$;

revoke all on function public.recompute_entitlement(uuid) from public, anon, authenticated;
revoke all on function public.apply_payment(text, uuid, text, int, numeric, text, timestamptz, timestamptz) from public, anon, authenticated;
grant execute on function public.recompute_entitlement(uuid) to service_role;
grant execute on function public.apply_payment(text, uuid, text, int, numeric, text, timestamptz, timestamptz) to service_role;

-- ============ billing: cliente e assinatura do Stripe ============
-- Uma linha por conta que já abriu um pagamento no Stripe. Não decide
-- acesso (quem decide é payments -> entitlements): serve para o "Gerenciar
-- assinatura" de Minha conta, para recusar uma segunda assinatura e para
-- cancelar a assinatura quando a conta é excluída ou pede reembolso.

create table if not exists billing (
  user_id uuid primary key references auth.users(id) on delete cascade,
  stripe_customer_id text unique,
  subscription_id text,
  subscription_status text,          -- como o Stripe diz: active, past_due, canceled, incomplete...
  cancel_at_period_end boolean not null default false,
  current_period_end timestamptz,
  event_at timestamptz,              -- quando esta situação foi lida da API do Stripe
  updated_at timestamptz not null default now()
);

alter table billing enable row level security;

-- o aluno lê a própria linha; ninguém além do service_role escreve
drop policy if exists "billing_select_own" on billing;
create policy "billing_select_own" on billing for select using (auth.uid() = user_id);

-- grava a situação da assinatura. O Stripe não garante a ordem dos avisos,
-- e o stripe-webhook relê a assinatura na API: uma leitura mais antiga que
-- a última gravada não sobrescreve nada. Campo
-- null não apaga o que já havia (o checkout só sabe o cliente, por exemplo).
create or replace function public.apply_billing(
  p_user uuid,
  p_customer text,
  p_subscription text,
  p_status text,
  p_cancel_at_period_end boolean,
  p_period_end timestamptz,
  p_event_at timestamptz
)
returns void
language plpgsql
security definer set search_path = public
as $$
begin
  insert into billing (user_id, stripe_customer_id, subscription_id, subscription_status,
                       cancel_at_period_end, current_period_end, event_at, updated_at)
  values (p_user, p_customer, p_subscription, p_status,
          coalesce(p_cancel_at_period_end, false), p_period_end, p_event_at, now())
  on conflict (user_id) do update set
    stripe_customer_id = coalesce(excluded.stripe_customer_id, billing.stripe_customer_id),
    subscription_id = coalesce(excluded.subscription_id, billing.subscription_id),
    subscription_status = coalesce(excluded.subscription_status, billing.subscription_status),
    cancel_at_period_end = case when p_cancel_at_period_end is null then billing.cancel_at_period_end
                                else excluded.cancel_at_period_end end,
    current_period_end = coalesce(excluded.current_period_end, billing.current_period_end),
    event_at = greatest(excluded.event_at, billing.event_at),
    updated_at = now()
  where billing.event_at is null or excluded.event_at is null or excluded.event_at >= billing.event_at;
end;
$$;

revoke all on function public.apply_billing(uuid, text, text, text, boolean, timestamptz, timestamptz) from public, anon, authenticated;
grant execute on function public.apply_billing(uuid, text, text, text, boolean, timestamptz, timestamptz) to service_role;

-- ============ stripe_events: avisos já processados ============
-- O Stripe pode mandar o mesmo evento mais de uma vez. O stripe-webhook só
-- grava o id aqui depois de processar tudo; um evento já gravado é
-- respondido com 200 sem refazer nada. As gravações em si também são
-- idempotentes (apply_payment e apply_billing), então um erro no meio do
-- caminho só faz o Stripe tentar de novo.

create table if not exists stripe_events (
  id text primary key,
  type text not null,
  processed_at timestamptz not null default now()
);

alter table stripe_events enable row level security;
-- de propósito: nenhuma policy. Só o service_role lê e escreve.

-- ============ consultas úteis (não fazem parte da migração) ============
-- Situação da assinatura de uma conta:
--   select * from billing where user_id = '<uuid>';
-- Últimos eventos do Stripe processados:
--   select * from stripe_events order by processed_at desc limit 20;
-- Dar um mês na mão (cortesia), sem passar pelo Stripe:
--   select public.apply_payment('manual-2026-10-18-fulano', '<uuid>', '60dias', 60, 0,
--                               'approved', now(), null);
