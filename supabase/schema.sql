-- iTOEFL — schema do MVP (sincronização de progresso do aluno)
--
-- Rode este arquivo no SQL Editor do Supabase (Dashboard > SQL Editor > New query).
-- Ele cria só o necessário para contas de aluno + progresso sincronizado entre
-- dispositivos. O conteúdo dos módulos continua vindo do build (artifact/index.html);
-- não é servido pelo banco.
--
-- Se um dia você quiser servir o conteúdo do banco (editar sem rebuild), rode
-- também schema-content-optional.sql e popule com content-seed-optional.json.

-- ============ PERFIL ============

create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

-- ============ ESTADO DO ALUNO (uma linha por usuário, um blob JSON) ============
-- state guarda as chaves localStorage sincronizáveis (progresso, SRS, drills, quiz).
-- Preferências de dispositivo (tema, aba ativa, preset do cronômetro) NÃO entram aqui.

create table if not exists user_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- ============ ROW LEVEL SECURITY ============

alter table profiles enable row level security;
alter table user_state enable row level security;

drop policy if exists "profiles_select_own" on profiles;
drop policy if exists "profiles_insert_own" on profiles;
drop policy if exists "profiles_update_own" on profiles;
create policy "profiles_select_own" on profiles for select using (auth.uid() = id);
create policy "profiles_insert_own" on profiles for insert with check (auth.uid() = id);
create policy "profiles_update_own" on profiles for update using (auth.uid() = id);

drop policy if exists "user_state_select_own" on user_state;
drop policy if exists "user_state_insert_own" on user_state;
drop policy if exists "user_state_update_own" on user_state;
create policy "user_state_select_own" on user_state for select using (auth.uid() = user_id);
create policy "user_state_insert_own" on user_state for insert with check (auth.uid() = user_id);
create policy "user_state_update_own" on user_state for update using (auth.uid() = user_id);

-- ============ CRIAÇÃO AUTOMÁTICA DO PERFIL NO SIGNUP ============

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id) values (new.id)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============ ACESSO PAGO (2026-09-17) ============
-- Tabela separada de `profiles` de propósito: o aluno pode LER sua própria
-- linha (pra saber se já pagou), mas não existe nenhuma policy de insert/
-- update para o papel "authenticated" -- com RLS ligado e sem essas
-- policies, a escrita fica bloqueada por padrão. Só o service_role (usado
-- pela edge function mp-webhook, nunca exposto ao navegador) grava aqui.
-- Sem isso, um aluno poderia soltar `supabase.from('profiles').update(...)`
-- no console do navegador e se autoliberar.

create table if not exists entitlements (
  user_id uuid primary key references auth.users(id) on delete cascade,
  paid boolean not null default false,
  paid_at timestamptz,
  mp_payment_id text,
  updated_at timestamptz not null default now()
);

alter table entitlements enable row level security;

drop policy if exists "entitlements_select_own" on entitlements;
create policy "entitlements_select_own" on entitlements for select using (auth.uid() = user_id);
-- de propósito: nenhuma policy de insert/update/delete pra "authenticated"

-- ============ LIMPEZA DO LOGIN POR NOME DE USUÁRIO (2026-10-06) ============
-- O login por nome de usuário existiu entre 2026-09-17 e 2026-09-22 e foi
-- revertido: hoje o site só autentica por e-mail. Este bloco remove o que
-- aquela versão criou no banco (a função que traduzia usuário em e-mail
-- ficava exposta a `anon` sem necessidade). Em projeto novo, onde nada disso
-- existe, os comandos abaixo não fazem nada.

drop function if exists public.email_for_username(text);
drop index if exists profiles_username_unique;
alter table profiles drop constraint if exists profiles_username_format;
alter table profiles drop column if exists username;

-- ============ CUPONS DE DESCONTO (2026-09-24) ============
-- Cupons percentuais aplicados no checkout (`create-checkout`, que roda com
-- o token do próprio aluno, não com o service_role -- por isso a policy de
-- select abaixo é necessária: sem ela, RLS bloquearia a leitura mesmo de
-- cupons ativos). Só percentual (sem valor fixo), sem data de expiração nem
-- limite de usos -- controle é só o campo `active`: crie a linha pra ligar
-- o cupom, ponha `active=false` (ou apague a linha) pra desligar. Só o
-- service_role escreve aqui (nenhuma policy de insert/update/delete pra
-- "authenticated"); criar/editar cupons é feito pelo SQL Editor do Supabase.

create table if not exists coupons (
  code text primary key,
  percent int not null check (percent > 0 and percent <= 100),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

alter table coupons enable row level security;

drop policy if exists "coupons_select_active" on coupons;
create policy "coupons_select_active" on coupons
  for select using (active = true);
-- de propósito: nenhuma policy de insert/update/delete pra "authenticated"

-- Exemplo de como criar um cupom (rode no SQL Editor, ajustando código/%):
--   insert into coupons (code, percent) values ('LANCAMENTO20', 20);
-- Pra desligar sem apagar o histórico:
--   update coupons set active = false where code = 'LANCAMENTO20';

-- ============ PLANOS COM PRAZO (2026-10-08) ============
-- Três planos: Sprint (30 dias), Standard (90 dias) e Premium (sem prazo).
-- Preço e prazo de cada um ficam em supabase/functions/_shared/plans.ts.
-- O bloco abaixo é o mesmo de supabase/migrations/20261008_planos.sql, que é
-- o arquivo a rodar num banco que já existe. Aqui ele serve a quem monta um
-- projeto do zero. Mudou um, mudar o outro.
--
-- A REGRA (uma só, usada em compra, renovação, troca de plano e reembolso):
-- `entitlements` é sempre recalculada do extrato em `payments`, lendo os
-- pagamentos aprovados do mais antigo para o mais novo.
--   1. Plano com prazo: os dias contam a partir do fim do acesso que a conta
--      ainda tem, ou da data do pagamento se o acesso já venceu ou nunca
--      existiu. Renovar antes de vencer SOMA.
--   2. Plano sem prazo (Premium): o acesso passa a não ter fim. Os dias que
--      restavam de um plano com prazo não viram crédito.
--   3. Quem já tem acesso sem prazo não ganha nada comprando plano com prazo
--      (o create-checkout recusa essa compra antes de cobrar).
--   4. Reembolso ou chargeback: o pagamento sai da conta e o prazo é
--      recalculado só com os que sobraram. Sem nenhum, o acesso termina.
--   5. O mesmo pagamento avisado duas vezes não soma dias duas vezes.

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
