# Roadmap iTOEFL

Memória entre sessões. Atualizar ao concluir cada etapa.

**Última atualização:** 2026-09-03
**Agora:** Fases 3 e boa parte da 4 concluídas. Os 10 módulos no formato 2026;
cronômetro de seção, gravador de Speaking e export/import de progresso no ar.
`artifact/index.html` ≈ 450 KB. Próximo: widgets de drill (M4/M5) + SRS no M6,
ou Fase 5 (Supabase).

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

## Fase 4 — Produto

- [x] **Cronômetro por seção** — widget flutuante, presets Reading 28′ /
      Listening 18′ / Speaking 8′ / Writing 23′ / Prova 85′, beep ao zerar,
      preset lembrado em `toefl_timer_preset`.
- [x] **Gravador de Speaking** — widget flutuante, `getUserMedia` +
      `MediaRecorder`, playback inline, trata permissão negada.
- [x] **Export/import de progresso** — botões na sidebar; export baixa
      `itoefl-progresso.json` + copia p/ clipboard; import mescla e recarrega.
- [x] **Ajustes visuais** — "Prep oficial" → "Preparação independente" +
      disclaimer; marca de progresso só em h2 (61 checkboxes, não 162).
- [ ] Widgets de drill interativos para M4 (*Build a Sentence* — reordenar
      fragmentos) e M5 (reescrita B1→C1). M3 usa o gravador; M6 abaixo.
- [ ] Revisão espaçada (SRS) no M6 — widget de flashcards sobre as 50 palavras
      do Kit de Emergência (`toefl_srs_*`).

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
