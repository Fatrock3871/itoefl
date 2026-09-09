# Roadmap iTOEFL

MemÃ³ria entre sessÃµes. Atualizar ao concluir cada etapa.

**Ãšltima atualizaÃ§Ã£o:** 2026-09-09
**Agora:** Fase 7 (expansÃ£o do conteÃºdo). **M1, M2, M4, M3, M5 e M6 feitos.** PrÃ³ximo:
**M7 Simulados**. `artifact/index.html` â‰ˆ 706 KB.

---

## DecisÃµes travadas

| DecisÃ£o | Escolha | Data |
|---|---|---|
| Formato do TOEFL | **2026** (CEFR 1â€“6, adaptativo, ~1h25). O formato antigo 0â€“120 fica sÃ³ em `_archive/` | 2026-09-02 |
| Linha de base | **Pacote do chat de consolidaÃ§Ã£o** (pipeline Python + mÃ³dulos 0â€“4/7 prontos) | 2026-09-02 |
| DistribuiÃ§Ã£o | Site estÃ¡tico gerado; servido localmente para dev | 2026-09-02 |
| Fonte da verdade | `consolidated/*.md` (texto) + `app/*.json` e `drills_data.py` (widgets) | 2026-09-02 |
| Backend Supabase | Sim, mas **depois** do conteÃºdo dos 10 mÃ³dulos | 2026-09-02 |
| Ferramental | Python 3.13 + Git 2.55 + pacote `markdown` | 2026-09-02 |

---

## Fase 0 â€” FundaÃ§Ã£o âœ…

- [x] Snapshots de seguranÃ§a em `_snapshots/`
- [x] `CLAUDE.md` e `ROADMAP.md`
- [x] `scripts/serve.py` (serve `artifact/index.html`)
- [x] Git 2.55 instalado pelo usuÃ¡rio
- [x] `markdown` instalado via pip

## Fase 1 â€” Adotar o pacote de consolidaÃ§Ã£o âœ…

- [x] Material extraÃ­do de `Downloads/itoefl_1.zip`
- [x] AnÃ¡lise em `docs/analise-material-consolidacao.md`
- [x] `index.html` antigo â†’ `_archive/index-old-monolith.html`
- [x] 10 `.md` do formato antigo â†’ `_archive/content-old-format/`
- [x] `consolidated/ app/ artifact/ supabase/` promovidos para a raiz
- [x] M5, M6, M8, M9 antigos copiados para `consolidated/_a-portar/`
- [x] Build testada: `build_pipeline.py` + `build.py` geram `artifact/index.html`
- [x] `CLAUDE.md` reescrito para o formato 2026 e a nova arquitetura
- [x] `git init` + commit inicial (`a5efab0`) â€” gerados no `.gitignore`
- [x] Smoke-test: HTTP 200, 6 painÃ©is, 8 quiz-drills, 143 checkboxes, 0 placeholders
- [ ] UsuÃ¡rio abrir `artifact/index.html` no navegador e validar visualmente

## Fase 2 â€” Auditar o que jÃ¡ veio pronto (M0â€“M4, M7) âœ…

- [x] Formato 2026 verificado contra fontes pÃºblicas â€” material da consolidaÃ§Ã£o confiÃ¡vel
- [x] Lidos os 6 mÃ³dulos (`modulo_0,1,2,3,4,7`) â€” todos no formato 2026, qualidade alta
- [x] Corrigido: mapa de mÃ³dulos trocado no M0 (M3=Speaking, M4=Writing) â€” ~15 refs
- [x] Corrigido: refs a "MÃ³dulo 5/6" no M7 â†’ reapontadas para M3/M4/M1
- [x] Corrigido: artefatos "Digite MÃ“DULO N" removidos de M1/M2/M7 + `</content>` solto no M1
- [x] Rebuild limpa; relatÃ³rio em `docs/auditoria-modulos-2026.md`
- Lacunas observadas (nÃ£o bloqueiam): M3/M4 sÃ£o texto+drills em papel, sem widget
  interativo como M1/M2; M7 descreve o cronÃ´metro mas nÃ£o o implementa; a
  calculadora de score do M0 Ã© tabela de referÃªncia, nÃ£o um widget.

### PendÃªncia residual

- [ ] M7 Parte 1: "ApÃ³s MÃ³dulos 1â€“5 / MÃ³dulo 6" como prÃ©-requisito dos simulados
      â€” o "1â€“5" agora estÃ¡ coerente (M5 existe e Ã© conteÃºdo de ensino); revisar
      redaÃ§Ã£o ao portar M6.

## Fase 3 â€” Portar/reescrever os mÃ³dulos que faltam âœ…

Ordem: M5 â†’ M6 â†’ M9 â†’ M8. Todos feitos.

- [x] **M5 â†’ "Registro & SofisticaÃ§Ã£o RetÃ³rica"** â€” decisÃ£o do usuÃ¡rio
      (2026-09-02): repropÃ³sito, nÃ£o remoÃ§Ã£o. `consolidated/modulo_5_registro.md`
      reaproveita o Atlas LinguÃ­stico (retiered para bandas CEFR), os 10
      marcadores de alto impacto e os exemplos contrastivos; aplica Ã s 3 tasks
      produtivas de 2026 (Take an Interview, Write an Email, Academic Discussion).
      Registrado em `build_pipeline.py` e `build.py`. Fragmento = 24.327 chars.
- [x] **M6 Vocabulary** â€” portado para `consolidated/modulo_6_vocabulary.md`.
      Contagem verificada: 144 linhas de tabela em negrito na origem â†’ 144 no
      destino (100 entradas de lÃ©xico por Ã¡rea + 15 verbos + 10 adjetivos + 8
      collocations + tabelas de protocolo). ReferÃªncias a "Speaking Task 1" â†’
      "Take an Interview" e "Writing Task 2" â†’ "Write for an Academic Discussion";
      4 entradas duplicadas do arquivo antigo substituÃ­das por termos novos
      (incremental, acidification, redundancy). Fragmento = 67.351 chars.
      **Pendente:** widget de flashcards + SRS â€” Ã© item da Fase 4, nÃ£o bloqueia.
- [x] **M9 Brazilian Traps** â€” `consolidated/modulo_9_braziliantraps.md`.
      ConteÃºdo (falsos cognatos, preposiÃ§Ãµes, fonemas) veio quase verbatim.
      MudanÃ§as 2026: "Speaking Task 1/2/3" â†’ *Take an Interview* / *Listen and
      Repeat*; "Writing Task 1/2" â†’ *Write for an Academic Discussion*;
      "corrector humano" removido (Speaking 100% IA); "score de Delivery" â†’
      "inteligibilidade e prosÃ³dia". Fragmento = 42.877 chars.
- [x] **M8 Exam Day** â€” `consolidated/modulo_8_examday.md`. Partes 2â€“5 e 7
      (sono, nutriÃ§Ã£o, psicologia, logÃ­stica) quase intactas. Reescritos:
      Parte 1 (D-4/D-2 referenciavam os templates do M5 antigo), Parte 6 inteira
      (Reading ~27â€“30min adaptativo, Listening ~18min, Speaking ~8min Listen and
      Repeat + Take an Interview, Writing ~23min Build a Sentence + Email +
      Academic Discussion), Parte 7 (cenÃ¡rios anti-colapso), Parte 8
      ("avaliaÃ§Ã£o humana" â†’ correÃ§Ã£o por IA). Fragmento = 37.218 chars.
- [x] M5, M6, M8, M9 registrados em `build_pipeline.py` e `build.py`.
      `consolidated/_a-portar/` removido.

## Fase 4 â€” Produto âœ…

- [x] **CronÃ´metro por seÃ§Ã£o** â€” widget flutuante, presets Reading 28â€² /
      Listening 18â€² / Speaking 8â€² / Writing 23â€² / Prova 85â€², beep ao zerar,
      preset lembrado em `toefl_timer_preset`.
- [x] **Gravador de Speaking** â€” widget flutuante, `getUserMedia` +
      `MediaRecorder`, playback inline, trata permissÃ£o negada.
- [x] **Export/import de progresso** â€” botÃµes na sidebar; export baixa
      `itoefl-progresso.json` + copia p/ clipboard; import mescla e recarrega.
- [x] **Ajustes visuais** â€” "Prep oficial" â†’ "PreparaÃ§Ã£o independente" +
      disclaimer; marca de progresso sÃ³ em h2 (61 checkboxes, nÃ£o 162).
- [x] **SRS no M6** â€” flashcards Leitner sobre as 50 palavras do Kit de
      EmergÃªncia. `app/vocab_kit.json` + `app/render_srs.py` + motor em
      `app.js`. Boxes 0â€“5, intervalos 0/1/3/7/16/30 dias, estado em
      `toefl_srs_kit50_v1`. Injetado no fragmento do M6 via `build_mod6`.
- [x] **`[hidden]` global** no `styles.css` â€” necessÃ¡rio no serve local
      (a Artifact jÃ¡ injeta essa regra); corrige widgets que usam `hidden`.
- [x] **Widget de Build a Sentence (M4)** â€” 10 itens de reordenaÃ§Ã£o pura,
      clicar-para-montar, verificar â†’ frase-modelo + nota. `build_sentence_data.py`
      + `render_build.py` + motor em `app.js`, estado `toefl_bsq_m4build_v1`.
- [~] M5 (reescrita B1â†’C1) â€” fica como exercÃ­cio de texto guiado com
      referÃªncia de correÃ§Ã£o; nÃ£o se beneficia de widget (Ã© produÃ§Ã£o livre
      sem gabarito Ãºnico). Fase 4 de conteÃºdo interativo considerada completa.

## Fase 5 â€” Backend Supabase âœ…

Toda a parte de cÃ³digo foi feita. O que resta Ã© operaÃ§Ã£o (passos em
`docs/supabase-setup.md`).

- [x] **Schema simplificado** â€” `supabase/schema.sql` reescrito: `profiles` +
      `user_state` (jsonb, uma linha por usuÃ¡rio) + RLS + gatilho de perfil no
      signup. As tabelas de conteÃºdo e o seed viraram
      `supabase/schema-content-optional.sql` / `content-seed-optional.json`
      (sÃ³ se um dia servir conteÃºdo do banco).
- [x] **Login (magic link) + sync no `app.js`** â€” mÃ³dulo de auth na sidebar
      (`authBox`, oculto se nÃ£o configurado). `signInWithOtp` por e-mail,
      `onAuthStateChange`, pull no login (recarrega se a nuvem for mais nova),
      push debounced (2,5 s) a cada escrita de chave sincronizÃ¡vel.
- [x] **Merge offline** â€” `toefl_dirty` marca ediÃ§Ãµes nÃ£o enviadas; no pull,
      ediÃ§Ãµes locais ganham e o resto da nuvem Ã© mesclado.
- [x] **Fallback offline** â€” sem config ou deslogado, o app Ã© exatamente o de
      antes (localStorage puro). `build.py` tolera config ausente/BOM/invÃ¡lida.
- [x] **`app/supabase_config.example.json`** commitado; `.json` real gitignored.
- [x] **`docs/supabase-setup.md`** â€” passo a passo (criar projeto, rodar schema,
      URLs de auth, preencher config, rebuild, troubleshooting).
- [x] **UsuÃ¡rio:** projeto Supabase criado ("ITOELF", ref `itfosjcymqfzjsftvjey`,
      SÃ£o Paulo), schema rodado, `app/supabase_config.json` preenchido com a
      **publishable key** (`sb_publishable_...`), site/redirect URLs configuradas
      para `http://localhost:8000`. Verificado via API: tabelas `profiles` e
      `user_state` existem, RLS ativa, email auth habilitado.
- [x] **Login testado pelo usuÃ¡rio** (2026-09-04) â€” magic link funcionou,
      e-mail e botÃ£o "Sair" aparecem na sidebar apÃ³s o login.
- [ ] Testar sync real com 2 dispositivos/navegadores (opcional, quando quiser).

**Nota de seguranÃ§a:** durante a configuraÃ§Ã£o, uma `sb_secret_...` key e a
legacy `service_role` JWT foram coladas na conversa por engano. Orientei o
usuÃ¡rio a rotacionÃ¡-las; a `publishable key` que o app usa nÃ£o Ã© afetada por
essa rotaÃ§Ã£o. Confirmar que a rotaÃ§Ã£o foi feita antes de considerar o projeto
Supabase "limpo" para uso continuado.

## Fase 5.5 â€” Redesenho + progressÃ£o sequencial âœ… (2026-09-07)

- [x] Pesquisa de referÃªncia (Khan Academy, Busuu, Babbel, Memrise via
      screenshots headless).
- [x] ProgressÃ£o sequencial: mÃ³dulo N destrava com N-1 a 100%. Selo por mÃ³dulo
      (nÃºmero / âœ“ / ðŸ”’), aviso ao clicar em bloqueado, contador "N de 10".
- [x] ConteÃºdo em `.section-card` por seÃ§Ã£o (padrÃ£o "unit card").
- [x] BotÃµes CTA em pill; H2 com borda de destaque.
- [x] `.side` com `min-width:0` (proteÃ§Ã£o grid). Confirmado sem overflow
      horizontal em 360â€“768 px.
- Documentado em `CLAUDE.md` (seÃ§Ãµes "ProgressÃ£o sequencial" e "Camadas visuais").

## Fase 7 â€” ExpansÃ£o do conteÃºdo (decisÃ£o do usuÃ¡rio, 2026-09-07)

O currÃ­culo (~50k palavras) Ã© um bom esqueleto de estratÃ©gia, mas fino em
prÃ¡tica, ensino de lÃ­ngua e exemplos resolvidos. Plano: expandir **mÃ³dulo por
mÃ³dulo, um por sessÃ£o**, dobrando o tamanho. Ordem por impacto:
M1 â†’ M2 â†’ M4 + M3 â†’ M6 â†’ M9 â†’ M0/M5/M7/M8.

- [x] **VerificaÃ§Ã£o do formato contra a ETS** â€” baixado o blueprint oficial
      2026. Nosso nÃºcleo confere. CorreÃ§Ãµes pontuais aplicadas (pontos brutos
      145 nÃ£o 120; itens pontuados). `docs/ets-blueprint-2026.md`.
- [x] **M1 Reading** (2026-09-08) â€” 5,3k â†’ 11,5k palavras. Adicionado:
      Parte 1.4 (os 9 tipos de pergunta), Parte 3 (LaboratÃ³rio de LÃ­ngua â€”
      gramÃ¡tica + 50 collocations + conectores + morfologia), Parte 4 (exemplo
      resolvido narrado), 13 drills graduados (era 3) cobrindo todos os
      formatos e tipos de questÃ£o, gabarito dos 67 itens, Parte 7 (protocolo
      de erros R1â€“R6). M1 agora usa `build_plain`. `commit 0bb2738`.
- [x] **M2 Listening** (2026-09-09) â€” 5,7k â†’ 10,5k palavras. Parte 1.4 (9 tipos
      de pergunta), Parte 3 (**LaboratÃ³rio de Escuta** â€” reduÃ§Ãµes, linking,
      contraÃ§Ãµes, nÃºmeros, 40 termos de campus, 30 idioms, linguagem funcional,
      sÃ­mbolos de anotaÃ§Ã£o), Parte 4 (exemplo narrado), 21 drills graduados
      (era 4), gabarito dos 51 itens, Parte 7 (protocolo L1â€“L6). `build_plain`.
- [x] **M4 Writing** (2026-09-09) â€” 3,9k â†’ 8,8k palavras. Parte 1.4 (como o
      e-rater corrige), Parte 3 (**LaboratÃ³rio de ProduÃ§Ã£o Escrita** â€” tipos de
      frase, run-on/comma splice, tempos, word forms, pontuaÃ§Ã£o, registro +
      as 11 famÃ­lias de estrutura do Build a Sentence com 22 mini-drills),
      Parte 4 (Email + Discussion escritos ao vivo), 30 Build a Sentence
      graduados + 6 prompts de Email + 6 de Discussion, respostas-modelo por
      banda (3/5/6), Parte 7 (W1â€“W6 + revisÃ£o dos 60â€“90 s). `build_plain`.
- [x] **M3 Speaking** (2026-09-09) â€” 4,3k â†’ 7,2k palavras. Parte 1.4 (blueprint:
      ~45s, sem preparo, cenÃ¡rio texto+Ã¡udio), Parte 2.1 (features do SpeechRater),
      Parte 3 (**LaboratÃ³rio de Fala** â€” 12 fonemas crÃ­ticos com IPA, -ED, word
      stress, ritmo/tapping, entonaÃ§Ã£o, weak forms, gestÃ£o de hesitaÃ§Ã£o, 40
      frases, rubrica de auto-gravaÃ§Ã£o /12), Parte 4 (Listen and Repeat + Take an
      Interview ao vivo), Grupo A (5 sets Listen and Repeat A1â†’C2) + Grupo B (48
      perguntas de Take an Interview por 6 funÃ§Ãµes + B7/B8) + Grupo C (shadowing),
      Parte 6 (gabarito de funÃ§Ã£o + respostas-modelo banda 3/5/6), Parte 7
      (S1â€“S6). TambÃ©m: correÃ§Ã£o de renderizaÃ§Ã£o de listas markdown em M2 e M3.
      `build_plain`. `commit 51876d0`.
- [x] **M5 Registro & SofisticaÃ§Ã£o** (2026-09-09) â€” 2,9k â†’ ~10k palavras.
      Parte 1.4 (a rubrica CEFR em nÃºmeros) + 1.5 (as 3 "vozes"), Parte 2.1
      (bancos de frases por funÃ§Ã£o retÃ³rica), os 10 marcadores expandidos
      (funÃ§Ã£o + antes/depois + uso indevido + quando nÃ£o usar), Parte 4
      (**LaboratÃ³rio de Registro** â€” nominalizaÃ§Ã£o, hedging calibrado, densidade
      por combinaÃ§Ã£o de oraÃ§Ãµes, cleft/fronting/inversÃ£o, coesÃ£o alÃ©m de
      conectores, escala de formalidade lexical, colocaÃ§Ãµes acadÃªmicas), Parte 5
      com exemplos extras por funÃ§Ã£o, Parte 6 (elevaÃ§Ã£o narrada frase a frase),
      Parte 7 (6 â†’ 14 drills, todos com gabarito), Parte 9 (protocolo RG1â€“RG6).
      `build_plain`. `commit 6c6e084`.
- [x] **M6 VocabulÃ¡rio** (2026-09-09) â€” ~5k â†’ ~9k palavras. As 120 palavras de
      referÃªncia (SeÃ§Ãµes 2â€“3) ficaram intactas; a lacuna era a ausÃªncia de
      exercÃ­cios. SeÃ§Ã£o 4 expandida (27 verbos / 19 adjetivos / 21 collocations),
      SeÃ§Ã£o 5 nova (**famÃ­lias de palavras + morfologia** para Complete the
      Words), SeÃ§Ã£o 6 nova (**nuance e precisÃ£o** â€” pares confundidos + falsos
      cognatos acadÃªmicos + verbos de reporte com postura), SeÃ§Ã£o 7 nova
      (**vocabulÃ¡rio funcional para Listening** â€” sinalizadores de palestra +
      phrasal verbs de campus), SeÃ§Ã£o 9 nova (**9 drills com gabarito**), SeÃ§Ã£o
      11 nova (protocolo V1â€“V6). SeÃ§Ãµes renumeradas (Kit 5â†’8, ativaÃ§Ã£o 6â†’10,
      checklist 7â†’12). Widget SRS reancorado para `<h2>SEÃ‡ÃƒO 9`. `commit ` a preencher.
- [ ] **M7 Simulados progressivos** â€” prÃ³ximo.
- [ ] M8, M9 â€” idem, um por vez.

## Fase 6 â€” PublicaÃ§Ã£o

- [ ] Publicar (GitHub Pages â€” o app Ã© estÃ¡tico e autocontido)
- [ ] Trocar Site URL / Redirect URLs do Supabase para o endereÃ§o publicado
- [ ] Testar login e sync no endereÃ§o final, inclusive no celular

---

## PendÃªncias

- **Verificar o formato 2026 contra fonte oficial da ETS.** O conteÃºdo assume os
  nÃºmeros do material de consolidaÃ§Ã£o (50 itens Reading, Speaking de 8 min, etc.).
  Vale uma checagem no site oficial antes de finalizar M0.
- **`git init` ainda nÃ£o feito** nesta sessÃ£o â€” prÃ³ximo passo.
- **`_archive/` e `_snapshots/`** devem entrar no `.gitignore`? Decidir no commit
  inicial. (SugestÃ£o: versionar `_archive/` uma vez, ignorar `_snapshots/`.)

## Baseline de contagem (2026-09-03, 10 mÃ³dulos)

Fragmentos: mod0=45.421, mod1=44.444, mod2=50.740, mod3=34.232, mod4=30.599,
mod5=24.327, mod6=67.351, mod7=59.798, mod8=37.218, mod9=42.877 chars.
`artifact/index.html` = 466.9 KB. **10 mÃ³dulos ativos (M0â€“M9)**, 121 tabelas,
0 placeholders. DiagnÃ³stico M0 = 10 questÃµes. Drills interativos = 3 (Reading)
+ 4 (Listening). M3/M4/M5/M6/M8/M9 sÃ£o texto + drills em papel (sem widget).

## ObservaÃ§Ãµes visuais (2026-09-02, screenshots headless)

- Look editorial: Fraunces (tÃ­tulos) + Inter (corpo) + IBM Plex Mono (rÃ³tulos);
  paleta creme/Ã¢mbar no claro, quase-preto no escuro. Limpo e legÃ­vel.
- Widgets de quiz/drill funcionam bem (card de passagem, contador, A/B/C/D,
  confirmarâ†’revelarâ†’refazer).
- **A ajustar:** rÃ³tulo "Prep oficial" na sidebar (soa como afiliaÃ§Ã£o ETS â€”
  trocar por "PreparaÃ§Ã£o independente" antes de publicar); 1 checkbox de
  progresso por h2 E h3 Ã© excessivo (sÃ³ h2 deveria contar); diagramas ASCII
  em bloco mono sÃ£o funcionais mas plainos.
- Publicar como Artifact foi **bloqueado pelo classificador** (marca "TOEFL" +
  "Prep oficial"). Preview local: `python scripts\serve.py`.
