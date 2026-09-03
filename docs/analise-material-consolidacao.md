# Análise — material do chat "TOEFL training material consolidation"

Origem: `Downloads/itoefl_1.zip` (idêntico a `itoefl.zip`), extraído em
`_incoming/consolidation-chat/`. Data da análise: 2026-09-02.

## O que veio no pacote

O chat de consolidação **não** produziu apenas texto — produziu uma segunda
versão do projeto inteiro, mais avançada que o `index.html` que já estava na
pasta de trabalho.

| Item | Conteúdo | Avaliação |
|---|---|---|
| `consolidated/*.md` | Módulos 0, 1, 2, 3, 4, 7 reescritos | **Formato 2026** (ver conflito abaixo) |
| `app/build_pipeline.py` | Markdown → `module_fragments_final.json` | Pipeline em Python — alinha com o ferramental daqui |
| `app/build.py` | fragments + CSS + JS → `artifact/index.html` | Build estático, sem dependências |
| `app/quiz_mod0.json` | **10 questões** de diagnóstico com gabarito comentado | Completo |
| `app/drills_data.py` | 3 drills de Reading + 4 de Listening, com passagens e explicações | Completo e interativo |
| `app/render_quiz.py` | Renderizador dos widgets de quiz (escolher→confirmar→revelar→refazer) | Reutilizável |
| `app/app.js` (208 linhas) | Tema, abas, checkboxes de progresso com badges por módulo, quizzes com persistência | Mais robusto que o `app.js` antigo |
| `app/styles.css` (205 linhas) | Tema claro/escuro/sistema | — |
| `artifact/index.html` (4.426 linhas) | Site final gerado | Produto montado |
| `supabase/schema.sql` | Tabelas de conteúdo (leitura pública) + progresso do aluno (RLS por usuário) + `auth` | **Novo:** backend real, contas, sincronização |
| `supabase/quiz_export.json` | Dados de quiz/drills prontos para popular o banco | — |

Cobertura: **módulos 0, 1, 2, 3, 4, 7**. Faltam **5 (Templates), 6 (Vocabulary),
8 (Exam Day), 9 (Brazilian Traps)** — que só existem na pasta `content/`.

## Conflito crítico: qual é o formato do TOEFL

Os dois materiais descrevem **exames diferentes**.

| | `content/*.md` (pasta de trabalho) | `_incoming/consolidation-chat/consolidated/*.md` |
|---|---|---|
| Referência | "formato pós-julho 2023" | "formato 2026" / "vigente desde 21/jan/2026" |
| Duração | ~2 h | ~1h25min |
| Pontuação | 0–120 | Bandas CEFR 1–6 (+ score legado 0–120) |
| Reading | 35 min, 2 passagens de ~10 questões | Adaptativo 2 estágios; tasks *Complete the Words*, *Read in Daily Life*, *Read an Academic Passage* |
| Listening | 36 min, conversas + palestras | Adaptativo 2 estágios; *Listen and Choose a Response*, *Listen to a Conversation/Announcement/Academic Talk* |
| Speaking | 4 tasks (1 Independent + 3 Integrated), ~17 min | 2 tasks (*Listen and Repeat*, *Take an Interview*), ~8 min, 55 pontos brutos |
| Writing | Integrated Writing + Academic Discussion | *Build a Sentence*, *Write an Email*, *Write for an Academic Discussion* |
| Templates longos | Centrais (Módulo 5) | Explicitamente desencorajados ("nenhum item pede discurso longo estruturado") |

Isto não é divergência de redação — é o exame inteiro. Se o formato 2026 estiver
correto, **o Módulo 5 (templates de Speaking longo) perde a razão de existir** e
partes de M3/M4 precisam ser refeitas.

**Ação pendente do usuário:** confirmar qual formato é o autoritativo. O material
de consolidação é mais recente e traz números específicos de 2026; a pasta
`content/` parece ser a versão anterior. `CLAUDE.md` hoje enshrines o formato
antigo e precisa ser corrigido assim que isso for decidido.

## Recomendação

Adotar o pacote de consolidação como nova linha de base, em vez de continuar do
`index.html` antigo:

1. O pipeline em Python já resolve o que seria a Fase 1–2 do plano original.
2. Os módulos 0–4 e 7 já estão construídos e no formato novo.
3. O schema Supabase transforma "progresso em localStorage" em "contas reais com
   sincronização" — um salto de produto, não só de código.

O trabalho restante vira: **portar M5, M6, M8, M9** da pasta `content/` para o
pipeline (atualizando ao formato 2026 onde necessário), montar a base Supabase e
publicar.
