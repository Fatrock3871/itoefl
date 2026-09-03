-- iTOEFL platform schema
-- Content tables (public read) + student progress tables (per-user, RLS-protected)

-- ============ CONTENT ============

create table if not exists modules (
  slug text primary key,               -- 'mod0', 'mod1', 'mod2', 'mod3', 'mod4', 'mod7'
  title text not null,
  order_index int not null,
  content_md text not null,            -- full consolidated markdown for the module
  updated_at timestamptz not null default now()
);

create table if not exists quiz_questions (
  id bigint generated always as identity primary key,
  module_slug text not null references modules(slug) on delete cascade,
  num int not null,
  topic text,
  prompt text not null,
  options jsonb not null,              -- {"A": "...", "B": "...", "C": "...", "D": "..."}
  correct text not null,
  why_right text,
  why_wrong text,
  unique (module_slug, num)
);

create table if not exists drills (
  id text primary key,                 -- 'mod1-d1', 'mod2-d3', etc.
  module_slug text not null references modules(slug) on delete cascade,
  title text not null,
  objective text,
  passage_html text,
  order_index int not null default 0
);

create table if not exists drill_items (
  id bigint generated always as identity primary key,
  drill_id text not null references drills(id) on delete cascade,
  num text not null,
  prompt text not null,
  options jsonb not null,
  correct text not null,
  explanation text,
  unique (drill_id, num)
);

-- ============ STUDENT PROGRESS ============

create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists module_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  module_slug text not null references modules(slug) on delete cascade,
  status text not null default 'not_started' check (status in ('not_started', 'in_progress', 'completed')),
  score numeric,
  updated_at timestamptz not null default now(),
  primary key (user_id, module_slug)
);

create table if not exists quiz_attempts (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  question_id bigint not null references quiz_questions(id) on delete cascade,
  selected_option text not null,
  is_correct boolean not null,
  answered_at timestamptz not null default now()
);

create table if not exists drill_attempts (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  drill_item_id bigint not null references drill_items(id) on delete cascade,
  selected_option text not null,
  is_correct boolean not null,
  answered_at timestamptz not null default now()
);

-- ============ INDEXES ============

create index if not exists idx_quiz_questions_module on quiz_questions(module_slug);
create index if not exists idx_drills_module on drills(module_slug);
create index if not exists idx_drill_items_drill on drill_items(drill_id);
create index if not exists idx_quiz_attempts_user on quiz_attempts(user_id);
create index if not exists idx_drill_attempts_user on drill_attempts(user_id);
create index if not exists idx_module_progress_user on module_progress(user_id);

-- ============ ROW LEVEL SECURITY ============

alter table modules enable row level security;
alter table quiz_questions enable row level security;
alter table drills enable row level security;
alter table drill_items enable row level security;
alter table profiles enable row level security;
alter table module_progress enable row level security;
alter table quiz_attempts enable row level security;
alter table drill_attempts enable row level security;

-- Content: readable by anyone (anon + authenticated), writable only via service role (no policy for insert/update/delete)
create policy "content_public_read_modules" on modules for select using (true);
create policy "content_public_read_quiz_questions" on quiz_questions for select using (true);
create policy "content_public_read_drills" on drills for select using (true);
create policy "content_public_read_drill_items" on drill_items for select using (true);

-- Profiles: users manage their own row
create policy "profiles_select_own" on profiles for select using (auth.uid() = id);
create policy "profiles_insert_own" on profiles for insert with check (auth.uid() = id);
create policy "profiles_update_own" on profiles for update using (auth.uid() = id);

-- Progress & attempts: users manage only their own rows
create policy "module_progress_select_own" on module_progress for select using (auth.uid() = user_id);
create policy "module_progress_upsert_own" on module_progress for insert with check (auth.uid() = user_id);
create policy "module_progress_update_own" on module_progress for update using (auth.uid() = user_id);

create policy "quiz_attempts_select_own" on quiz_attempts for select using (auth.uid() = user_id);
create policy "quiz_attempts_insert_own" on quiz_attempts for insert with check (auth.uid() = user_id);

create policy "drill_attempts_select_own" on drill_attempts for select using (auth.uid() = user_id);
create policy "drill_attempts_insert_own" on drill_attempts for insert with check (auth.uid() = user_id);
