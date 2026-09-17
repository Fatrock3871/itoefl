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
