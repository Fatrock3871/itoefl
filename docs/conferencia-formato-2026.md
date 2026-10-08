# Conferência dos números do formato 2026 contra a ETS

**Feita em:** 2026-10-07
**Escopo:** todo número de formato da prova que o site ensina (tempos, itens,
pontos, escala, ordem das seções, pausa), conferido contra documento oficial
da ETS. Complementa `docs/ets-blueprint-2026.md` (o resumo do blueprint) e
`docs/ets-materiais-oficiais.md` (o formato de cada tarefa).

**Regra seguida:** só foi corrigido o que um documento da ETS afirma de forma
direta. O que é ambíguo ou não é publicado ficou como estava e está listado na
seção 3. As contagens de questões do M7 não foram tocadas (o build continua
conferindo 19 blocos e 62 itens).

## 1. Fontes

Todas baixadas e lidas em 2026-10-07. Os três PDFs foram convertidos em texto
e conferidos por busca, não por resumo de terceiros.

| Sigla | Documento | URL |
|---|---|---|
| SPEC | *TOEFL iBT Test: 2026 Update. Test Blueprint and Specifications Document* (PDF, 18 páginas) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-test-specifications-2026.pdf |
| OVER | *Updated TOEFL iBT Test Overview* (PDF, 28 páginas) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-test-overview.pdf |
| BULL | *TOEFL iBT Information Bulletin 2026-2027*, em vigor de julho de 2026 a junho de 2027 (PDF, 17 páginas) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-bulletin.pdf |
| SCALE | *TOEFL Score Scale Update: A Guide for Institutions* (página) | https://www.ets.org/toefl/institutions/ibt/score-scale-update.html |
| SCORES | *Understanding Your TOEFL iBT Scores* (página) | https://www.ets.org/toefl/test-takers/ibt/scores/understand-scores.html |

O SPEC avisa que as especificações podem ter pequenas revisões. Refazer esta
conferência quando a ETS publicar versão nova de qualquer um dos cinco.

## 2. Número a número

Situação: **confere** (o site já estava certo), **corrigido** (estava errado
e foi arrumado nesta data), **em aberto** (ver seção 3).

### Estrutura e tempo

| Item | O que a ETS diz | Fonte | Situação |
|---|---|---|---|
| Ordem das seções | Reading, depois Listening, Writing e Speaking, para todos | OVER p. 4 | **corrigido**: M7 e M8 diziam que Writing e Speaking podiam trocar de ordem conforme o centro |
| Pausa | "There are no scheduled breaks in the TOEFL iBT test." Na Home Edition, "Unscheduled breaks are not allowed." | BULL p. 10 | **corrigido**: M7 e M8 ensinavam uma pausa oficial de 10 minutos depois do Listening, com protocolo de intervalo e lanche |
| Reading, itens | 50 (30 de "process academic written texts for meaning and form" + 20 de "read and comprehend information") | SPEC p. 2 | confere |
| Reading, pontos brutos | 35, com no máximo 1 ponto por item pontuado | SPEC p. 2 e p. 10 | confere |
| Reading, tempo total | 27 a 30 minutos pela tabela (18 a 21 + 9); "approx. base time" de 30 minutos | SPEC p. 2, OVER p. 4 | confere |
| Reading, divisão router e módulo | A tabela põe "18 min – 21 min" na coluna Router e "9 min" na coluna do módulo | SPEC p. 2 e p. 4 | **em aberto** |
| Listening, itens | 47 (25 a 29 de diálogo + 18 a 22 de monólogo) | SPEC p. 2 | confere |
| Listening, pontos brutos | 35, com no máximo 1 ponto por item pontuado | SPEC p. 2 e p. 13 | confere |
| Listening, tempo | Router 18 min + módulo inferior 7 min ou superior 11 min, ou seja, 25 a 29 minutos; "approx. base time" de 29 minutos | SPEC p. 2, OVER p. 4 | **corrigido**: o site dizia cerca de 18 minutos no total, com router de 7 |
| Writing | 12 itens (10 + 2), 20 pontos brutos, 23 minutos | SPEC p. 2, OVER p. 4 | confere |
| Write an Email | 7 minutos | OVER p. 14 | confere |
| Write for an Academic Discussion | 10 minutos | OVER p. 15 | confere |
| Speaking | 11 itens, 55 pontos brutos (até 5 por item), 8 minutos | SPEC p. 2 e p. 18 | confere |
| Listen and Repeat, tempo de resposta | No máximo de 8 a 12 segundos por frase | OVER p. 17 | **corrigido**: o M3 não trazia o número |
| Take an Interview, tempo de resposta | 45 segundos por pergunta, 4 perguntas | OVER p. 19 | **corrigido**: o M3 tratava os 45 s como estimativa não oficial |
| Total de itens | 120, sendo 108 corrigidos por máquina e 12 por IA | SPEC p. 2 | confere |
| Total de pontos brutos | 145 | SPEC p. 2 | confere |
| Duração da prova | Mínimo 1 h 23 min, máximo 1 h 29 min | SPEC p. 2 | confere |
| Adaptatividade | Reading e Listening em dois estágios; Writing e Speaking lineares | SPEC p. 3, OVER p. 3 | confere |

Conferência cruzada do tempo: 27 + 25 + 23 + 8 = 83 minutos, que é o mínimo
de 1 h 23 min da própria ETS. Com Listening de 18 minutos a soma daria 76, o
que confirma que o número antigo do site estava errado.

### Escala e nota

| Item | O que a ETS diz | Fonte | Situação |
|---|---|---|---|
| Escala | 1 a 6, de meio em meio ponto, desde 21 de janeiro de 2026 | SCORES | confere |
| Nota geral | Média das quatro seções, arredondada para a meia banda mais próxima (5,25 vira 5,5) | SCORES | confere |
| Bandas e CEFR | 6 = C2; 5 e 5,5 = C1; 4 e 4,5 = B2; 3 e 3,5 = B1; 2 e 2,5 = A2; 1 e 1,5 = A1 | OVER p. 21, SCALE | confere |
| Concordância com o 0 a 120 | 6 = 114+; 5,5 = 107+; 5 = 95+; 4,5 = 86+; 4 = 72+; 3,5 = 58+; 3 = 44+; 2,5 = 34+; 2 = 24+; 1,5 = 12+; 1 = 0+ | OVER p. 22 (Tabela 3), SCALE | **corrigido**: o M0 dizia que a ETS não publicava a tabela e usava faixas próprias (por exemplo B2 = 59 a 86, quando o oficial é 72 a 94) |
| O 0 a 120 no boletim | Um número só, o ponto médio da faixa equivalente, por dois anos a partir de janeiro de 2026 | SCALE, SCORES | confere ("até ~2028") |
| Validade e prazo | Notas valem 2 anos; saem em 3 dias | SCORES, OVER p. 3 | confere |

Faixas por nível CEFR que resultam da Tabela 3, usadas agora no M0: A1 0 a 23,
A2 24 a 43, B1 44 a 71, B2 72 a 94, C1 95 a 113, C2 114 a 120.

## 3. Em aberto

1. **Divisão do tempo do Reading entre router e módulo.** O site diz "router
   de 9 minutos e módulo de 18 a 21". A tabela do SPEC põe os números ao
   contrário: 18 a 21 na coluna Router, 9 na coluna do módulo. O total (27 a
   30) é o mesmo nas duas leituras e está confirmado. Não foi alterado porque
   pode ser tanto erro do site quanto célula trocada no PDF (no Listening é o
   módulo que varia, não o router). Aparece no M0, M1, M7, M8 e no
   `CLAUDE.md`. Se a ETS confirmar a leitura literal da tabela, trocar nos
   cinco.
2. **Quantos itens não contam ponto.** A ETS só diz que Reading e Listening
   "incluem itens não pontuados" (SPEC, nota 1). Os "~15" e "~12" do site são
   conta nossa: itens menos pontos brutos, com 1 ponto por item. É uma
   dedução boa, mas não é número publicado, por isso o til.
3. **Tempo de preparo no Take an Interview.** Os testes práticos não dão
   tempo de preparo, mas nenhum dos cinco documentos afirma isso com todas as
   letras. O M3 diz "nos testes práticos oficiais".
4. **Pausa não programada no centro de testes.** O BULL diz que pausas não
   programadas são monitoradas e que as "excessivas ou longas" são
   reportadas, mas não diz se o relógio da prova continua correndo. O M8
   manda ir ao banheiro antes e não promete nada.

5. **Soma dos tempos-base.** Os tempos-base do OVER somam 90 minutos (30 +
   29 + 23 + 8), mas o SPEC dá 1 h 29 min como máximo da prova. A diferença
   de um minuto é da própria ETS.

## 4. Presets do cronômetro

O cronômetro do site (os botões em `#stPresets`, no `app/build.py`) usa o
tempo-base de cada seção do OVER p. 4, que é o teto de cada uma, e o máximo
do SPEC para a prova inteira: Reading 30, Listening 29, Writing 23, Speaking
8, prova completa 89. Antes eram Reading 28, Listening 18 e prova completa
85, números que não vinham de documento nenhum. A ordem dos botões passou a
ser a da prova. Quem tinha um preset antigo salvo é levado ao novo
equivalente.

## 5. Onde foi mexido

`consolidated/modulo_0_embarque.md` (tabela 1.3, tabela do diagnóstico,
exemplo de cálculo, tempo do Listening), `modulo_2_listening.md` (tempo,
router, margem por item), `modulo_3_speaking.md` (tempos de resposta),
`modulo_7_simulados.md` (router do Listening, pausa, ordem das seções),
`modulo_8_examday.md` (toda a parte da pausa virou transição sem intervalo;
ordem fixa), `docs/ets-blueprint-2026.md` e a tabela de formato do
`CLAUDE.md` (Listening de 25 a 29 minutos; Reading com 35 itens pontuados, e
não 30, pela mesma conta do item 2 acima).

O grosso das edições veio de um subagente do Hermes interrompido no meio.
Cada mudança dele foi conferida de novo contra os PDFs antes de entrar, e
três foram ajustadas: a margem por item do Listening (32 a 37 segundos, não
30 a 37), a regra de pausa da Home Edition e uma frase do M8 que ainda
supunha ordem variável.
