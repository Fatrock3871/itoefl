# Publicar o iTOEFL

Passo a passo para o dono. Cada passo diz quem faz: **[Você]** é o dono,
**[Claude]** é o que o Claude faz depois, quando você pedir. Nada aqui foi
feito ainda: o site está pronto para publicar, mas não está publicado.

Hospedagem recomendada: **Cloudflare Pages** (grátis, aceita repositório
privado, dá HTTPS e domínio próprio). Se escolher outra, os passos 4 a 6
mudam e o resto fica igual: o endereço do site mora num lugar só
(`app/site.json`), e as regras de cabeçalho do `artifact/_headers` valem
também no Netlify. Em outra hospedagem, o Claude traduz essas regras.

## Antes de começar

1. **[Você]** Preencher os campos `[PREENCHER: ...]` de `legal/termos.md` e
   `legal/privacidade.md` (nome ou razão social, CPF ou CNPJ, e-mail de
   contato, ferramenta de IA da correção). Pode mandar os dados ao Claude
   que ele preenche.
2. **[Você]** Resolver a conta real do Mercado Pago e ter em mãos o
   **Access Token de produção** (começa com `APP_USR-`). Sem ele ninguém
   consegue pagar de verdade.

## Endereço

3. **[Você]** Escolher e comprar o domínio.
   - Para `.com.br`: em **registro.br** (precisa de CPF ou CNPJ). Custa por
     ano. Depois da compra, em "DNS" do registro.br, troque os servidores
     DNS pelos dois que o Cloudflare mostrar no passo 5.
   - Para `.com` e outros: dá para comprar direto no Cloudflare
     (Domain Registration), e aí o DNS já fica lá.
   - Sem domínio, o site funciona em `https://<nome>.pages.dev`, mas trocar
     depois dá retrabalho no Supabase, no Google e no Mercado Pago.

## Cloudflare Pages

4. **[Você]** Criar a conta grátis em `dash.cloudflare.com` e confirmar o
   e-mail.
5. **[Você]** Em **Websites > Add a site**, colocar o domínio (plano Free).
   O Cloudflare mostra dois servidores DNS: coloque-os no registro.br
   (passo 3). A troca leva de minutos a algumas horas.
6. **[Você]** Em **Workers & Pages > Create > Pages**, escolher um dos dois
   jeitos de subir o site:
   - **Subir a pasta (mais simples).** "Upload assets", nome do projeto
     `itoefl`, e arrastar a pasta `artifact` que o Claude buildar. A cada
     versão nova, repetir o upload.
   - **Ligar ao GitHub (automático a cada push).** "Connect to Git", dar
     acesso ao repositório privado `Fatrock3871/itoefl`, branch `main` e:
     - Build command: `pip install markdown && cd app && python build_pipeline.py && python build.py`
     - Build output directory: `artifact`
     - Variáveis de ambiente (Settings > Environment variables):
       `PYTHON_VERSION` = `3.13`, `SITE_URL` = o endereço final,
       `SUPABASE_URL` = a URL do projeto Supabase e
       `SUPABASE_PUBLISHABLE_KEY` = a chave publishable (a mesma do
       `app/supabase_config.json`; nunca a secret).
7. **[Você]** No projeto do Pages, **Custom domains > Set up a custom
   domain**: colocar o domínio (e o `www`, se quiser). O HTTPS sai sozinho.

## Endereço no código

8. **[Claude]** Trocar `SITE_URL` em `app/site.json` pelo endereço final
   (ex.: `https://itoefl.com.br`, sem barra no fim), buildar, rodar
   `python scripts\prepublish_check.py` (tem de dizer "Pronto para
   publicar") e commitar. É o único lugar do código com o endereço: dele
   saem canonical, og:url, `robots.txt` e `sitemap.xml`. O resto do site
   usa o endereço em que está aberto.

## Supabase

9. **[Você]** Em **Authentication > URL Configuration**:
   - **Site URL:** o endereço final, ex. `https://itoefl.com.br`.
   - **Redirect URLs:** adicionar `https://itoefl.com.br/**`. Pode manter o
     `http://localhost:8000/**` para os testes locais.
10. **[Claude]** Gravar o endereço nos secrets das functions e publicar as
    duas que o usam, conferindo a versão publicada depois:
    `supabase secrets set SITE_URL=https://itoefl.com.br`, depois
    `supabase functions deploy create-checkout` e
    `supabase functions deploy review-essay`. O `SITE_URL` das functions
    serve para a volta do pagamento (`create-checkout`) e para o link do
    e-mail de redação corrigida (`review-essay`, via `_shared/mail.ts`).

## Google (login com Google)

11. **[Você]** No Google Cloud Console, em **APIs e serviços > Credenciais**,
    no cliente OAuth do iTOEFL:
    - **Origens JavaScript autorizadas:** adicionar o endereço final.
    - **URIs de redirecionamento autorizados:** continua só a do Supabase,
      `https://itfosjcymqfzjsftvjey.supabase.co/auth/v1/callback`. Ela não
      muda com o domínio.
12. **[Você]** Em **Tela de consentimento OAuth**: colocar o domínio em
    "Domínios autorizados", a página inicial (`https://itoefl.com.br`), a
    política (`https://itoefl.com.br/privacidade`) e os termos
    (`https://itoefl.com.br/termos`). Depois **Publicar app** para sair do
    modo "Testing". Enquanto estiver em Testing, só os e-mails de teste
    cadastrados conseguem entrar com Google.

## Mercado Pago

13. **[Você]** Trocar o token de teste pelo de produção:
    `supabase secrets set MP_ACCESS_TOKEN=APP_USR-...` (ou pedir ao Claude
    e colar o token só no terminal, nunca no chat nem num arquivo).
14. **URLs de retorno:** nada a fazer no painel. A function `create-checkout`
    monta a volta (`?mp=success`, `?mp=failure`, `?mp=pending`) a partir
    do `SITE_URL` do passo 10, e com https o retorno automático liga.
15. **Webhook:** nada a fazer no painel. Cada pagamento já leva o endereço
    `https://itfosjcymqfzjsftvjey.supabase.co/functions/v1/mp-webhook`, que
    não muda com o domínio. Se um dia cadastrar webhook no painel do Mercado
    Pago, use esse mesmo endereço.

## E-mail próprio (SMTP)

16. **[Você]** Contratar um serviço de envio (ex.: Resend, Brevo ou o
    e-mail do próprio domínio) e criar o remetente
    `nao-responda@itoefl.com.br`. O serviço pede registros DNS (SPF, DKIM):
    cadastrar no Cloudflare, em DNS do domínio.
17. **[Você]** No Supabase, em **Authentication > Emails > SMTP Settings**,
    ligar o SMTP próprio com os dados do serviço. Sem isso, os e-mails de
    confirmação e de senha saem do servidor de teste do Supabase, que tem
    limite baixo por hora.
18. **[Claude]** Gravar os mesmos dados nos secrets das functions
    (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`),
    para o aviso de redação corrigida. Passo a passo em
    `docs/deploy-redacao.md`.

## Testar

19. **[Você]** No celular, com 4G e fora do Wi-Fi de casa, abrir
    `https://itoefl.com.br/apresentacao`:
    - fazer o diagnóstico grátis, criar conta, confirmar o e-mail e entrar;
    - entrar com Google;
    - comprar o plano mais barato e ver o acesso liberar (reembolsar depois
      pelo painel do Mercado Pago, se quiser);
    - no Chrome do Android ou no Safari do iPhone, "Adicionar à tela
      inicial" e abrir o app instalado sem internet.
20. **[Claude]** Conferir no endereço publicado: cabeçalhos de segurança,
    service worker instalado, `sitemap.xml` e `robots.txt`, e marcar a
    0.4 do `ROADMAP.md`.

## Observação sobre a página inicial

No Cloudflare Pages, o endereço raiz (`/`) abre o app (a tela de login), e a
apresentação fica em `/apresentacao`. A tela de login já tem o link
"Conhecer a plataforma e os planos". Fazer a raiz abrir a apresentação
exige mudar o nome do arquivo do app (o Cloudflare manda `/index.html` para
`/`), mudança separada que o Claude faz se você quiser. Até lá, divulgue o
link `/apresentacao`.
