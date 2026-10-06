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
