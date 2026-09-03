# Auditoria dos módulos prontos (M0–M4, M7) — formato 2026

Data: 2026-09-02. Fase 2 do roadmap. Todos os seis módulos que vieram do pacote
de consolidação foram lidos e conferidos contra o formato TOEFL 2026.

## Verificação do formato contra fonte externa

Os números que o material da consolidação afirma foram checados contra fontes
públicas (Study.com, Magoosh, BestMyTest, toeflpractice.io, myspeakingscore.com)
sobre a mudança do TOEFL iBT de 21 de janeiro de 2026. **Confirmado:**

- Reading e Listening adaptativos em dois estágios (router → módulo). ✓
- Pontuação em bandas CEFR 1–6 (0,5 em 0,5), **média** das 4 seções, não soma. ✓
- Score legado 0–120 reportado em paralelo até ~2028. ✓
- Duração total ~1h30. ✓
- Speaking: ~8 min, 11 itens, 2 tarefas — Listen and Repeat (7) + Take an
  Interview (4). Sem mais discurso longo. ✓
- Reading até ~50 itens, Listening até ~47, Writing até ~12, Speaking até ~11. ✓
- "Complete the Words" é tarefa de Reading (formato tipo C-test). ✓

Divergência menor não resolvível sem documento oficial da ETS: o material diz
"35 pontos brutos" para Reading e Listening com "30/35 itens pontuados" de 1 pt
cada — a soma não fecha (30 itens × 1 pt ≠ 35). A ETS não publica a tabela de
conversão bruto→banda. Tratado como aproximação pedagógica; não alterado.

**Conclusão:** o material da consolidação é confiável como base de conteúdo.

## Qualidade por módulo

| Módulo | Formato 2026 | Estrutura | Drills | Qualidade |
|---|---|---|---|---|
| M0 Embarque | ✅ | 9 partes, diagnóstico + calculadora CEFR + cronogramas | quiz de 10 | Alta |
| M1 Reading | ✅ | 4 partes (Game Rules/AI Hack/Drills/Gabarito) | 3 drills | Alta |
| M2 Listening | ✅ | 4 partes | 4 drills | Alta |
| M3 Speaking | ✅ | 4 partes | 7 drills | Alta — muito completo |
| M4 Writing | ✅ | 4 partes | 5 drills c/ gabarito | Alta |
| M7 Simulados | ✅ | 8 partes, 4 simulados progressivos | simulado 2 detalhado | Alta |

## Problemas encontrados e o que foi feito

### Corrigidos nesta sessão

1. **Mapa de módulos trocado no M0.** O corpo do M0 tratava "Módulo 3" como
   Writing e "Módulo 4" como Speaking, mas os arquivos são
   `modulo_3_speaking.md` e `modulo_4_writing.md`. Todas as ~15 referências
   cruzadas em M0 (Partes 5, 6 e 7) foram invertidas para o mapa correto:
   **M3 = Speaking, M4 = Writing.**

2. **Referências a "Módulo 5/6" em M7.** O M7 mandava "consultar frameworks do
   Módulo 5/6" para Speaking e Writing. No formato 2026 esses frameworks estão
   dentro do próprio M3 (esqueletos de resposta por função) e M4 (templates de
   e-mail e discussão). Todas as ocorrências foram reapontadas para M3/M4. A
   menção à "versão de digitação livre no Módulo 6" foi reapontada para M1.

3. **Artefatos de geração de chat.** M1, M2 e M7 terminavam com uma linha
   *"Digite \"MÓDULO N\" para gerar o conteúdo completo..."* — sobra do processo
   de geração original. Removidas. Também removido um `</content>` solto ao final
   do M1.

### Pendentes — dependem da decisão sobre o M5

4. **`ROADMAP.md` — mapa de módulos.** O M7 (Parte 1, tabela dos 4 simulados)
   diz "Após Módulos 1–5" e "Após Módulo 6" como pré-requisitos. Isso assume que
   M5 ainda existe como módulo de ensino. Reescrever quando o destino do M5
   estiver decidido (virar "Frameworks de resposta rápida" ou ser removido).

5. **Numeração dos módulos a portar.** Os arquivos em `consolidated/_a-portar/`
   (M5, M6, M8, M9 no formato antigo) fazem referência cruzada ao mapa antigo
   (M3 = Speaking, M4 = Writing — que por acaso coincide — mas também M5 =
   templates de Speaking longo, que não existe mais). Resolver durante o porte
   de cada um.

## Contagens (baseline pós-auditoria, 2026-09-02)

Fragmentos gerados: mod0=45.421, mod1=44.444, mod2=50.740, mod3=34.232,
mod4=30.599, mod7=59.798 chars. `artifact/index.html` = 285.907 bytes.
Build roda limpa; zero placeholders; zero artefatos de geração nos módulos ativos.
