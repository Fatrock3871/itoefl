# Configurar o Supabase (contas + progresso sincronizado)

O app funciona 100% sem isto — o progresso fica no `localStorage` do navegador.
O Supabase adiciona **login e sincronização entre dispositivos**: o aluno entra
com um link enviado por e-mail e o progresso (checkboxes, flashcards SRS, quiz,
Build a Sentence) passa a acompanhar a conta.

O que **não** sincroniza (fica sempre local por dispositivo): tema, aba ativa,
preset do cronômetro.

---

## 1. Criar o projeto Supabase (grátis)

1. Entre em <https://supabase.com> e crie uma conta.
2. **New project** → escolha um nome, uma senha de banco (guarde) e a região
   mais próxima (ex.: São Paulo). Aguarde ~2 minutos até provisionar.

## 2. Rodar o schema

1. No painel do projeto: **SQL Editor** → **New query**.
2. Cole o conteúdo de `supabase/schema.sql` e clique em **Run**.
   Isso cria as tabelas `profiles` e `user_state`, as políticas de RLS e o
   gatilho que cria o perfil no primeiro login.
3. (Opcional, só se um dia quiser editar o conteúdo dos módulos pelo banco em
   vez de pelo build) rode também `supabase/schema-content-optional.sql` e
   popule com `supabase/content-seed-optional.json`.

## 3. Configurar o e-mail de login

1. **Authentication** → **Providers** → confirme que **Email** está ativado.
2. **Authentication** → **URL Configuration**:
   - **Site URL:** o endereço onde o app vai rodar. Para testar localmente:
     `http://localhost:8000`. Quando publicar, troque para a URL final
     (ex.: `https://seu-usuario.github.io/itoefl`).
   - **Redirect URLs:** adicione o mesmo endereço (e qualquer outro de onde
     você for abrir o app).
3. O plano grátis usa o serviço de e-mail do próprio Supabase, com um limite
   baixo de mensagens por hora — suficiente para uso pessoal. Para volume maior,
   configure um SMTP próprio em **Authentication → Emails**.

## 4. Ligar o app às credenciais

1. No painel: **Project Settings** → **API**. Copie:
   - **Project URL** (ex.: `https://abcdefgh.supabase.co`)
   - **Project API keys → `anon` / `public`** (a chave longa que começa com `eyJ…`)
2. Na pasta do projeto:
   ```
   copy app\supabase_config.example.json app\supabase_config.json
   ```
   Abra `app\supabase_config.json` e preencha `url` e `anonKey` com os valores
   copiados. **Salve como UTF-8 (o build tolera BOM).**
   > A `anon key` é pública por natureza (vai no HTML do navegador). O arquivo
   > está no `.gitignore` só por higiene; a segurança real vem das políticas de
   > RLS do schema, que garantem que cada usuário só lê/escreve a própria linha.
3. Rebuild:
   ```
   cd app
   python build_pipeline.py
   python build.py
   ```
   O `build.py` deve imprimir `supabase: configurado`.
4. `python scripts\serve.py` e abra o app. Na barra lateral aparece
   **"Entrar para sincronizar"**.

## 5. Como funciona no uso

- **Entrar:** clique no botão, digite o e-mail, confira a caixa de entrada e
  clique no link. Ao voltar, o app mostra o e-mail e um botão **Sair**.
- **Primeiro login num dispositivo novo:** o app baixa o progresso da nuvem e
  recarrega a página.
- **Edições:** cada mudança de progresso é enviada para a nuvem ~2,5 s depois
  (com um aviso "Sincronizado.").
- **Offline / deslogado:** tudo continua no `localStorage`; ao entrar de novo,
  as edições feitas offline têm prioridade e são mescladas com a nuvem.
- **Conflito entre dispositivos:** a regra é simples — o dispositivo com edições
  não enviadas ganha na hora de mesclar. Não é um merge campo a campo; para uso
  de uma pessoa só, é suficiente.

## Resolução de problemas

| Sintoma | Causa provável |
|---|---|
| Botão "Entrar" não aparece | `build.py` imprimiu `nao configurado`; confira `app/supabase_config.json` e rebuilde |
| "Erro: ..." ao pedir o link | Site URL / Redirect URL não batem com o endereço onde o app está aberto |
| Link do e-mail abre e nada acontece | O redirect aponta para outro endereço; ajuste em Authentication → URL Configuration |
| "Erro ao sincronizar" | O schema não foi rodado, ou as políticas de RLS não foram criadas |
| Não recebe o e-mail | Limite de envio do plano grátis atingido; aguarde ou configure SMTP próprio |
