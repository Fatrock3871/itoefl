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

-- ============ REDAÇÕES PARA CORREÇÃO (2026-10-14) ============
-- Envio de redação com correção assistida. O bloco abaixo é o mesmo de
-- supabase/migrations/20261014_redacoes.sql, que é o arquivo a rodar num
-- banco que já existe. Aqui ele serve a quem monta um projeto do zero. Mudou
-- um, mudar o outro.

-- ============ redações: quem corrige ============
-- Tabela própria, e não uma coluna em `profiles`, de propósito: `profiles`
-- tem policy de update para o próprio aluno (o certificado grava o nome lá),
-- então uma coluna `is_admin` ali poderia ser ligada pelo console do
-- navegador. Aqui não há policy de escrita nenhuma: só se vira corretor por
-- um insert no SQL Editor (ver docs/deploy-redacao.md).

create table if not exists admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table admins enable row level security;

-- cada um só consegue ver a própria linha: é assim que o site descobre se
-- deve mostrar o painel do corretor
drop policy if exists "admins_select_own" on admins;
create policy "admins_select_own" on admins for select using (auth.uid() = user_id);
-- de propósito: nenhuma policy de insert/update/delete pra "authenticated"

-- security definer: a função lê `admins` sem depender da policy acima, e as
-- policies de essay_submissions usam esta função
create or replace function public.is_admin()
returns boolean
language sql
stable
security definer set search_path = public
as $$
  select exists (select 1 from admins where user_id = auth.uid());
$$;

revoke all on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated, service_role;

-- ============ redações: os envios ============

create table if not exists essay_submissions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  topic_id text not null check (topic_id in ('E1','E2','E3','E4','E5','D1','D2','D3','D4','D5')),
  task text not null check (task in ('email', 'discussion')),
  text text not null check (char_length(text) between 1 and 5000),
  word_count int not null check (word_count between 1 and 600),
  seconds_used int not null check (seconds_used between 0 and 600),
  consented_at timestamptz,                -- consentimento LGPD, gravado no 1º envio
  submitted_at timestamptz not null default now(),
  due_on date not null,                    -- devolução prevista: 3 dias úteis
  status text not null default 'na_fila' check (status in ('na_fila', 'em_correcao', 'devolvida')),
  -- devolutiva: os 4 critérios de 0 a 5 (meio ponto), a nota final e o nível
  -- calculados pela function review-essay, e o resto do retorno em JSON
  score_task numeric(2,1) check (score_task between 0 and 5),
  score_organization numeric(2,1) check (score_organization between 0 and 5),
  score_grammar numeric(2,1) check (score_grammar between 0 and 5),
  score_vocabulary numeric(2,1) check (score_vocabulary between 0 and 5),
  final_score numeric(2,1) check (final_score between 0 and 5),
  level text,
  feedback jsonb,
  graded_by uuid references auth.users(id) on delete set null,
  returned_at timestamptz,
  constraint essay_task_matches_topic check ((task = 'email') = (topic_id like 'E%')),
  constraint essay_returned_is_complete check (
    status <> 'devolvida' or (final_score is not null and feedback is not null and returned_at is not null)
  )
);

comment on table essay_submissions is
  'Redações enviadas para correção assistida. Apagadas junto com a conta (on delete cascade).';

-- a fila do corretor ordena pelo prazo; o aluno lê o próprio histórico
create index if not exists essay_submissions_queue_idx on essay_submissions (status, due_on, submitted_at);
create index if not exists essay_submissions_user_idx on essay_submissions (user_id, submitted_at desc);

alter table essay_submissions enable row level security;

-- o aluno lê só as próprias; o corretor lê todas
drop policy if exists "essays_select_own_or_admin" on essay_submissions;
create policy "essays_select_own_or_admin" on essay_submissions
  for select using (auth.uid() = user_id or public.is_admin());
-- de propósito: nenhuma policy de insert/update/delete pra "authenticated".
-- Envio e devolução passam pelas edge functions (service_role).

-- ============ redações: entrada de um envio ============
-- Chamada só pela submit-essay, depois de ela conferir acesso pago, tamanho e
-- mínimo de palavras. A trava por conta impede que dois cliques no mesmo
-- segundo passem os dois pelo intervalo de 4 dias.

create or replace function public.create_essay_submission(
  p_user uuid,
  p_topic text,
  p_task text,
  p_text text,
  p_words int,
  p_seconds int,
  p_due date,
  p_consent boolean
)
returns essay_submissions
language plpgsql
security definer set search_path = public
as $$
declare
  v_last timestamptz;
  v_row essay_submissions;
begin
  perform pg_advisory_xact_lock(hashtext('essay:' || p_user::text));

  select max(submitted_at) into v_last from essay_submissions where user_id = p_user;
  if v_last is not null and v_last > now() - interval '4 days' then
    raise exception 'intervalo: proximo envio em %', v_last + interval '4 days'
      using errcode = 'P0001';
  end if;
  -- o consentimento é pedido no 1º envio
  if v_last is null and not coalesce(p_consent, false) then
    raise exception 'consentimento: o primeiro envio exige consentimento' using errcode = 'P0001';
  end if;

  insert into essay_submissions (user_id, topic_id, task, text, word_count, seconds_used, consented_at, due_on)
  values (p_user, p_topic, p_task, p_text, p_words, p_seconds,
          case when p_consent then now() end, p_due)
  returning * into v_row;
  return v_row;
end;
$$;

revoke all on function public.create_essay_submission(uuid, text, text, text, int, int, date, boolean) from public, anon, authenticated;
grant execute on function public.create_essay_submission(uuid, text, text, text, int, int, date, boolean) to service_role;

-- ============ consultas úteis (não fazem parte da migração) ============
-- Tornar uma conta corretora (troque o e-mail):
--   insert into admins (user_id)
--   select id from auth.users where email = 'voce@exemplo.com'
--   on conflict do nothing;
-- Tirar o papel de corretor:
--   delete from admins where user_id = (select id from auth.users where email = 'voce@exemplo.com');
-- Fila do dia:
--   select id, topic_id, status, submitted_at, due_on from essay_submissions
--   where status <> 'devolvida' order by due_on, submitted_at;
-- Apagar um envio de teste (libera o intervalo de 4 dias da conta):
--   delete from essay_submissions where id = '<uuid do envio>';

-- ============ PAGAMENTO PELO STRIPE (2026-10-18) ============
-- Planos Mensal (assinatura) e Vitalício. O bloco abaixo é o mesmo de
-- supabase/migrations/20261018_stripe.sql, que é o arquivo a rodar num
-- projeto que já existe. Regras no cabeçalho da migração.

-- ============ payments: período pago da assinatura ============

alter table payments add column if not exists period_end timestamptz;

comment on column payments.period_end is
  'Fim do periodo pago por esta fatura (assinatura Mensal). null nos pagamentos unicos.';
comment on column entitlements.plan is
  'Plano do ultimo pagamento que contou: mensal, vitalicio; ou sprint, standard, premium, legado (antigos).';

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
  v_end timestamptz;
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
    if r.days is null and r.period_end is null then
      v_lifetime := true;
      v_plan := r.plan;
    elsif not v_lifetime then
      if r.period_end is not null then
        -- assinatura: vale até o fim do período pago, com 1 dia de tolerância
        v_end := r.period_end + interval '1 day';
        v_expires := greatest(coalesce(v_expires, v_end), v_end);
      else
        -- plano antigo com dias: soma ao fim do prazo que ainda valia
        v_expires := greatest(coalesce(v_expires, r.approved_at), r.approved_at)
                     + make_interval(days => r.days);
      end if;
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
-- cancelar a assinatura quando a conta é excluída ou compra o Vitalício.

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
--   select public.apply_payment('manual-2026-10-18-fulano', '<uuid>', 'mensal', null, 0,
--                               'approved', now(), now() + interval '30 days');
