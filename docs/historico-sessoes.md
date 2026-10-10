# Histórico de sessões do iTOEFL

O que cada sessão fez, as fases antigas do projeto e listas de pendências que
já foram substituídas. Movido do `ROADMAP.md` em 2026-10-07, sem alterar o
texto. **Nada aqui é lista de pendências válida:** a única é a seção "Tudo que
falta" do `ROADMAP.md`. Sessão nova entra no topo.

---

## Sessão 2026-10-08 (segunda leva): cronogramas, três planos, tela de apresentação

Sessão do desenvolvedor a pedido do gerente (Hermes), com as decisões do dono
do dia: nomes dos cronogramas, diagnóstico grátis sem conta, reembolso de 7
dias, selo "Recomendado".

- `81efb94` Cronogramas do M0 viram Intensivo (30), Regular (60) e Completo
  (90). Sem migração: nenhuma chave guardava o nome.
- `72e461c` Planos no servidor: preço e prazo em
  `supabase/functions/_shared/plans.ts`, `create-checkout` recebe só o id,
  `mp-webhook` grava pela função de banco `apply_payment`, tabela `payments`
  e `entitlements.expires_at`. Migração em
  `supabase/migrations/20261008_planos.sql`.
- `3740b2d` Planos no site: escolha na tela de compra, acesso vencido no
  bloqueio e em Minha conta, termos com planos e reembolso, e
  `docs/deploy-planos.md`.
- `d62324e` Tela de apresentação (`artifact/apresentacao.html`), com o
  diagnóstico sem conta e a tabela de planos.
- `06e1697` Divergências da ETS: pontos brutos 35 contra 30 (o site fica com
  o Blueprint e o M0 explica), envio de notas e versão do sistema apontam
  para a página oficial.
- Plano da versão gratuita em `docs/versao-gratuita.md`, sem implementar.

O smoke test foi de 168 para 201 checagens.

**Não executado, de propósito:** nenhum SQL rodou, nenhuma function foi
publicada, o site não foi publicado. As duas functions foram revisadas por
leitura e nunca rodaram (a máquina não tem Deno): a primeira execução é o
deploy, e o `docs/deploy-planos.md` traz os testes de compra que cobrem
isso.

**Não verificado:** nada em aparelho real. A tela de apresentação foi
conferida em Chrome a 1280 e a 375 px, nos dois temas. O texto dela e o dos
termos novos precisam ser lidos pelo dono, e os termos por advogado.

---

## Sessão 2026-10-08: caça a erros, conferência de conteúdo, auditoria e melhorias

Sessão do desenvolvedor a pedido do gerente (Hermes), em três fases.

**Fase 1, erros.** O site sem login foi percorrido num Chrome de verdade
(`scripts/cdp.py`, cliente do DevTools só com a biblioteca padrão): os 10
módulos, todos os widgets, recarga, 375 px, dois temas, service worker.

- `a86c38f` Contraste AA: botões laranja davam 3,4:1 no claro e 2,7:1 no
  escuro. Mapa do curso da gaveta estava com altura zero.
- `8a0ca18` Data da sequência em UTC (o dia virava às 21h), sequência marcada
  só por abrir o site, HTML no registro de erros, reinício incompleto,
  importação sem marcar sincronização, "✓" no rótulo de continuar, texto de
  concluir Parte não clicável.
- `7e6ac8a` `scripts/build_teste.py` gera a pasta inteira (manifesto, service
  worker, ícones).
- `d2ab7a2` `scripts/smoke_browser.py`: passada do smoke test com recarga,
  celular, contraste e ciclo do service worker.

Conferido e sem defeito: persistência de todos os widgets, estouro em 375 px,
links internos, os quatro links da ETS e o service worker depois de um build
novo (mostra o aviso, troca no "Recarregar", abre offline).

**Fase 2, conteúdo.** `eb90f10`. Registro em
`docs/conferencia-conteudo-2026-10.md`. Os três PDFs da ETS de hoje são
idênticos aos de ontem. Corrigidos M0, M3, M5, M7 e M8.

**Fase 3, nível da plataforma.** `c2b1cb2` auditoria em
`docs/auditoria-plataforma-2026-10.md`. Depois, em ordem: `e5bc999`
devolutiva em palavras e barra do topo; `e4b39a8` cartão "Comece aqui";
`92d3152` teclado, janelas, rótulos, `lang="en"`, toque; `6b89240` sequência
na gaveta, fontes por `<link>`, erros de login em português.

O smoke test foi de 126 para 168 checagens.

**Não verificado:** nada rodou em aparelho real nem com leitor de tela. As
páginas web da ETS foram lidas por ferramenta que resume; só os PDFs foram
conferidos por busca literal. A tela de login foi vista, mas login, compra e
sincronização de verdade não foram exercitados (dependem do Supabase).

---

## Sessão 2026-10-07 (noite): banco, conferência com a ETS, PWA, videoaulas, aprofundamento

Sessão do desenvolvedor a pedido do gerente (Hermes), retomando três
worktrees que tinham ficado pela metade. Tudo foi revisado antes de entrar no
`main`. Commits, na ordem:

- `76c795e` `build.py` cria `artifact/` se não existir (clone novo quebrava).
- `9768244`, `9b28877`, `4edb84f` Banco de questões: formato do item, JSON
  Schema, validador, 228 itens migrados (origem 228, destino 228) e
  `supabase/schema-bank.sql`, só escrito, nunca executado. O smoke test passou
  a validar o banco e a acusar `bank/items/migrado/` desatualizado.
- `bcbccd4` Números do formato 2026 conferidos contra cinco fontes da ETS,
  registro em `docs/conferencia-formato-2026.md`. Saiu a pausa de 10 minutos
  que não existe, Listening passou a 25 a 29 minutos, ordem das seções fixa,
  concordância oficial com o 0 a 120.
- `be77dd9` PWA: manifesto, ícones, service worker com versão carimbada,
  botão "Instalar app", dica do iOS e aviso de nova versão.
- `5b964dc` Plano B do gravador no iPhone: só gravar por padrão, opção "Só
  transcrever".
- `a06b5bc` Videoaulas: `app/videos.json`, player que só carrega no clique,
  "aula assistida" no progresso, legenda e transcrição recolhível.
- `7269538` Bloco `:::aprofundamento` no pipeline e seletor de trilha.
- `867fc69` Este arquivo: o histórico saiu do `ROADMAP.md`.
- `f548f40` Presets do cronômetro no tempo-base da ETS (Reading 30,
  Listening 29, Writing 23, Speaking 8, prova 89).
- `3bc5baa` Travessão de pausa fora das explicações em português dos drills
  e do diagnóstico (31 trocas).

O smoke test foi de 81 para 126 checagens, com duas passadas novas no
navegador: uma simulando iPhone e outra num build de exemplo feito em pasta
temporária (vídeos e bloco de aprofundamento de mentira, que não entram no
site).

**Não verificado:** nada disto rodou em aparelho real. PWA, gravador no
iPhone e player de vídeo só passaram por Chrome headless.

---

## Sessão 2026-10-07 — Formato real da prova, simulados interativos, viés de gabarito

O usuário delegou a gestão do projeto "por enquanto" e pediu para ser chamado
só em pontos cruciais. Decisões dele nesta sessão: M7 vira interativo, M9
fica como está.

**Origem:** leitura dos quatro testes práticos gratuitos da ETS no formato
2026 (`docs/ets-materiais-oficiais.md`). Dois exercícios do site ensinavam
um formato que não é o da prova.

**Feito, tudo commitado e no GitHub:**

- **M1, Complete the Words de digitar.** Widget novo em que o aluno digita o
  final da palavra, sem alternativas. 8 parágrafos acadêmicos originais, 80
  lacunas, B1 a C1+. Método CTW (2.1) e exemplo resolvido (4.1) reescritos.
  Os 32 itens antigos de múltipla escolha viraram "Grupo A2, treino de base".
- **M4, Build a Sentence no molde da prova.** Fala de contexto, trechos
  fixos, espaços a preencher e, em 5 itens, um bloco que sobra. 30 itens
  originais com foco em pergunta indireta. Widget com id novo (`m4build2`):
  o progresso do widget antigo não se aplica.
- **M4, caixa de escrita.** Campo com cronômetro (7 ou 10 minutos), contador
  de palavras e mínimo de 100 na discussão, embaixo dos 12 enunciados. O
  texto fica salvo e sincroniza. É a tela em que a correção por agente da
  Etapa 3 vai se encaixar.
- **M3, Speaking em cenário.** 5 cenários de Listen and Repeat (7 frases
  crescentes) e 4 entrevistas (4 perguntas em escada), com áudio sintético e
  texto escondido. A entrevista tem contagem de 45 segundos por resposta.
- **M7 interativo.** 19 blocos, 62 questões, correção só na entrega. O
  pipeline lê as questões e o gabarito do próprio `.md`.
- **M7:** os quatro testes oficiais gratuitos indicados como simulados extras.
- **M0:** calculadora de score (percentual por seção em banda, mais a banda
  geral) e resumo do módulo no topo.
- **M0, treino no seu nível.** Sorteia, a cada sessão, 5 exercícios cuja
  faixa CEFR inclui o nível estimado do aluno, misturando habilidades e
  priorizando o que ainda não foi feito. 40 exercícios têm faixa declarada.
- **Tempos corrigidos** no M4 e no M8: e-mail de 7 minutos com três pontos
  obrigatórios, discussão de 10 minutos com mínimo de 100 palavras, Build a
  Sentence em cerca de 6.

**Defeito grave achado no caminho: gabarito viciado em uma letra.** A resposta
certa era "B" em 66% a 81% dos itens de quase todos os drills, e "C" em 7 das
10 questões do diagnóstico. Marcar sempre a mesma letra dava nota alta, o que
invalidava o diagnóstico e o painel de desempenho. Corrigido em duas camadas:

1. `app/rebalance.py` redistribui a letra correta no build, de forma
   determinística, e remapeia as citações "(B)" das explicações. Depois:
   nenhuma letra passa de 38% em nenhum módulo. Conferido por script: 118
   itens, 85 mudaram de letra, 218 citações, 0 inconsistências.
2. A pedido do usuário, o `app.js` embaralha a ordem das alternativas na
   tela a cada carregamento e a cada "Refazer". A correção usa a letra de
   origem, então o progresso salvo continua valendo.

**Auditoria de consistência dos 10 módulos (por script, não por leitura):**
0 referências cruzadas quebradas ("Módulo N, Parte X", "Parte X.Y"), 0
parágrafos repetidos, e os números da prova conferem com o blueprint em
todos os módulos, exceto os tempos de Writing do M8, corrigidos. O script
não avalia qualidade de texto: isso continua dependendo de leitura humana.

**Smoke test:** de 33 para 75 checagens.

**O que ficou de fora, com o motivo:**

- **Gerar questões novas por nível.** O usuário pediu que o sistema "gere
  questões de acordo com cada nível de diagnóstico". O que foi feito escolhe
  entre exercícios que já existem. Criar questão nova na hora exige o banco
  de questões (Etapa 2) ou chamada de IA por aluno (Etapa 3, que depende do
  modelo de cobrança). Hoje o conjunto por nível é pequeno: 40 exercícios.
- **Writing e Speaking dos simulados do M7** continuam em texto. Só a
  múltipla escolha virou interativa.
- **Painel "Seu desempenho real" e a meta diária** ainda não contam os
  exercícios novos (Complete the Words, Build a Sentence, Speaking, M7).
- **Nada disso foi testado por uma pessoa num navegador de verdade.** Tudo
  passou no Chrome headless. O áudio dos conjuntos de Speaking depende da
  voz sintética do aparelho e não foi ouvido.
- **Os textos novos são originais meus e não passaram por revisão de um
  professor de inglês.** Vale uma leitura antes de vender.

---

## Sessão 2026-10-06 — GitHub, roadmap único e cinco pendências de código

- **Repositório no GitHub:** `https://github.com/Fatrock3871/itoefl`, privado,
  branch `main`. README reescrito para colaboradores.
- **Debug do checkout removido.** O erro do Mercado Pago agora vai só para o
  log da function; o aluno vê mensagem genérica.
- **Minha conta ganhou duas seções.** "Acesso" mostra pago, sem acesso ou
  conta de administrador, lendo `entitlements`. "Excluir conta" pede a
  palavra EXCLUIR, chama a function nova `delete-account` e limpa os dados do
  aparelho. A function só apaga o dono do token e confere a palavra de novo
  no servidor.
- **Termos de Uso e Política de Privacidade** em `legal/*.md`, publicados como
  páginas próprias para abrirem sem login. Rascunho, com campos a preencher.
- **Limpeza:** `showLockMessage()`, `.lock-msg` e `UNLOCK_PCT` removidos;
  textos que ainda falavam em "usuário e senha" corrigidos; `schema.sql`
  passou a apagar as sobras do login por nome de usuário; `CLAUDE.md`,
  `docs/supabase-setup.md` e `docs/mercadopago-setup.md` atualizados.
- **Bug real achado no caminho: o webhook do Mercado Pago nunca rodaria.** O
  `mp-webhook` estava publicado com verificação de JWT ligada. O Mercado Pago
  não manda header de autenticação, então o Supabase respondia 401 antes de o
  código rodar. Nenhum pagamento aprovado liberaria acesso. Não tinha
  aparecido porque nenhum pagamento de teste chegou a ser aprovado.
  Corrigido em `supabase/config.toml` (`verify_jwt = false` só para essa
  function) e republicado. Conferido por chamada direta: antes 401, agora
  `ok` para notificação que não é pagamento e 502 para pagamento inexistente,
  que é o comportamento esperado do código.
- **Publicado no Supabase nesta sessão:** `create-checkout` v11 (conteúdo
  conferido contra o arquivo local), `mp-webhook` v4, `delete-account` v1.
- **Não testado:** a exclusão de conta de ponta a ponta com um usuário real.
  Testado só o formulário (smoke test) e a recusa de chamada sem login.
  Testar com uma conta descartável antes de publicar.
- Smoke test passou de 23 para 33 checagens.

---

## Sessão 2026-09-24 — Cupom de desconto no checkout; botão "Pagar" travado de novo

- **Cupom de desconto: implementado, aguardando teste do usuário.** Decisões
  travadas com o usuário antes de mexer: cupons vivem numa tabela nova no
  Supabase (não hardcoded, pra poder criar/desligar sem rebuild), só
  desconto percentual (sem valor fixo), sem data de expiração nem limite de
  usos — controle é só um campo `active` (liga/desliga a linha).
  - `supabase/schema.sql`: tabela `coupons` (`code` texto primário,
    `percent` 1–100, `active` boolean). RLS com policy de select só pra
    `active = true`; nenhuma policy de insert/update/delete pra
    `authenticated` — só o SQL Editor (ou `service_role`) cria/edita cupons.
    Exemplo de uso comentado no próprio arquivo (`insert into coupons
    (code, percent) values ('LANCAMENTO20', 20);`).
  - `supabase/functions/create-checkout/index.ts`: aceita `coupon` opcional
    no corpo da chamada; se vier preenchido, busca na tabela (case
    insensitive via `ilike`), recusa com 400 + mensagem clara se inválido/
    inativo, senão recalcula `unit_price` com o desconto antes de criar a
    preferência no Mercado Pago.
  - `app/build.py`: campo "Cupom de desconto (opcional)" novo no `#payGate`,
    reaproveitando as classes `.auth-field`/`.auth-label`/`.auth-input` que
    o login já usava (sem CSS novo).
  - `app/app.js`: manda o valor do campo junto no `create-checkout`; e —
    achado no caminho — o tratamento de erro genérico só mostrava "Edge
    Function returned a non-2xx status code" pra qualquer falha, incluindo
    cupom inválido. Corrigido lendo o corpo JSON de verdade da resposta
    (`res.error.context.json()`) pra mostrar a mensagem real ("Cupom
    inválido ou expirado.").
  - **Testado de ponta a ponta e funcionando (2026-09-24).** `schema.sql`
    rodado (tabela `coupons` criada), cupom `TESTE20` (20%) inserido via SQL
    Editor, aplicado no checkout sandbox com sucesso. **Achado no
    caminho, mesmo padrão já visto na sessão 2026-09-22:** o primeiro
    `supabase functions deploy create-checkout` reportou sucesso mas a
    versão publicada continuou sendo a antiga (sem lógica de cupom) —
    resultado observado foi preço sempre R$ 9,90, sem erro nenhum, porque a
    function nem tentava ler o cupom ainda. Confirmado comparando a aba
    "Code" do painel (com Ctrl+Shift+R) com o arquivo local; um segundo
    deploy resolveu. Vale desconfiar disso de novo sempre que um fix na
    função não parecer "pegar" no teste.
- **Botão "Pagar" do Mercado Pago travado de novo (mesmo sintoma da sessão
  2026-09-22, item 4) — causa raiz confirmada de vez.** Usuário mandou print
  mostrando a tela "Revise os dados antes de pagar" (checkout hospedado pelo
  próprio Mercado Pago, fora do nosso controle) com o botão "Pagar"
  cinza/desabilitado, mesmo com cartão salvo selecionado. **Importante:** o
  campo "Inserir cupom" visível nessa tela é um recurso **nativo do Mercado
  Pago**, sem relação com o cupom que a gente construiu (o nosso fica antes,
  na nossa própria tela `#payGate`, antes do redirect) — não foi essa
  mudança que quebrou o botão.
  - **Confirmado nesta sessão:** é sempre `NordicHydrateRootError: An
    recoverable error occurred during hydration` em
    `px-checkout-frontend/app.5d279d12.js` (confirmado no Console pelo
    próprio usuário, e depois de novo por um agente Claude com acesso ao
    navegador via extensão Claude in Chrome, que bateu no mesmo erro e
    documentou a causa: **qualquer extensão de navegador ativa** quebra a
    hidratação React dessa página do MP, não é uma extensão específica.
    Confirma a suspeita original da sessão 2026-09-22.
  - **Único workaround conhecido: aba anônima/incógnito de verdade**, sem
    nenhuma extensão carregada (o que inclui não poder usar Claude in Chrome
    nessa aba, já que ele próprio é uma extensão). Testar o cartão de
    pagamento em si (preencher número/CVV/CPF e clicar "Pagar") por isso
    só pode ser feito manualmente pelo usuário, nunca por um agente com
    acesso ao navegador via extensão.
  - **Ainda pendente:** com o cupom confirmado funcionando (checkout mostrou
    R$ 7,92 corretamente), falta só o usuário completar o pagamento de teste
    numa aba anônima de verdade com os dados de cartão de teste (Mastercard
    `5031 7557 3453 0604`, validade `11/30`, CVV `123`, titular `APRO`, CPF
    `191.111.111-11`) pra confirmar aprovação e liberação de acesso de ponta
    a ponta.
- **Nova frente aberta pelo usuário, sem decisão ainda:** considerar trocar
  o Mercado Pago por outro gateway de pagamento "pra facilitar" — motivo
  não detalhado ainda (pode ser o histórico de bugs de sandbox/checkout
  travado, ou outro motivo). **Combinado com o usuário:** terminar o cupom
  primeiro (é independente de gateway, funciona igual em qualquer um) e
  discutir a troca depois, com calma. Nenhuma pesquisa de alternativa
  (Stripe, Pagar.me, etc.) feita ainda — conversa não retomada nesta sessão.

---

## Sessão 2026-09-22 — Google login, Mercado Pago configurados; login volta a ser só e-mail

- **Login com Google: configurado e funcionando.** Usuário criou o app no
  Google Cloud (hoje via "Google Auth Platform", não mais a antiga tela
  "OAuth consent screen"), gerou Client ID/Secret, colou no Supabase
  (Authentication → Providers → Google). Achado no caminho: o campo
  "Client IDs" do Supabase tinha sido preenchido com o nome do projeto
  ("ITOELF") em vez do Client ID de verdade — corrigido.
- **Mercado Pago: configurado de ponta a ponta.** Schema rodado de novo
  (cria `entitlements`), aplicação criada no painel do Mercado Pago,
  credenciais de teste obtidas, Supabase CLI instalado via Scoop (não
  winget — o pacote `Supabase.CLI` não existe lá; `npm` também não estava
  disponível, o projeto não usa Node pra mais nada), `supabase link`,
  `MP_ACCESS_TOKEN` configurado como secret, as duas edge functions
  (`create-checkout`, `mp-webhook`) publicadas. Preço ajustado de R$ 197
  para **R$ 9,90** (`PRICE_BRL` na function + texto do botão em `build.py`).
- **Bug real achado e corrigido testando o checkout ao vivo:** o botão
  "Comprar acesso" dava sempre "Não autenticado.", mesmo logado —
  `client.functions.invoke("create-checkout")` não estava anexando o header
  `Authorization` com o token de sessão (só mandava o `apikey`). Corrigido
  buscando a sessão via `client.auth.getSession()` e passando o
  `access_token` explicitamente no header da chamada.
- **Teste de compra: checkout abre e processa pagamento; só falta achar o
  cartão de teste certo pra ver a liberação de acesso de ponta a ponta.**
  Sequência real do que aconteceu (deixado detalhado de propósito, é fácil
  de esquecer a ordem):
  1. Erro "At least one policy returned UNAUTHORIZED." (`blocked_by:
     PolicyAgent`, código `PA_UNAUTHORIZED_RESULT_FROM_POLICIES`) ao criar a
     preferência — **não é bug nosso**, é a política antifraude do Mercado
     Pago bloqueando a conta real do usuário (provavelmente por ainda não
     estar totalmente validada/ativada, mesmo com pendências resolvidas no
     meio do caminho). **Resolvido usando as credenciais de PRODUÇÃO da
     CONTA DE TESTE** (`TESTUSER5753308815578190935`, logada numa janela
     anônima separada) em vez das credenciais de teste da conta real — é
     assim que o Mercado Pago documenta o fluxo de sandbox: a conta de teste
     inteira já é sandbox, então usa as próprias credenciais "de produção"
     dela sem risco.
  2. Depois disso, novo erro: `"auto_return invalid. back_url.success must
     be defined"` — o Mercado Pago exige que as `back_urls` sejam **https**
     de verdade quando `auto_return` está ligado; `http://localhost` não
     serve. Corrigido em `create-checkout/index.ts`: `auto_return` só é
     enviado quando o `origin` é https (ou seja, liga sozinho quando o site
     for publicado de verdade; em localhost o aluno só precisa clicar num
     botão "Voltar" na tela do Mercado Pago).
  3. **Achado no processo:** o deploy da função (`supabase functions deploy
     create-checkout`) várias vezes reportou sucesso no terminal mas não
     atualizava o código de verdade (confirmado comparando o arquivo local
     com a aba "Code" do painel) — **sem causa raiz identificada**, só
     resolvido insistindo (rodar de novo, conferir a aba "Overview" pelo
     horário do último deploy, dar Ctrl+Shift+R na aba "Code" do painel
     pra não ver cache do navegador). Vale desconfiar disso de novo se um
     fix não parecer "pegar".
  4. Depois dos dois fixes, o checkout abriu de verdade — mas o botão
     "Pagar" não reagia a clique nenhum. Causa: **uma extensão do
     navegador** quebrando a hidratação do React da página do Mercado Pago
     (console mostrava `NordicHydrateRootError`/React error #418 e um aviso
     de CSP bloqueando um script inline — assinatura clássica de extensão
     mexendo no DOM antes da página carregar). **Resolvido testando numa
     janela anônima** (extensões desativadas por padrão).
  5. **Onde parou:** na aba anônima, logado como o usuário de teste
     (`TESTUSER5753308815578190935`), o pagamento chegou a ser processado
     (sem mais travar), mas foi recusado mesmo usando o cartão recomendado
     já salvo na conta (Mastercard Santander ****3311) e também um cartão
     digitado na mão com nome de titular `APRO` (que deveria simular
     aprovação automática). Não é mais um bug de código/configuração
     conhecido — é sobre achar a combinação de cartão de teste que essa
     conta específica aceita. **Adiado pra uma próxima sessão.**
- **Pendência de limpeza:** `create-checkout/index.ts` está devolvendo o
  corpo inteiro do erro do Mercado Pago (`mpBody`/`mpStatus`) na resposta
  HTTP, só pra depurar durante essa sessão. Não vaza nenhum segredo, mas
  não é algo que faça sentido o aluno ver — trocar de volta por uma
  mensagem genérica quando o pagamento estiver 100% confirmado.
- **Achado no caminho: limite de e-mail do plano grátis do Supabase.**
  Testar criação de conta repetidas vezes bateu no limite de envio de
  e-mail (confirmação/recuperação) mais de uma vez. "Confirm email" foi
  desligado temporariamente em Authentication → Providers → Email pra
  testar sem depender de e-mail — **lembrar de ligar de volta antes de ir
  pra produção**, senão qualquer um cria conta sem confirmar o e-mail de
  verdade. Nesse processo, "Enable email provider" (o toggle principal, não
  o "Confirm email") foi desligado por engano uma vez — religado.
- **Login volta a ser só e-mail+senha (commit 315f380), sem nome de
  usuário.** Reverte a decisão de 2026-09-17: tirado o campo "Nome de
  usuário" do cadastro e do login, o link "Esqueci meu usuário", a seção
  "Nome de usuário" de Minha conta, e todo o código de
  checagem/atualização de usuário em `app.js` (a RPC `email_for_username`
  não é mais chamada pelo site, mas continua existindo no schema do
  Supabase — remover do banco é opcional, não urgente). Login e cadastro
  chamam `signInWithPassword`/`signUp` direto com e-mail.
- **Fix de configuração:** `Authentication → URL Configuration → Site URL`
  estava como `http://localhost:8000` (a raiz, que só mostra uma listagem
  de pastas) em vez de `http://localhost:8000/artifact/index.html` (o site
  de verdade) — corrigia o link de confirmação de e-mail caindo na página
  errada.
- **⚠️ Duas senhas reais do usuário apareceram em texto puro no chat**
  durante essa sessão (a senha do banco de dados do Supabase, colada sem
  querer num comando de terminal, e a senha da conta Google/admin
  `pietrooliveiramarquespp@gmail.com`, mencionada diretamente). Recomendado
  ao usuário trocar as duas; não há como saber se ele já trocou.

---

## Sessão 2026-09-21 — UX da logo, navegação por Parte, progresso granular

- **Logo:** removida a moldura quadrada e depois o halo branco em volta da
  flor (pedidos em duas rodadas); tentativa de bolinha animada "pulando" da
  logo até o "i" foi implementada, testada, e depois **removida** a pedido
  (usuário achou feia). Fonte do wordmark trocada pra Baloo 2 (bubble/rounded,
  igual à referência que o usuário mandou); layout logo-em-cima/texto-embaixo
  aplicado em `.brand` (sidebar) e `.auth-gate-brand` (login/paywall). Avião
  decorativo sobre o wordmark: adicionado, ajustado (trajeto i→L e volta,
  sempre bico pra baixo, espelhando de lado por perna do trajeto) e depois
  **removido por completo** a pedido do usuário.
- **Sidebar:** logo centralizada de verdade (bug: `justify-content:space-between`
  com o botão de fechar empurrava a marca pra esquerda). "Mapa do curso"
  reposicionado pra ficar logo acima da lista de módulos, não mais entre a
  logo e o card de progresso.
- **Navegação livre + qualidade:** suíte de smoke test (`scripts/smoke_test.py`,
  23 checagens) continua sendo a rede de segurança padrão, rodada a cada
  mudança de fonte nesta sessão.
- **Paginação por Parte tipo flashcard:** cada módulo mostrava todas as
  Partes (H2) empilhadas; agora só uma Parte fica visível por vez, com barra
  "Parte X de Y" (Anterior/Próxima) no topo e botão grande no fim de cada
  Parte pra avançar. Posição salva por módulo (`toefl_partpos_v1`).
- **Transição entre módulos:** ao terminar a última Parte de um módulo, os
  botões de navegação oferecem ir direto pro próximo módulo em vez de só
  travar/desabilitar; no último módulo (M9) mostra uma nota de curso
  concluído.
- **Progresso granular por subseção:** antes só dava pra marcar a Parte (H2)
  inteira como concluída. Cada subseção (h3) ganhou seu próprio checkbox
  "Marcar esta subseção como concluída" + um ✓ visível no título mesmo
  fechada (`toefl_h3progress_v1`, sincroniza como o resto do progresso).
- **"Continuar de onde parei":** novo botão na sidebar (card de Progresso
  Geral) que grava a última subseção lida (via o mesmo observer que auto-abre
  subseções ao rolar) e pula direto pra lá — troca de módulo, abre a
  subseção, dá scroll e um flash de destaque. Integrado com a paginação por
  Parte (pula pra Parte certa antes de rolar até a subseção).
- **Revisão de conteúdo PT/inglês:** a pedido do usuário, um agente leu os 10
  módulos inteiros checando se as explicações em português estavam rasas
  demais e se algum exercício estava incorretamente em português. Resultado:
  **conteúdo já estava correto** (separação PT/inglês consistente, explicações
  já densas com exemplos). Achados 2 nits cosméticos, corrigidos: gabarito
  confuso no M6 Drill 6, título "6 fonemas" no M9 que na verdade lista 9.
- Diversos ajustes menores de UI já cobertos em sessões anteriores (fonte
  maior, dashboard semanal interativo, ícones/contraste do login) seguem
  valendo, não repetidos aqui.

---

## Mapa do que falta (2026-09-20, atualizado em 2026-09-24)

> Substituído em 2026-10-06 pela seção "Tudo que falta" no topo deste
> arquivo. Mantido aqui só pelo detalhe de cada item.

### 🔴 Bloqueia uso real por alguém além do usuário/dono

1. **Publicar o site.** Hoje só roda local (`python scripts\serve.py`). Sem
   isso, nenhum link existe pra mandar pra ninguém testar. Checklist da
   Fase 6 já preparado em sessão anterior, nunca executado. **Pendências
   pra quando publicar:** trocar o Site URL/Redirect URLs do Supabase (hoje
   `localhost:8000`) pra URL final; adicionar a mesma URI de callback nova
   nas Authorized redirect URIs do Google Cloud; religar "Confirm email".
2. ~~**Configurar login com Google.**~~ **FEITO (2026-09-22).** Provedor
   ativado no Supabase, credenciais OAuth criadas no Google Cloud, testado
   e funcionando. App Google ainda em modo "Testing" — só e-mails
   adicionados como testador conseguem logar por ele; qualquer pessoa
   consegue logar por e-mail/senha normalmente.
3. **Configurar Mercado Pago — muito perto de pronto, mas com um bug novo
   (ou recorrente) achado em 2026-09-24.** Credenciais, CLI, secret e as
   duas edge functions publicados; preço ajustado pra R$ 9,90; cupom de
   desconto implementado (ver Sessão 2026-09-24). O botão "Pagar" da tela
   hospedada pelo próprio Mercado Pago voltou a ficar travado/desabilitado
   mesmo com cartão salvo selecionado — mesmo sintoma da sessão anterior
   (extensão do navegador quebrando a hidratação React da página), ainda
   não confirmado se é a mesma causa ou algo novo; usuário vai testar em
   aba anônima e checar o Console. **Falta:** confirmar a causa do botão
   travado, achar a combinação de cartão de teste que essa conta de teste
   aceita (recusou o cartão salvo recomendado e um cartão `APRO` digitado à
   mão), tirar o debug temporário de `create-checkout/index.ts`, religar o
   "Confirm email" do Supabase, e trocar as credenciais de teste pelas de
   produção antes de cobrar de verdade. **Em discussão, sem decisão:**
   usuário levantou a possibilidade de trocar o Mercado Pago por outro
   gateway de pagamento — conversa aberta, retomar quando o usuário priorizar.

### 🟡 Funcionalidades pedidas, ainda não construídas

4. **Vídeos explicativos por módulo.** Usuário está gravando por fora
   (ferramenta de IA, provavelmente Synthesia/HeyGen). Quando mandar os
   arquivos/links, falta decidir hospedagem e montar o player no
   `.panel-head` de cada módulo.
5. ~~**Cupom de desconto no checkout.**~~ **FEITO e testado (2026-09-24).**
   Tabela `coupons` no Supabase (código, percentual, ativo), validado na
   edge function `create-checkout` antes de gerar a preferência no Mercado
   Pago, campo novo na tela de pagamento do site. Testado de ponta a ponta
   com o cupom `TESTE20` (20%), preço final correto no checkout sandbox.
   Ver detalhe completo na Sessão 2026-09-24 acima.
6. **Correção por IA (Speaking/Writing).** Adiada de propósito até o
   projeto ter retorno financeiro (custo por chamada de API). Foi
   parcialmente compensada por duas features mais baratas já implementadas:
   áudio sintético no Listening e transcrição automática no gravador do
   Speaking — nenhuma delas dá nota, só ajuda na autoavaliação.
7. **"Minha conta" — itens que faltam:**
   - Ver status de pagamento ali dentro (a tabela `entitlements` já existe,
     só falta mostrar "Pago ✓" / "Sem acesso" na tela).
   - Excluir conta (exige função server-side com `service_role`, não dá
     pra fazer só no navegador por segurança — maior escopo que os outros
     itens da tela).

### 🟢 Qualidade e robustez

8. ~~**Nenhuma suíte de teste automatizada.**~~ **FEITO (2026-09-20).**
   `scripts/smoke_test.py`: builda o site, roda 23 checagens num Chrome
   headless (gate, progresso/meta diária, painel, Minha conta, tema,
   certificado, pronúncia/áudio, gravador, ausência de erro de JS) +
   mojibake, sai com código 1 se algo falhar. `python scripts\smoke_test.py`.
9. ~~**Tratamento de erro de rede.**~~ **FEITO (2026-09-20).** Corrigido um
   bug real: `checkEntitlement()` não checava erro de consulta e podia
   bloquear quem já tinha pago por causa de uma falha transitória.
   Adicionado `.catch()` no fim das cadeias de chamada que ainda não
   tinham (login, cadastro, checkout, formulários de Minha conta), pra
   não deixar botão travado pra sempre sem mensagem numa rejeição de rede.
10. **Nunca testado em celular real.** Toda a verificação de responsividade
    desta sessão foi via Chrome headless (com limitações conhecidas de
    viewport simulado); nenhum teste em aparelho físico.
11. **Nenhum usuário real testou o fluxo completo.** Maior lacuna de
    qualidade do projeto em si (não de código): dificuldade dos drills,
    ritmo dos módulos, clareza das explicações, nada disso foi validado
    fora desta sessão.
12. **Revisão de consistência pós-edições.** Depois de tantas rodadas de
    corte/reescrita de tom nos 10 módulos, vale uma passada final
    conferindo que nada ficou quebrado, repetido ou com referência cruzada
    desatualizada (padrão do que já aconteceu uma vez em M7, corrigido).

### ⚪ Decisões antigas nunca respondidas (baixa prioridade, podem estar obsoletas)

13. **M0 "expandido como introdução"?** Pergunta de 2026-09-10, nunca
    retomada. M0 já ganhou reescrita de tom depois disso; provavelmente
    não é mais relevante, mas nunca foi formalmente descartada.
14. **Verificar o formato 2026 contra a fonte oficial da ETS** antes de
    considerar o conteúdo definitivamente "fechado" (pendência original
    de 2026-09-03, nunca marcada como feita).

---

## Reescrita de tom dos 10 módulos (2026-09-17) — CONCLUÍDA

A pedido do usuário (diretriz de designer instrucional sênior), o texto vivo
de cada módulo (aberturas, transições, blockquotes explicativos) foi
reescrito em tom de mentor/colega sênior, eliminando fórmulas robóticas
("neste módulo iremos explorar") e travessões usados como pausa dramática.
Tabelas, drills, roteiros passo a passo e blocos de código (diagramas ASCII,
gabaritos) foram deliberadamente preservados sem alteração, por instrução
explícita do usuário.

Diretriz de pontuação seguida em todos os módulos e em toda escrita futura
para este usuário: sem travessão (—) nem meia-risca (–) como recurso de
pausa, ênfase ou separação de ideias, só vírgula, dois-pontos ou frase curta
com ponto final. Hífen fica restrito a palavras compostas gramaticais.
Exceções legítimas mantidas (auditadas módulo a módulo, não são violação):
travessão dentro de bloco de código (diagramas/linhas do tempo) e travessão
como placeholder de célula vazia/N-A em tabela. Meia-risca em intervalo
numérico ("0–120", "CEFR 1–6") também é exceção, por ser convenção
tipográfica diferente da pausa de prosa.

Módulos M0–M9 todos commitados individualmente, cada um com verificação
estrutural (contagem de headings e linhas de tabela idêntica ao HEAD antes
da edição) e auditoria de travessões remanescentes. M0 precisou de um commit
de correção (16 travessões reintroduzidos por engano na primeira passada).

---

## Frentes abertas (2026-09-10) — não misturar

Conversa pulou entre três assuntos. Estado de cada um:

### 1. Conteúdo / lista de módulos
- **Fase 7 concluída:** todos os 10 módulos (M0–M9) expandidos e commitados.
- **PENDENTE — decisão do usuário:**
  - **M0:** o usuário achou que "sumiu". Esclarecido que **não sumiu** (é a 1ª aba,
    sempre aberta, tem o diagnóstico de 10 questões). Falta ele dizer se quer o M0
    **expandido como introdução** ou deixar como está.
  - **M9 (Brazilian Traps):** usuário pediu para **remover**. Sinalizei que M9 é
    conteúdo original (não fui eu que adicionei) e que M1/M4/M7/M8 hoje têm
    referências a ele (sistema de códigos de erro). Falta ele confirmar:
    remover de vez (+ limpar refs) OU fundir o útil em M1/M3/M4 OU manter.
  - Nada foi removido ainda.

### 2. Design / front-end (v2 FEITO — commit ff24901)
- Usuário achou o v1 raso ("só mudou as cores, cara de IA"). Pediu mapa da
  jornada no topo + inspiração em design diferente/inovador (Pinterest).
- Pesquisei tendência 2026 (movimento "anti-IA": tipografia com personalidade,
  anti-grid, brutalismo tátil, textura) e apliquei uma direção **editorial-
  brutalista**: fonte Bricolage Grotesque + Inter; cards/tabelas/pre/botões com
  borda preta 2px + sombra "carimbada" 4px 4px 0; textura de papel sutil (SVG
  noise); logo mark; abertura de módulo com número gigante contornado (efeito
  capa de revista); H2 com espinha laranja; tabelas com cabeçalho preto sólido
  + zebra; bullets seta laranja; negrito com marca-texto sutil.
- **Mapa da jornada** (o pedido central): nav fixo no topo do conteúdo com os
  10 módulos como estações conectadas por trilha — atual destacado, concluído
  ✓, bloqueado 🔒, clicável (mesmo lock de 70%). `build.py` monta o markup,
  `app.js` sincroniza estado em `updateBadges()`/`showTab()`.
- Ajuste fino: tirei sombra repetida das tabelas (pesado com muitas na
  página), afinei borda do blockquote, suavizei o marca-texto do negrito.
- Verificado em claro/escuro, M0/M1, screenshot headless. Sem mudança de conteúdo.
- **v3 (commits 1ce190a, 4c5b34f, 3b482d2):** feedback do usuário no v2 — sidebar
  "feia", queria só o ícone de 3 barrinhas, conteúdo mais bem distribuído,
  fontes padronizadas ("Strong" pros títulos, "Integral CF bold" pro texto),
  tirar as `<hr>` no meio do texto.
  - Sidebar virou **menu-gaveta**: fora da tela por padrão (só o hamburger na
    barra da jornada), abre por cima do conteúdo com backdrop, fecha ao
    navegar/clicar fora/Esc. `.shell` perdeu o grid de 2 colunas.
  - `main`/`.panel-inner` centralizados num container mais largo (1220px/840px)
    — usa o espaço que a sidebar fixa ocupava.
  - `<hr>` no meio do texto virou só espaçamento (sem linha visível).
  - **Fontes:** "Integral CF" é grátis só para uso pessoal (licença paga pra
    uso público) — sinalizado ao usuário, que optou por trocar por
    alternativa aberta. "Strong" era o estilo de texto do Instagram (negrito +
    itálico + caixa alta), não uma fonte — confirmado com o usuário.
    Corpo passou de Inter para **Plus Jakarta Sans** (Google Fonts, OFL);
    título do módulo + "PARTE N" de cada card ganharam o tratamento
    negrito+itálico+caixa-alta (não aplicado em h3/h4 — usados demais,
    atrapalharia a escaneabilidade). Mono removido de badges/rótulos
    decorativos, mantido só em `<code>`/`<pre>` e nos 2 cronômetros.
- **v4 (commit 06897ff):** avatar do usuário (inicial do e-mail, placeholder —
  sem upload real, login é magic link sem perfil); bug de corte corrigido
  (`.journey` era `sticky`, cortava o conteúdo ao rolar — virou estático);
  coluna direita `.rail` com índice "Nesta parte" (links pros H2 do módulo
  atual) pra não deixar tudo num bloco central único, some abaixo de 1080px;
  travessões tirados de todo texto de interface que eu gero (não dos 10
  módulos de conteúdo — isso é tarefa separada, pendente de confirmação);
  checkbox de "concluir" movido do início do H2 pro fim do card
  (`finalizeSection()` em app.js); desbloqueio agora exige 70% dos checkboxes
  **e** todas as questões dos widgets interativos confirmadas
  (`moduleQuizPct()`) — só vale pra M0 (quiz) e M4 (Build a Sentence), que são
  os únicos módulos com widget de questão clicável hoje.
- **v5 (commit ab5736e):** travessões removidos também do **texto dos 10
  módulos** (não só da UI), a pedido do usuário ("pode tomar a frente
  primeiro"). Script de reflow + substituição com várias camadas de proteção
  (tabelas por célula, pseudo-listas em negrito reconhecidas pelo dígito,
  pareamento só quando curto/sem cruzar frase, fences intocados). Processo
  encontrou e corrigiu 2 bugs reais antes de commitar (ver histórico do
  commit para detalhe). Verificado: parênteses/aspas balanceados nos 10
  arquivos, 225 tabelas renderizando ok, 0 mojibake. Sobram ~24 travessões
  dentro de blocos de código (ASCII/checklist) e ~19 células de tabela "—"
  (convenção de vazio/N-A) — deliberadamente preservados.
- **Mobile testado (390–504px):** sem overflow horizontal de página
  (`scrollWidth <= innerWidth`, checado via probe JS injetado + headless
  Chrome); `.rail` corretamente some abaixo de 1080px; tabelas largas rolam
  dentro do próprio `.table-wrap`, não vazam pra página. Nada quebrado.
- **v6 (commits 760642d, 5aa6df5):**
  - **Nivelamento de verdade:** confirmado que `isUnlocked()` nunca exigiu
    acerto mínimo no diagnóstico (M0), só responder as 10 — usuário achou que
    havia um "limite de acertos" e pediu confirmação + que o resultado
    passasse a fazer algo. Agora `updateLevelBadge()` calcula a banda CEFR
    (mesma tabela do M0 Parte 4.2) e recomenda um dos 3 cronogramas (Parte
    6.1–6.3) assim que as 10 são confirmadas; fica num badge fixo na sidebar.
  - **Cores:** `--shadow-hard` (a sombra "carimbada" de todo card/botão)
    trocada de preta pra laranja; borda de `.section-card.done` (verde) também
    virou laranja.
  - **Vícios de linguagem de IA:** pesquisei a lista mais documentada de 2026
    (fontes na resposta) e cruzei com o corpus. Real e corrigido: construção
    "não é X, é Y" (25 ocorrências, ~18 reescritas com variação); "jornada"
    trocado por "progresso"/"sequência" nos rótulos visíveis. Checado e
    **descartado** (não é vício aqui, é conteúdo correto): "robust"/
    "fundamental" no M6 são o próprio vocabulário sendo ensinado; os 636 `;`
    do corpus são majoritariamente gabaritos de questão em formato compacto
    (uso apropriado ao gênero), não "padding" de IA.
- **v7 (commit 507af44):** usuário reportou verde residual 3 vezes seguidas,
  cada uma apontando pra um lugar diferente — cada "achei e corrigi" anterior
  só pegava parte do problema:
  1. `.section-card.done` (borda) → laranja.
  2. Todo `var(--good)`/`--good-wash` em CSS (`.opt.correct`, `.quiz-summary`,
     `.bsq-card.correct`, `.srs-g2`/`.srs-done`/`.srs-restart`) → laranja.
  3. A causa raiz de verdade: **inline styles em `app.js`**, que sobrescrevem
     CSS/classe e por isso nenhuma busca em `styles.css` achava. Duas
     mensagens de feedback (flash de export/import e mensagem de auth do
     Supabase) faziam `el.style.color = "var(--good)"` direto no JS pro caso
     "sucesso" — trocado pra `var(--accent)`. De bônus: `--ink-dim` (usado no
     caso neutro da msg de auth) nunca existiu no `styles.css`, virava cor
     herdada silenciosamente; trocado pro token real `--ink-2`.
  - `--good`/`--good-wash` **removidos das 3 paletas** (claro, escuro por
    sistema, escuro forçado) — sem definição, não tem como reaparecer verde
    por acidente de novo.
  - Achado de brinde na varredura: `--shadow-hard` no bloco
    `:root[data-theme="dark"]` (tema escuro escolhido manualmente, diferente
    do `prefers-color-scheme`) ainda estava `#000` — o fix da sombra preta→
    laranja do v6 só tinha coberto o bloco de sistema. Agora laranja nos 3
    lugares.
  - Verificação final: todos os hex de 6 dígitos do `artifact/index.html`
    listados e conferidos manualmente — sobra só preto/marrom (tinta/fundo) e
    laranja/âmbar/terracota (accent/danger). Zero verde em qualquer forma
    (variável, classe ou inline).
- **v8 (commits 0d39225, adbea34):**
  - **Foto de perfil:** avatar do usuário logado (círculo com a inicial) agora
    é clicável — abre seletor de arquivo, redimensiona no navegador (canvas,
    crop quadrado 160×160, JPEG 0.82) e mostra a foto; "×" no canto remove.
    Guardada em `toefl_avatar_v1`, entrou em `SYNC_PREFIXES` — sincroniza pelo
    `user_state` jsonb existente, sem bucket de storage novo.
  - **"Textos pesados":** causa raiz era o próprio alargamento de
    `.panel-inner` (800px→960px, feito a pedido nesta sessão) sem dar a
    parágrafo/lista/blockquote um `max-width` próprio — linha de texto tinha
    virado 110–130+ caracteres, bem acima da faixa confortável (~65–75).
    Agora `max-width:68ch` nesses elementos (card e tabela continuam largos,
    só o texto corrido ganha coluna de leitura estreita); mais respiro
    (margem 14px/7px→18px/9px, fonte 15.5px→16px). Contraste card/fundo no
    tema escuro aumentado (`--paper`/`--bg` estavam quase idênticos) e
    textura de ruído global reduzida (opacity 0.38/0.35→0.22/0.18).
- **v9 (commits abddfcf, b3414c6, c16f019):**
  - **Foto de perfil não aparecia:** todo caminho de erro do upload manual
    falhava calado (MIME type não confiável em alguns navegadores/SO, cota do
    `localStorage` sem aviso). Endurecido + mensagens de erro/sucesso visíveis;
    avatar de 26px→34px. Segue sem confirmação de que resolveu.
  - **Login com Google:** usuário preferiu trocar de abordagem — em vez de só
    upload manual, logar com Google e puxar a foto do perfil Google
    automaticamente (`user_metadata.avatar_url`/`.picture` da sessão). Upload
    manual continua existindo como override. **Pendente do usuário:** ativar
    o provedor Google no painel do Supabase + Google Cloud Console — passo a
    passo em `docs/supabase-setup.md` §3.1; eu não tenho como fazer essa parte
    (exige as contas do próprio usuário).
  - **Roadmap do topo:** usuário não gostou da trilha de módulos fixa acima
    do conteúdo — movida para dentro do menu hamburger (topo da sidebar,
    acima de "Progresso geral"), com cores próprias pro tema sempre-escuro da
    rail. Barra do topo agora só tem hamburger + tema + login/avatar.
- **v10 (commits 3445e39, c0243e4, de96df9, 5c2c479):**
  - **Avatar:** foto não preenchia o círculo — `<img>` dentro de flex container
    não esticava direito; virou `position:absolute; inset:0` (não depende mais
    do flexbox pra se esticar). Foto do Google vinha em baixa resolução
    (`=s96-c`); forçado `=s256-c`. Círculo 34px→44px.
  - **Títulos h3** (subtítulos de parte/drill) de preto → `var(--accent-strong)`
    (mesmo tratamento que h4 já tinha).
  - **Cabeçalho de tabela:** usava `background:var(--ink)`, que inverte
    direção errada no escuro (vira quase-branco + texto branco = ilegível).
    Token novo `--th-bg` (laranja no claro, preto no escuro — direção que o
    usuário pediu). Mesmo bug achado e corrigido em `.panel pre` (bloco de
    código: fundo e texto ficavam idênticos no escuro).
  - **Achado de brinde:** `:root[data-theme="dark"]` (tema escuro manual,
    diferente de "seguir o sistema") tinha ficado com `--bg`/`--paper`/`--hair`
    desatualizados desde o fix de contraste 2 rodadas atrás — um `replace_all`
    só pegou o bloco do `@media` por indentação diferente (2 vs 4 espaços) e
    passou batido. Sincronizado. **Lição de processo:** ao editar os dois
    blocos de tema escuro juntos, sempre `Grep` a variável depois do
    `replace_all` pra confirmar 2 ocorrências, nunca confiar só na mensagem
    de sucesso da ferramenta — a indentação diferente entre os dois blocos já
    causou esse mesmo silêncio duas vezes.
  - **"Seu progresso: conclua 70%":** saiu da barra fixa do topo (ao lado do
    hamburger) e foi para baixo do `<h1>` de cada módulo (`.ph-progress-hint`),
    a pedido do usuário.
- **v11 (commits e757f1d, 5c2c479 [ver acima], 8d8ef2e, da717a5):**
  - **Hamburger:** vivia dentro da coluna centralizada (`main`, max-width
    1320px + padding) — em tela larga ficava longe da borda real. Virou
    `position:fixed; top/left:16px`, ancorado na quina de verdade da viewport.
  - **Login obrigatório:** decisão do usuário (2026-09-14) — o app não pode
    mais abrir direto no conteúdo quando o Supabase está configurado. Nova
    tela `#authGate` (overlay full-screen, Google + e-mail) bloqueia tudo até
    logar; some com `goOnline()`. **Só existe se `supabase_config.json`
    estiver preenchido** — sem config, app continua 100% offline como sempre
    (decidido em `build.py` na hora do build). Falha ao carregar a lib do
    Supabase (CDN bloqueado) libera o conteúdo mesmo assim, pra não trancar o
    aluno fora do material por causa de rede. `docs/supabase-setup.md`
    atualizado pra refletir esse comportamento nos dois casos.
- **v12 (commit ddc4c4c) — review externa de UX do M0:** usuário trouxe uma
  revisão de produto com 6 pontos; escolheu começar pelos 3 rápidos (dos
  outros 3 — calculadora de score interativa, dashboard semanal preenchível/
  persistente, reestruturação do M0 com resumo executivo — nenhum foi
  iniciado, ficam para quando o usuário priorizar):
  1. `.pbadge` (o "%") aparecia em módulo travado sem checar `isUnlocked()` —
     só o `.num-badge` respeitava o bloqueio, os dois se contradiziam.
  2. `.num-badge` virava só "🔒" quando travado, escondendo o número em 8 dos
     10 módulos — o conteúdo referencia "Módulo 0, 1, 4, 7..." por número, e
     não tinha como achar isso na sidebar. Número agora sempre visível; o
     bloqueio continua claro pela classe `.locked` (opacidade + borda
     tracejada), não pelo texto do badge.
  3. Gravador/cronômetro flutuantes apareciam em toda aba, inclusive nas de
     referência pura. Agora só em mod1/2/3/4/7 (`PRACTICE_MODULES`).
  Verificado ao vivo via Chrome headless com progresso semeado no
  `localStorage` (headless funcionou desta vez — user-data-dir isolado evita
  o Chrome do usuário "engolir" o comando quando já está aberto).
- **v13 (commit 5837c13) — 2/4 da review de conteúdo (M1/M5/M6/M7/M8/M0):**
  usuário confirmou os achados da review externa (estrutura consistente
  M1→M5, ruptura de nomenclatura em M6, nota do Simulado 1 sem destaque em
  M7, tom "coach" pontual mas sustentado por disclaimer+números reais em M8,
  citação da fonte ETS real mas não conferida número a número) e priorizou
  os 2 rápidos:
  - M6: "SEÇÃO N" → "PARTE N" em todo o módulo (29 ocorrências — 12 títulos +
    17 refs cruzadas + 1 uso genérico minúsculo que o replace automático não
    pegou). Resolve de tabela o efeito colateral que o usuário apontou: a
    barra "Nesta parte" também mudava de rótulo por módulo, porque reflete o
    texto do heading.
  - M7: nota "Simulado 1 = diagnóstico do M0" era parágrafo comum, sem
    destaque — virou blockquote com 📌 (mesmo padrão dos callouts ⚠️/📌 já
    usados no resto do site).
  - **Não feito ainda (não é rápido, precisa de confirmação separada):**
    validar os números oficiais linha a linha contra o PDF real da ETS
    ("TOEFL iBT Test: 2026 Update Test Blueprint and Specifications
    Document") — é pesquisa externa, não edição de código.
- **v14 (commit 8aa3911) — lista de 12 pontos, item 1 (prioridade máxima),
  fatia 1/3:** usuário trouxe uma lista de 12 ações estruturais/interatividade
  (fonte externa, "pronta pra colar"), pediu pra seguir em ordem com aviso
  antes de cada bloco. Item 1 = tornar os Action Drills interativos.
  - **Escopo real corrigido em 2 rodadas:** não é "todos os módulos" (só M1/M2
    têm esse formato; M3/M4/M5/M6/M8/M9 não usam múltipla escolha estática; M7
    tem formato parecido mas em escala de simulado completo, decisão à parte).
    Contagem real de M1: **67 itens** (não 41 — a primeira contagem só pegou
    o Grupo C; Grupos A e B usam rótulos diferentes). Usuário escolheu fatiar
    por grupo, Grupo A primeiro.
  - **Achado técnico que mudou a abordagem:** `build_mod1()`/`build_mod2()`
    (o código que injetaria o widget) existiam mas **não eram chamados** —
    `main()` usava `build_plain()` pros dois desde que os módulos foram
    "expandidos" (comentário no próprio código). E a `build_mod1()` antiga
    fatiava num marcador (`"PARTE 3: ACTION DRILLS"`) que não existe mais —
    o módulo foi renumerado pra 7 partes, Action Drills é Parte 5 agora.
    Reescrita do zero pra estrutura atual, não reaproveitamento de código morto.
  - **Entregue:** Grupo A (Complete the Words, 32 itens/5 textos) — nova
    `MOD1_ACTION_DRILLS_A` em `drills_data.py`, `build_mod1()` reescrita fatia
    a Parte 5/Grupo A e troca pelo widget (mesmo motor do M0), remove a tabela
    de gabarito redundante do Grupo A na Parte 6. Verificado: 42 qcards no
    site (10 M0 + 32 novos), zero id duplicado, estático antigo confirmado
    removido, Grupos B/C e M2 intactos.
  - **v15 (commits 685fddc, 7e257e6, 4974909) — item 1 completo pra M1+M2:**
    usuário autorizou seguir sem pausa entre blocos ("continue até o final").
    Grupo B do M1 (14 itens) e Grupo C do M1 (21 itens, inclui `C3.7` —
    implementado suporte a múltipla seleção em `render_quiz.py`/`app.js`,
    `data-multi="N"` no `.qcard`, testado ao vivo via clique simulado em
    Chrome headless: limite de N marcações respeitado, correção por conjunto
    funcionando). Depois M2 inteiro (51 itens, 4 grupos — Listen and Choose
    a Response/Conversation/Announcement/Academic Talk), mesma reescrita de
    `build_modN()` que M1 precisou (marcador antigo não existia mais).
    **Total: 118 itens novos interativos, 128 no site inteiro (+ M0).**
    Verificado a cada fatia: contagem de `qcard` bate exato, zero id
    duplicado, estático antigo removido, gabarito redundante removido mantendo
    Score Consolidado, módulos vizinhos intocados.
  - **Item 2 da lista (botão "Corrigir")** já sai satisfeito de graça: o
    próprio widget reaproveitado (M0) sempre teve "Confirmar resposta" +
    feedback inline, sem precisar navegar até o Gabarito.
  - **Item 3 (commit 916e70e):** painel novo "Seu desempenho real até agora"
    (M0, Parte 4, depois de 4.3) soma automaticamente os acertos confirmados
    em todos os Action Drills de M1+M2 (via `computeQuizAccuracy()`, novo em
    `app.js`, prefixo `mod1-`/`mod2-` no id do drill) e mostra a banda CEFR
    (reaproveita `cefrBandFromPct`, a mesma tabela do diagnóstico) — zero
    input manual, atualiza sozinho a cada "Confirmar resposta" em qualquer
    aba. `isMultiCard`/`isCardCorrect` saíram do closure por-drill pra escopo
    compartilhado nesse processo. Testado ao vivo via headless com respostas
    seedadas no localStorage: 4/6 certas → 67%/B2; 12/12 → 100%/C2, ambos
    batendo a tabela da Parte 4.2.
  - **Item 5 (persistência) já estava resolvido** antes desta lista sequer
    existir — o login com Supabase (v11) já sincroniza checkboxes, SRS, Build
    a Sentence e agora os quizzes de M1/M2/M0 entre dispositivos.
  - **Item 7 (commit af69cc7):** cada Action Drill com "alvo: N min" no
    título ganha um botão "⏱ Iniciar cronômetro (N min)" que carrega esse
    valor no widget de cronômetro flutuante existente (nova
    `setDrillTimerMinutes`, exposta pela IIFE do cronômetro). Lê o alvo do
    próprio texto que o conteúdo já tinha, não duplicou em lugar nenhum.
    Drills sem alvo em minutos (ex.: `mod2-a`, ritmo por item em segundos)
    ficam de fora de propósito. Testado ao vivo: 22 botões injetados (13 M1 +
    9 M2, bate exato), clique carrega "04:00" corretamente, `mod2-a`
    confirmado sem botão.
  - **Item 9 (commit 9c6677e):** todo h3 de conteúdo (fora os títulos dos
    próprios widgets — `Drill .../Grupo ...`, que ficam sempre visíveis) virou
    clicável, recolhendo/expandindo o que vem depois até o próximo h3. Nada
    começa escondido. Implementado como a **última** IIFE do `app.js` de
    propósito — outras partes (botão de cronômetro, índice lateral) dependem
    da posição original dos elementos em relação aos h3/h2, então essa
    reestruturação de DOM só podia rodar depois de tudo que já conta com essa
    estrutura. Testado ao vivo: 274 subseções viraram accordion; 29 títulos de
    widget confirmados fora; ciclo completo de clique (visível→escondido→
    visível, `display:none` computado de verdade); botão de cronômetro e quiz
    confirmados funcionando normalmente depois da reestruturação.
  - **Item 8 considerado obsoleto pra M1/M2** — não existe mais Gabarito
    separado pra navegar até (virou inline nos widgets); não se aplica a
    outros módulos, que não tinham esse par drill/gabarito.
  - **Item 10 (commit 706855c):** o "Registro" de cada Protocolo de Análise de
    Erros (M1-M6; M7 fica de fora, protocolo de triagem próprio) virou
    formulário de verdade — data, drill, resultado, códigos daquele módulo
    (checkboxes com os mesmos R1-R6/L1-L6/S1-S6/W1-W6/RG1-RG6/V1-V6 que a
    tabela já tinha), histórico salvo e sincronizado, detecção automática de
    "código 3+ vezes = prioridade" (antes era só um aviso de texto, virou
    cálculo). Novo `render_errorlog.py` + `ERRLOG_CODES`/`split_registro_block`
    em `build_pipeline.py`. **Achado de bônus:** `main()` ainda chamava
    `build_plain()` pro mod4 em vez de `build_mod4()` — mesmo padrão de bug
    do M1/M2 (código pronto, nunca ligado). Corrigido junto: o widget de
    Build a Sentence (10 itens) passa a aparecer de verdade em M4 pela
    primeira vez. Testado ao vivo: 3 submissões reais, histórico correto
    (mais recente primeiro), prioridade detectada certo ("R2 3×"), delete
    funcionando, persistência confirmada.
  - **Certificado de conclusão** (pedido à parte, não da lista de 12):
    botão na sidebar (some até concluir os 10 módulos + o quiz do último —
    o gate normal só valida o módulo *anterior* ao destravar o próximo, o
    último nunca era conferido sozinho) abre modal não-oficial com nome
    (e-mail logado ou "Aluno(a) iTOEFL"), data da primeira conclusão e botão
    de imprimir/PDF. Testado ao vivo semeando os 86 checkboxes do site.
  - **3 ajustes de UI** (pedidos à parte): tema virou alternador estrito
    claro/escuro (sem "Sistema", 1ª visita usa a preferência do SO só como
    ponto de partida — testado o ciclo de cliques); "Nesta parte" ganhou mais
    contraste (`--ink-2`→`--ink`, peso 600→700); tela de login redesenhada
    pra usar a identidade visual real do site (lockup de marca completo,
    kicker tombado, marca-d'água gigante) em vez de cara de formulário
    genérico — sem descrição específica do que incomodava, foi julgamento
    próprio; pode precisar de mais uma rodada se algo específico ainda
    incomodar.
  - **Pendente da lista original de 12:** M7 (decisão de design à parte —
    simulado completo não deveria ter feedback item a item), item 11 (painel
    de progresso consolidado — parcialmente coberto pelo painel do item 3,
    falta estender pra outros módulos/tipos de item), item 12 (teste de
    responsividade mobile, nunca feito em viewport real nesta leva de
    mudanças).
- **Acesso pago via Mercado Pago (commit b6e0db8, 2026-09-17)** — pedido à
  parte: só quem pagou vê o conteúdo, exceto a conta admin
  (`pietrooliveiramarquespp@gmail.com`, bypass hardcoded em `app.js`).
  Pagamento único vitalício, confirmado com o usuário antes de mexer no
  schema. Tabela nova `entitlements` (sem policy de escrita pro papel
  "authenticated" — só o `service_role` da edge function grava `paid=true`,
  um aluno não consegue se autoliberar pelo console do navegador). Duas edge
  functions novas: `create-checkout` (cria a preferência no Mercado Pago) e
  `mp-webhook` (reconfirma o pagamento na API do MP antes de liberar — nunca
  confia só na notificação). Gate novo `#payGate` some só depois do login se
  a conta não tiver pago. **Pendente do usuário — nada disso funciona sem
  isso, ver `docs/mercadopago-setup.md`:** rodar `schema.sql` de novo, criar
  credenciais no Mercado Pago, instalar/ligar o Supabase CLI, configurar o
  secret `MP_ACCESS_TOKEN`, publicar as duas functions, testar em sandbox
  antes de produzir. Preço (`PRICE_BRL`) é um placeholder (R$ 197) — ajustar
  em `supabase/functions/create-checkout/index.ts` **e** no texto do botão em
  `app/build.py` antes de publicar de verdade.
- **Login com Google:** ainda não funciona — usuário confirmou que não
  completou a ativação do provedor no painel do Supabase. Sem mudança de
  código pendente; guia em `docs/supabase-setup.md` §3.1.
- **Fase 6 preparada, não executada (2026-09-17):** checklist completo escrito
  (sem remoto git configurado ainda — nenhum repo no GitHub pra este projeto).
  Usuário pediu só pra deixar pronto, sem publicar.
- **Botão "Reiniciar todo o progresso" (commit c86eb57):** zona de perigo na
  sidebar, apaga checkboxes/quiz/SRS/Build a Sentence/registro de
  erros/certificado (não mexe em avatar/tema). Achado no caminho: reload
  imediato depois do reset tinha uma corrida real com o push debounced
  (2.5s) pra nuvem — o próximo `pull()` acharia a nuvem "mais nova" (ainda
  com o progresso antigo) e desfaria o reset. Corrigido expondo
  `forceSyncPush()` (push sem debounce, com Promise) — só recarrega depois
  que a nuvem confirma.
- **Emojis decorativos removidos (mesmo commit c86eb57):** 58 ocorrências
  em `consolidated/*.md` (🏋️ antes de cada drill, 📊/📘/🔴/🎧/📖/🚀/🔥 em
  cabeçalhos), conferidas uma a uma por contexto antes de tirar. Mantido:
  ✅❌✔☐✓ (certo/errado), ⚠️🚨 (avisos), setas (conectores), a legenda
  funcional ✍️/🎤 do M9 e qualquer emoji dentro de conteúdo sendo lido pelo
  aluno. **Cuidado técnico:** a primeira tentativa trocou LF→CRLF ao
  reescrever os arquivos (Python `open()` em modo texto no Windows traduz
  por padrão) e inflou o diff pra milhares de linhas — revertido e refeito
  com `newline=""` nos dois lados.
- **Login troca de link mágico por usuário+senha (commit 711b750,
  2026-09-17):** pedido do usuário — cadastro pede e-mail+usuário+senha,
  login só usuário+senha, e-mail vira recuperação (esqueci senha/usuário).
  Google continua do lado. Supabase Auth só autentica por e-mail
  nativamente — resolvido com uma função no banco (`email_for_username`,
  SECURITY DEFINER, liberada pra `anon`) que traduz usuário→e-mail antes de
  chamar `signInWithPassword`. Coluna `username` nova em `profiles` (única,
  formato validado por CHECK). Reescrita completa da tela de login em
  `build.py`/`app.js` — maior mudança de código só de UI da sessão, alto
  risco de erro de sintaxe; verificado ao vivo via Chrome headless (zero
  erros de JS, os 3 formulários existem, troca login↔cadastro funciona). O
  fluxo que depende do Supabase de verdade (RPC, signUp, recuperação) só dá
  pra confirmar depois que o usuário rodar o schema novo — `schema.sql`
  precisa ser rodado de novo no SQL Editor (seção "LOGIN POR NOME DE
  USUÁRIO"), documentado em `docs/supabase-setup.md`.
- **Acesso pago pendente de confirmar com Google login funcionando:** a
  tela de paywall (`#payGate`) só aparece depois do login — sem o Google OU
  o usuário/senha funcionando de ponta a ponta, não dá pra testar o fluxo
  completo de compra ainda.
- **Pendente:** Fase 6 (publicar no GitHub Pages) segue depois da aprovação do
  usuário — é ação pública/difícil de reverter, não faço sem confirmar.

### 3. Estrutura / navegação linear (FEITO — commit 7fcdd49)
- `app.js`: `UNLOCK_PCT = 70` (era 100). Módulo N libera com 70% do N-1.
  Mensagem de bloqueio mostra o % atual. Bloqueados seguem visíveis na sidebar.

---

## Fase 0 — Fundação ✅

- [x] Snapshots de segurança em `_snapshots/`
- [x] `CLAUDE.md` e `ROADMAP.md`
- [x] `scripts/serve.py` (serve `artifact/index.html`)
- [x] Git 2.55 instalado pelo usuário
- [x] `markdown` instalado via pip

## Fase 1 — Adotar o pacote de consolidação ✅

- [x] Material extraído de `Downloads/itoefl_1.zip`
- [x] Análise em `docs/analise-material-consolidacao.md`
- [x] `index.html` antigo → `_archive/index-old-monolith.html`
- [x] 10 `.md` do formato antigo → `_archive/content-old-format/`
- [x] `consolidated/ app/ artifact/ supabase/` promovidos para a raiz
- [x] M5, M6, M8, M9 antigos copiados para `consolidated/_a-portar/`
- [x] Build testada: `build_pipeline.py` + `build.py` geram `artifact/index.html`
- [x] `CLAUDE.md` reescrito para o formato 2026 e a nova arquitetura
- [x] `git init` + commit inicial (`a5efab0`) — gerados no `.gitignore`
- [x] Smoke-test: HTTP 200, 6 painéis, 8 quiz-drills, 143 checkboxes, 0 placeholders
- [ ] Usuário abrir `artifact/index.html` no navegador e validar visualmente

## Fase 2 — Auditar o que já veio pronto (M0–M4, M7) ✅

- [x] Formato 2026 verificado contra fontes públicas — material da consolidação confiável
- [x] Lidos os 6 módulos (`modulo_0,1,2,3,4,7`) — todos no formato 2026, qualidade alta
- [x] Corrigido: mapa de módulos trocado no M0 (M3=Speaking, M4=Writing) — ~15 refs
- [x] Corrigido: refs a "Módulo 5/6" no M7 → reapontadas para M3/M4/M1
- [x] Corrigido: artefatos "Digite MÓDULO N" removidos de M1/M2/M7 + `</content>` solto no M1
- [x] Rebuild limpa; relatório em `docs/auditoria-modulos-2026.md`
- Lacunas observadas (não bloqueiam): M3/M4 são texto+drills em papel, sem widget
  interativo como M1/M2; M7 descreve o cronômetro mas não o implementa; a
  calculadora de score do M0 é tabela de referência, não um widget.

### Pendência residual

- [ ] M7 Parte 1: "Após Módulos 1–5 / Módulo 6" como pré-requisito dos simulados
      — o "1–5" agora está coerente (M5 existe e é conteúdo de ensino); revisar
      redação ao portar M6.

## Fase 3 — Portar/reescrever os módulos que faltam ✅

Ordem: M5 → M6 → M9 → M8. Todos feitos.

- [x] **M5 → "Registro & Sofisticação Retórica"** — decisão do usuário
      (2026-09-02): repropósito, não remoção. `consolidated/modulo_5_registro.md`
      reaproveita o Atlas Linguístico (retiered para bandas CEFR), os 10
      marcadores de alto impacto e os exemplos contrastivos; aplica às 3 tasks
      produtivas de 2026 (Take an Interview, Write an Email, Academic Discussion).
      Registrado em `build_pipeline.py` e `build.py`. Fragmento = 24.327 chars.
- [x] **M6 Vocabulary** — portado para `consolidated/modulo_6_vocabulary.md`.
      Contagem verificada: 144 linhas de tabela em negrito na origem → 144 no
      destino (100 entradas de léxico por área + 15 verbos + 10 adjetivos + 8
      collocations + tabelas de protocolo). Referências a "Speaking Task 1" →
      "Take an Interview" e "Writing Task 2" → "Write for an Academic Discussion";
      4 entradas duplicadas do arquivo antigo substituídas por termos novos
      (incremental, acidification, redundancy). Fragmento = 67.351 chars.
      **Pendente:** widget de flashcards + SRS — é item da Fase 4, não bloqueia.
- [x] **M9 Brazilian Traps** — `consolidated/modulo_9_braziliantraps.md`.
      Conteúdo (falsos cognatos, preposições, fonemas) veio quase verbatim.
      Mudanças 2026: "Speaking Task 1/2/3" → *Take an Interview* / *Listen and
      Repeat*; "Writing Task 1/2" → *Write for an Academic Discussion*;
      "corrector humano" removido (Speaking 100% IA); "score de Delivery" →
      "inteligibilidade e prosódia". Fragmento = 42.877 chars.
- [x] **M8 Exam Day** — `consolidated/modulo_8_examday.md`. Partes 2–5 e 7
      (sono, nutrição, psicologia, logística) quase intactas. Reescritos:
      Parte 1 (D-4/D-2 referenciavam os templates do M5 antigo), Parte 6 inteira
      (Reading ~27–30min adaptativo, Listening ~18min, Speaking ~8min Listen and
      Repeat + Take an Interview, Writing ~23min Build a Sentence + Email +
      Academic Discussion), Parte 7 (cenários anti-colapso), Parte 8
      ("avaliação humana" → correção por IA). Fragmento = 37.218 chars.
- [x] M5, M6, M8, M9 registrados em `build_pipeline.py` e `build.py`.
      `consolidated/_a-portar/` removido.

## Fase 4 — Produto ✅

- [x] **Cronômetro por seção** — widget flutuante, presets Reading 28′ /
      Listening 18′ / Speaking 8′ / Writing 23′ / Prova 85′, beep ao zerar,
      preset lembrado em `toefl_timer_preset`.
- [x] **Gravador de Speaking** — widget flutuante, `getUserMedia` +
      `MediaRecorder`, playback inline, trata permissão negada.
- [x] **Export/import de progresso** — botões na sidebar; export baixa
      `itoefl-progresso.json` + copia p/ clipboard; import mescla e recarrega.
- [x] **Ajustes visuais** — "Prep oficial" → "Preparação independente" +
      disclaimer; marca de progresso só em h2 (61 checkboxes, não 162).
- [x] **SRS no M6** — flashcards Leitner sobre as 50 palavras do Kit de
      Emergência. `app/vocab_kit.json` + `app/render_srs.py` + motor em
      `app.js`. Boxes 0–5, intervalos 0/1/3/7/16/30 dias, estado em
      `toefl_srs_kit50_v1`. Injetado no fragmento do M6 via `build_mod6`.
- [x] **`[hidden]` global** no `styles.css` — necessário no serve local
      (a Artifact já injeta essa regra); corrige widgets que usam `hidden`.
- [x] **Widget de Build a Sentence (M4)** — 10 itens de reordenação pura,
      clicar-para-montar, verificar → frase-modelo + nota. `build_sentence_data.py`
      + `render_build.py` + motor em `app.js`, estado `toefl_bsq_m4build_v1`.
- [~] M5 (reescrita B1→C1) — fica como exercício de texto guiado com
      referência de correção; não se beneficia de widget (é produção livre
      sem gabarito único). Fase 4 de conteúdo interativo considerada completa.

## Fase 5 — Backend Supabase ✅

Toda a parte de código foi feita. O que resta é operação (passos em
`docs/supabase-setup.md`).

- [x] **Schema simplificado** — `supabase/schema.sql` reescrito: `profiles` +
      `user_state` (jsonb, uma linha por usuário) + RLS + gatilho de perfil no
      signup. As tabelas de conteúdo e o seed viraram
      `supabase/schema-content-optional.sql` / `content-seed-optional.json`
      (só se um dia servir conteúdo do banco).
- [x] **Login (magic link) + sync no `app.js`** — módulo de auth na sidebar
      (`authBox`, oculto se não configurado). `signInWithOtp` por e-mail,
      `onAuthStateChange`, pull no login (recarrega se a nuvem for mais nova),
      push debounced (2,5 s) a cada escrita de chave sincronizável.
- [x] **Merge offline** — `toefl_dirty` marca edições não enviadas; no pull,
      edições locais ganham e o resto da nuvem é mesclado.
- [x] **Fallback offline** — sem config ou deslogado, o app é exatamente o de
      antes (localStorage puro). `build.py` tolera config ausente/BOM/inválida.
- [x] **`app/supabase_config.example.json`** commitado; `.json` real gitignored.
- [x] **`docs/supabase-setup.md`** — passo a passo (criar projeto, rodar schema,
      URLs de auth, preencher config, rebuild, troubleshooting).
- [x] **Usuário:** projeto Supabase criado ("ITOELF", ref `itfosjcymqfzjsftvjey`,
      São Paulo), schema rodado, `app/supabase_config.json` preenchido com a
      **publishable key** (`sb_publishable_...`), site/redirect URLs configuradas
      para `http://localhost:8000`. Verificado via API: tabelas `profiles` e
      `user_state` existem, RLS ativa, email auth habilitado.
- [x] **Login testado pelo usuário** (2026-09-04) — magic link funcionou,
      e-mail e botão "Sair" aparecem na sidebar após o login.
- [ ] Testar sync real com 2 dispositivos/navegadores (opcional, quando quiser).

**Nota de segurança:** durante a configuração, uma `sb_secret_...` key e a
legacy `service_role` JWT foram coladas na conversa por engano. Orientei o
usuário a rotacioná-las; a `publishable key` que o app usa não é afetada por
essa rotação. Confirmar que a rotação foi feita antes de considerar o projeto
Supabase "limpo" para uso continuado.

## Fase 5.5 — Redesenho + progressão sequencial ✅ (2026-09-07)

- [x] Pesquisa de referência (Khan Academy, Busuu, Babbel, Memrise via
      screenshots headless).
- [x] Progressão sequencial: módulo N destrava com N-1 a 100%. Selo por módulo
      (número / ✓ / 🔒), aviso ao clicar em bloqueado, contador "N de 10".
- [x] Conteúdo em `.section-card` por seção (padrão "unit card").
- [x] Botões CTA em pill; H2 com borda de destaque.
- [x] `.side` com `min-width:0` (proteção grid). Confirmado sem overflow
      horizontal em 360–768 px.
- Documentado em `CLAUDE.md` (seções "Progressão sequencial" e "Camadas visuais").

## Fase 7 — Expansão do conteúdo (decisão do usuário, 2026-09-07)

O currículo (~50k palavras) é um bom esqueleto de estratégia, mas fino em
prática, ensino de língua e exemplos resolvidos. Plano: expandir **módulo por
módulo, um por sessão**, dobrando o tamanho. Ordem por impacto:
M1 → M2 → M4 + M3 → M6 → M9 → M0/M5/M7/M8.

- [x] **Verificação do formato contra a ETS** — baixado o blueprint oficial
      2026. Nosso núcleo confere. Correções pontuais aplicadas (pontos brutos
      145 não 120; itens pontuados). `docs/ets-blueprint-2026.md`.
- [x] **M1 Reading** (2026-09-08) — 5,3k → 11,5k palavras. Adicionado:
      Parte 1.4 (os 9 tipos de pergunta), Parte 3 (Laboratório de Língua —
      gramática + 50 collocations + conectores + morfologia), Parte 4 (exemplo
      resolvido narrado), 13 drills graduados (era 3) cobrindo todos os
      formatos e tipos de questão, gabarito dos 67 itens, Parte 7 (protocolo
      de erros R1–R6). M1 agora usa `build_plain`. `commit 0bb2738`.
- [x] **M2 Listening** (2026-09-09) — 5,7k → 10,5k palavras. Parte 1.4 (9 tipos
      de pergunta), Parte 3 (**Laboratório de Escuta** — reduções, linking,
      contrações, números, 40 termos de campus, 30 idioms, linguagem funcional,
      símbolos de anotação), Parte 4 (exemplo narrado), 21 drills graduados
      (era 4), gabarito dos 51 itens, Parte 7 (protocolo L1–L6). `build_plain`.
- [x] **M4 Writing** (2026-09-09) — 3,9k → 8,8k palavras. Parte 1.4 (como o
      e-rater corrige), Parte 3 (**Laboratório de Produção Escrita** — tipos de
      frase, run-on/comma splice, tempos, word forms, pontuação, registro +
      as 11 famílias de estrutura do Build a Sentence com 22 mini-drills),
      Parte 4 (Email + Discussion escritos ao vivo), 30 Build a Sentence
      graduados + 6 prompts de Email + 6 de Discussion, respostas-modelo por
      banda (3/5/6), Parte 7 (W1–W6 + revisão dos 60–90 s). `build_plain`.
- [x] **M3 Speaking** (2026-09-09) — 4,3k → 7,2k palavras. Parte 1.4 (blueprint:
      ~45s, sem preparo, cenário texto+áudio), Parte 2.1 (features do SpeechRater),
      Parte 3 (**Laboratório de Fala** — 12 fonemas críticos com IPA, -ED, word
      stress, ritmo/tapping, entonação, weak forms, gestão de hesitação, 40
      frases, rubrica de auto-gravação /12), Parte 4 (Listen and Repeat + Take an
      Interview ao vivo), Grupo A (5 sets Listen and Repeat A1→C2) + Grupo B (48
      perguntas de Take an Interview por 6 funções + B7/B8) + Grupo C (shadowing),
      Parte 6 (gabarito de função + respostas-modelo banda 3/5/6), Parte 7
      (S1–S6). Também: correção de renderização de listas markdown em M2 e M3.
      `build_plain`. `commit 51876d0`.
- [x] **M5 Registro & Sofisticação** (2026-09-09) — 2,9k → ~10k palavras.
      Parte 1.4 (a rubrica CEFR em números) + 1.5 (as 3 "vozes"), Parte 2.1
      (bancos de frases por função retórica), os 10 marcadores expandidos
      (função + antes/depois + uso indevido + quando não usar), Parte 4
      (**Laboratório de Registro** — nominalização, hedging calibrado, densidade
      por combinação de orações, cleft/fronting/inversão, coesão além de
      conectores, escala de formalidade lexical, colocações acadêmicas), Parte 5
      com exemplos extras por função, Parte 6 (elevação narrada frase a frase),
      Parte 7 (6 → 14 drills, todos com gabarito), Parte 9 (protocolo RG1–RG6).
      `build_plain`. `commit 6c6e084`.
- [x] **M6 Vocabulário** (2026-09-09) — ~5k → ~9k palavras. As 120 palavras de
      referência (Seções 2–3) ficaram intactas; a lacuna era a ausência de
      exercícios. Seção 4 expandida (27 verbos / 19 adjetivos / 21 collocations),
      Seção 5 nova (**famílias de palavras + morfologia** para Complete the
      Words), Seção 6 nova (**nuance e precisão** — pares confundidos + falsos
      cognatos acadêmicos + verbos de reporte com postura), Seção 7 nova
      (**vocabulário funcional para Listening** — sinalizadores de palestra +
      phrasal verbs de campus), Seção 9 nova (**9 drills com gabarito**), Seção
      11 nova (protocolo V1–V6). Seções renumeradas (Kit 5→8, ativação 6→10,
      checklist 7→12). Widget SRS reancorado para `<h2>SEÇÃO 9`. `commit 791d2c0`.
- [x] **M7 Simulados progressivos** (2026-09-09) — ~4k → ~7,5k palavras. A
      estrutura de 4 simulados já batia com o formato 2026. Adicionado:
      pré-requisitos por simulado + conversão banda CEFR↔0–120 (Parte 1),
      template da semana entre simulados (Parte 2), Simulado 2 muito expandido
      (CtW 4→12 c/ formato C-test, +texto Daily Life, +Academic Passage,
      Listening 4→10 itens, Build a Sentence 3→8, respostas-modelo banda 3/5),
      Simulado 3 (CtW 3→8), **Parte 6 reescrita** — a taxonomia de triagem agora
      espelha 1-a-1 os protocolos R/L/S/W/V/RG dos módulos (SR-*→M1, SL-*→M2,
      SS-*→M3, SW-*→M4) com código de reparo exato + consolidação entre 2
      simulados, Parte 9 nova (calendário de 8 semanas). `build_plain`.
      `commit 4a50fab`.
- [x] **M8 Exam Day Protocol** (2026-09-09) — ~4,3k → ~6,4k palavras. Corrigida a
      inconsistência de ordem das seções (Parte 6 tinha R→L→Speaking→Writing;
      unificado com M7/CLAUDE.md para **R→L→[pausa]→Writing→Speaking** + aviso de
      que W↔S varia por centro/modalidade — **confirmar na inscrição ETS**).
      Adicionado: micro-orçamento de tempo por seção + cross-links aos códigos de
      triagem do M7; subseção **TOEFL iBT Home Edition** (requisitos técnicos,
      regras de ambiente, quadro branco no lugar de papel, checklist próprio);
      ensaio dos protocolos nos Simulados 3–4; +8 cenários anti-colapso; regras
      de reteste (3 dias, validade 2 anos, MyBest); Parte 9 nova (**cola mental**
      de uma página). `build_plain`. `commit 0bacb28`.
- [x] **M9 Brazilian Trap Library** (2026-09-10) — ~4,3k → ~7,5k palavras.
      Parte 1 liga cada trap ao código de reparo. Parte 2.1 preposições +14;
      Parte 2.3 ganhou 5 subseções novas (incontáveis, artigo indefinido/a-an,
      ordem das palavras, present perfect × passado, plural/concordância de
      número). Parte 3 falsos cognatos +16. Parte 4: FONEMA 7–9 (/ɪ/–/iː/, /ʌ/,
      epêntese inicial com S) + 4.1b acento de palavra em cognatos. Parte 5 +8 +
      mini-banco de frases de e-mail (cross-ref M5 corrigida 4.2→5.2). Parte 7
      glossário 30→~50. **Parte 8 nova** (mapa reverso código M7 → trecho do
      módulo). **Parte 9 nova** (sprint de eliminação de 2 semanas).
      `build_plain`. `commit 4c1e6df`.

**Fase 7 concluída.** Fragmentos finais: mod0=42k, mod1=84k, mod2=77k, mod3=54k,
mod4=66k, mod5=75k, mod6=118k, mod7=86k, mod8=45k, mod9=68k. `artifact` ≈ 777 KB.
Currículo passou de ~50k para ~110k palavras. Todos os módulos com protocolo de
erros próprio, drills com gabarito, exemplos resolvidos; M7 e M9 amarram os
códigos de erro entre si.

## Fase 6 — Publicação (preparado em 2026-09-17, ainda não executado)

Usuário pediu pra deixar pronto sem publicar ainda. Estado hoje: **sem
remoto git configurado** (`git remote -v` vazio) — nenhum repositório no
GitHub existe pra este projeto ainda. `artifact/index.html` é gitignored
(gerado, nunca commitado) — pra publicar, o jeito mais simples é buildar
localmente (onde `app/supabase_config.json` já existe com as credenciais
reais) e mandar só o artifact pra uma branch/pasta que o GitHub Pages sirva,
sem CI — evita ter que colocar segredos do Supabase em GitHub Actions.

Checklist pra quando o usuário confirmar:

- [ ] Criar o repositório no GitHub (público, já que Pages grátis exige
      público num repo pessoal — ou usar GitHub Pro/Team se quiser privado)
- [ ] `git remote add origin <url>` + `git push -u origin master` (ou `main`)
- [ ] Copiar `artifact/index.html` (build local, com o Supabase real
      embutido) pra `docs/index.html` na raiz do repo **ou** uma branch
      `gh-pages` — GitHub Pages serve a partir de um desses dois
- [ ] Settings → Pages → Source: a branch/pasta escolhida acima
- [ ] Anotar a URL final (`https://<usuario>.github.io/<repo>/` ou domínio
      customizado, se houver)
- [ ] Supabase → Authentication → URL Configuration: trocar Site URL e
      Redirect URLs de `http://localhost:8000` pra essa URL final
- [ ] Testar login (e-mail + Google, se já configurado) e sync no endereço
      final, inclusive no celular
- [ ] Toda vez que o conteúdo/código mudar depois disso: rebuildar local e
      repetir a cópia pro `docs/`/`gh-pages` — não é automático sem CI

---

## Pendências

- **Vídeos explicativos por módulo (pedido do usuário, 2026-09-20).** O
  usuário está gravando, por fora do projeto, um vídeo curto por módulo
  explicando "o que fazer neste módulo" numa ferramenta de vídeo por IA
  (a primeira sugerida numa resposta anterior: Synthesia/HeyGen, não
  confirmado qual exatamente). Quando ele mandar os arquivos ou links
  (um por módulo, pode ser aos poucos, não precisa ser tudo de uma vez),
  falta: decidir onde hospedar (Supabase Storage, já que o app já usa
  Supabase, ou um link externo tipo YouTube/Vimeo não listado publicamente)
  e construir o player embutido no topo do painel de cada módulo (`.panel-head`
  em `app/build.py`, ao lado do h1). Nada implementado ainda, só a estrutura
  combinada.
- **Cupom de desconto no checkout (pedido do usuário, 2026-09-18).** Adicionar
  suporte a cupom de desconto na hora da compra (tela de pagamento / botão
  "Comprar acesso"). Ainda não desenhado: precisa decidir onde os cupons
  vivem (tabela nova no Supabase? campo fixo no código?), se são percentuais
  ou valor fixo, se têm validade/limite de uso, e como isso se conecta com
  `create-checkout`/`mp-webhook` (o preço vem do Mercado Pago, então o
  desconto provavelmente precisa ajustar o valor da preference antes de
  criar o checkout, não só cosmético na tela). Não implementado ainda,
  só registrado aqui a pedido do usuário pra não perder o pedido.
- **Verificar o formato 2026 contra fonte oficial da ETS.** O conteúdo assume os
  números do material de consolidação (50 itens Reading, Speaking de 8 min, etc.).
  Vale uma checagem no site oficial antes de finalizar M0.
- **`git init` ainda não feito** nesta sessão — próximo passo.
- **`_archive/` e `_snapshots/`** devem entrar no `.gitignore`? Decidir no commit
  inicial. (Sugestão: versionar `_archive/` uma vez, ignorar `_snapshots/`.)

## Baseline de contagem (2026-09-03, 10 módulos)

Fragmentos: mod0=45.421, mod1=44.444, mod2=50.740, mod3=34.232, mod4=30.599,
mod5=24.327, mod6=67.351, mod7=59.798, mod8=37.218, mod9=42.877 chars.
`artifact/index.html` = 466.9 KB. **10 módulos ativos (M0–M9)**, 121 tabelas,
0 placeholders. Diagnóstico M0 = 10 questões. Drills interativos = 3 (Reading)
+ 4 (Listening). M3/M4/M5/M6/M8/M9 são texto + drills em papel (sem widget).

## Observações visuais (2026-09-02, screenshots headless)

- Look editorial: Fraunces (títulos) + Inter (corpo) + IBM Plex Mono (rótulos);
  paleta creme/âmbar no claro, quase-preto no escuro. Limpo e legível.
- Widgets de quiz/drill funcionam bem (card de passagem, contador, A/B/C/D,
  confirmar→revelar→refazer).
- **A ajustar:** rótulo "Prep oficial" na sidebar (soa como afiliação ETS —
  trocar por "Preparação independente" antes de publicar); 1 checkbox de
  progresso por h2 E h3 é excessivo (só h2 deveria contar); diagramas ASCII
  em bloco mono são funcionais mas plainos.
- Publicar como Artifact foi **bloqueado pelo classificador** (marca "TOEFL" +
  "Prep oficial"). Preview local: `python scripts\serve.py`.
