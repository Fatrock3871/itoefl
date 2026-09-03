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
cd ..
python scripts\serve.py      # abre http://localhost:8000/artifact/index.html
```

`artifact/index.html` é **gerado** — CSS e JS ficam embutidos nele pelo
`build.py`. Nunca editar `artifact/index.html` à mão: a próxima build sobrescreve.
Editar sempre a fonte (`consolidated/`, `app/styles.css`, `app/app.js`,
`app/*.json`, `app/drills_data.py`) e rebuildar.

## Arquitetura

```
consolidated/*.md         Texto dos módulos — fonte da verdade do conteúdo corrido
consolidated/_a-portar/   Módulos 5, 6, 8, 9 no formato ANTIGO, aguardando porte
app/build_pipeline.py     Monta os fragmentos HTML por módulo; injeta os widgets
app/build.py              Monta artifact/index.html (nav + painéis + CSS + JS)
app/quiz_mod0.json        As 10 questões do diagnóstico (M0)
app/drills_data.py        Drills interativos de Reading (M1) e Listening (M2)
app/render_quiz.py        Renderizador dos widgets de quiz/drill
app/app.js                Runtime: tema, abas, progresso (checkboxes + badges), quizzes
app/styles.css            Estilo (tema claro/escuro/sistema)
app/module_fragments*.json  Saída do pipeline (gerado; não editar)
artifact/index.html       Site final (gerado; não editar)
supabase/schema.sql       Backend planejado: conteúdo público + progresso por aluno (RLS)
supabase/quiz_export.json Dados de quiz/drill prontos para popular o banco
scripts/serve.py          Servidor local
docs/                     Análises e notas de decisão
_archive/                 Versão pré-2026: index.html monolítico + os 10 .md antigos
_snapshots/               Cópias com timestamp antes de mudanças estruturais
```

### Regra central de conteúdo

- **Texto corrido de um módulo** → editar o `.md` em `consolidated/`.
- **Questões do diagnóstico** → `app/quiz_mod0.json`.
- **Drills de Reading/Listening** → `app/drills_data.py`.
- **Comportamento/interação** → `app/app.js` ou `app/render_quiz.py`.
- **Estilo** → `app/styles.css`.
- Depois de qualquer edição de fonte, rodar as duas builds e conferir
  `artifact/index.html` no navegador.

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
| Reading | ~18–21 min + 9 min router | 50 (30 pontuados) | 35 | Sim (2 estágios) |
| Listening | ~18 min | 47 (35 pontuados) | 35 | Sim (2 estágios) |
| Writing | ~23 min | 12 | 20 | Não (linear) |
| Speaking | ~8 min | 11 | 55 | Não (linear) |
| **Total** | **~1h23–1h29** | 120 | 120 | |

Correção: 108 itens por máquina + 12 por IA. Pontuação reportada em **bandas
CEFR 1–6** (com score legado 0–120 como referência).

Tipos de item por seção:

- **Reading:** Complete the Words · Read in Daily Life · Read an Academic Passage
- **Listening:** Listen and Choose a Response · Listen to a Conversation ·
  Listen to an Announcement · Listen to an Academic Talk
- **Writing:** Build a Sentence · Write an Email · Write for an Academic Discussion
- **Speaking:** Listen and Repeat (7 itens) · Take an Interview (4 itens)

Implicações que o conteúdo deve respeitar:

- Não há mais discurso longo estruturado no Speaking. **Templates longos de
  Speaking (o antigo Módulo 5) estão obsoletos.**
- Writing são textos multi-frase objetivos, não redações longas.
- O que pontua: precisão instantânea, prosódia natural, controle gramatical
  automático — vindo de repetição deliberada, não de scripts decorados.
- Qualquer conteúdo gerado que contradiga esta seção está errado.

## Módulos

| ID | Módulo | Estado |
|---|---|---|
| M0 | Embarque & Diagnóstico | ✅ formato 2026, 10 questões |
| M1 | Reading | ✅ formato 2026, 3 drills |
| M2 | Listening | ✅ formato 2026, 4 drills |
| M3 | Speaking | ✅ formato 2026 |
| M4 | Writing | ✅ formato 2026 |
| M5 | Templates | ⚠️ obsoleto no formato 2026 — decidir se vira "Frameworks de resposta rápida" ou sai |
| M6 | Vocabulário acadêmico | 🔴 só existe no formato antigo — portar |
| M7 | Simulados progressivos | ✅ formato 2026 |
| M8 | Exam Day Protocol | 🔴 portar (maior parte é format-agnostic) |
| M9 | Brazilian Trap Library | 🔴 portar (falsos cognatos são format-agnostic) |

## Estado e progresso do usuário (runtime)

`localStorage`, chaves com prefixo `toefl_`: `toefl_progress_v1` (checkboxes),
`toefl_theme_v1`, `toefl_active_tab`, `toefl_quiz_<drillId>_v1`. Ao mudar o
formato do estado, escrever migração — não descartar progresso salvo.

## Onde estamos

Consultar `ROADMAP.md` antes de qualquer tarefa. É a memória entre sessões.
Atualizar ao concluir cada etapa.
