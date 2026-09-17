# Roadmap iTOEFL

Memória entre sessões. Atualizar ao concluir cada etapa.

**Última atualização:** 2026-09-17
**Agora:** Fase 7 (conteúdo) concluída. **3 frentes abertas em paralelo** (ver abaixo).
`artifact/index.html` ≈ 954 KB. Login agora obrigatório quando o Supabase
está configurado (ver v11) — isso muda o comportamento em produção depois da
Fase 6, não só em dev.

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

## Decisões travadas

| Decisão | Escolha | Data |
|---|---|---|
| Formato do TOEFL | **2026** (CEFR 1–6, adaptativo, ~1h25). O formato antigo 0–120 fica só em `_archive/` | 2026-09-02 |
| Linha de base | **Pacote do chat de consolidação** (pipeline Python + módulos 0–4/7 prontos) | 2026-09-02 |
| Distribuição | Site estático gerado; servido localmente para dev | 2026-09-02 |
| Fonte da verdade | `consolidated/*.md` (texto) + `app/*.json` e `drills_data.py` (widgets) | 2026-09-02 |
| Backend Supabase | Sim, mas **depois** do conteúdo dos 10 módulos | 2026-09-02 |
| Ferramental | Python 3.13 + Git 2.55 + pacote `markdown` | 2026-09-02 |

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
