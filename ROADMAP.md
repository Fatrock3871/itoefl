# Roadmap iTOEFL

Memória entre sessões. Atualizar ao concluir cada etapa.

**Última atualização:** 2026-09-02
**Agora:** Fundação + reestruturação concluídas. Build roda ponta a ponta.
Próximo alvo: portar M6 (Vocabulary) para o pipeline no formato 2026.

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
- [ ] `git init` + commit inicial ← **em andamento**
- [ ] Abrir `artifact/index.html` no navegador e validar visualmente

## Fase 2 — Auditar o que já veio pronto (M0–M4, M7)

- [ ] Ler cada `consolidated/*.md` e conferir contra o formato 2026 do `CLAUDE.md`
- [ ] Conferir os 7 drills (3 Reading + 4 Listening) — respostas e explicações
- [ ] Conferir a calculadora de score do M0 (bandas CEFR)
- [ ] Listar lacunas: M3/M4 têm drills interativos? M7 tem cronômetro?

## Fase 3 — Portar os 4 módulos que faltam

Ordem: M6 → M9 → M8 → M5.

- [ ] **M6 Vocabulary** — extrair o léxico de `_a-portar/modulo_6_vocabulary_ANTIGO.md`
      (~228 linhas de tabela) para `consolidated/modulo_6_vocabulary.md` +
      widget de flashcards. Registrar contagem: N palavras na origem → N no destino.
- [ ] **M9 Brazilian Traps** — falsos cognatos e substituições (format-agnostic);
      atualizar só a parte de SpeechRater/Speaking ao formato 2026.
- [ ] **M8 Exam Day** — protocolo dos 7 dias, biohacking, logística
      (quase tudo format-agnostic); reescrever "durante o exame, seção a seção"
      para as 4 seções novas.
- [ ] **M5 Templates** — decidir: transformar em "Frameworks de resposta rápida"
      para *Take an Interview* / *Write an Email* / *Academic Discussion*, ou
      remover. Não portar templates de Speaking longo.
- [ ] Registrar os 4 módulos novos em `app/build.py` (lista `MODS`)

## Fase 4 — Produto

- [ ] Cronômetro por seção no formato 2026 (Reading/Listening adaptativos)
- [ ] Widgets de drill para M3/M4 se ainda não houver
- [ ] Revisão espaçada (SRS) no M6
- [ ] Gravador de Speaking para *Listen and Repeat* / *Take an Interview* (`MediaRecorder`)
- [ ] Export/import do progresso em JSON

## Fase 5 — Backend Supabase

- [ ] Usuário cria projeto Supabase e passa URL + anon key
- [ ] Aplicar `supabase/schema.sql`
- [ ] Popular tabelas de conteúdo com `quiz_export.json` + os módulos
- [ ] Login (magic link) no `app.js`; migrar progresso de localStorage → banco
- [ ] Fallback para localStorage quando deslogado

## Fase 6 — Publicação

- [ ] Testar em tela de celular
- [ ] Publicar (GitHub Pages ou Artifact)

---

## Pendências

- **Verificar o formato 2026 contra fonte oficial da ETS.** O conteúdo assume os
  números do material de consolidação (50 itens Reading, Speaking de 8 min, etc.).
  Vale uma checagem no site oficial antes de finalizar M0.
- **`git init` ainda não feito** nesta sessão — próximo passo.
- **`_archive/` e `_snapshots/`** devem entrar no `.gitignore`? Decidir no commit
  inicial. (Sugestão: versionar `_archive/` uma vez, ignorar `_snapshots/`.)

## Baseline de contagem (2026-09-02, pós-build)

Fragmentos gerados: mod0=45k, mod1=45k, mod2=51k, mod3=34k, mod4=31k, mod7=60k chars.
`artifact/index.html` = 286.657 bytes.
Diagnóstico M0 = 10 questões. Drills = 3 (Reading) + 4 (Listening).
