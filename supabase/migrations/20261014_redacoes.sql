-- iTOEFL: envio de redação para correção (2026-10-14)
--
-- Rodar no SQL Editor de um projeto que JÁ TEM o schema.sql e a migração
-- 20261008_planos.sql. O passo a passo completo, com o teste de ponta a
-- ponta, está em docs/deploy-redacao.md. Rodar duas vezes não estraga nada.
--
-- O que este arquivo cria:
--   1. `admins`: quem pode corrigir. Ninguém entra aqui pelo site.
--   2. `essay_submissions`: as redações enviadas e as devolutivas.
--   3. `create_essay_submission`: a única porta de entrada de uma redação,
--      chamada pela edge function submit-essay com a service_role.
--
-- Quem escreve em cada tabela:
--   - aluno: NADA direto. Envia pela function submit-essay, que confere
--     acesso pago, intervalo de 4 dias, tamanho e mínimo de palavras.
--   - corretor (linha em `admins`): lê todas as redações. Muda o estado e
--     devolve pela function review-essay, que confere de novo se ele é
--     corretor e se a devolutiva está no formato.
--   - service_role (as functions): o resto.
-- Por isso não existe nenhuma policy de insert, update ou delete para o papel
-- "authenticated" nas duas tabelas.
--
-- O corpo abaixo (da primeira seção em diante) está copiado igual no fim de
-- supabase/schema.sql, para quem monta um projeto do zero. Mudou um, mudar o
-- outro: o smoke test reprova se divergirem.

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
