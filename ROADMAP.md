# Roadmap iTOEFL

Memória entre sessões. Atualizar ao concluir cada etapa.

**Última atualização:** 2026-10-13
**O que tem neste arquivo:** a lista única de pendências ("Tudo que falta") e
as decisões travadas. Nada mais.
**Histórico:** o que cada sessão fez, as fases antigas e o mapa de pendências
de setembro estão em `docs/historico-sessoes.md`. Sessão nova entra lá, no
topo, e aqui só se marca o item.
**Plano de expansão:** as frentes de app, videoaulas, banco de questões,
correção por agente e conversação estão detalhadas em
`docs/roadmap-expansao.md`. As etapas 1 a 6 abaixo são o resumo dele.
**Conferência do formato da prova:** `docs/conferencia-formato-2026.md` (números)
e `docs/conferencia-conteudo-2026-10.md` (regras, Home Edition, notas).
**Agora:** o site está pronto para publicar e a Etapa 0 (publicar, pagamento,
teste em celular) bloqueia todo o resto. Os três planos e a tela de
apresentação estão em código, sem publicar: o próximo passo do dono é o
`docs/deploy-planos.md`. Fora dela, já estão feitos o PWA, o
plano B do gravador no iPhone, a infraestrutura de videoaulas e de
aprofundamento e a primeira parte do banco de questões.

---

## Tudo que falta (consolidado em 2026-10-06)

Lista única de pendências, juntando o que estava espalhado neste arquivo
(mapa de 2026-09-20, sessões de setembro, Fase 6, lista de 12 pontos, review
do M0) com o plano de expansão de `docs/roadmap-expansao.md`. **Esta seção
substitui o "Mapa do que falta" antigo,** que fica só como histórico em
`docs/historico-sessoes.md`, junto com as sessões e as fases. Marcar `[x]`
aqui ao concluir.

Legenda de quem faz: **(U)** só o usuário consegue (contas, painéis,
pagamento, aparelho físico). **(C)** código ou conteúdo, feito em sessão.
**(D)** decisão do usuário antes de qualquer trabalho.

### Etapa 0: lançar o que já existe

Nada das etapas seguintes anda sem esta. Ordem sugerida de cima para baixo.

**0.1 Arrumar a casa**

- [x] (C) Commitar o trabalho do cupom, que está pronto e testado mas ainda
      sem commit (`app.js`, `build.py`, `create-checkout/index.ts`,
      `schema.sql`, este arquivo, `docs/roadmap-expansao.md`).
- [x] (C) Colocar `supabase/.temp/` no `.gitignore`.
- [x] (C) Tirar o debug de `create-checkout/index.ts` (linha 105 ainda devolve
      `mpStatus` e `mpBody` para o aluno) e publicar a function. Conferir na
      aba "Code" do painel se o deploy pegou, já falhou calado duas vezes.

**0.2 Segurança, antes de qualquer aluno real**

- [ ] (U) Trocar a senha do banco do Supabase e a senha da conta Google
      admin. As duas apareceram em texto puro num chat em 2026-09-22.
- [ ] (U) Confirmar que a `sb_secret` e a `service_role` coladas por engano
      na fase do Supabase foram rotacionadas. O projeto já migrou para as
      JWT Signing Keys, então a `service_role` não se troca mais gerando
      outro JWT secret: ela morre ao desativar as chaves antigas em
      Settings > API Keys (reversível). Ordem: (1) `sb_secret` nova e a
      antiga apagada; (2) publicar as 5 functions, que desde 2026-10-14 só
      usam as chaves novas (`supabase/functions/_shared/keys.ts`) e têm
      `verify_jwt = false` com a checagem do token no próprio código;
      (3) testar compra e excluir conta; (4) desativar as chaves antigas.
      Feito até o (2) em 2026-10-14: usuário trocou a `sb_secret`, e as 5
      functions foram publicadas (create-checkout v16, mp-webhook v9,
      delete-account v6, submit-essay v1, review-essay v1), com o código
      novo conferido no ar e as 5 respondendo sem erro de chave.
      Falta o (3) e o (4), com o usuário.
      Não revogar o Legacy JWT secret: não é preciso, ele não vazou.
- [ ] (U) Apagar do banco a função `email_for_username` (só as linhas 97 a
      100 do `schema.sql`, não o arquivo inteiro). Em 2026-10-14 ela ainda
      existia em produção.
- [ ] (U) Religar "Confirm email" no Supabase (desligado para teste).
- [ ] (U+C) Configurar um SMTP próprio no Supabase. O limite de envio do
      plano grátis já estourou só com testes, e com alunos reais vai travar
      cadastro e recuperação de senha.

**0.3 Pagamento**

- [ ] (D) Ficar no Mercado Pago ou trocar de gateway. Aberto desde
      2026-09-24. Decidir junto com o modelo de cobrança da correção por IA
      (Etapa 3), porque assinatura muda o requisito.
- [x] (D) Preço de lançamento. Decidido em 2026-10-07: três planos, ver
      "Decisões travadas". O preço único de R$ 9,90 vitalício sai.
- [x] (C) Implementar os três planos, **em código, sem publicar**
      (2026-10-08). Escolha de plano na tela de compra; preço e prazo no
      servidor (`supabase/functions/_shared/plans.ts`), o navegador manda só
      o id; tabela `payments` (extrato) e `entitlements.expires_at`,
      recalculada do extrato pela função `apply_payment`; aviso de acesso
      vencido no bloqueio e em Minha conta, com "Renovar ou mudar de plano";
      cupom percentual sobre o preço do plano; termos com planos, validade e
      reembolso de 7 dias. Regra: renovar antes de vencer soma os dias,
      Premium troca o prazo por vitalício, reembolso recalcula. As functions
      nunca rodaram (a máquina não tem Deno): a primeira execução é o deploy.
- [ ] (U) Publicar os planos, seguindo `docs/deploy-planos.md` na ordem:
      rodar `supabase/migrations/20261008_planos.sql`, publicar
      `create-checkout` e `mp-webhook`, conferir a versão publicada e fazer a
      compra de teste de cada plano (inclui vencimento, aviso repetido e
      reembolso).
- [ ] (U) Passar por advogado os dois trechos de `legal/termos.md` marcados
      `REVISAR (advogado)`: seção 6 (planos, validade, renovação) e seção 7
      (reembolso de 7 dias, sem reembolso proporcional depois). O build
      avisa enquanto a marca existir.
- [ ] (U) Concluir a compra de teste em aba anônima, sem extensão nenhuma,
      e ver o acesso ser liberado de ponta a ponta. Dados do cartão de teste
      na Sessão 2026-09-24 de `docs/historico-sessoes.md`.
- [ ] (U) Resolver a validação da conta real do Mercado Pago (a criação de
      checkout com ela foi bloqueada pelo antifraude) e trocar as
      credenciais de teste pelas de produção.
- [x] (C) Mostrar "Pago" ou "Sem acesso" em Minha conta (a tabela
      `entitlements` já existe).

**0.4 Publicar**

- [ ] (D) Onde hospedar e com qual endereço. Recomendação: Cloudflare
      Pages (grátis, aceita repositório privado, HTTPS e domínio próprio).
      Um domínio próprio vale a pena desde já: o endereço entra nas
      configurações de Supabase, Google, gateway e, depois, nas lojas, e
      trocar depois dá retrabalho em todos.
- [x] (C) Site pronto para publicar, sem publicar (2026-10-17). Passo a
      passo do dono em `docs/publicar.md`. O endereço mora só em
      `app/site.json` (`SITE_URL`; a variável de ambiente vence) e sai em
      canonical, og:url, `robots.txt` e `sitemap.xml`. O build gera o
      `artifact/_headers` (segurança, CSP, `sw.js` e manifesto sem cache) e
      aceita `SUPABASE_URL` e `SUPABASE_PUBLISHABLE_KEY` do ambiente para o
      build de CI. O service worker regrava limpa a resposta redirecionada
      do pré-cache. A `create-checkout` usa o secret `SITE_URL` para a volta
      do pagamento (falta deploy). `scripts/prepublish_check.py` reprova
      enquanto houver `[PREENCHER]`, `SITE_URL` local, chave secreta no
      `supabase_config.json`, credencial `TEST-` ou smoke test falhando; o
      smoke test mostra o resultado só como aviso.
- [ ] (D) Raiz do site: no Cloudflare Pages `/` abre o app e a apresentação
      fica em `/apresentacao`. Para a raiz abrir a apresentação é preciso
      renomear o arquivo do app (o Cloudflare manda `/index.html` para `/`).
- [x] (U) Criar o repositório no GitHub e configurar o remoto. Feito em
      2026-10-06: `https://github.com/Fatrock3871/itoefl`, privado, branch
      `main` (a antiga `master` foi renomeada). Repositório privado não
      publica no GitHub Pages gratuito, o que pesa na decisão de
      hospedagem acima.
- [ ] (C) Publicar o `artifact/` buildado, seguindo `docs/publicar.md`
      (trocar `SITE_URL`, `prepublish_check.py` passando, secret `SITE_URL`
      e deploy de `create-checkout` e `review-essay`).
- [ ] (U) Supabase: trocar Site URL e Redirect URLs de `localhost:8000` para
      o endereço final (passo 9 de `docs/publicar.md`).
- [ ] (U) Google Cloud: adicionar o endereço final nas origens autorizadas
      e tirar o app do modo "Testing", senão só testadores cadastrados logam
      com Google (passos 11 e 12 de `docs/publicar.md`).
- [x] (C) Página de termos de uso e política de privacidade. Escritas em
      `legal/*.md`, geradas pelo build como `artifact/termos.html` e
      `artifact/privacidade.html`, com link no cadastro, na compra, em Minha
      conta e na sidebar.
- [ ] (U) Preencher os campos `[PREENCHER: ...]` dos dois textos (nome ou
      razão social, CPF ou CNPJ, e-mail de contato). O build avisa enquanto
      faltar. Os textos são um rascunho: passar por um advogado antes de
      vender.
- [ ] (U) Rodar o `supabase/schema.sql` atualizado no SQL Editor. Ele apaga
      do banco a função `email_for_username` e a coluna `username`, sobras do
      login por nome de usuário. A função ficava exposta a visitante sem
      login e devolvia o e-mail de qualquer nome de usuário.
- [x] (C) Excluir conta (função no servidor com `service_role`). Pendência
      antiga que vira obrigação com LGPD e com as lojas.

**0.5 Validar**

- [ ] (U) Testar o site publicado num Android e num iPhone reais. Nunca foi
      feito, toda verificação até hoje foi em Chrome headless.
- [ ] (U) Testar a sincronização com dois aparelhos na mesma conta.
- [ ] (U) Colocar de 3 a 5 pessoas reais para fazer o fluxo inteiro
      (cadastro, compra, estudo) e anotar onde travam. É a maior lacuna do
      projeto: dificuldade dos drills, ritmo e clareza nunca foram validados
      por ninguém de fora.
- [ ] (C) Rodar `python scripts\smoke_test.py` no build final.

### Etapa 0B: pendências de conteúdo e produto herdadas

Pequenas, independentes entre si, podem entrar em qualquer intervalo.

- [x] (C) Passada de consistência nos 10 módulos depois das reescritas de
      tom: repetição, trecho quebrado, referência cruzada desatualizada.
- [x] (C) Conferir os números do formato 2026 linha a linha contra o
      documento oficial da ETS. Feito em 2026-10-07, registrado com as URLs
      em `docs/conferencia-formato-2026.md`. Corrigido: a prova não tem pausa
      de 10 minutos (M7 e M8 ensinavam uma), o Listening dura de 25 a 29
      minutos e não 18, a ordem das seções é fixa, a ETS publica a
      concordância entre as bandas e o 0 a 120 (o M0 usava faixas próprias) e
      os tempos de resposta do Speaking são oficiais.
- [x] (C) Caça a erros no site inteiro, num Chrome de verdade (2026-10-08).
      Corrigidos: data da sequência em UTC (o dia virava às 21h), sequência
      marcada só por abrir o site, HTML digitado no registro de erros,
      reinício que deixava subseções e calculadora, importação sem marcar
      sincronização, mapa do curso invisível na gaveta, contraste dos botões
      abaixo de AA nos dois temas, texto de "marcar como concluída" que não
      clicava. O smoke test ganhou uma passada com recarga, tela de 375 px,
      contraste e service worker (`scripts/smoke_browser.py`).
- [x] (C) Conferência do resto do conteúdo contra a ETS (2026-10-08), em
      `docs/conferencia-conteudo-2026-10.md`. Corrigidos M0, M3, M5, M7 e M8:
      45 s sem preparo na entrevista, concordância oficial no M7, regras da
      Home Edition (TOEFL Test App, celular ou espelho no check-in, check-in
      a partir de 15 min antes), atraso no centro sem tolerância,
      cancelamento de score, 4 envios incluídos, documento físico com
      assinatura, e "decore 3 esqueletos" reescrito.
- [x] (C) Auditoria da plataforma e primeira leva de melhorias (2026-10-08),
      em `docs/auditoria-plataforma-2026-10.md`: devolutiva em palavras nos
      exercícios, barra do topo com módulo e Parte, cartão "Comece aqui",
      teclado e leitor de tela (subseções, janelas, rótulos, inglês
      marcado), alvos de toque, sequência de dias na gaveta, fontes por
      `<link>`. O que sobrou sem depender de decisão está na seção 5 dela.
- [x] (C) Tela de apresentação com os três planos (2026-10-08):
      `artifact/apresentacao.html`, gerada pelo build. Chamada, o que tem
      dentro (números tirados do build), diagnóstico grátis sem conta com
      banda e cronograma, tabela dos planos com "Recomendado" no Standard,
      reembolso de 7 dias, perguntas frequentes e links legais. Testada em
      desktop e 375 px, nos dois temas. Ficaram de fora as capturas de tela
      do desenho original. Falta (U) ler o texto da página, e, ao publicar,
      apontar o endereço público para ela.
- [x] (D) Colisão de nomes entre os cronogramas do M0 e os planos de preço.
      Decidido e feito em 2026-10-08: os cronogramas passam a ser Intensivo
      (30 dias), Regular (60) e Completo (90). Nenhuma chave de
      `localStorage` guardava o nome (a recomendação é recalculada do
      diagnóstico e o id das subseções é por posição), então não houve
      migração.
- [x] (C) Versão gratuita (2026-10-17). O dono aprovou o modelo B
      (freemium, amostra fixa sem prazo). Feito: `app/free_sample.json`
      (M0 inteiro, Parte 1 de cada módulo, 1 Complete the Words, 1 drill de
      Listening, 1 Listen and Repeat, 3 Build a Sentence, nenhum simulado),
      bloqueio por Parte e por exercício na conta logada sem plano em dia,
      com motivo e botão para os planos, envio de redação trancado,
      progresso contando só a amostra, convite no login, seção na
      apresentação, Minha conta e uma linha nos Termos. Detalhes na seção 11
      de `docs/versao-gratuita.md`. O bloqueio é de interface até a Etapa 2.
- [ ] (U) Ler a linha nova da conta grátis nos Termos (item 6, marcada
      REVISAR para o advogado) e conferir a conta grátis com uma conta de
      teste sem plano depois de publicar.
- [ ] (D) Versão gratuita, o que ficou para depois: contador de visitas ou
      medição de uso (seção 7 de `docs/versao-gratuita.md`), e a degustação
      por tempo (modelo C) só depois da Etapa 2.
- [ ] (D) O site diz que Speaking e Writing são corrigidos "100% por IA" e
      cita e-rater e SpeechRater; a ETS de 2026 não nomeia os motores. Ver a
      seção 4 de `docs/conferencia-conteudo-2026-10.md`, com os outros pontos
      que ficaram em aberto (preço no Brasil, documento aceito para
      brasileiros).
- [x] (C) Divergências da ETS fechadas em 2026-10-08. Pontos brutos de
      Reading e Listening: o "0-30" da Tabela 1 do Overview não é a escala
      antiga (na mesma coluna Writing é 0-20 e Speaking 0-55, que são pontos
      brutos), então a divergência com o Blueprint (35) é real; o site segue
      o Blueprint, o mais específico, e o M0 explica os três números (bruto,
      banda, escala antiga). Preço do envio adicional e versão do Windows:
      o site não cita número e o M8 manda conferir na página da ETS, com
      link. Seção 7 de `docs/conferencia-conteudo-2026-10.md`.
- [ ] (D) Reading: o site diz router de 9 minutos e módulo de 18 a 21; a
      tabela da ETS põe os números nas colunas contrárias. O total (27 a 30)
      está certo. Não foi alterado, ver a seção 3 da conferência.
- [x] (C) Corrigir a tabela de formato do `CLAUDE.md`: o total de pontos
      brutos está 120, mas as seções somam 145, que é o número registrado na
      verificação contra a ETS (Fase 7 do histórico).
- [x] (U) M8: a ordem Writing e Speaking não varia por centro. A ETS fixa
      Reading, Listening, Writing, Speaking (conferência de 2026-10-07), e o
      M8 foi corrigido.
- [x] (D) M7: decidido em 2026-10-07 que viram interativos. Feito: 19 blocos,
      62 questões, correção só na entrega do bloco.
- [x] (C) M4: o texto tem 30 itens de Build a Sentence e o widget só 10.
- [x] (C) M0: calculadora de score interativa e resumo executivo no topo
      (dois itens da review externa que nunca foram iniciados).
- [x] (C) Estender o painel "Seu desempenho real" para além de M1 e M2.
      Feito em 2026-10-07: inclui Complete the Words, Build a Sentence e M7.
- [x] (D) M9: decidido em 2026-10-07 que fica como está. A pergunta sobre
      expandir o M0 como introdução foi atendida pelo resumo no topo do módulo.
- [x] (C) Limpeza: remover `showLockMessage()` e `.lock-msg` (código morto),
      a RPC `email_for_username` e a coluna `username` do banco, e atualizar
      o `CLAUDE.md` (faltam as chaves `toefl_partpos_v1`,
      `toefl_h3progress_v1`, `toefl_avatar_v1`, os renderizadores
      `render_errorlog.py` e `render_weeklydash.py`, o `smoke_test.py` e as
      edge functions).
- [x] (C) Travessão de pausa trocado por vírgula, dois-pontos ou ponto nas
      explicações em português de `app/drills_data.py` (23) e
      `app/quiz_mod0.json` (8), em 2026-10-07. Ficaram de propósito os do
      texto em inglês e os que separam rótulo em título.
- [ ] (C) Mesma passada de travessão nos `consolidated/*.md` (59 ocorrências
      em 8 módulos, parte delas em inglês ou em diagrama) e nos textos de
      interface de `app/app.js` e `app/build.py`. Não foi olhado caso a caso.
      Só o que estiver em português: no inglês o travessão fica (decisão de
      2026-10-13).
- [ ] (C) **Revisão de conteúdo de 2026-10-13** (professor de inglês; 79
      críticos, 346 importantes, 187 de estilo; relatórios fora do
      repositório, em `itoefl-gerencia/revisao/`). Entra em três rodadas:
  - [x] Rodada 1 (2026-10-13): os críticos, mais as decisões A (travessão
        só em português) e C (drills legados apagados). 77 de 79 aplicados,
        2 adiados para a rodada 2, nenhum recusado. A lista item a item
        está em `itoefl-gerencia/revisao/APLICADO-rodada1.md`.
  - [x] Rodada 2 concluída em 2026-10-16 (importantes, pontuação do inglês e
        as 2 Sentence Simplification do M7; fica de fora encurtar as
        passagens; lista em `itoefl-gerencia/revisao/APLICADO-rodada2.md`).
        Escopo original: os importantes, a decisão B (tirar Sentence
        Simplification, Insert a Sentence, Prose Summary e arrastar para a
        tabela; encurtar as passagens para o padrão da prova) e devolver a
        pontuação do inglês onde o travessão virou ":" ou "·". Inclui os 2
        críticos adiados: o Grupo A2 do M1 (lacunas com alternativas, que
        não é o formato da prova) e os tipos extintos nos drills do M1.
  - [x] Rodada 3 (estilo) concluída em 2026-10-18: 151 itens aplicados, 2 recusados, o resto já estava feito; lista em `itoefl-gerencia/revisao/APLICADO-rodada3.md`.
- [x] (C) Mover o histórico de sessões deste arquivo para
      `docs/historico-sessoes.md` (2026-10-07). Aqui ficam só esta lista e as
      decisões travadas.

### Etapa 0C: alinhar as tarefas ao formato real da prova

Achado em 2026-10-07 ao ler os quatro testes práticos gratuitos da ETS no
formato 2026. Análise completa em `docs/ets-materiais-oficiais.md`. Vem antes
do banco de questões, porque define o formato de dois tipos de item.

- [x] (C) M7: indicar os quatro testes oficiais gratuitos como simulados
      extras, com link para a ETS.
- [x] (C) **Complete the Words está no formato errado.** O site usa lacuna de
      palavra inteira com 4 alternativas; a prova apaga o final da palavra e o
      aluno digita as letras, sem alternativas. São 30 dos 50 itens de
      Reading. Falta: widget de digitar letras, parágrafos acadêmicos
      originais e revisão do Método CTW no M1.
- [x] (C) **Build a Sentence está simplificado demais.** Na prova cada item é
      resposta a uma fala, tem trechos fixos e às vezes um bloco que sobra,
      com foco em perguntas indiretas. Falta estender o widget e escrever
      itens novos.
- [x] (C) Listen and Repeat: conjuntos de 7 frases de um mesmo cenário,
      crescendo de tamanho, só ouvidas (o texto hoje aparece antes).
- [x] (C) Take an Interview: cenários de 4 perguntas do mesmo tema, em escada.
- [x] (C) M4: e-mail de 7 minutos com 3 pontos obrigatórios e cenário que
      também pode ser cotidiano; discussão com mínimo de 100 palavras.

### Etapa 0D: sobras da leva de 2026-10-07

- [ ] (U) Abrir o site e testar os exercícios novos de verdade: Complete the
      Words (M1), Build a Sentence e caixa de escrita (M4), os conjuntos com
      áudio (M3), um bloco de simulado (M7), a calculadora e o treino por
      nível (M0). Só foram testados em Chrome headless.
- [ ] (U) Passar os textos novos em inglês por um professor: 8 parágrafos
      (`app/ctw_data.py`), 30 itens (`app/build_sentence_data.py`) e os
      cenários de Speaking (`app/speaking_data.py`).
- [x] (C) Painel "Seu desempenho real" e meta diária contam os exercícios
      novos (2026-10-07): Reading inclui o Complete the Words de digitar, e
      há linhas novas para Build a Sentence e para os simulados do M7. A
      estimativa de nível usada no treino por nível herda isso.
- [x] (C) Writing e Speaking dos simulados do M7 interativos (2026-10-07):
      Listen and Repeat e entrevista com áudio e texto escondido, caixa de
      escrita no e-mail e na discussão, e as 13 respostas-modelo fechadas até
      o aluno pedir (antes ficavam à vista, embaixo do enunciado). O Build a
      Sentence do M7 continua no molde antigo, de reordenar e escrever.
- [ ] (C) Geração de questões por nível: depende do banco (Etapa 2).

### Etapa 1: app instalável e videoaulas

Detalhe em `docs/roadmap-expansao.md`, seções 3 e 4.

- [x] (C) PWA: manifesto, service worker com versão carimbada pelo build,
      ícones, botão "Instalar app", aviso de nova versão (2026-10-07).
      Testado em Chrome headless via localhost: o service worker instala,
      guarda os 6 arquivos e assume a página. Nunca testado em aparelho real:
      nem a instalação em si, nem o uso offline com login.
- [ ] (U) Instalar e testar nas 4 plataformas: Android, Windows, macOS, iOS.
- [x] (C) Plano B para a transcrição do gravador no iPhone (2026-10-07). No
      iPhone e no iPad o padrão é só gravar, com a opção "Só transcrever, sem
      gravar áudio". Navegador sem reconhecimento de fala mostra um aviso fixo
      e segue gravando. Testado com um iPhone simulado no smoke test; falta o
      teste em iPhone de verdade, que entra no item (U) acima. Transcrição no
      servidor continua na Etapa 5.
- [ ] (D) Hospedagem dos vídeos. Recomendação: YouTube não listado agora.
- [ ] (U) Entregar os vídeos gravados, pode ser um por vez.
- [x] (C) `app/videos.json` e player com carregamento no clique, no topo do
      módulo e de cada Parte. "Aula assistida" conta no progresso
      (2026-10-07). A lista começa vazia e nada aparece. Aceita YouTube (pelo
      id do vídeo) e arquivo próprio (URL). Testado no smoke test com um
      build de exemplo; nunca com vídeo de verdade.
- [x] (C) Legenda e transcrição recolhível (2026-10-07). No YouTube a legenda
      é a do próprio vídeo, pedida em português; em arquivo próprio é um
      `.vtt`. O build avisa quando o vídeo não tem transcrição.
- [ ] (D) Cadastrar um vídeo aumenta o total do módulo: quem já tinha o
      módulo em 100% (e o certificado) volta a ficar abaixo até marcar a
      aula. Se isso incomodar, a alternativa é a aula não contar para quem já
      concluiu. Hoje conta para todos.
- [x] (C) Seletor "trilha rápida" ou "trilha completa" (2026-10-07). Fica na
      sidebar e só aparece quando houver bloco de aprofundamento no site, o
      que ainda não é o caso. A escolha fica em `toefl_trilha_v1`, local do
      aparelho como o tema.
- [ ] (D) A trilha escolhida deve acompanhar a conta, de um aparelho para
      outro? Hoje não acompanha.

### Etapa 2: banco de questões e aprofundamento

Detalhe em `docs/roadmap-expansao.md`, seções 4 e 5.

- [x] (C) Formato do item e script de validação em `bank/` (2026-10-07):
      `bank/README.md`, `bank/schema/item.schema.json`, `bank/tools/validate.py`
      e 15 testes em `bank/tools/test_bank.py`.
- [x] (C) Tabelas `items` e `attempts` com RLS, leitura só para quem pagou
      (2026-10-07). **Só escritas** em `supabase/schema-bank.sql`, nunca
      executadas.
- [ ] (U) Autorizar e rodar o `supabase/schema-bank.sql`, de preferência
      primeiro num projeto de rascunho. Depois disso falta (C) o script que
      publica `bank/items/` na tabela `items`.
- [x] (C) Migrar os itens atuais para o banco, com contagem declarada
      (2026-10-07). Origem 228, destino 228: 10 do diagnóstico, 118 dos Action
      Drills (67 no M1, 51 no M2), 8 parágrafos de Complete the Words (80
      lacunas), 30 de Build a Sentence e 62 dos simulados do M7. Conferido
      também contra o site gerado: 128 `.qcard` + 62 `.exam-q` + 30
      `.bsq-card` + 8 `.ctw` = 228. Os "128" do plano eram só diagnóstico e
      Action Drills. Todos entram como `rascunho`. O smoke test valida o
      banco e reprova se `bank/items/migrado/` ficar atrás das fontes.
- [x] (D) `MOD1_DRILLS` e `MOD2_DRILLS` em `app/drills_data.py` (35 itens)
      eram importados pelo pipeline mas não apareciam no site, e repetiam em
      parte os Action Drills. Decisão do dono em 2026-10-13: apagar. Apagados
      da fonte no mesmo dia; o banco tinha 228 itens antes e tem 228 depois,
      porque eles nunca entraram.
- [ ] (C) Modo prática com filtros e "só as que errei".
- [ ] (C) Caderno de erros com revisão espaçada e botão "reportar questão".
- [ ] (D) Tamanho da amostra que o usuário revisa por lote. Sugestão: 10%.
- [ ] (C+U) Produzir os lotes até 600 itens: 200 Reading, 200 Listening,
      150 Build a Sentence, 50 enunciados de Writing.
- [ ] (C) Áudio de Listening com voz neural, gerado uma vez por item.
- [x] (C) Bloco de aprofundamento recolhível no pipeline (2026-10-07).
      Marcação `:::aprofundamento Título` ... `:::` nos `.md`, descrita no
      `CLAUDE.md`. Só a infraestrutura: nenhum bloco foi escrito. O exemplo
      de teste vive no smoke test e não entra no site.
- [ ] (C) Checkpoint de questões no fim de cada Parte. Depende do banco
      publicado e do modo prática.
- [ ] (C) Escrever o aprofundamento, um módulo por sessão: M3, M1, M2, M4,
      depois M5, M6, M9, M0, M7, M8.
- [ ] (C+U) Banco v2, 1.500 itens, com Listen and Repeat e Interview.

### Etapa 3: redações com correção por agente

Detalhe em `docs/roadmap-expansao.md`, seção 6.

- [ ] (D) Modelo de cobrança: créditos, assinatura ou cota incluída. Acesso
      vitalício de R$ 9,90 não paga correção ilimitada.
- [ ] (C) Piloto com 50 redações para medir custo e qualidade por modelo.
- [ ] (C) Rubrica versionada por task e conjunto de calibração.
- [ ] (C) Tabelas `submissions` e `feedback`, edge function `grade-writing`
      com cota e limite no servidor.
- [ ] (C) Tela de escrita (cronômetro, contador de palavras), tela de
      devolutiva e histórico com evolução.
- [ ] (C) Painel de revisão para a equipe ajustar notas.
- [ ] (C) Consentimento de LGPD no primeiro envio.
- [ ] (C) Cobrança do que for decidido (créditos ou assinatura) no gateway.

### Etapa 4: lojas de aplicativo

Detalhe em `docs/roadmap-expansao.md`, seção 3.

- [ ] (U) Abrir a conta de desenvolvedor Google cedo, por causa do período
      de teste obrigatório para conta nova.
- [ ] (D) Nome do app nas lojas. "TOEFL" é marca registrada da ETS e já
      causou um bloqueio de publicação neste projeto. Conferir a regra de
      cada loja para uso de marca de terceiro.
- [ ] (C+U) Play Store via PWABuilder, com `assetlinks.json` no domínio.
- [ ] (C+U) Microsoft Store via PWABuilder.
- [ ] (D) Conta Apple Developer e acesso a um Mac ou build em CI.
- [ ] (C) Casca Capacitor com notificação de lembrete de estudo.
- [ ] (U) Conferir a regra de pagamento dentro de app vigente na data.
- [ ] (C+U) Submissão à App Store, iOS e macOS.

### Etapa 5: Speaking com nota

Detalhe em `docs/roadmap-expansao.md`, seção 7.

- [ ] (C) Upload de áudio e transcrição no servidor.
- [ ] (C) Listen and Repeat com nota de pronúncia por palavra e fonema.
- [ ] (C) Simulador de Take an Interview por turnos, com rubrica e
      calibração reaproveitadas das redações.
- [ ] (C) Entrevista com perguntas de seguimento.

### Etapa 6: longo prazo

- [ ] (C) Banco v3, 3.000 itens ou mais.
- [ ] (C) Simulados adaptativos em dois estágios montados do banco.
- [ ] (C) Conversa por voz em tempo real, só dentro de plano de assinatura.
- [ ] (U) Comunidade de alunos e encontros ao vivo.

### Fora do código, a pensar antes de ter aluno pagante

Não foram pedidos, apareceram ao consolidar a lista.

- Canal de suporte ao aluno (um e-mail de contato já resolve no começo).
- Página de venda e forma de divulgação. Hoje a primeira tela é o login.
  **Pedido pelo usuário em 2026-10-07, para pensar depois:** uma tela de
  apresentação antes do login e da compra, mostrando o que a plataforma
  oferece. É o lugar natural para a tabela dos três planos (ver "Decisões
  travadas"), então convém desenhar as duas coisas juntas.
- Medição de uso, para saber onde os alunos param.
- **No radar, pedido pelo usuário em 2026-10-13:** cursor do mouse
  personalizado, que muda conforme a pessoa mexe no app. Falta o usuário
  dizer o que imagina (um cursor da marca no site todo, ou um que reage a
  botão, alternativa, arrastar). Cuidados quando for feito: não vale em
  celular, e o cursor de texto e o de link precisam continuar reconhecíveis.
- **No radar, pedido pelo usuário em 2026-10-13:** possível filiação a
  plataformas de venda de conteúdo digital, como a Kirvano. A decidir junto
  com o item do gateway (0.3), porque nessas plataformas o checkout é delas:
  a liberação do acesso em `entitlements` teria de vir de um aviso da
  plataforma, no lugar do `mp-webhook`. A conferir antes: taxas, como
  funciona o programa de afiliados, se aceitam os três planos com prazo e
  se avisam o nosso servidor a cada venda e reembolso.
- Plano do Supabase: conferir limites e política de pausa do plano grátis
  antes de depender dele com gente pagando.

---

## Decisões travadas

| Decisão | Escolha | Data |
|---|---|---|
| Formato do TOEFL | **2026** (CEFR 1–6, adaptativo, ~1h25). O formato antigo 0–120 fica só em `_archive/` | 2026-09-02 |
| Linha de base | **Pacote do chat de consolidação** (pipeline Python + módulos 0–4/7 prontos) | 2026-09-02 |
| Distribuição | Site estático gerado; servido localmente para dev | 2026-09-02 |
| Fonte da verdade | `consolidated/*.md` (texto) + `app/*.json` e `drills_data.py` (widgets) | 2026-09-02 |
| Backend Supabase | Sim, mas **depois** do conteúdo dos 10 módulos | 2026-09-02 |
| Ferramental | Python 3.13 + Git 2.55 + pacote `markdown` | 2026-09-02 |
| Precificação | Três planos. **Sprint**, 30 dias, R$ 39,90: prova já marcada, só simulado e plano de emergência (Pareto). **Standard**, 90 dias, R$ 89,90: o mais vendido, tempo para os 4 pilares com calma. **Premium (Passaporte)**, vitalício, R$ 149,90: quem vai tentar a prova várias vezes ou planeja com mais de um ano de antecedência. Substitui o R$ 9,90 vitalício | 2026-10-07 |
| Nomes dos cronogramas do M0 | **Intensivo** (30 dias), **Regular** (60 dias), **Completo** (90 dias). "Sprint", "Standard" e "Premium" ficam só para os planos de preço | 2026-10-08 |
| Diagnóstico grátis | As 10 questões do M0 abertas na tela de apresentação, **sem conta**, com o resultado de banda | 2026-10-08 |
| Versão gratuita | **Modelo B**, freemium por conteúdo, sem prazo: M0 inteiro, Parte 1 de cada módulo, 1 Complete the Words, 1 drill de Listening, 1 Listen and Repeat, 3 Build a Sentence, nenhum simulado, sem correção de redação. Lista em `app/free_sample.json` | 2026-10-17 |
| Reembolso | **7 dias** em todos os planos, pelo direito de arrependimento do CDC (art. 49) | 2026-10-08 |
| Selo na tabela de planos | **"Recomendado"** no Standard. Nunca "mais escolhido" ou "mais vendido": sem dado de venda seria afirmação falsa | 2026-10-08 |
| Travessão | A regra "sem travessão como pausa" vale **só para texto em português**. Em texto em inglês (passagens, transcrições, respostas-modelo, exemplos) o travessão é pontuação correta e permitido | 2026-10-13 |
| Tipos de pergunta extintos | **Remover** Sentence Simplification, Insert a Sentence, Prose Summary e arrastar para a tabela, e **encurtar as passagens** para o padrão da prova de 2026. Entra na rodada 2 da revisão de conteúdo | 2026-10-13 |
| Drills legados | **Apagar** `MOD1_DRILLS` e `MOD2_DRILLS` de `app/drills_data.py`: não apareciam no site | 2026-10-13 |
| Revisão de conteúdo de 2026-10-13 | Entra em **3 rodadas**: 1) críticos, 2) importantes + tipos extintos + pontuação do inglês, 3) estilo | 2026-10-13 |
