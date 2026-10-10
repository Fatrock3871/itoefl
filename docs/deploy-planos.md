# Publicar os três planos: passo a passo para o dono

**Escrito em:** 2026-10-08
**Estado:** o código está pronto e commitado. **Nada foi executado fora do
repositório:** nenhum SQL rodou, nenhuma function foi publicada, nenhuma
credencial nem o painel do Mercado Pago foram tocados.

Cada passo abaixo é uma das ações que o `AGENTS.md` reserva ao dono. A ordem
importa: **SQL, depois functions, depois conferência da versão publicada,
depois as compras de teste.**

## O que você precisa saber antes

- **As functions nunca rodaram.** Esta máquina não tem Deno nem Node, então
  `create-checkout` e `mp-webhook` foram revisadas por leitura e pelo smoke
  test (que confere preço, prazo e que o preço não vem do navegador), mas a
  primeira execução de verdade é o deploy. Por isso o teste de compra do
  passo 5 não é opcional.
- **O site novo funciona com o banco antigo e com o novo.** Se a coluna
  `expires_at` ainda não existir, o site lê só `paid` e trata como acesso sem
  prazo. Dá para buildar e abrir o site antes do passo 1 sem quebrar nada.
- **As functions novas NÃO funcionam com o banco antigo.** O `mp-webhook`
  novo chama a função de banco `apply_payment()`, criada no passo 1. Publicar
  a function antes do SQL faz todo pagamento falhar na gravação.
- **Quem pagou antes continua com acesso vitalício.** A migração registra
  essas compras como plano `legado`, sem prazo.
- Use as **credenciais de teste** do Mercado Pago em todos os testes.

## Os preços e onde eles moram

| Plano | Validade | Preço |
|---|---|---|
| Sprint | 30 dias | R$ 39,90 |
| Standard (Recomendado) | 90 dias | R$ 89,90 |
| Premium | vitalício | R$ 149,90 |

O valor cobrado sai de `supabase/functions/_shared/plans.ts` (servidor). O
valor mostrado sai de `app/plans.json` (site). O navegador manda só o id do
plano. O smoke test reprova se os dois arquivos divergirem. Mudar preço:
editar os dois, rebuildar o site e publicar de novo as duas functions.

## A regra de renovação e troca de plano

O acesso de uma conta é sempre recalculado do extrato de pagamentos (tabela
`payments`), do mais antigo para o mais novo:

1. **Plano com prazo** (Sprint, Standard): os dias contam a partir do fim do
   acesso que a conta ainda tem. Se já venceu, ou é a primeira compra, contam
   da data do pagamento. Renovar antes de vencer soma, não desperdiça dias.
2. **Premium:** o acesso passa a não ter fim. Os dias que restavam não viram
   crédito.
3. **Conta com acesso vitalício** não consegue comprar outro plano: o
   `create-checkout` recusa antes de cobrar.
4. **Reembolso ou chargeback:** o pagamento sai da conta e o prazo é
   recalculado com os que sobraram. Sem nenhum, o acesso termina.
5. **Aviso repetido** do Mercado Pago para o mesmo pagamento não soma dias
   duas vezes.

Exemplo: Sprint em 1º de março (vale até 31 de março), Standard em 20 de
março: o acesso vai até 29 de junho (31 de março mais 90 dias).

---

## Passo 1: SQL

1. Supabase, **SQL Editor**, New query.
2. Cole o conteúdo inteiro de `supabase/migrations/20261008_planos.sql` e
   rode. Ele pode ser rodado mais de uma vez sem estragar nada, e não apaga
   dado nenhum.
3. Confira, uma consulta por vez:

```sql
-- tem de listar plan e expires_at
select column_name from information_schema.columns
where table_schema = 'public' and table_name = 'entitlements';

-- os dois números têm de ser iguais (cada compra antiga virou uma linha do extrato)
select (select count(*) from entitlements where paid) as contas_pagas,
       (select count(*) from payments) as pagamentos;

-- as duas têm de dar false: aluno logado e visitante NÃO podem chamar a função
select has_function_privilege('authenticated', 'public.apply_payment(text, uuid, text, int, numeric, text, timestamptz)', 'execute') as aluno,
       has_function_privilege('anon', 'public.apply_payment(text, uuid, text, int, numeric, text, timestamptz)', 'execute') as visitante;
```

Se a terceira consulta der `true` em qualquer coluna, **pare**: um aluno
conseguiria se dar acesso. Avise antes de seguir.

4. Opcional, mas recomendado: ensaio da regra dentro de uma transação que é
   desfeita no fim. Troque `<UUID>` pelo id de uma conta de teste (Supabase,
   Authentication, Users).

```sql
begin;
select public.apply_payment('ensaio-1', '<UUID>', 'sprint', 30, 39.90, 'approved', now());
select plan, expires_at from entitlements where user_id = '<UUID>';   -- daqui a 30 dias
select public.apply_payment('ensaio-2', '<UUID>', 'standard', 90, 89.90, 'approved', now());
select plan, expires_at from entitlements where user_id = '<UUID>';   -- daqui a 120 dias
select public.apply_payment('ensaio-2', '<UUID>', 'standard', 90, 89.90, 'approved', now());
select plan, expires_at from entitlements where user_id = '<UUID>';   -- igual: repetido não soma
select public.apply_payment('ensaio-3', '<UUID>', 'premium', null, 149.90, 'approved', now());
select plan, expires_at from entitlements where user_id = '<UUID>';   -- premium, expires_at vazio
select public.apply_payment('ensaio-3', null, null, null, null, 'refunded', null);
select plan, expires_at from entitlements where user_id = '<UUID>';   -- volta para 120 dias
rollback;
```

O arquivo fica em `supabase/migrations/` só para organizar. O projeto não usa
`supabase db push`: a aplicação é sempre pelo SQL Editor.

## Passo 2: publicar as functions

No terminal, na pasta do projeto, com o Supabase CLI já ligado ao projeto
(`docs/mercadopago-setup.md`, passo 3):

```powershell
supabase functions deploy create-checkout
supabase functions deploy mp-webhook
```

As duas importam `supabase/functions/_shared/plans.ts`; o CLI empacota esse
arquivo junto. `delete-account` não precisa de deploy (só um comentário
mudou). Nenhum segredo novo: continua valendo o `MP_ACCESS_TOKEN`.

## Passo 3: conferir a versão publicada

O deploy já reportou sucesso sem atualizar o código neste projeto. Confira no
painel, **Edge Functions**, aba **Code** de cada uma:

| Function | Tem de aparecer | Não pode aparecer |
|---|---|---|
| `create-checkout` | `findPlan(planId)` e `../_shared/plans.ts` | `PRICE_BRL` |
| `mp-webhook` | `apply_payment` e `parseReference` | `.from("entitlements").upsert` |

E pelo terminal, o webhook tem de continuar aceitando chamada sem login:

```powershell
curl.exe -X POST "https://itfosjcymqfzjsftvjey.supabase.co/functions/v1/mp-webhook?type=merchant_order&id=1"
```

Resposta esperada: `ok`. Se vier `Missing authorization header`, o
`config.toml` não foi aplicado: publique o `mp-webhook` de novo.

## Passo 4: buildar o site e abrir localmente

```powershell
cd app
python build_pipeline.py
python build.py
cd ..
python scripts\smoke_test.py
python scripts\serve.py
```

O smoke test tem de terminar com "Tudo passou". O site continua não
publicado: o teste é em `http://localhost:8000/artifact/index.html`.

## Passo 5: compra de teste de cada plano

Use aba anônima, sem extensão, com **duas contas que não sejam a de
administrador** (a conta admin pula a tela de compra). Cartão e usuário de
teste: Sessão 2026-09-24 de `docs/historico-sessoes.md`.

Depois de cada compra, confira três coisas: a tela do Mercado Pago, Minha
conta no site, e as tabelas no Supabase (`select * from payments order by
created_at desc;` e `select * from entitlements;`).

**Conta A, a sequência inteira da regra:**

| # | Ação | Na tela do Mercado Pago | Em Minha conta | No banco |
|---|---|---|---|---|
| 1 | Entrar sem ter comprado | | Tela "Libere seu acesso", com os três planos e Standard marcado | Sem linha, ou `paid = false` |
| 2 | Comprar **Sprint** | "iTOEFL: plano Sprint (30 dias de acesso)", R$ 39,90 | "Plano Sprint: acesso liberado até (hoje + 30 dias)" | `payments`: 1 linha, `days = 30`, `amount = 39.90`. `entitlements.expires_at` em 30 dias |
| 3 | Minha conta, "Renovar ou mudar de plano", comprar **Standard** | "plano Standard (90 dias de acesso)", R$ 89,90 | "Plano Standard: acesso liberado até (hoje + 120 dias)" | 2 linhas. `expires_at` em 120 dias |
| 4 | De novo "Renovar ou mudar de plano", comprar **Premium** | "plano Premium (acesso vitalício)", R$ 149,90 | "Plano Premium: acesso vitalício liberado" e o botão de renovar some | 3 linhas. `expires_at` vazio |

Se no passo 2 a tela do Mercado Pago mostrar "Acesso vitalício à plataforma"
por R$ 9,90, a `create-checkout` antiga ainda está publicada: volte ao passo 3.

**Conta B, vencimento, aviso repetido e reembolso:**

| # | Ação | Resultado esperado |
|---|---|---|
| 5 | Comprar **Standard** | Acesso até hoje + 90 dias |
| 6 | Reenviar o aviso do pagamento duas vezes (comando abaixo, com o id que está em `payments.mp_payment_id`) | Responde `ok` e `expires_at` **não muda** |
| 7 | Forçar o vencimento (SQL abaixo) e recarregar o site | Tela "Seu acesso venceu", com a data. Em Minha conta: "O plano Standard venceu em ..." |
| 8 | Comprar **Sprint** com a conta vencida | Acesso até hoje + 30 dias (conta da data nova, não da antiga) |
| 9 | Devolver esse pagamento no painel do Mercado Pago | Em alguns segundos `payments.status = 'refunded'` e a conta volta a ficar vencida |

```powershell
# passo 6: troque <ID> pelo mp_payment_id
curl.exe -X POST "https://itfosjcymqfzjsftvjey.supabase.co/functions/v1/mp-webhook?type=payment&data.id=<ID>"
```

```sql
-- passo 7: empurra o pagamento 91 dias para trás e recalcula
update payments set approved_at = now() - interval '91 days' where mp_payment_id = '<ID>';
select public.recompute_entitlement('<UUID da conta B>');
```

Se o passo 9 não mudar nada em um minuto, o Mercado Pago não avisou o
reembolso. Registre isso e desfaça na mão:
`select public.apply_payment('<ID>', null, null, null, null, 'refunded', null);`

**Cupom (só se você autorizar criar um cupom de teste):** com um cupom de 20%
ativo, a compra do Standard tem de sair por R$ 71,92 na tela do Mercado Pago
e em `payments.amount`. Cupom inexistente tem de mostrar "Cupom inválido ou
expirado" sem abrir o pagamento.

## Como atender um pedido de reembolso (7 dias)

1. Conferir em `payments` que a compra tem 7 dias ou menos (`approved_at`).
2. Devolver o valor no painel do Mercado Pago.
3. O acesso é retirado sozinho pelo `mp-webhook`. Conferir em `payments` que
   a linha ficou `refunded`. Se não ficou, usar o comando do passo 9.

## Se algo der errado

- **As mudanças de banco são só acréscimos.** Não há o que desfazer para o
  site antigo voltar a funcionar.
- **Voltar as functions:** o código anterior aos planos está no commit
  `81efb94`. `git checkout 81efb94 -- supabase/functions/create-checkout supabase/functions/mp-webhook`,
  publicar as duas, e depois `git checkout HEAD -- supabase/functions` para
  restaurar a pasta. Atenção: a `mp-webhook` antiga grava acesso sem prazo
  para qualquer pagamento.
- **Log de erro:** painel, Edge Functions, Logs. O `mp-webhook` registra
  "external_reference sem plano reconhecido" quando recebe um pagamento que
  não nasceu da `create-checkout` nova (por exemplo, um link de pagamento
  aberto antes do deploy). Esse pagamento não libera acesso sozinho: dar o
  acesso na mão com `apply_payment` (exemplo no fim do arquivo da migração).

## O que continua pendente depois disto

Nada disto é resolvido por este deploy (ver `ROADMAP.md`, Etapa 0):

- Trocar as credenciais de teste do Mercado Pago pelas de produção, depois
  de resolver a validação da conta real.
- Preencher os campos `[PREENCHER: ...]` de `legal/termos.md` e passar por
  advogado os dois trechos marcados `REVISAR (advogado)` (planos e validade;
  reembolso). O build avisa enquanto existirem.
- Publicar o site.
- O bloqueio de quem não pagou ou venceu continua sendo só visual: o
  conteúdo vai embutido no HTML. O prazo no banco passa a valer de verdade
  quando o conteúdo for servido do banco (Etapa 2).
