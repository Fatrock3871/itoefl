# Roadmap iTOEFL

Memória entre sessões. Atualizar ao concluir cada etapa.

**Última atualização:** 2026-09-02
**Agora:** Fases 0–2 concluídas. M5 reescrito como "Registro & Sofisticação
Retórica" e integrado ao build (7 módulos ativos: M0–M5, M7).
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

## Fase 3 — Portar/reescrever os módulos que faltam

Ordem: M5 (feito) → M6 → M9 → M8.

- [x] **M5 → "Registro & Sofisticação Retórica"** — decisão do usuário
      (2026-09-02): repropósito, não remoção. `consolidated/modulo_5_registro.md`
      reaproveita o Atlas Linguístico (retiered para bandas CEFR), os 10
      marcadores de alto impacto e os exemplos contrastivos; aplica às 3 tasks
      produtivas de 2026 (Take an Interview, Write an Email, Academic Discussion).
      Registrado em `build_pipeline.py` e `build.py`. Fragmento = 24.327 chars.
- [ ] **M6 Vocabulary** — extrair o léxico de `_a-portar/modulo_6_vocabulary_ANTIGO.md`
      (~228 linhas de tabela) para `consolidated/modulo_6_vocabulary.md` +
      widget de flashcards. Registrar contagem: N palavras na origem → N no destino.
- [ ] **M9 Brazilian Traps** — falsos cognatos e substituições (format-agnostic);
      atualizar só a parte de SpeechRater/Speaking ao formato 2026. Referências
      a "templates do Módulo 5" precisam virar "Atlas Linguístico do Módulo 5".
- [ ] **M8 Exam Day** — protocolo dos 7 dias, biohacking, logística
      (quase tudo format-agnostic); reescrever "durante o exame, seção a seção"
      para as 4 seções novas. Referências a "templates do Módulo 5" idem.
- [ ] Registrar M6, M8, M9 em `app/build.py` (lista `MODS`) ao portar cada um

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

## Baseline de contagem (2026-09-02, pós-M5)

Fragmentos: mod0=45.421, mod1=44.444, mod2=50.740, mod3=34.232, mod4=30.599,
mod5=24.327, mod7=59.798 chars.
`artifact/index.html` = 310.479 bytes. 7 módulos ativos, 162 checkboxes de progresso.
Diagnóstico M0 = 10 questões. Drills = 3 (Reading) + 4 (Listening).
