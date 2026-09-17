# Configurar o acesso pago (Mercado Pago)

Desde 2026-09-17, o app tem uma segunda tela depois do login: quem não pagou
vê a tela de compra (`#payGate`) em vez do conteúdo. **Sua conta
(`pietrooliveiramarquespp@gmail.com`) sempre passa direto, sem checar
pagamento** — isso está hardcoded em `app.js` (`ADMIN_EMAIL`), não depende de
nenhuma configuração abaixo.

Nada disso funciona sem os passos manuais desta página — eu não tenho como
criar sua conta Mercado Pago, gerar suas chaves, nem publicar as edge
functions no seu projeto Supabase. Isso exige acesso que só você tem.

## Como funciona

1. Aluno loga (e-mail ou Google) → passa pelo `#authGate` de sempre.
2. Se não for a conta admin, o app confere a tabela `entitlements` no
   Supabase. Sem linha `paid = true` → mostra `#payGate` ("Comprar acesso").
3. Clique em "Comprar acesso" → chama a edge function `create-checkout`, que
   cria uma preferência de pagamento no Mercado Pago e devolve a URL de
   checkout. O navegador é redirecionado pra lá.
4. Aluno paga no Mercado Pago → o Mercado Pago notifica a edge function
   `mp-webhook` (URL configurada automaticamente na criação da preferência,
   não precisa cadastrar nada no painel do MP) → ela reconfirma o pagamento
   direto na API do Mercado Pago (nunca confia só na notificação) e grava
   `paid = true` na tabela `entitlements` do aluno.
5. O Mercado Pago também redireciona o navegador de volta pro site
   (`?mp=success`) → o app tenta confirmar o acesso por até ~15 segundos
   (o webhook é assíncrono, pode chegar um pouco depois do redirect) antes
   de pedir pra atualizar a página manualmente.

`entitlements` é uma tabela separada de `profiles`, sem nenhuma permissão de
escrita pro navegador (só o `service_role`, usado pela edge function, grava
nela) — um aluno não consegue se autoliberar digitando algo no console do
navegador.

---

## 1. Rodar o schema novo

No SQL Editor do Supabase, rode de novo `supabase/schema.sql` inteiro (ele
usa `create table if not exists` e `drop policy if exists`/`create policy`,
então é seguro rodar por cima do que já existe — não apaga nada). Isso cria
a tabela `entitlements`.

## 2. Criar as credenciais no Mercado Pago

1. Crie/entre na sua conta em <https://www.mercadopago.com.br>.
2. **Seu negócio → Configurações → Credenciais de produção** (ou
   "Credenciais de teste" pra testar antes de cobrar de verdade).
3. Copie o **Access Token** (começa com `APP_USR-...` em produção, ou
   `TEST-...` em teste). É o único segredo que as duas edge functions
   precisam.

## 3. Instalar e ligar o Supabase CLI

Isso roda no seu terminal, não é algo que eu execute:

```powershell
# instala o CLI (npm) — se não tiver Node, veja https://supabase.com/docs/guides/cli
npm install -g supabase

# autentica com sua conta Supabase (abre o navegador)
supabase login

# dentro da pasta do projeto (onde está supabase/config.toml)
supabase link --project-ref itfosjcymqfzjsftvjey
```

## 4. Configurar o segredo e publicar as edge functions

```powershell
# o access token do passo 2 -- nunca cole isso no chat comigo, só no terminal
supabase secrets set MP_ACCESS_TOKEN=APP_USR-xxxxxxxxxxxxxxxxxxxxxxxx

supabase functions deploy create-checkout
supabase functions deploy mp-webhook
```

`SUPABASE_URL`, `SUPABASE_ANON_KEY` e `SUPABASE_SERVICE_ROLE_KEY` já existem
automaticamente no ambiente de toda edge function do projeto — não precisa
configurar esses três.

## 5. Ajustar preço e nome do produto

Em `supabase/functions/create-checkout/index.ts`, os dois primeiros valores:

```ts
const PRICE_BRL = 197.0;
const PRODUCT_TITLE = "iTOEFL — Acesso vitalício à plataforma";
```

O texto do botão "Comprar acesso — R$ 197" em `app/build.py` **não** puxa
esse valor automaticamente — se mudar o preço, mude os dois lugares e rode
`supabase functions deploy create-checkout` de novo, além de rebuildar o site
(`python build_pipeline.py && python build.py`).

## 6. Testar

1. Use as **credenciais de teste** do Mercado Pago primeiro (passo 2, "modo
   teste") e um usuário de teste do MP (criado no mesmo painel de
   credenciais) pra simular um pagamento aprovado sem gastar dinheiro de
   verdade.
2. Logue no site com uma conta que **não** seja a admin.
3. Clique em "Comprar acesso" → deve abrir o checkout do Mercado Pago.
4. Pague com os dados de teste do MP → deve voltar pro site com
   `?mp=success` na URL e liberar o acesso em alguns segundos.
5. Confira na tabela `entitlements` do Supabase se a linha do usuário tem
   `paid = true` e `mp_payment_id` preenchido.
6. Só depois disso, troque para as credenciais de **produção** (repita o
   passo 4 com o Access Token de produção) antes de cobrar de alguém de
   verdade.

## Resolução de problemas

| Sintoma | Causa provável |
|---|---|
| Botão "Comprar acesso" dá erro ao clicar | Edge function `create-checkout` não publicada, ou `MP_ACCESS_TOKEN` não configurado |
| Pagou mas o acesso não libera | Confira os logs da função `mp-webhook` no painel do Supabase (Edge Functions → Logs); o pagamento pode não ter chegado como "approved" ainda, ou o `external_reference` não bateu |
| `entitlements` não existe | `schema.sql` não foi rodado depois da atualização de 2026-09-17 |
| Minha própria conta pede pagamento | Confira se o e-mail logado é exatamente `pietrooliveiramarquespp@gmail.com` (o mesmo usado no login) |
