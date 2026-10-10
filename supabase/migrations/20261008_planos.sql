-- iTOEFL: três planos de preço com prazo (2026-10-08)
--
-- ESTE ARQUIVO FOI ESCRITO E NUNCA EXECUTADO. Rodar SQL no Supabase exige
-- autorização explícita do dono (AGENTS.md). Passo a passo e ordem em
-- docs/deploy-planos.md. O mesmo conteúdo está em supabase/schema.sql, para
-- quem monta um projeto do zero.
--
-- Pode ser rodado mais de uma vez sem estragar nada: tudo aqui é
-- "if not exists", "create or replace" ou "on conflict do nothing".
--
-- O que muda:
--   entitlements   ganha `plan` e `expires_at` (null = sem prazo)
--   payments       tabela nova: uma linha por pagamento aprovado (o extrato)
--   funções        apply_payment() e recompute_entitlement(), só service_role
--
-- A REGRA (uma só, usada em compra, renovação, troca de plano e reembolso):
-- `entitlements` é sempre recalculada do extrato em `payments`, lendo os
-- pagamentos aprovados do mais antigo para o mais novo.
--   1. Plano com prazo (Sprint 30 dias, Standard 90 dias): os dias contam a
--      partir do fim do acesso que a conta ainda tem, ou da data do pagamento
--      se o acesso já venceu ou nunca existiu. Renovar antes de vencer SOMA,
--      não desperdiça os dias que restavam.
--   2. Plano sem prazo (Premium): o acesso passa a não ter fim. Os dias que
--      restavam de um plano com prazo deixam de importar e não viram crédito.
--   3. Quem já tem acesso sem prazo não ganha nada comprando plano com prazo
--      (o create-checkout recusa essa compra antes de cobrar).
--   4. Reembolso ou chargeback: o pagamento sai da conta e o prazo é
--      recalculado só com os que sobraram. Sem nenhum, o acesso termina.
--   5. O mesmo pagamento avisado duas vezes pelo Mercado Pago não soma dias
--      duas vezes: a chave de `payments` é o id do pagamento.

-- ============ entitlements: plano e validade ============

alter table entitlements add column if not exists plan text;
alter table entitlements add column if not exists expires_at timestamptz;

comment on column entitlements.paid is
  'true se a conta tem ao menos um pagamento aprovado. Sozinho NAO quer dizer acesso liberado: conferir expires_at.';
comment on column entitlements.plan is
  'Plano do ultimo pagamento que contou: sprint, standard, premium, ou legado (compra anterior aos planos).';
comment on column entitlements.expires_at is
  'Fim do acesso. null = sem prazo (Premium e compras antigas).';

-- ============ payments: o extrato ============

create table if not exists payments (
  mp_payment_id text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  plan text not null,
  days int check (days is null or days > 0),        -- null = sem prazo
  amount numeric(10,2),                              -- valor pago, já com cupom
  status text not null default 'approved' check (status in ('approved', 'refunded')),
  approved_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists payments_user_idx on payments (user_id, approved_at);

alter table payments enable row level security;

-- o aluno pode ler os próprios pagamentos; ninguém além do service_role escreve
drop policy if exists "payments_select_own" on payments;
create policy "payments_select_own" on payments for select using (auth.uid() = user_id);
-- de propósito: nenhuma policy de insert/update/delete pra "authenticated"

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
begin
  -- uma conta por vez: dois avisos simultâneos do Mercado Pago para o mesmo
  -- aluno não podem ler o extrato pela metade
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
      v_lifetime := true;
      v_plan := r.plan;
    elsif not v_lifetime then
      -- soma ao fim do prazo que ainda valia na data deste pagamento; se já
      -- tinha vencido (ou é o primeiro), conta da data do pagamento
      v_expires := greatest(coalesce(v_expires, r.approved_at), r.approved_at)
                   + make_interval(days => r.days);
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
          case when v_lifetime then null else v_expires end, now())
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
-- Chamada pelo mp-webhook. p_status: 'approved' ou 'refunded'.
-- Repetir a chamada com os mesmos dados não muda nada.

create or replace function public.apply_payment(
  p_payment_id text,
  p_user uuid,
  p_plan text,
  p_days int,
  p_amount numeric,
  p_status text,
  p_approved_at timestamptz
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
    -- o que foi gravado na primeira vez (de quem é, qual plano, quando) não
    -- é reescrito por um aviso repetido. Um pagamento já reembolsado também
    -- não volta a valer por causa de um aviso "approved" atrasado.
    insert into payments (mp_payment_id, user_id, plan, days, amount, status, approved_at)
    values (p_payment_id, p_user, p_plan, p_days, p_amount, 'approved', coalesce(p_approved_at, now()))
    on conflict (mp_payment_id) do nothing;
    select user_id into v_user from payments where mp_payment_id = p_payment_id;
  end if;

  perform public.recompute_entitlement(v_user);
end;
$$;

-- só o service_role (edge function mp-webhook) chama as duas. Sem isto, o
-- Supabase deixaria qualquer aluno logado chamar apply_payment() pela API e
-- se dar acesso.
revoke all on function public.recompute_entitlement(uuid) from public, anon, authenticated;
revoke all on function public.apply_payment(text, uuid, text, int, numeric, text, timestamptz) from public, anon, authenticated;
grant execute on function public.recompute_entitlement(uuid) to service_role;
grant execute on function public.apply_payment(text, uuid, text, int, numeric, text, timestamptz) to service_role;

-- ============ quem já tinha pago antes dos planos ============
-- Compras do preço único antigo eram acesso vitalício e continuam sendo:
-- entram no extrato como plano "legado", sem prazo. A linha de entitlements
-- delas não é tocada (paid = true e expires_at null já quer dizer sem prazo).

insert into payments (mp_payment_id, user_id, plan, days, amount, status, approved_at)
select coalesce(e.mp_payment_id, 'legado-' || e.user_id::text), e.user_id, 'legado', null, null,
       'approved', coalesce(e.paid_at, e.updated_at, now())
from entitlements e
where e.paid
on conflict (mp_payment_id) do nothing;

update entitlements set plan = 'legado' where paid and plan is null;

-- ============ consultas úteis (não fazem parte da migração) ============
-- Dar acesso na mão (cortesia, teste), sem passar pelo Mercado Pago:
--   select public.apply_payment('manual-2026-10-08-fulano', '<uuid do usuário>',
--                               'standard', 90, 0, 'approved', now());
-- Desfazer:
--   select public.apply_payment('manual-2026-10-08-fulano', null, null, null, null, 'refunded', null);
-- Ver o extrato e a situação de uma conta:
--   select * from payments where user_id = '<uuid>' order by approved_at;
--   select * from entitlements where user_id = '<uuid>';
