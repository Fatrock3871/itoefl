# Publicar o iTOEFL (Cloudflare Pages + Stripe)

Passo a passo para o dono, em ordem. Cada passo diz quem faz: **[Você]** é o
dono, **[Claude]** é o que o Claude faz quando você pedir e autorizar. Nada
aqui foi feito ainda: o código está pronto, mas nada foi publicado, nenhuma
function foi para o ar, nenhum SQL rodou e nada foi criado no Stripe.

Decisões de 2026-10-18 (detalhes em "Decisões travadas" do `ROADMAP.md`):

- Hospedagem: **Cloudflare Pages**, no teste e no lançamento pago. É grátis
  e permite uso comercial.
- Pagamento: **Stripe** no cartão, em todos os planos. **Pix pelo Mercado
  Pago** só nos planos de pagamento único, até o Stripe liberar o Pix.
- Planos: Mensal R$ 29,90 (assinatura), 60 dias R$ 49,90, 90 dias R$ 59,90 e
  Anual R$ 129,90 (pagamento único). Preço, dias e o selo "Mais escolhido"
  ficam num arquivo só: `supabase/functions/_shared/plans.json`.

Regra de ouro: **primeiro tudo em modo de TESTE do Stripe**. As chaves reais
só entram no fim (passo 30), depois de as compras de teste darem certo.
Nunca cole chave nenhuma no chat, num arquivo do projeto ou no Git: chave
só vai no painel do Supabase (Secrets) ou no terminal.

## Antes de começar

1. **[Você]** Preencher os campos `[PREENCHER: ...]` de `legal/termos.md` e
   `legal/privacidade.md` (nome ou razão social, CPF ou CNPJ, e-mail de
   contato, ferramenta de IA da correção). Pode mandar os dados ao Claude,
   que ele preenche.
2. **[Você]** Escolher o e-mail que recebe as sugestões da versão de teste.
   **[Claude]** coloca em `FEEDBACK_EMAIL`, no `app/site.json`. Enquanto a
   chave `BETA` estiver `true`, o site mostra a faixa "Versão de teste" com o
   link "Enviar sugestão". No lançamento pago, trocar `BETA` para `false`.

## Endereço

3. **[Você]** Escolher e comprar o domínio.
   - Para `.com.br`: em **registro.br** (precisa de CPF ou CNPJ). Depois da
     compra, em "DNS" do registro.br, troque os servidores DNS pelos dois que
     o Cloudflare mostrar no passo 5.
   - Para `.com` e outros: dá para comprar direto no Cloudflare (Domain
     Registration), e aí o DNS já fica lá.
   - Sem domínio, o site funciona em `https://<nome>.pages.dev`, mas trocar
     depois dá retrabalho no Supabase, no Google e no Stripe.

## Cloudflare Pages

4. **[Você]** Criar a conta grátis em `dash.cloudflare.com` e confirmar o
   e-mail.
5. **[Você]** Em **Websites > Add a site**, colocar o domínio (plano Free).
   O Cloudflare mostra dois servidores DNS: coloque-os no registro.br. A troca
   leva de minutos a algumas horas.
6. **[Você]** Em **Workers & Pages > Create > Pages > Connect to Git**, dar
   acesso ao repositório privado `Fatrock3871/itoefl`, branch `main`, e
   preencher:
   - Build command: `pip install markdown && cd app && python build_pipeline.py && python build.py`
   - Build output directory: `artifact`
   - Variáveis de ambiente (Settings > Environment variables):
     - `PYTHON_VERSION` = `3.13`
     - `SITE_URL` = o endereço final, ex. `https://itoefl.com.br`
     - `SUPABASE_URL` = a URL do projeto Supabase
     - `SUPABASE_PUBLISHABLE_KEY` = a chave publishable (a mesma do
       `app/supabase_config.json`; **nunca** a secret)
     - opcionais: `BETA` (`1` ou `0`) e `FEEDBACK_EMAIL`, que vencem o que
       estiver no `app/site.json`

   A cada push no `main`, o Cloudflare builda e publica sozinho. O build gera
   o `artifact/_headers` com os cabeçalhos de segurança e o `sw.js` sem cache.
   Alternativa sem GitHub: "Upload assets" e arrastar a pasta `artifact` que
   o Claude buildar (repetir a cada versão).
7. **[Você]** No projeto do Pages, **Custom domains > Set up a custom
   domain**: colocar o domínio (e o `www`, se quiser). O HTTPS sai sozinho.
8. **[Claude]** Trocar `SITE_URL` em `app/site.json` pelo endereço final,
   rodar `python scripts\prepublish_check.py` (tem de dizer "Pronto para
   publicar") e commitar.

## Supabase: endereço e login

9. **[Você]** Em **Authentication > URL Configuration**:
   - **Site URL:** o endereço final, ex. `https://itoefl.com.br`.
   - **Redirect URLs:** adicionar `https://itoefl.com.br/**`. Pode manter o
     `http://localhost:8000/**` para os testes locais.
10. **[Você]** No Google Cloud Console, em **APIs e serviços > Credenciais**,
    no cliente OAuth do iTOEFL, adicionar o endereço final em **Origens
    JavaScript autorizadas**. A URI de redirecionamento continua só a do
    Supabase (`https://itfosjcymqfzjsftvjey.supabase.co/auth/v1/callback`).
11. **[Você]** Em **Tela de consentimento OAuth**: domínio autorizado,
    página inicial, política (`/privacidade`) e termos (`/termos`). Depois
    **Publicar app**, senão só os e-mails de teste conseguem entrar com Google.

## Stripe em modo de TESTE

12. **[Você]** Criar a conta em `dashboard.stripe.com` (conta brasileira,
    moeda BRL). Deixe ligado o botão **Modo de teste** (canto superior
    direito): tudo dos passos 13 a 18 é feito com ele ligado.
13. **[Você]** Em **Configurações > Dados públicos da empresa**, colocar
    **GB Corporation** como nome que aparece na fatura do cartão (descritor
    do extrato). Preencher também o e-mail de suporte.
14. **[Você]** Em **Desenvolvedores > Chaves de API**, copiar a **chave
    secreta de teste** (`sk_test_...`). No painel do Supabase, em **Edge
    Functions > Secrets**, criar o segredo `STRIPE_SECRET_KEY` com ela.
    Criar também `SITE_URL` com o endereço final (sem barra no fim).
15. **[Você]** Em **Desenvolvedores > Webhooks > Adicionar endpoint**:
    - URL: `https://itfosjcymqfzjsftvjey.supabase.co/functions/v1/stripe-webhook`
    - Eventos a marcar, exatamente estes seis:
      `checkout.session.completed`, `invoice.paid`,
      `invoice.payment_failed`, `customer.subscription.updated`,
      `customer.subscription.deleted`, `charge.refunded`.
    - Depois de criar, clicar em **Revelar** no "Segredo da assinatura"
      (`whsec_...`) e criar no Supabase o segredo `STRIPE_WEBHOOK_SECRET`
      com ele. A versão de API do endpoint pode ser a que o painel sugerir:
      o webhook relê tudo na API com uma versão fixa.
16. **[Você]** Em **Configurações > Billing > Portal do cliente**, ativar o
    portal e marcar:
    - **Cancelar assinaturas**: ligado, "no fim do período de cobrança" (o
      aluno usa o mês que já pagou);
    - **Atualizar forma de pagamento**: ligado;
    - **Histórico de faturas**: ligado;
    - **Trocar de plano**: desligado (os outros planos são pagamento único);
    - links de termos e privacidade: o endereço final com `/termos` e
      `/privacidade`.

    Salvar. É por aqui que o aluno cancela em 1 clique (Minha conta >
    "Gerenciar ou cancelar a assinatura").
17. **[Você]** Em **Configurações > Billing > Assinaturas e e-mails**, deixar
    as novas tentativas automáticas ligadas e escolher **cancelar a
    assinatura** quando todas as tentativas falharem.
18. **[Você]** Pedir o Pix: em **Configurações > Formas de pagamento**,
    procurar Pix e pedir acesso (no Brasil é por convite e só serve para
    pagamento único). Quando o Stripe liberar, avise o Claude: ele troca
    `pix_mercado_pago` para `false` em `supabase/functions/_shared/plans.json`
    e passa o Pix para o Stripe.

## Banco e functions (só com a sua autorização, a cada vez)

19. **[Claude]** Com a sua autorização, no SQL Editor do Supabase, rodar
    nesta ordem: `supabase/migrations/20261008_planos.sql` (se ainda não
    rodou) e `supabase/migrations/20261018_stripe.sql`. As duas podem rodar
    mais de uma vez sem estragar nada.
20. **[Claude]** Com a sua autorização, publicar as functions e conferir no
    painel (aba "Code") que a versão publicada é a nova:
    `create-checkout`, `stripe-webhook`, `stripe-portal`, `mp-webhook`,
    `delete-account` e `review-essay`. O deploy já reportou sucesso sem
    atualizar o código uma vez: a conferência é obrigatória.

## Compras de teste (ainda em modo de teste)

21. **[Você]** No site publicado, em aba anônima e sem extensões, criar uma
    conta, abrir "Ver os planos" e comprar com o cartão de teste
    **4242 4242 4242 4242**, qualquer validade futura, qualquer CVC e
    qualquer CEP. Conferir em Minha conta:
    - **90 dias**: acesso liberado por 90 dias;
    - **60 dias** comprado em seguida: o prazo passa para 150 dias (somou);
    - **Mensal**: aparece "Assinatura Mensal ativa: renova em ...", e o
      botão "Gerenciar ou cancelar a assinatura" abre o portal do Stripe;
    - no portal, **cancelar**: na volta, Minha conta diz que não haverá nova
      cobrança, e o acesso continua até o fim do que foi pago;
    - **Anual**: soma 365 dias.
22. **[Você]** Testar recusa: comprar com o cartão **4000 0000 0000 0002**.
    O Stripe mostra o erro e nada é liberado. Para ver uma renovação sem
    esperar um mês, use um relógio de teste do Stripe (Billing > Relógios de
    teste) ou peça ao Claude o roteiro.
23. **[Você]** Testar reembolso: no painel do Stripe, em **Pagamentos**,
    reembolsar uma das compras. Em Minha conta, os dias dela somem (e, se
    for o Mensal, a assinatura é cancelada).
24. **[Você]** Testar o Pix (se o Mercado Pago estiver pronto): escolher
    60 dias, 90 dias ou Anual, marcar "Pix" e pagar no ambiente de teste do
    Mercado Pago (`docs/mercadopago-setup.md`).
25. **[Claude]** Conferir nos logs da `stripe-webhook` que cada evento foi
    processado uma vez só e sem erro.

## Mercado Pago (só o Pix)

26. **[Você]** Resolver a conta real do Mercado Pago e, quando for vender,
    trocar o segredo `MP_ACCESS_TOKEN` no Supabase pelo de produção
    (`APP_USR-...`). Nada a cadastrar no painel: cada Pix já leva o endereço
    do `mp-webhook`.

## E-mail próprio (SMTP)

27. **[Você]** Contratar um serviço de envio (ex.: Resend ou Brevo) e criar
    o remetente `nao-responda@<seu domínio>`, com os registros DNS (SPF,
    DKIM) no Cloudflare.
28. **[Você]** No Supabase, em **Authentication > Emails > SMTP Settings**,
    ligar o SMTP próprio. Sem isso, os e-mails de confirmação e de senha
    saem do servidor de teste do Supabase, que tem limite baixo.
29. **[Claude]** Gravar os mesmos dados nos secrets das functions
    (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`), para o
    aviso de redação corrigida (`docs/deploy-redacao.md`).

## Trocar para as chaves reais (quando for cobrar de verdade)

30. **[Você]** No Stripe, ativar a conta (dados da empresa e conta bancária)
    e **desligar o Modo de teste**. Refazer em modo real os passos 13, 15, 16
    e 17: o modo real tem chaves, endpoint de webhook e portal próprios.
    No Supabase, trocar `STRIPE_SECRET_KEY` pela `sk_live_...` e
    `STRIPE_WEBHOOK_SECRET` pelo `whsec_...` do endpoint real. Não precisa
    publicar as functions de novo: elas leem os segredos a cada chamada.
31. **[Você]** Fazer uma compra real do plano de 60 dias e reembolsar pelo
    painel, para ver o caminho inteiro com dinheiro de verdade.
32. **[Claude]** Trocar `BETA` para `false` no `app/site.json` quando o
    teste acabar, buildar, rodar o smoke test e commitar.

## Testar no celular

33. **[Você]** No celular, com 4G e fora do Wi-Fi de casa, abrir
    `https://<seu domínio>/apresentacao`: diagnóstico grátis, criar conta,
    confirmar o e-mail, entrar com Google, comprar um plano de teste e
    "Adicionar à tela inicial".
34. **[Claude]** Conferir no endereço publicado: cabeçalhos de segurança,
    service worker, `sitemap.xml` e `robots.txt`, e marcar a 0.4 do
    `ROADMAP.md`.

## Observações

- **Página inicial.** No Cloudflare Pages, a raiz (`/`) abre o app (a tela
  de login) e a apresentação fica em `/apresentacao`. Divulgue o link
  `/apresentacao` até decidir mudar isso.
- **Mudar preço.** Editar só `supabase/functions/_shared/plans.json`,
  buildar e publicar `create-checkout`, `stripe-webhook` e `mp-webhook`.
  Assinaturas já existentes continuam no preço antigo: o Stripe guarda o
  preço de cada uma.
- **O que é de quem no código.** `create-checkout` abre o pagamento,
  `stripe-webhook` libera e tira acesso, `stripe-portal` abre o portal,
  `delete-account` cancela a assinatura antes de apagar a conta. A regra
  de acesso (toda compra soma dias; reembolso tira os dias daquela
  cobrança) está no cabeçalho de `supabase/migrations/20261018_stripe.sql`.
