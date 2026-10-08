# Banco de questões (v1)

Fonte da verdade do banco de questões do iTOEFL, em arquivos JSON versionados
no Git e validados por script. Segue a seção 5 de `docs/roadmap-expansao.md`:
a fonte é arquivo, o resto é gerado. As tabelas `items` e `attempts` estão
escritas em `supabase/schema-bank.sql`, que ainda não foi executado em banco
nenhum: rodar SQL e publicar os itens são passos posteriores, que precisam de
autorização do dono. O script de publicação ainda não existe.

```
bank/
  README.md                 este arquivo
  schema/item.schema.json   JSON Schema de um item
  items/                    os itens: cada .json é uma lista de itens
    migrado/                gerado por tools/migrate.py a partir do site (não editar à mão)
  tools/
    validate.py             valida todos os itens e imprime o resumo
    migrate.py              gera items/migrado/ a partir das fontes atuais
    test_bank.py            testes do validador e da migração
```

## Comandos

```bash
python bank/tools/migrate.py               # regenera items/migrado/ e mostra origem vs. destino
python bank/tools/validate.py              # valida bank/items; sai com 1 se houver erro
python -m unittest bank/tools/test_bank.py # testes
```

O `scripts/smoke_test.py` roda o validador e confere que `items/migrado/`
está em dia com as fontes: item quebrado, ou fonte editada sem rodar o
`migrate.py` de novo, reprova o smoke test.

Só biblioteca padrão. O `migrate.py` importa `app/render_exam.py`, que usa o
pacote `markdown` (a mesma dependência do build).

## Formato do item

Cada arquivo em `items/` é uma lista JSON de objetos como este:

```json
{
  "id": "mod1-b2.b2.2",
  "section": "reading",
  "task_type": "Read in Daily Life",
  "exam_format": true,
  "format": "mcq",
  "skill": null,
  "cefr_min": "A2",
  "cefr_max": "B1",
  "stimulus": {"kind": "text", "format": "html", "title": "Drill B2 · Cardápio · alvo: 3 min",
               "content": "<p>...</p>", "audio_ref": null},
  "group": "mod1-b2",
  "prompt": "A customer orders a Classic Club with fries at 11:45 a.m. Before any discount, the price is:",
  "text_format": "html",
  "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "answer": "B",
  "explanation": "...",
  "hint": null,
  "trap_codes": [],
  "tags": [],
  "status": "rascunho",
  "source": {"kind": "migrado", "file": "app/drills_data.py",
             "ref": "MOD1_ACTION_DRILLS_B:mod1-b2#B2.2", "live_on_site": true,
             "answer_letter": "origem", "build_map": {"A": "A", "B": "C", "C": "D", "D": "B"}}
}
```

| Campo | Conteúdo |
|---|---|
| `id` | Estável, minúsculo, `[a-z0-9]` com `-` e `.`. Nunca muda depois de publicado, porque `attempts` aponta para ele. Itens migrados herdam o id do widget do site: id do drill + número do item na fonte (`mod2-c1.c1.2`, `mod1-a3.4`), bloco do simulado + número (`mod7-b6.3`). A repetição em `mod2-c1.c1.2` é porque a fonte já numera o item como `C1.2`. |
| `section` | `reading`, `listening`, `writing`, `speaking` ou `general` (fora das quatro seções: o diagnóstico de gramática e vocabulário do M0). |
| `task_type` | Um dos tipos do formato 2026: Complete the Words, Read in Daily Life, Read an Academic Passage, Listen and Choose a Response, Listen to a Conversation, Listen to an Announcement, Listen to an Academic Talk, Build a Sentence, Write an Email, Write for an Academic Discussion, Listen and Repeat, Take an Interview. Mais `Grammar and Vocabulary`, só na seção `general`. O validador confere que o tipo pertence à seção. |
| `exam_format` | `true` se o item reproduz o formato da tarefa na prova. `false` para treino de base: os Complete the Words de múltipla escolha (na prova é digitação) e o diagnóstico. |
| `format` | Como o aluno responde: `mcq`, `multi_select`, `fill_words`, `build_sentence`. Define a forma de `options` e `answer` (tabela abaixo). |
| `select_count` | Só em `multi_select`: quantas alternativas marcar. |
| `skill` | Habilidade ou tipo de pergunta, quando a fonte declara (Factual Information, Inference, Vocabulary in Context...). No diagnóstico, o tópico (verb tense, conectivos...). |
| `cefr_min`, `cefr_max` | Faixa CEFR (A1 a C2) ou os dois `null` quando a fonte não declara. `C1+` na fonte vira C1 a C2. |
| `stimulus` | O que o aluno lê ou ouve antes da pergunta, ou `null`. `kind`: `text` ou `audio` (em `audio`, `content` é a transcrição). `format`: `plain`, `html` ou `markdown`. `audio_ref`: caminho no storage quando houver áudio gravado; hoje sempre `null`, o site usa a voz do navegador. |
| `group` | Itens que dividem o mesmo estímulo (o drill, o bloco do simulado). Opcional. O estímulo vai repetido em cada item, para cada linha da tabela `items` se bastar sozinha. |
| `prompt` | O enunciado, em inglês. Em `build_sentence`, a resposta com os espaços numerados `{1} {2}` no lugar dos blocos e o texto fixo já impresso. |
| `text_format` | Formato de `prompt`, `options`, `explanation` e `hint`: `plain`, `html` ou `markdown`. |
| `options`, `answer` | Ver tabela abaixo. |
| `explanation` | Em português do Brasil. Cita alternativas como `(B)`, entre parênteses, sempre na letra de origem. Pode ficar vazia quando a fonte não tem (o validador avisa, não reprova). |
| `hint` | Nota mostrada junto da pergunta, ou `null`. |
| `trap_codes` | Códigos de armadilha do curso: R1 a R6, L1 a L6, W1 a W6, S1 a S6. Vazio nos migrados: as fontes não marcam. |
| `tags` | Etiquetas livres (`diagnostico`, `simulado-2`, `sobra-um-bloco`). |
| `status` | `rascunho`, `revisado` ou `publicado`. |
| `source` | De onde o item veio. `kind`: `migrado` ou `original`. `file` e `ref`: onde está na fonte. `live_on_site`: aparece hoje no `artifact/index.html`. `answer_letter`: sempre `origem` (ver abaixo). `build_map`: letra de origem para letra mostrada pelo build, ou `null`. |

### `options` e `answer` por formato

| `format` | `options` | `answer` |
|---|---|---|
| `mcq` | objeto letra → texto (`A` a `D`, às vezes só `A` a `C`) | uma letra, que existe em `options` |
| `multi_select` | objeto letra → texto | lista de letras, todas em `options`, sem repetir, com `select_count` elementos |
| `fill_words` | `null` | as palavras completas, na ordem das lacunas `[[palavra]]` do `stimulus.content` |
| `build_sentence` | lista dos blocos que aparecem para o aluno (resposta + bloco que sobra), em ordem alfabética para não entregar a resposta | os blocos na ordem certa, um por espaço `{n}` do `prompt` |

No `fill_words` a marcação é a do `app/ctw_data.py`: `[[palavra]]` é uma
lacuna; o aluno vê a primeira metade da palavra (arredondada para baixo) e
digita o resto.

## Letras das alternativas: guardamos a de origem

Nas fontes a resposta certa é quase sempre a mesma letra (nos itens de
múltipla escolha migrados: B em 116 de 189). O `app/rebalance.py` redistribui
as letras na hora do build, de forma determinística, e o `app.js` ainda
embaralha a ordem na tela.

Decisão desta versão: **o banco guarda a letra de origem**, igual à fonte, e
não aplica a redistribuição. Motivos: o item continua batendo linha a linha
com a fonte (fácil de conferir e de regenerar), e as explicações continuam
corretas sem remapear `(B)`. Para não perder a ligação com o site,
`source.build_map` registra para onde o build leva cada letra, calculado
chamando o próprio `rebalance.py` com a mesma chave que o build usa. Uma
resposta gravada pelo site (`data-letter`, a letra depois do build) se
converte para a letra do banco invertendo esse mapa. `build_map` é `null`
quando o build não troca as letras: múltipla seleção e questões de inserção
com `[■A]`.

Consequência para quem for servir o banco: **a ordem das alternativas precisa
ser embaralhada na hora de mostrar**, como o `app.js` já faz, ou o vício de
letra volta. Itens novos, escritos direto no banco, devem nascer com a letra
certa distribuída entre A, B, C e D.

## Regras

1. `id` único em todo o banco e estável. Não reaproveitar id de item apagado.
2. A resposta existe entre as opções (ou bate com as lacunas, em `fill_words`).
3. `task_type` pertence à `section`.
4. `cefr_min` ≤ `cefr_max`, ou os dois `null`.
5. Explicação em português do Brasil; conteúdo-alvo em inglês. Sem travessão
   como pausa nos textos novos.
6. Conteúdo original. Nada copiado nem adaptado de perto de material da ETS:
   só o formato (ver `docs/ets-materiais-oficiais.md`).
7. Item novo nasce `rascunho`. Passa a `revisado` depois da revisão por um
   segundo agente sem ver o gabarito e da amostra humana (roadmap, seção C2).
   Só `publicado` vai para o aluno.
8. Rodar `validate.py` antes de commitar. Erro reprova; aviso não.

Itens novos vão em arquivos próprios dentro de `items/` (por exemplo
`items/lote-001/reading-read-in-daily-life.json`), nunca em `items/migrado/`,
que o `migrate.py` reescreve.

## Itens migrados (v1)

`items/migrado/` é uma cópia gerada das fontes que o site usa hoje. Enquanto o
site continuar lendo de `app/` e `consolidated/`, **aquelas fontes são a
verdade**: corrija lá e rode `migrate.py` de novo. Todos entram como
`rascunho`, porque nenhum passou pela revisão da seção C2 do roadmap, mesmo
estando no ar no site.

Contagem conferida pelo `migrate.py` (ele falha se origem e destino
divergirem):

| Fonte | Origem | Destino |
|---|---:|---:|
| `app/quiz_mod0.json` | 10 | 10 |
| `app/drills_data.py`, Action Drills M1 (67) e M2 (51) | 118 | 118 |
| `app/ctw_data.py`, parágrafos (80 lacunas) | 8 | 8 |
| `app/build_sentence_data.py` | 30 | 30 |
| `consolidated/modulo_7_simulados.md`, 19 blocos | 62 | 62 |
| **Total** | **228** | **228** |

Os "128 itens atuais" do roadmap são os 10 do diagnóstico mais os 118 dos
Action Drills. Somando os outros tipos que já existem no site, são 228 itens
(190 de múltipla escolha, 8 parágrafos de Complete the Words e 30 Build a
Sentence).

Ajustes feitos na migração, todos no `migrate.py`:

- **Listen and Choose a Response dos drills do M2:** na fonte, a fala vinha no
  `prompt`. No banco ela vira `stimulus` de áudio e o `prompt` fica "Choose the
  best response.", como na prova.
- **Simulados do M7:** os itens são lidos pelo mesmo `convert_exam_blocks` do
  build, então a contagem é a mesma que o build confere
  (`M7_EXPECTED_ITEMS`). O tipo de tarefa vem do título `####` do bloco; o
  estímulo é o texto entre o título (ou o gabarito anterior) e a primeira
  questão; a `*(nota: ...)*` ao lado das alternativas vira `hint`. Os itens do
  M7 não declaram nível CEFR e muitos não têm explicação: o validador avisa.
- **Complete the Words de múltipla escolha** (Action Drills A do M1 e Bloco A
  do Simulado 2) entram com `exam_format: false`.

### Fora da migração

- `MOD1_DRILLS` e `MOD2_DRILLS` em `app/drills_data.py` (35 itens): são
  importados mas não renderizados pelo `build_pipeline.py`, repetem em parte os
  Action Drills (os 8 de `mod1-d1` são idênticos aos de `mod1-a3`) e reusam os
  ids `mod2-d1` a `mod2-d3`. Decisão do dono: apagar da fonte ou revisar e
  migrar como itens novos.
- Itens 11 e 12 do Bloco A do Simulado 2: digitação livre, sem alternativas e
  fora do widget. Pequenos demais para virar `fill_words` sozinhos.
- Writing de produção (Write an Email, Academic Discussion) e Speaking: são
  enunciados sem gabarito; entram no banco quando houver correção (Ondas 3 e 5).
