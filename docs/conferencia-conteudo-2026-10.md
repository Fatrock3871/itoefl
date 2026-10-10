# Conferência do conteúdo contra a ETS (outubro de 2026)

**Feita em:** 2026-10-08
**Escopo:** tudo que o site afirma sobre a prova fora dos números de formato,
que já tinham sido conferidos em `docs/conferencia-formato-2026.md`: tempos de
resposta, escala e concordância, MyBest, validade, envio de notas, Home
Edition, documento, pausas, inscrição e taxas, prazo de resultado, reteste.
Mais as contradições internas entre módulos.

**Regra seguida:** só foi corrigido o que um documento da ETS afirma de forma
direta, ou o que contradizia outro trecho do próprio site já conferido. O
resto está na seção 4, em aberto. As contagens de questões do M7 não foram
tocadas (19 blocos, 62 itens).

## 1. Fontes

Todas acessadas em 2026-10-08.

| Sigla | Documento | URL |
|---|---|---|
| BULL | *TOEFL iBT Information Bulletin 2026-2027* (PDF) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-bulletin.pdf |
| OVER | *Updated TOEFL iBT Test Overview* (PDF) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-test-overview.pdf |
| SPEC | *Test Blueprint and Specifications Document* (PDF) | https://www.ets.org/content/dam/ets-org/pdfs/toefl/toefl-ibt-test-specifications-2026.pdf |
| SCORES | *Understanding Your TOEFL iBT Scores* | https://www.ets.org/toefl/test-takers/ibt/scores/understand-scores.html |
| SEND | *Sending Your Scores* | https://www.ets.org/toefl/test-takers/ibt/scores/send-scores.html |
| FEES | *Fees* | https://www.ets.org/toefl/test-takers/ibt/register/fees.html |
| HOME | *At Home Testing: Equipment and Environment Requirements* | https://www.ets.org/toefl/test-takers/ibt/register/at-home-requirements.html |
| ID | *ID Requirements* | https://www.ets.org/toefl/test-takers/ibt/register/id.html |
| FAQ | *Testing Policies FAQ* | https://www.ets.org/toefl/test-takers/ibt/faq/testing-policies-toefl-ibt.html |

**Como foi conferido.** Os três PDFs foram baixados de novo hoje e comparados
por hash SHA-1 com as cópias de 2026-10-07 guardadas em `_snapshots/ets-pdfs/`:
são idênticos byte a byte. As citações de BULL, OVER e SPEC foram conferidas
por busca no texto extraído desses PDFs, não por resumo. As páginas web foram
lidas por uma ferramenta que resume o conteúdo, então as citações de SEND,
FEES, HOME e FAQ podem não ser literais: nenhuma correção do site se apoia só
nelas. Os quatro links de testes práticos do M7 respondem 200 (a ETS
redireciona de `/content/dam/ets-org/pdfs/toefl/` para `/pdfs/toefl/`).

## 2. O que confere

| Tema | O que a ETS diz | Fonte | Onde está no site |
|---|---|---|---|
| Itens e tempo por seção | Reading 50 e 30 min, Listening 47 e 29 min, Writing 12 e 23 min, Speaking 11 e 8 min | OVER p. 4 | M0 a M4, M7, M8, cronômetro |
| Listen and Repeat | "a maximum of 8 to 12 seconds to record a response" | OVER p. 17 | M3 |
| Take an Interview | "They have 45 seconds to answer each question" | OVER p. 19 | M3, widget de entrevista (45 s) |
| Write an Email | "Test takers have 7 minutes to complete this task" | OVER p. 14 | M4, caixas de escrita |
| Academic Discussion | "They have 10 minutes"; "An effective response will contain at least 100 words" | OVER p. 15 | M4, caixas de escrita |
| Escala 1 a 6 | Meio em meio ponto desde 21 de janeiro de 2026; nota geral é a média das quatro | SCORES, OVER p. 21 | M0 |
| Concordância com 0 a 120 | 6 = 114+; 5,5 = 107+; 5 = 95+; 4,5 = 86+; 4 = 72+; 3,5 = 58+; 3 = 44+; 2,5 = 34+; 2 = 24+; 1,5 = 12+; 1 = 0+ | OVER p. 22 | M0 Parte 1.3 |
| MyBest | Continua no formato 2026: "your MyBest scores, which combine your best scores for each section from all your valid TOEFL iBT scores from the last 2 years" | BULL p. 11 | M8 Parte 8 |
| Validade | "TOEFL scores remain valid for 2 years after the test date" | BULL p. 11 | M8 Parte 8 |
| Reteste | "There is no limit to the number of times you can take the test, but you cannot take it more than once in a 3-day period" | BULL p. 3 | M8 Parte 8 |
| Pausas | "There are no scheduled breaks in the TOEFL iBT test." Home Edition: "Unscheduled breaks are not allowed." | BULL p. 10 | M7, M8 |
| Chegada ao centro | "you must arrive at least 30 minutes before your assigned start time" | BULL p. 8 | M8 Parte 5 |
| Home Edition, fone | Fone de ouvido e earphone não são permitidos; usar alto-falante | HOME | M8 Parte 5 |
| Home Edition, sala | "You must be alone in a room with no one else entering" | BULL p. 10 | M8 Parte 5 |
| Score não oficial | Reading e Listening aparecem na tela no fim da prova | BULL p. 11 | M8 Parte 8 |
| Nome idêntico | Nome e data de nascimento do documento têm de bater com a inscrição | BULL p. 6 | M8 Parte 5 |

## 3. O que foi corrigido

| Onde | Como estava | Como ficou | Fonte |
|---|---|---|---|
| M5, Parte 5.1 | "~5 segundos de preparação e ~30–45 segundos de resposta" no Take an Interview | 45 segundos por pergunta, sem tempo de preparo nos testes práticos oficiais | OVER p. 19; contradizia o M3 |
| M3, Grupo B e B8 | "5 s de silêncio para planejar", "~40 s", "~5 s de planejamento por item" | Começar a falar em seguida e usar os 45 s da prova | OVER p. 19; contradizia a Parte 1 do próprio M3 |
| M7, Speaking do Simulado 2 | "Responda em ~40 segundos cada" | 45 segundos, sem preparo | OVER p. 19 |
| M7, Parte 1, tabela de conversão | "não é uma conversão oficial exata"; B1 ~42–71, A2 ~20–41, A1 ~0–19; "banda 5 ≈ 100+" | Concordância oficial: B1 44–71, A2 24–43, A1 0–23, com as meias bandas | OVER p. 22; contradizia o M0 |
| M7, Parte 1 e Parte 3 | "Fixar templates", "Fixação de Template" | "Fixar a estrutura e a mecânica", "Fixação de Estrutura" | Princípio do projeto (M0 Parte 2, M3 Parte 2.3) |
| M0, Parte 7.3, alavancador 1 | "Templates de Write an Email ... decore 3 esqueletos e adapte" | Treinar a ordem (motivo, 3 pontos, próximo passo) com 3 e-mails cronometrados; texto decorado pode ser anulado | BULL p. 14 ("text that is substantially similar to that found in other TOEFL test responses"); M4 Parte 2.2 |
| M0, Parte 7.3, alavancador 5 | Complete the Words descrito como "padrão de ordenação lexical" | Completar o final das palavras (gramática, forma, collocation) | `docs/ets-materiais-oficiais.md` |
| M7, Parte 2 e Parte 5 | Simulado com fone e papel, sem ressalva; "TOEPO" em "toefl.org: pago" | Aviso para quem fará a Home Edition (alto-falante, quadro branco ou folha no plástico); a linha do material pago aponta para ets.org sem nome nem preço | HOME, BULL p. 10; o nome e o endereço antigos não foram achados na ETS |
| M8, Parte 5, documento | "geralmente passaporte" | Documento original, físico, válido, com foto e assinatura; conferir a regra do país na página da ETS | BULL p. 6 |
| M8, Parte 5, centro | "caneta/lápis" | Lápis; não se pode levar papel próprio | BULL p. 10 |
| M8, Parte 5, Home Edition | "ETS Test Browser" e "system check" | "TOEFL Test App" e checagem de equipamento, pelo painel My TOEFL Home | BULL p. 10 |
| M8, Parte 5, anotações | Três opções, incluindo "folha plástica transparente" | As duas da ETS: quadro branco pequeno, ou uma folha dentro de plástico transparente | BULL p. 10 |
| M8, Parte 5, celular | "celular fica fora da sala" | Celular ou espelho de mão é exigido no check-in; verificação de identidade por aplicativo 48 h antes, quando pedida | BULL p. 6 e p. 10 |
| M8, Parte 5, linha do tempo | Check-in em T-30 | Check-in só a partir de 15 minutos antes; tolerância de 30 minutos depois do horário | BULL p. 10 |
| M8, Parte 7, atraso | "Muitos centros têm uma janela de tolerância" | Quem chega depois do horário não faz a prova e perde a taxa | BULL p. 8 |
| M8, Parte 7, nome diferente | "contate a ETS para reagendar sem custo total" | Sem reembolso; resolver antes do dia | BULL p. 4 e p. 6 |
| M8, Parte 8, cancelamento | "cancelar antes de visualizar (ou logo após, com custo)" | Cancelar é no fim da prova e não custa; o que custa é reativar, em até 60 dias | BULL p. 11 |
| M8, Parte 8, resultado | "Poucos dias úteis" | Cerca de 3 dias | BULL p. 11 |
| M8, Parte 8, envio | Não dizia nada | Até 4 envios incluídos, escolhidos até as 22h da véspera | BULL p. 11 |
| M8, Parte 9 | "Reading (~28 min)" | "~27–30 min", como no resto do módulo | SPEC p. 2 |

O smoke test ganhou duas checagens para estas correções:
`content_no_outdated_exam_claims` e `content_states_confirmed_exam_rules`.

## 4. Em aberto

Nada daqui foi alterado no site.

1. **Preço da prova no Brasil.** A página FEES pede para escolher o país num
   seletor que não abre fora do navegador. O site não cita preço, e continua
   sem citar. Taxas que a ETS publica para todos: inscrição expressa US$ 49,
   remarcação US$ 69 (até 4 dias completos antes), reembolso de 50% no
   cancelamento dentro do prazo, reativação de score US$ 20. Vieram de FEES
   por leitura resumida: conferir no navegador antes de pôr no M8.
2. **Preço do envio adicional de score.** FEES diz US$ 29, SEND diz US$ 25.
   Divergência da própria ETS. **Resolvido em 2026-10-08:** o site nunca
   citou o valor e continua sem citar. O M8 (Parte 8) agora manda conferir o
   valor atual na página SEND, com link.
3. **Documento aceito para brasileiros.** A regra por país fica no mesmo
   seletor. O boletim aceita, no país de cidadania, passaporte, carteira de
   motorista e identidade nacional, sempre físicos e com assinatura. Se a CNH
   e a nova CIN servem no Brasil não foi possível confirmar. O M8 manda
   conferir na página e recomenda passaporte.
4. **Tempo de preparo no Speaking.** Nenhum documento afirma nem nega. O site
   diz "os testes práticos oficiais não dão tempo de preparo", que é o que se
   vê nos quatro PDFs de prática.
5. **Voltar a questões já respondidas** em Reading e Listening. O M8 diz que
   "normalmente não há como voltar"; o M7 fala em não gastar tempo revisando.
   A ETS não diz nada nos documentos lidos.
6. **Correção só por IA.** O site diz que Speaking e Writing são corrigidos
   100% por IA e cita "e-rater" e "SpeechRater". O SPEC marca os itens como
   "AI Scored" mas não nomeia os motores, e a revisão paga de score é feita
   por "scoring specialists". Trocar "100% por IA" por "por IA" seria mais
   seguro; como aparece em seis módulos, fica para decisão.
7. **Pontos brutos de Reading e Listening.** O SPEC p. 2 dá 35 e 35. A Tabela
   1 do OVER p. 21 traz "Raw Score Range 0-30" para as duas. O site segue o
   SPEC. **Conferido de novo em 2026-10-08, ver a seção 7:** a divergência é
   real e o site fica com o SPEC.
8. **Itens por IA.** O SPEC dá o total "108 por máquina e 12 por IA", mas as
   linhas da própria tabela somam 107 e 13. O site repete o total.
9. **Duração total.** O SPEC dá de 1h23 a 1h29, que é o que o site ensina. As
   páginas web dizem "just under 2 hours" e mandam reservar 2h30 com o
   check-in. Vale uma frase no M8 sobre reservar a manhã inteira.
10. **Home Edition, sistema.** HOME pede Windows 11 ou superior; a FAQ diz 10.
    O M8 diz só "Windows ou macOS". **Resolvido em 2026-10-08:** o site
    segue sem citar versão, e o M8 (Parte 5) agora manda conferir o requisito
    atual na página HOME, com link.
11. **Tempo do Build a Sentence** (~6 min no site) é conta nossa: 23 menos 7
    menos 10.
12. Seguem abertos da conferência anterior: divisão do tempo do Reading entre
    router e módulo, e o que acontece com o relógio numa pausa não programada
    no centro.

## 5. Contradições internas resolvidas

| Contradição | Resolução |
|---|---|
| Preparo no Take an Interview: M5 e M3 (drills) davam 5 s; M3 Parte 1 e M8 diziam sem preparo | Sem preparo, nos quatro lugares |
| Tempo de resposta: 30 a 45 s (M5), ~40 s (M3, M7) contra 45 s (M3 Parte 1) | 45 s em todos |
| Concordância 0 a 120: M7 "não oficial" com faixas próprias contra M0 "oficial" | M7 usa as faixas do M0 |
| Decorar: M0 "decore 3 esqueletos" e M7 "fixar templates" contra M3 "não um script decorado" | M0 e M7 falam em estrutura treinada |
| Reading: "~28 min" (M8 Parte 9) contra "~27–30" (M8 Parte 6) | 27 a 30 |
| Ambiente do simulado (fone, papel) contra Home Edition (sem fone, sem papel solto) | M7 avisa quem fará a Home Edition |

## 6. Para o dono decidir

- **Nomes dos cronogramas contra nomes dos planos. Resolvido em 2026-10-08.**
  Os cronogramas de estudo do M0 tinham os mesmos nomes dos planos de preço,
  com prazos diferentes. O dono decidiu renomear os cronogramas: Intensivo
  (30 dias), Regular (60 dias) e Completo (90 dias). Os nomes Sprint,
  Standard e Premium ficam só para os planos de preço.
- Itens 6 e 9 da seção 4.

## 7. Pontos brutos de Reading e Listening: 35 ou 30 (2026-10-08)

**A pergunta.** O "0 a 30" do OVER seria a escala antiga por seção (o 0 a
120 dividido em quatro), e não pontos brutos? Se fosse, não haveria
divergência com o SPEC.

**Como foi conferido.** Busca no texto extraído dos dois PDFs guardados em
`_snapshots/ets-pdfs/` (os mesmos de 2026-10-07, idênticos por hash aos
baixados em 2026-10-08).

**O que os documentos dizem.**

| Documento | Trecho | Reading | Listening | Writing | Speaking |
|---|---|---|---|---|---|
| OVER p. 21, Tabela 1, "Raw Score and Band Score Ranges", coluna "Raw Score Range" | "Table 1 presents the raw score and band score ranges for the TOEFL test" | 0-30 | 0-30 | 0-20 | 0-55 |
| SPEC p. 2, Blueprint Table, coluna "Raw Points" | Nota 1: "Items include non-scored items in the reading and listening sections"; "Max points per item is 1 for scored items" | 35 | 35 | 20 | 55 |
| OVER p. 22, Tabela 3, "Score Concordance Between the 1–6 Band Levels and the 0–30 and 0–120 Score Scales" | "For two years, TOEFL will provide references to the old score scale in the score reports" | 0–30 | 0–30 | 0–30 | 0–30 |

**Conclusão: a hipótese não se sustenta.** A Tabela 1 do OVER não é a escala
antiga. Três motivos:

1. O título e a coluna dizem "Raw Score", e o parágrafo que a apresenta
   também.
2. Na mesma coluna, Writing vai de 0 a 20 e Speaking de 0 a 55. Esses são os
   pontos brutos do SPEC. Na escala antiga as quatro seções iam de 0 a 30:
   se a tabela fosse a escala antiga, Writing e Speaking também estariam em
   0-30.
3. A escala antiga aparece em outro lugar do mesmo documento, a Tabela 3, e
   lá sim as quatro seções usam 0–30.

Então existem dois "0 a 30" no OVER, e eles são coisas diferentes: o da
Tabela 3 é a escala antiga (correto, e é o que o aluno vê no relatório); o da
Tabela 1 é apresentado como ponto bruto de Reading e Listening e **diverge**
do SPEC, que dá 35. É uma divergência entre dois documentos da ETS, não um
erro de leitura nosso. A coincidência do número pode ser a origem do erro
(se for erro) na Tabela 1, mas isso é suposição: nenhum dos dois documentos
explica.

**Fonte escolhida: o SPEC (*Test Blueprint and Specifications Document*).** É
o mais específico dos dois: lista os itens por competência, diz que Reading
e Listening incluem itens não pontuados, e fixa 1 ponto por item pontuado.
O OVER é um documento de apresentação e dá só a faixa, sem a conta. O site
continua com 35 e 35, e o total bruto continua 145 (com a Tabela 1 do OVER
seria 135).

**O que mudou no site.** O M0 (Parte 2.2) ganhou um aviso logo abaixo da
tabela de pontos, "Três números que não se misturam": ponto bruto (não
aparece no resultado), banda de 1 a 6 (a nota oficial) e escala antiga de 0
a 30 por seção e 0 a 120 no total (referência por dois anos). O aviso diz
que o Overview traz "0–30" na tabela de pontos brutos, que o Blueprint dá 35
e qual dos dois o curso segue.

**O que continua sem resposta.** Qual dos dois números a ETS usa de fato.
Para o aluno não faz diferença: ponto bruto não aparece no relatório e não
entra em nenhuma conta do curso (a calculadora do M0 trabalha com
porcentagem de acerto e banda).
