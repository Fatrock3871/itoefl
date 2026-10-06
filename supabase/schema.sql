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

-- ============ LOGIN POR NOME DE USUÁRIO (2026-09-17) ============
-- Troca o "entrar por link no e-mail" por usuário+senha de verdade. O
-- Supabase Auth só autentica por e-mail (ou telefone), não por username --
-- então o login por usuário funciona resolvendo username -> e-mail aqui no
-- banco (função abaixo) e chamando signInWithPassword com o e-mail
-- encontrado. O cadastro continua pedindo e-mail (fica em auth.users,
-- exige confirmação antes do primeiro login) + usuário + senha.

alter table profiles add column if not exists username text;

drop index if exists profiles_username_unique;
create unique index profiles_username_unique
  on profiles (lower(username)) where username is not null;

alter table profiles drop constraint if exists profiles_username_format;
alter table profiles add constraint profiles_username_format
  check (username is null or username ~ '^[a-z0-9_]{3,20}$');

-- Resolve username -> e-mail. SECURITY DEFINER pra poder ler auth.users
-- (RLS de `profiles` só libera o dono ler a própria linha, e isso
-- precisa funcionar ANTES do login, sem sessão nenhuma). Fica exposta a
-- anon de propósito -- é o único jeito do formulário de login funcionar
-- com usuário em vez de e-mail. Risco aceito: alguém pode usar isso pra
-- descobrir SE um username existe (não descobre a senha, nem pode logar
-- sem ela) -- razoável pra um app de uso pessoal/pequena escala.
create or replace function public.email_for_username(uname text)
returns text
language sql
security definer
set search_path = public
as $$
  select u.email
  from auth.users u
  join public.profiles p on p.id = u.id
  where lower(p.username) = lower(uname)
  limit 1;
$$;

revoke all on function public.email_for_username(text) from public;
grant execute on function public.email_for_username(text) to anon, authenticated;

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
