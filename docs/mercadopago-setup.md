# Configurar o acesso pago (Mercado Pago)

> **Desde 2026-10-18 o Mercado Pago cuida só do Pix** dos planos de
> pagamento único (60 dias, 90 dias e Anual). O cartão, em todos os planos,
> é pelo Stripe. Preços em `supabase/functions/_shared/plans.json` (não mais
> em `app/plans.json`). Passo a passo atual em `docs/publicar.md`; o texto
> abaixo é a configuração antiga, útil para as credenciais e o ambiente de
> teste do Mercado Pago.

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
   Supabase. Sem acesso em dia (nunca comprou, ou `expires_at` já passou) →
   mostra `#payGate`, com a escolha de plano.
3. O aluno escolhe o plano e clica em "Comprar" → chama a edge function
   `create-checkout` com o id do plano. Ela decide o preço, cria uma
   preferência de pagamento no Mercado Pago e devolve a URL de checkout. O
   navegador é redirecionado pra lá.
4. Aluno paga no Mercado Pago → o Mercado Pago notifica a edge function
   `mp-webhook` (URL configurada automaticamente na criação da preferência,
   não precisa cadastrar nada no painel do MP) → ela reconfirma o pagamento
   direto na API do Mercado Pago (nunca confia só na notificação), registra
   o pagamento em `payments` e recalcula o prazo em `entitlements`.
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
supabase functions deploy delete-account
```

`SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEYS` e `SUPABASE_SECRET_KEYS` já
existem automaticamente no ambiente de toda edge function do projeto: não
precisa configurar esses três. As functions não usam mais `SUPABASE_ANON_KEY`
nem `SUPABASE_SERVICE_ROLE_KEY` (ver `supabase/functions/_shared/keys.ts`).

**O `mp-webhook` precisa aceitar chamada sem login.** O Mercado Pago não manda
header de autenticação, então a verificação de JWT dessa function fica
desligada em `supabase/config.toml` (`[functions.mp-webhook] verify_jwt =
false`). Com ela ligada, o Supabase responde 401 antes de o código rodar e
nenhum pagamento libera acesso. Para conferir depois de publicar:

```powershell
curl.exe -X POST "https://itfosjcymqfzjsftvjey.supabase.co/functions/v1/mp-webhook?type=merchant_order&id=1"
```

Tem que responder `ok`. Se responder `Missing authorization header`, o
`config.toml` não foi aplicado: rode o deploy do `mp-webhook` de novo.

## 5. Planos e preços

Desde 2026-10-08 são três planos (Sprint, Standard e Premium), com prazo.
O passo a passo para publicar essa mudança, a regra de renovação e os testes
de compra estão em `docs/deploy-planos.md`.

O preço mora em dois arquivos, que têm de dizer a mesma coisa:

- `supabase/functions/_shared/plans.ts`: o valor **cobrado** e o prazo
  gravado. Roda no servidor.
- `app/plans.json`: o valor **mostrado** na tela de compra e na tela de
  apresentação.

O navegador manda só o id do plano. Para mudar preço ou prazo: editar os
dois arquivos (o smoke test reprova se divergirem), rebuildar o site e rodar
`supabase functions deploy create-checkout` e
`supabase functions deploy mp-webhook`.

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
