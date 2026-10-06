# Configurar o Supabase (contas + progresso sincronizado)

Sem este arquivo configurado, o app funciona 100% sem login — o progresso fica
no `localStorage` do navegador, sem tela de entrada. **Com ele configurado**,
o app passa a exigir login antes de liberar o conteúdo (tela `#authGate`,
decisão do usuário em 2026-09-14): o aluno entra com **e-mail + senha** ou
Google,
e o progresso (checkboxes, flashcards SRS, quiz, Build a Sentence, registro
de erros) passa a acompanhar a conta e sincronizar entre dispositivos. Uma
falha ao carregar a biblioteca do Supabase (CDN bloqueado/sem internet)
libera o conteúdo mesmo assim — só a ausência de configuração ou uma falha de
rede evita o bloqueio, nunca um bug trava o aluno pra fora do próprio
material.

**Cadastro e login:** e-mail + senha, ou conta Google. O e-mail confirma que
a conta é real (se a confirmação por e-mail estiver ligada no seu projeto, que
é o padrão do Supabase) e serve como recuperação: "Esqueci minha senha" manda
um link de redefinição pro e-mail cadastrado. O login por nome de usuário
existiu por alguns dias em setembro de 2026 e foi removido; o `schema.sql`
atual apaga do banco o que aquela versão criou.

O que **não** sincroniza (fica sempre local por dispositivo): tema, aba ativa,
preset do cronômetro.

---

## Estado atual (2026-09-03)

Projeto **ITOELF** já criado (ref `itfosjcymqfzjsftvjey`, região São Paulo).
`app/supabase_config.json` preenchido com a **publishable key**
(`sb_publishable_...`) — o padrão novo do Supabase, seguro no navegador.
A app builda com `supabase: configurado` e o botão "Entrar para sincronizar"
aparece na sidebar (biblioteca `supabase-js@2` carrega e aceita a chave).

**Pendências:**
1. Confirmar que o schema (`supabase/schema.sql`) rodou no SQL Editor.
2. Configurar Site URL / Redirect URLs (passo 3 abaixo).
3. Testar o login real (e-mail + link).

> 🔐 **Segurança — dois valores foram expostos numa conversa e devem ser
> rotacionados:** a *secret key* `sb_secret_...` (API Keys → Publishable and
> secret → rotacionar) e a *legacy service_role* (Reveal JWT secret →
> "Generate a new JWT secret"). A publishable key que a app usa **não** é
> afetada por rolar o JWT secret, então dá para rotacionar sem quebrar nada.

---

## 1. Criar o projeto Supabase (grátis) — *já feito*

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

## 3.1 Login com Google (foto de perfil automática)

O app já tem o botão **"Entrar com Google"** pronto no código — falta só ligar
o provedor no painel do Supabase (isso **eu não consigo fazer por você**: exige
a sua conta do Google Cloud e o seu painel do Supabase).

1. **Google Cloud Console** (<https://console.cloud.google.com>):
   - Crie um projeto (ou use um existente) → **APIs & Services** →
     **OAuth consent screen**: tipo *External*, preencha nome do app e e-mail
     de suporte. Não precisa publicar (pode ficar em "Testing" com o seu
     e-mail na lista de testadores, suficiente para uso pessoal).
   - **APIs & Services → Credentials → Create Credentials → OAuth client ID**:
     tipo **Web application**.
   - Em **Authorized redirect URIs**, adicione a URL de callback do Supabase:
     `https://itfosjcymqfzjsftvjey.supabase.co/auth/v1/callback`
     (troque `itfosjcymqfzjsftvjey` pela ref do seu projeto, em Project
     Settings → General; é a mesma que já está em `app/supabase_config.json`).
   - Copie o **Client ID** e o **Client Secret** gerados.
2. **Supabase → Authentication → Providers → Google**: ative o toggle, cole o
   Client ID e o Client Secret, salve.
3. Confirme que **Authentication → URL Configuration** já tem
   `http://localhost:8000` (ou o endereço que você usa) em Site URL /
   Redirect URLs — é o mesmo ajuste do passo 3 acima, vale para os dois
   provedores.
4. Rebuild não é necessário para isso (é config do Supabase, não do app) —
   só recarregue a página e teste o botão "Entrar com Google".

**Sobre a foto de perfil:** ao entrar com Google, o avatar do site passa a
usar automaticamente a foto da conta Google (vem no `user_metadata` da sessão,
sem passo extra nenhum). Uma foto enviada manualmente pelo botão do avatar
sempre tem prioridade sobre a do Google, caso queira usar outra.

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
4. `python scripts\serve.py` e abra o app. A tela de login (`#authGate`)
   aparece antes de qualquer conteúdo, com **"Entrar com Google"** e
   **"Entrar com e-mail"**.

## 5. Como funciona no uso

- **Entrar:** "Entrar com Google" loga direto; e-mail + senha loga na hora,
  sem sair da página. Depois de logado, o app mostra o e-mail, o avatar e um
  botão **Sair**.
- **Criar conta:** "Criar conta" pede e-mail + senha. Se a confirmação por
  e-mail estiver ligada (padrão do Supabase), o aluno confirma antes do
  primeiro login.
- **Esqueci a senha:** link na tela de login, pede só o e-mail e manda um link
  de redefinição.
- **Minha conta** (engrenagem no topo): tema, situação do acesso pago, troca
  de e-mail e senha, e exclusão da conta. A exclusão depende da edge function
  `delete-account` estar publicada (`supabase functions deploy delete-account`).
- **Primeiro login num dispositivo novo:** o app baixa o progresso da nuvem e
  recarrega a página.
- **Edições:** cada mudança de progresso é enviada para a nuvem ~2,5 s depois
  (com um aviso "Sincronizado.").
- **Deslogado:** a tela de login cobre o conteúdo — não dá pra navegar os
  módulos sem entrar (só quando o Supabase está configurado; sem ele o app
  segue offline sem tela nenhuma). Uma vez logado, o progresso volta a viver
  no `localStorage` do navegador entre visitas; ao entrar de novo depois de
  editar offline (ex.: sem internet), essas edições têm prioridade e são
  mescladas com a nuvem.
- **Conflito entre dispositivos:** a regra é simples — o dispositivo com edições
  não enviadas ganha na hora de mesclar. Não é um merge campo a campo; para uso
  de uma pessoa só, é suficiente.

## Resolução de problemas

| Sintoma | Causa provável |
|---|---|
| Tela de login não aparece | `build.py` imprimiu `nao configurado`; confira `app/supabase_config.json` e rebuilde |
| "E-mail ou senha incorretos" mesmo com os dados certos | A conta ainda não confirmou o e-mail (se a confirmação estiver ligada) |
| Link de recuperação/confirmação abre e nada acontece | O redirect aponta pra outro endereço; ajuste em Authentication → URL Configuration |
| "Erro ao sincronizar" | O schema não foi rodado, ou as políticas de RLS não foram criadas |
| Não recebe o e-mail de confirmação/recuperação | Limite de envio do plano grátis atingido; aguarde ou configure SMTP próprio |
