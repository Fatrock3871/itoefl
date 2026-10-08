-- iTOEFL — banco de questões (Etapa 2 do ROADMAP)
--
-- ESTE ARQUIVO AINDA NÃO FOI EXECUTADO EM BANCO NENHUM (escrito em 2026-10-07).
-- Rodar SQL no Supabase exige autorização explícita do dono (AGENTS.md).
-- Antes de rodar em produção, testar num projeto de rascunho ou numa branch
-- do Supabase. Depende de `schema.sql` já aplicado (usa `entitlements`).
--
-- Cria duas tabelas:
--   items     os itens do banco, espelho de bank/items/**/*.json (a fonte da
--             verdade continua sendo o arquivo no Git; a tabela é publicação)
--   attempts  uma linha por resposta do aluno a um item
--
-- É aqui que o conteúdo pago passa a ser protegido de verdade: a leitura de
-- `items` só é liberada por RLS a quem tem `entitlements.paid = true`. Hoje o
-- bloqueio do site é só visual, porque o conteúdo vai embutido no HTML.

-- ============ QUEM PAGOU ============
-- Função única usada pelas policies abaixo. `security definer` para ler
-- `entitlements` sem depender da policy daquela tabela, e `stable` para o
-- Postgres poder avaliar uma vez por consulta, não uma vez por linha.

create or replace function public.has_paid_access()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from entitlements e
    where e.user_id = auth.uid() and e.paid
  );
$$;

revoke all on function public.has_paid_access() from public;
grant execute on function public.has_paid_access() to authenticated;

-- ============ ITENS ============
-- Os campos seguem bank/schema/item.schema.json (ver bank/README.md). Colunas
-- próprias para o que entra em filtro do modo prática (seção, tipo, formato,
-- nível, grupo, estado, etiquetas); jsonb para o que só é exibido.
-- `options` e `answer` guardam a letra de ORIGEM: quem mostrar o item precisa
-- embaralhar a ordem das alternativas, como o app.js já faz.

create table if not exists items (
  id            text primary key check (id ~ '^[a-z0-9]+([-.][a-z0-9]+)*$'),
  section       text not null check (section in ('reading', 'listening', 'writing', 'speaking', 'general')),
  task_type     text not null,
  exam_format   boolean not null,
  format        text not null check (format in ('mcq', 'multi_select', 'fill_words', 'build_sentence')),
  select_count  integer check (select_count is null or select_count >= 2),
  skill         text,
  cefr_min      text check (cefr_min in ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')),
  cefr_max      text check (cefr_max in ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')),
  stimulus      jsonb,
  group_id      text,
  prompt        text not null,
  text_format   text not null check (text_format in ('plain', 'html', 'markdown')),
  options       jsonb,
  answer        jsonb not null,
  explanation   text not null default '',
  hint          text,
  trap_codes    text[] not null default '{}',
  tags          text[] not null default '{}',
  status        text not null default 'rascunho' check (status in ('rascunho', 'revisado', 'publicado')),
  source        jsonb,
  updated_at    timestamptz not null default now(),
  check ((cefr_min is null) = (cefr_max is null))
);

create index if not exists items_filter_idx on items (section, task_type, status);
create index if not exists items_group_idx on items (group_id);
create index if not exists items_tags_idx on items using gin (tags);

alter table items enable row level security;

-- Só quem pagou lê, e só o que está publicado. Rascunho e revisado ficam
-- invisíveis para o aluno mesmo que subam para a tabela por engano.
drop policy if exists "items_select_paid_published" on items;
create policy "items_select_paid_published" on items
  for select to authenticated
  using (status = 'publicado' and public.has_paid_access());
-- de propósito: nenhuma policy de insert/update/delete. Só o service_role
-- (o script de publicação do banco, que ainda não existe) escreve aqui.

-- ============ TENTATIVAS ============
-- Uma linha por resposta. Ficam fora do blob `user_state` porque cresceriam
-- sem limite. `answer` é o que o aluno respondeu, na mesma forma do campo
-- `answer` do item: letra de origem em mcq, lista de letras em ordem
-- alfabética em multi_select, lista de palavras em fill_words, lista de
-- blocos em build_sentence.
-- `item_id` não tem "on delete cascade": item publicado não se apaga (o id é
-- estável), tira-se do ar mudando `status`.

create table if not exists attempts (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  item_id     text not null references items(id),
  answer      jsonb not null,
  correct     boolean not null default false,
  time_ms     integer check (time_ms is null or time_ms >= 0),
  created_at  timestamptz not null default now()
);

create index if not exists attempts_user_item_idx on attempts (user_id, item_id, created_at desc);
create index if not exists attempts_user_recent_idx on attempts (user_id, created_at desc);

-- `correct` é calculado no servidor, comparando com o gabarito do item. O
-- valor mandado pelo navegador é ignorado, para o aluno não conseguir gravar
-- acerto falso pelo console. `created_at` também é carimbado aqui.
create or replace function public.attempts_set_correct()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  expected jsonb;
begin
  select i.answer into expected from items i where i.id = new.item_id;
  new.correct := coalesce(new.answer = expected, false);
  new.created_at := now();
  return new;
end;
$$;

drop trigger if exists attempts_before_insert on attempts;
create trigger attempts_before_insert
  before insert on attempts
  for each row execute function public.attempts_set_correct();

alter table attempts enable row level security;

drop policy if exists "attempts_select_own" on attempts;
create policy "attempts_select_own" on attempts
  for select to authenticated
  using (auth.uid() = user_id);

drop policy if exists "attempts_insert_own_paid" on attempts;
create policy "attempts_insert_own_paid" on attempts
  for insert to authenticated
  with check (auth.uid() = user_id and public.has_paid_access());
-- de propósito: nenhuma policy de update/delete. Tentativa é histórico, não
-- se edita. A exclusão da conta apaga tudo pelo "on delete cascade" de user_id.

-- ============ CONFERÊNCIA DEPOIS DE RODAR ============
-- Logado como aluno sem pagamento: as duas consultas devem voltar vazias.
--   select count(*) from items;
--   insert into attempts (item_id, answer) values ('mod0-diag.1', '"A"');  -- deve falhar
-- Logado como aluno pago: `items` mostra só os publicados, e o insert acima
-- grava `correct` de acordo com o gabarito, qualquer que seja o valor enviado.
