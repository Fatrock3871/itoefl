# iTOEFL — Plataforma de Preparação TOEFL iBT

Plataforma web de estudo para o **TOEFL iBT no formato 2026** (adaptativo,
alinhado ao CEFR), em português, voltada a candidatos brasileiros. O currículo
está dividido em 10 módulos (M0–M9). A aplicação é um site estático gerado por
um pipeline de build em Python a partir de Markdown.

## Ferramental

Máquina do usuário: Windows, **Python 3.13**, **Git 2.55**. Não há Node.
O pacote Python `markdown` (3.10+) é a única dependência do build —
`python -m pip install markdown` se faltar.

## Como buildar e rodar

```powershell
cd app
python build_pipeline.py     # consolidated/*.md  -> app/module_fragments_final.json
python build.py              # fragments + styles.css + app.js  -> artifact/index.html
                             # legal/*.md  -> artifact/termos.html, artifact/privacidade.html
cd ..
python scripts\serve.py      # abre http://localhost:8000/artifact/index.html
python scripts\smoke_test.py # builda e roda as checagens num Chrome headless
```

`artifact/index.html` é **gerado** — CSS e JS ficam embutidos nele pelo
`build.py`. Nunca editar `artifact/index.html` à mão: a próxima build sobrescreve.
Editar sempre a fonte (`consolidated/`, `app/styles.css`, `app/app.js`,
`app/*.json`, `app/drills_data.py`) e rebuildar.

## Arquitetura

```
consolidated/*.md         Texto dos 10 módulos (M0–M9) — fonte da verdade do conteúdo
app/build_pipeline.py     Monta os fragmentos HTML por módulo; injeta os widgets
app/build.py              Monta artifact/index.html (nav + painéis + CSS + JS)
app/quiz_mod0.json        As 10 questões do diagnóstico (M0)
app/drills_data.py        Drills interativos de Reading (M1) e Listening (M2)
app/vocab_kit.json        As 50 palavras do Kit de Emergência (flashcards SRS do M6)
app/build_sentence_data.py  30 itens de Build a Sentence no molde da prova (M4)
app/ctw_data.py           8 parágrafos de Complete the Words no molde da prova (M1)
app/speaking_data.py      Cenários de Listen and Repeat e de Take an Interview (M3)
app/render_quiz.py        Renderizador dos widgets de quiz/drill
app/render_srs.py         Renderizador do widget de flashcards (M6)
app/render_build.py       Renderizador do widget Build a Sentence (M4)
app/render_ctw.py         Renderizador do Complete the Words de digitar (M1)
app/render_speaking.py    Renderizador dos conjuntos de Speaking com áudio (M3)
app/render_wbox.py        Caixa de escrita com cronômetro e contador (M4)
app/render_exam.py        Blocos de simulado do M7: lê as questões e o gabarito do próprio .md
app/rebalance.py          Redistribui a letra correta no build e marca as citações "(B)"
app/videos.json           Cadastro das videoaulas (começa vazio: sem vídeo, nada aparece)
app/render_video.py       Valida o videos.json e injeta os players no topo do módulo e das Partes
app/render_errorlog.py    Renderizador do formulário de Registro de erros (M1 a M6)
app/render_weeklydash.py  Renderizador do dashboard semanal (M0)
app/app.js                Runtime: tema, abas, progresso (checkboxes + badges), quizzes
app/styles.css            Estilo (tema claro/escuro/sistema)
app/manifest.json         Manifesto da PWA (o build copia para artifact/)
app/sw.js                 Service worker da PWA; o build troca __BUILD_VERSION__ por um hash do conteúdo
app/icons/                Ícones da PWA, gerados por scripts/make_icons.py e versionados
app/module_fragments*.json  Saída do pipeline (gerado; não editar)
artifact/index.html       Site final (gerado; não editar)
legal/*.md                Termos de Uso e Política de Privacidade (fonte)
artifact/termos.html      Páginas legais (geradas pelo build.py; não editar)
artifact/privacidade.html
artifact/manifest.json, sw.js, icons/   PWA (gerados pelo build.py; não editar)
supabase/schema.sql       Backend: profiles, user_state (jsonb), entitlements, coupons, com RLS
supabase/functions/       Edge functions: create-checkout, mp-webhook, delete-account
supabase/config.toml      Config das functions (mp-webhook roda sem verificação de JWT)
supabase/schema-bank.sql  Banco de questões: tabelas items e attempts com RLS. ESCRITO, NUNCA EXECUTADO
bank/                     Banco de questões em JSON (formato, schema, validador, 228 itens migrados). Ver bank/README.md
supabase/schema-content-optional.sql   Tabelas de conteúdo — só se um dia servir do banco
supabase/content-seed-optional.json    Seed das tabelas de conteúdo (opcional)
app/supabase_config.json  Credenciais (gitignored; .example commitado). Sem ele → modo offline
scripts/serve.py          Servidor local
scripts/smoke_test.py     Suíte de checagens automáticas (rodar antes de commitar)
docs/                     Análises e notas de decisão
_archive/                 Versão pré-2026: index.html monolítico + os 10 .md antigos
_snapshots/               Cópias com timestamp antes de mudanças estruturais
```

### Regra central de conteúdo

- **Texto corrido de um módulo** → editar o `.md` em `consolidated/`.
- **Questões do diagnóstico** → `app/quiz_mod0.json`.
- **Drills de Reading/Listening** → `app/drills_data.py`.
- **Itens de Build a Sentence (M4)** → `app/build_sentence_data.py`.
- **Parágrafos de Complete the Words (M1)** → `app/ctw_data.py`.
- **Cenários de Speaking (M3)** → `app/speaking_data.py`.
- **Questões dos simulados (M7)** → no próprio `consolidated/modulo_7_simulados.md`.
  Cada bloco de múltipla escolha seguido de `**Gabarito:** 1-B · 2-C` vira
  widget sozinho. O build falha se a contagem de blocos ou itens mudar sem
  atualizar `M7_EXPECTED_*` em `build_pipeline.py`.
- **Palavras dos flashcards (M6)** → `app/vocab_kit.json`.
- **Videoaulas** → `app/videos.json` (as instruções estão no próprio
  arquivo). O build só gera a capa; o player carrega no clique. A caixa "aula
  assistida" é um `.pchk` com `data-pid` `modN-video-<id>`, guardado em
  `toefl_progress_v1` junto com as Partes, então cadastrar um vídeo aumenta
  o total do módulo e quem estava em 100% deixa de estar até assistir.
- **Banco de questões** → `bank/items/`. A pasta `bank/items/migrado/` é
  gerada das fontes acima por `bank/tools/migrate.py`: depois de mudar
  questão em qualquer uma delas, rodar o `migrate.py` de novo, senão o smoke
  test reprova. Item novo do banco vai em outra pasta de `bank/items/`.
- **Comportamento/interação** → `app/app.js` e os `app/render_*.py`.
- **Estilo** → `app/styles.css`.
- **Termos e privacidade** → `legal/*.md`. O build avisa enquanto houver campo
  `[PREENCHER: ...]` sem preencher.
- **Código de servidor** → `supabase/functions/`. Mudança ali só vale depois
  de `supabase functions deploy <nome>`. O deploy já reportou sucesso sem
  atualizar o código; conferir a versão publicada depois de cada deploy.

Os módulos M0 a M7 têm um `build_modN()` no pipeline que injeta os widgets no
fragmento; M8 e M9 usam `build_plain()`. Em M3 e M4 o lugar do widget é
marcado no `.md` com um parágrafo `%%%NOME%%%`, que o pipeline troca.

**Bloco de aprofundamento:** teoria densa que fica recolhida até o aluno
abrir. Em qualquer `.md` de `consolidated/`:

```
:::aprofundamento Título opcional
Markdown normal: parágrafos, listas, tabelas, ####.
:::
```

As duas cercas ficam sozinhas na linha, coladas na margem, fora de lista,
tabela e citação. Dentro do bloco não entra `#`, `##` nem `###` (são eles que
montam as Partes e o accordion) nem outro bloco. Marcação errada derruba o
build. O bloco não conta no progresso. O seletor "Trilha de estudo" da
sidebar (rápida: blocos fechados; completa: abertos) só aparece quando existe
ao menos um bloco no site. Hoje não existe nenhum: o exemplo usado no teste
vive só no `scripts/smoke_test.py`, que o cola numa cópia temporária do M3.

**Formato real das tarefas:** antes de criar ou mudar exercício, ler
`docs/ets-materiais-oficiais.md`. Ele descreve o molde de cada tarefa visto
nos testes práticos oficiais de 2026. O conteúdo da ETS não pode ser copiado
nem adaptado de perto: só o formato.

**Letras das alternativas:** nos dados de origem a resposta certa era quase
sempre "B". `rebalance.py` redistribui no build, e o `app.js` ainda embaralha
a ordem na tela a cada sessão (`shuffleChoices`). Por isso: citar alternativa
em explicação sempre como `(B)`, entre parênteses, que é o que as duas etapas
sabem remapear. A correção e o progresso salvo usam `data-letter`, a letra
depois do rebalanceamento do build, nunca a posição na tela. Cronômetro, gravador e
export/import ficam no shell (`build.py`) e valem para todas as abas.
- Depois de qualquer edição de fonte, rodar as duas builds e conferir
  `artifact/index.html` no navegador.

**PWA:** o site é instalável. O service worker só é registrado em https ou
em localhost, nunca em `file://`. Ele serve do cache o que está na lista
`PRECACHE` de `app/sw.js`: arquivo novo em `artifact/` que precise funcionar
offline tem que entrar nessa lista e no hash de versão do `build.py`. Build
com conteúdo igual gera a mesma versão; conteúdo novo gera versão nova e o
aluno vê "Nova versão disponível" na visita seguinte. Testando em
localhost, o site fica preso na versão em cache até clicar em Recarregar.

## Convenções

- **Nunca editar arquivos gerados** (`artifact/index.html`,
  `app/module_fragments*.json`).
- **Snapshot antes de mudança estrutural:** copiar o afetado para
  `_snapshots\<yyyyMMdd-HHmmss>-<motivo>\`. Com o Git em uso, commitar antes.
- **Verificação por contagem, não por impressão.** Ao portar um módulo, comparar
  contagem de itens origem vs. destino e declarar o número.
- Interface e explicações em **português do Brasil**; conteúdo-alvo (inglês)
  permanece em inglês.
- Sem framework, sem bundler. Dependência única: `markdown` (build-time) +
  fontes do Google (runtime).

## Formato do TOEFL iBT — 2026 (autoritativo)

Decisão travada do usuário (2026-09-02): o projeto segue o **formato vigente
desde 21 de janeiro de 2026**. O material em `_archive/content-old-format/`
descreve o formato anterior (0–120, ~2h, 4 speaking tasks) e **não** deve ser
usado como referência de conteúdo — só como matéria-prima a ser reescrita.

| Seção | Duração | Itens | Pontos brutos | Adaptativo |
|---|---|---|---|---|
| Reading | ~18–21 min + 9 min router | 50 (35 pontuados) | 35 | Sim (2 estágios) |
| Listening | ~25–29 min (router 18 + módulo 7 ou 11) | 47 (35 pontuados) | 35 | Sim (2 estágios) |
| Writing | ~23 min | 12 | 20 | Não (linear) |
| Speaking | ~8 min | 11 | 55 | Não (linear) |
| **Total** | **~1h23–1h29** | 120 | 145 | |

Correção: 108 itens por máquina + 12 por IA. Pontuação reportada em **bandas
CEFR 1–6** (com score legado 0–120 como referência). Os 145 pontos brutos não
são o score 0–120: são a soma das quatro seções antes da conversão, conferida
em `docs/ets-blueprint-2026.md`. A conferência número a número contra as
fontes da ETS (com o que ainda é ambíguo) está em
`docs/conferencia-formato-2026.md`.

Tipos de item por seção:

- **Reading:** Complete the Words · Read in Daily Life · Read an Academic Passage
- **Listening:** Listen and Choose a Response · Listen to a Conversation ·
  Listen to an Announcement · Listen to an Academic Talk
- **Writing:** Build a Sentence · Write an Email · Write for an Academic Discussion
- **Speaking:** Listen and Repeat (7 itens) · Take an Interview (4 itens)

Implicações que o conteúdo deve respeitar:

- Não há mais discurso longo estruturado no Speaking. Os templates longos de
  Speaking do Módulo 5 antigo (Independent + 3 Integrated) e o template de
  Integrated Writing estão **obsoletos** — o M5 foi reescrito como módulo de
  registro/retórica, não de templates de task.
- Writing são textos multi-frase objetivos, não redações longas.
- O que pontua: precisão instantânea, prosódia natural, controle gramatical
  automático — vindo de repetição deliberada, não de scripts decorados.
- Qualquer conteúdo gerado que contradiga esta seção está errado.

## Módulos

| ID | Módulo | Estado |
|---|---|---|
| M0 | Embarque & Diagnóstico | ✅ formato 2026, 10 questões, calculadora de score, treino por nível |
| M1 | Reading | ✅ formato 2026: 8 textos de Complete the Words de digitar (80 lacunas) + 67 itens de múltipla escolha |
| M2 | Listening | ✅ formato 2026, 4 drills |
| M3 | Speaking | ✅ formato 2026: 5 cenários de Listen and Repeat e 4 entrevistas, com áudio |
| M4 | Writing | ✅ formato 2026: 30 itens de Build a Sentence no molde da prova + 12 caixas de escrita |
| M5 | Registro & Sofisticação Retórica | ✅ reescrito para 2026 — camada transversal de elevação de banda (Atlas Linguístico em bandas CEFR + 10 marcadores + aplicação por task) |
| M6 | Vocabulário acadêmico | ✅ portado para 2026 — 100 entradas de léxico + arsenal cross-temático + kit de 50 palavras |
| M7 | Simulados progressivos | ✅ formato 2026: 19 blocos interativos (62 questões), correção só na entrega |
| M8 | Exam Day Protocol | ✅ portado — Parte 6 (seção a seção) reescrita para as 4 seções de 2026 |
| M9 | Brazilian Trap Library | ✅ portado — referências a tasks extintas atualizadas |

**Todos os 10 módulos estão ativos no build.** `consolidated/_a-portar/` foi
removido; os originais pré-2026 dos 10 módulos seguem em
`_archive/content-old-format/`.

## Navegação livre entre módulos (decisão revertida em 2026-09-20)

**Decisão anterior (até 2026-09-20, não usar como referência):** o app bloqueava
a navegação, módulo N só abria com o módulo N-1 100% concluído.

**Decisão atual:** navegação **livre** entre os 10 módulos, a qualquer momento,
em qualquer ordem — não é mais um curso sequencialmente travado. O que continua
existindo, sem mudança, é a **medição de conclusão por módulo** (checkboxes de
progresso `.pchk`, % na sidebar/jornada, selo ✓ quando 100%, e o certificado
final, que ainda exige os 10 módulos concluídos). `isUnlocked(key)` em `app.js`
foi deixada no código (sempre retorna `true` agora) só por compatibilidade com
`updateBadges()`, que ainda a chama; não reintroduzir lógica de bloqueio ali
sem pedido explícito do usuário. `showLockMessage()` e `.lock-msg`, que eram
código morto, foram removidos em 2026-10-06.

## Camadas visuais (runtime, montadas no `app.js`)

Passes de DOM na carga, antes de qualquer widget: (1) `.table-wrap` em toda
`.panel table`; (2) `.section-card` — agrupa o conteúdo de cada `<h2>` até o
próximo `<h2>` num card, estilo "unit card". Não tocam nos `.md`.

## Estado e progresso do usuário (runtime)

`localStorage`, chaves com prefixo `toefl_`.

Sincronizadas com a conta (casam com `SYNC_PREFIXES` em `app.js`):
`toefl_progress_v1` (checkboxes das Partes), `toefl_h3progress_v1` (checkboxes
das subseções), `toefl_quiz_<drillId>_v1`, `toefl_srs_kit50_v1`,
`toefl_bsq_m4build2_v1`, `toefl_ctw_<id>_v1`, `toefl_spk_<id>_v1`,
`toefl_write_<id>_v1` (textos das caixas de escrita), `toefl_exam_<id>_v1`
(simulados do M7), `toefl_scorecalc_v1`, `toefl_errlog_<módulo>_v1` (registro
de erros),
`toefl_cert_date_v1`, `toefl_streak_v1`, `toefl_dailygoal_v1`,
`toefl_weeklydash_v1`, `toefl_avatar_v1`.

Sempre locais, por aparelho: `toefl_theme_v1`, `toefl_active_tab`,
`toefl_timer_preset`, `toefl_partpos_v1` (Parte aberta em cada módulo),
`toefl_lastpos_v1` (alvo do "Continuar de onde parei"), `toefl_trilha_v1`
(trilha rápida ou completa: preferência de leitura, não progresso). `toefl_sync_at` e
`toefl_dirty` são internos do sync.

**Sincronização:** quando o Supabase está configurado e o aluno logado, as
chaves sincronizadas são empacotadas num blob e salvas em `user_state.state`.
`safeSet` marca `toefl_dirty` e agenda um push debounced. Setup:
`docs/supabase-setup.md`.

**Conta e acesso pago:** `entitlements` guarda quem pagou e só o `service_role`
escreve nela (via `mp-webhook`). "Minha conta" mostra a situação do acesso e
permite excluir a conta, o que chama a function `delete-account` e apaga em
cascata `profiles`, `user_state` e `entitlements`. O bloqueio de quem não pagou
é só uma camada visual: o conteúdo vai embutido no HTML.

Os botões Exportar/Importar na sidebar empacotam todas as chaves `toefl_*` em
JSON. Ao mudar o formato do estado, escrever migração — não descartar progresso.

## Onde estamos

Consultar `ROADMAP.md` antes de qualquer tarefa. É a memória entre sessões.
Atualizar ao concluir cada etapa.
