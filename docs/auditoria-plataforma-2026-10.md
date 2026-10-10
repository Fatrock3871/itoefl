# Auditoria da plataforma (outubro de 2026)

**Feita em:** 2026-10-08
**Olhar:** de um aluno que pagou e de um designer exigente.
**Como foi medido:** site sem login (`scripts/build_teste.py`) servido em
`http://127.0.0.1`, num Chrome headless dirigido pelo DevTools
(`scripts/cdp.py`). Os 10 módulos e todos os widgets foram usados, a página
foi recarregada, a tela foi posta em 375 px, os dois temas foram medidos e as
capturas foram olhadas uma a uma. **Limite:** nenhum aparelho real, nenhum
leitor de tela de verdade, nenhum aluno de verdade. O que depende disso está
marcado.

Legenda: **Impacto** alto, médio ou baixo para o aluno. **Esforço** P (até
uma hora), M (algumas horas), G (um dia ou mais). **Situação:** *feito* (com
o commit), *fila* (dá para fazer sem o dono), *dono* (precisa de decisão,
backend ou pagamento).

## 1. Resumo

O conteúdo é o ponto forte: completo, no formato certo da prova, com
exercícios que respondem e guardam o progresso. O que segura a nota do
produto está em volta do conteúdo:

1. **A devolutiva dos exercícios dependia só de cor.** Resposta errada em
   vermelho, certa em laranja, sem uma palavra dizendo qual é qual.
2. **Não havia começo.** O aluno caía na Parte 1 do Módulo 0, um texto sobre
   a prova, sem ninguém dizer o que fazer primeiro nem onde ficava o menu.
3. **No celular o botão do menu flutuava em cima do texto**, e os dois
   botões redondos (gravador e cronômetro) em cima das alternativas.
4. **Teclado e leitor de tela ficavam de fora** das 277 subseções
   recolhíveis, e todo o inglês era lido com voz de português.
5. **A primeira tela para quem não tem conta é o login**, sem uma linha
   sobre o que o produto é. Depende do dono (seção 6).

## 2. Achados por critério

### 2.1 Primeiros 5 minutos

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| A1 | Quem ainda não tem conta vê só "Entre para continuar". Nada diz o que é a plataforma, o que tem dentro nem quanto custa | Alto | G | dono (seção 6) |
| A2 | Depois do login o aluno cai na Parte 1 do M0, que é teoria. O diagnóstico, que é o primeiro passo certo, está na Parte 3, e o resumo que avisa isso é um parágrafo corrido | Alto | M | fila |
| A3 | O menu fica escondido atrás de um botão de três traços sem rótulo. Progresso, meta do dia e lista de módulos só aparecem para quem abre | Médio | M | fila (barra do topo com o nome do módulo) |
| A4 | O título da paginação repete a palavra: "Parte 1 de 9 · PARTE 1: O TARGET MATRIX" | Baixo | P | fila |

### 2.2 Navegação

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| B1 | O botão do menu é fixo e flutua sobre o conteúdo. No celular ele tapa o começo das linhas enquanto o aluno rola | Alto | M | fila |
| B2 | Rolando a página, o aluno não sabe em que módulo e em que Parte está | Médio | M | fila (mesma barra do B1) |
| B3 | O "Mapa do curso" da gaveta estava com altura zero: só o título e um vazio | Médio | P | feito, `a86c38f` |
| B4 | "Continuar de onde parei" saía com "✓" grudado no título | Baixo | P | feito, `8a0ca18` |
| B5 | No computador a gaveta também começa fechada, mesmo com tela sobrando. Uma barra lateral fixa acima de 1200 px mostraria o progresso o tempo todo | Médio | M | dono: a gaveta fechada foi pedido dele |
| B6 | Gravador e cronômetro só aparecem em M1, M2, M3, M4 e M7. Certo, mas no celular os dois círculos de 54 px cobrem a última alternativa de cada questão | Médio | P | fila |

### 2.3 Clareza dos exercícios e da devolutiva

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| C1 | Depois de confirmar, a alternativa errada fica vermelha e a certa laranja, sem texto. Quem não distingue as duas cores não sabe se acertou. Vale para os quizzes e para os simulados | Alto | M | fila |
| C2 | Não há uma frase de veredito ("Você marcou B, a correta é D"). A explicação começa direto na gramática | Alto | P | fila (junto do C1) |
| C3 | O painel "Seu desempenho real" dá banda com qualquer amostra: uma questão certa vira "Banda 6 (C2)" | Médio | P | fila |
| C4 | "Entregar este bloco" fica apagado até responder tudo, sem dizer quantas faltam | Médio | P | fila |
| C5 | Build a Sentence: "Refazer" recarrega a página inteira | Baixo | M | não feito |
| C6 | Speaking: a marcação "repeti igual / errei" é autoavaliação, e a tela não diz isso com clareza. Nota de verdade depende de correção no servidor | Médio | G | dono (Etapa 5 do ROADMAP) |
| C7 | Escrita: a caixa guarda o texto mas não devolve nada além da contagem de palavras | Alto | G | dono (Etapa 3, correção por agente, é paga) |
| C8 | Registro de erros aceitava HTML digitado | Baixo | P | feito, `8a0ca18` |

### 2.4 Motivação e sensação de progresso

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| D1 | A sequência de dias quebrava para quem estuda depois das 21h (data em UTC) e contava dia só por abrir o site | Alto | P | feito, `8a0ca18` |
| D2 | A sequência só aparece dentro do Painel, que só abre com login. Não há número de dias na gaveta | Médio | P | fila |
| D3 | Concluir um módulo não tem nenhum momento de comemoração: o selo vira ✓ e só | Médio | M | não feito |
| D4 | A meta do dia é fixa em 1 atividade. Não dá para ajustar | Baixo | M | dono (é regra de produto) |
| D5 | Progresso mede "Parte marcada como lida", não desempenho. Dá para chegar a 100% sem acertar nada | Médio | G | dono (muda o que o certificado significa) |
| D6 | "Meta batida hoje! (3/1)" | Baixo | P | feito, `8a0ca18` |

### 2.5 Celular

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| E1 | Nenhuma página estoura a largura em 375 px, nos 10 módulos com tudo aberto. Agora há checagem automática | (ok) | | `d2ab7a2` |
| E2 | Alvos de toque pequenos: botão de pronúncia de 27 px (360 deles), lacunas do Complete the Words com 26 px de altura, "Apagar texto" com 23 px | Médio | P | fila |
| E3 | "Marcar esta parte como concluída": só a caixinha de 19 px respondia | Médio | P | feito, `8a0ca18` |
| E4 | 162 das 218 tabelas rolam para o lado no celular. Funciona, mas nada avisa que há mais coluna à direita | Médio | M | fila (sombra na borda) |
| E5 | Nunca testado em aparelho real | Alto | | dono (Etapa 0.5) |

### 2.6 Acessibilidade (WCAG AA)

| # | Problema | Critério | Impacto | Esforço | Situação |
|---|---|---|---|---|---|
| F1 | Texto branco sobre o laranja da marca: 3,4:1 no claro e 2,7:1 no escuro. Texto laranja sobre fundo creme: 4,0:1 | 1.4.3 | Alto | M | feito, `a86c38f`, com checagem nos dois temas |
| F2 | As 277 subseções abrem com clique num `<h3>`: sem foco de teclado, sem papel de botão, sem estado aberto ou fechado | 2.1.1, 4.1.2 | Alto | P | fila |
| F3 | Nenhum trecho em inglês tem `lang="en"`. Leitor de tela lê as questões com pronúncia de português | 3.1.2 | Alto | M | fila (widgets; o texto corrido mistura as duas línguas e fica de fora) |
| F4 | Janelas (painel, conta, certificado) sem `role="dialog"`, sem levar o foco para dentro; a de conta não fecha com Esc | 4.1.2, 2.4.3 | Médio | M | fila |
| F5 | Sem link "pular para o conteúdo"; o módulo atual não é anunciado na lista | 2.4.1, 4.1.2 | Médio | P | fila |
| F6 | 16 caixas de escrita e 44 campos do painel semanal sem rótulo | 1.3.1, 4.1.2 | Médio | P | fila |
| F7 | A correção de uma questão não é anunciada (sem região viva) | 4.1.3 | Médio | P | fila (junto do C1) |
| F8 | Campos de digitar tiram o contorno de foco (`outline:none`) e trocam por cor de borda | 2.4.7 | Baixo | P | fila |
| F9 | Ícones de olho e de usuário da tela de login são emoji escuro sobre campo escuro no tema escuro | 1.4.11 | Baixo | P | fila |
| F10 | Só uma regra respeita "reduzir movimento" | 2.3.3 | Baixo | P | fila |
| F11 | Nunca testado com leitor de tela de verdade (NVDA, VoiceOver, TalkBack) | | Alto | | dono, junto do teste em aparelho |

### 2.7 Desempenho

Medido em `127.0.0.1`, ou seja, sem rede: os números de tempo são piso.

| Medida | Valor |
|---|---|
| `index.html` | 1,38 MB (329 KB com gzip) |
| Nós no DOM | 26.644, com 218 tabelas |
| DOMContentLoaded | 1,6 s (local) |
| CSS embutido | 93 KB (18 KB com gzip) |
| JS embutido | 171 KB (47 KB com gzip) |
| Páginas legais | 100 KB cada, porque levam o CSS inteiro do app |

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| G1 | As fontes entram por `@import` dentro do CSS, que o navegador só descobre depois de ler o CSS: uma ida a mais à rede antes do primeiro texto | Médio | P | fila |
| G2 | Os 10 módulos vão no mesmo HTML. Com gzip e service worker é aceitável (329 KB, e a segunda visita vem do cache), mas o navegador monta 26 mil nós de uma vez, o que pesa em celular fraco | Médio | G | não feito: partir o HTML por módulo mexe no build, no service worker e no offline |
| G3 | As páginas legais carregam 93 KB de CSS para usar umas 30 regras | Baixo | M | não feito |
| G4 | São pedidos 16 pesos de fonte em 3 famílias | Baixo | P | não feito: mexe na identidade |
| G5 | As páginas legais não tinham ícone (404 em `favicon.ico`) | Baixo | P | fila |
| G6 | O servidor precisa mandar gzip ou brotli. Sem isso o primeiro acesso baixa 1,4 MB | Alto | | dono (escolha de hospedagem, Etapa 0.4) |

### 2.8 Consistência visual

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| H1 | Meia banda com ponto num lugar ("4–4.5") e vírgula em outro ("4,5") | Baixo | P | feito na interface, `8a0ca18`. As tabelas do M0 ainda usam ponto |
| H2 | O texto corrido tem 18 px e o enunciado das questões 14,5 px. No computador a questão parece nota de rodapé | Médio | P | fila |
| H3 | Ícones são emoji (⚙️ 📊 🎯 🔊). Mudam de desenho conforme o aparelho e não seguem a cor do tema | Médio | M | dono: trocar por ícones de linha mexe na identidade |
| H4 | "pra" e "para", "você" e imperativo se alternam nos textos de interface | Baixo | M | não feito |
| H5 | Travessão de pausa em 59 pontos dos módulos e em textos de interface | Baixo | M | já está no ROADMAP (Etapa 0B) |
| H6 | O cronômetro nascia com "28:00" no HTML e pulava para "30:00" | Baixo | P | feito, `a86c38f` |

### 2.9 Estados vazios e mensagens de erro

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| I1 | Estados vazios do Painel e do desempenho são bons: dizem o que fazer | (ok) | | |
| I2 | Erro de login não mapeado aparece como "Erro: " seguido da mensagem em inglês do servidor | Médio | P | fila |
| I3 | Sem aviso de "você está sem internet". Offline o site funciona, mas o aluno logado não sabe que o progresso ainda não subiu | Médio | M | fila |
| I4 | Importar arquivo errado dizia só "Arquivo inválido"; arquivo sem dado nenhum dizia "0 itens importados" e recarregava | Baixo | P | feito, `8a0ca18` |
| I5 | Microfone negado: a mensagem não diz como liberar | Baixo | P | não feito |

## 3. Ordem de execução

O que não depende do dono, do maior ganho para o menor:

1. **C1, C2, F7** devolutiva com palavra e veredito, anunciada.
2. **B1, B2, A3, B6** barra do topo com o nome do módulo; botões flutuantes menores no celular.
3. **A2, A4** cartão "Comece aqui" e título da paginação.
4. **F2, F4, F5, F6, F3** teclado, janelas, rótulos, `lang="en"`.
5. **E2, F8, F9** alvos de toque e foco.
6. **C3, C4, D2** amostra mínima para banda, "faltam N", sequência na gaveta.
7. **G1, G5, H2, I2, F10** fontes, ícone, tamanho do enunciado, erro de login, movimento.

A situação de cada um é atualizada na seção 5 conforme entra.

## 4. Bugs achados na varredura (Fase 1)

Todos corrigidos, cada um com checagem no smoke test.

| Bug | Checagem |
|---|---|
| Data da sequência e da meta em UTC | `real_streak_and_goal_use_local_date` |
| Abrir o site marcava sequência e sincronização | `real_opening_the_site_marks_nothing` |
| Registro de erros com `innerHTML` | `real_errlog_shows_typed_text_not_html` |
| Reiniciar deixava subseções, calculadora e painel semanal | `real_reset_clears_all_progress` |
| Importar não marcava alteração pendente | `real_import_restores_and_marks_dirty` |
| Mapa do curso com altura zero | `real_sidebar_map_is_visible` |
| "✓" no rótulo de continuar | `real_resume_label_has_no_checkmark` |
| Texto de concluir Parte não clicável | `real_mark_done_text_is_clickable`, `mark_done_label_wraps_text` |
| Contraste abaixo de AA | `contrast_aa_light`, `contrast_aa_dark` |
| Meia banda com ponto | `real_band_label_uses_comma` |
| E-mail fictício virando `mailto:` | `real_no_mailto_links` |
| Versão de teste sem manifesto nem service worker | `teste_build_is_installable` |

Conferido e sem defeito: o progresso de todos os widgets volta depois de
recarregar (`real_progress_survives_reload`); nada estoura em 375 px
(`mobile_375_no_horizontal_overflow`); o service worker mostra o aviso depois
de um build novo, troca de versão no "Recarregar" e abre offline
(`sw_*`); links internos e os quatro links da ETS respondem.

## 5. O que foi implementado nesta rodada

Nas tabelas da seção 2, "fila" é a situação de quando a auditoria foi
escrita. A situação final é esta:

| Itens | O que entrou | Commit | Checagens novas |
|---|---|---|---|
| C1, C2, F7, C3, C4 | Etiqueta em cada alternativa corrigida ("sua resposta", "correta") e frase de veredito com as duas letras, anunciada por leitor de tela, em quizzes e simulados. "Faltam N questões para entregar." Banda só a partir de 10 respostas | `e5bc999` | `real_feedback_says_right_or_wrong_in_words`, `real_exam_shows_how_many_left`, `real_no_band_from_tiny_sample` |
| B1, B2, A3, B6, A4 | Barra do topo que gruda, vai de borda a borda e mostra módulo e Parte; clicar nela abre o menu. Gravador e cronômetro menores no celular. Paginação sem repetir "PARTE N" | `e5bc999` | `mobile_top_bar_sticks_and_names_the_place` |
| A2 | Cartão "Comece aqui" no topo do M0, com dois estados (antes e depois do diagnóstico) | `e4b39a8` | `real_start_card_leads_to_diagnostic`, `real_start_card_follows_diagnostic_and_dismisses`, `real_start_card_stays_dismissed` |
| F2, F4, F5, F6, F3, F8, F9, F10, E2 | Subseções por botão com `aria-expanded`; janelas com `role="dialog"`, foco, Tab preso e Esc; link de pular; `aria-current`; rótulos; `lang="en"`; contorno de foco; alvos de toque de 36 px; menos movimento; ícones do login no escuro | `92d3152` | `a11y_subsections_are_buttons_with_state`, `a11y_dialogs_have_role_and_name`, `a11y_every_field_has_a_label`, `a11y_skip_link_and_current_module`, `a11y_english_content_is_marked`, `real_keyboard_opens_subsections_and_dialogs` |
| D2, G1, G5, H2, I2 | Sequência de dias na gaveta; fontes por `<link>` com preconnect; ícone nas páginas legais; enunciado e alternativas maiores; erros de login em português | `6b89240` | `streak_line_in_sidebar`, `fonts_load_by_link_not_import`, `auth_errors_are_in_portuguese` |

**Ficou na fila, sem depender do dono:** E4 (aviso de que a tabela rola para
o lado), I3 (aviso de sem internet), D3 (comemoração ao concluir módulo), C5
(Build a Sentence sem recarregar a página), G2 e G3 (peso do HTML e das
páginas legais), H4 (uniformizar "pra" e "para"), I5 (como liberar o
microfone).

**Limite do que foi verificado:** tudo acima passou em Chrome headless, em
tela de 1280 px e de 375 px emulada. Nenhum item foi testado em aparelho
real nem com leitor de tela de verdade. O `lang="en"` é aplicado por uma
regra simples (texto sem acento e sem palavras comuns do português): pode
deixar de marcar uma alternativa em inglês que contenha, por exemplo, " de ".

## 6. Desenhado, à espera do dono

### 6.1 Tela de apresentação com os três planos

**Por que espera:** a tabela precisa dos preços implementados
(`create-checkout`, validade em `entitlements`, texto dos termos), e isso é
gateway e edge function.

**Onde entra:** antes do login. Hoje `authGate` cobre a tela inteira. A
proposta é uma página própria, `artifact/apresentacao.html`, gerada pelo
`build.py` como as páginas legais, e o `index.html` continuar sendo o app. O
endereço público aponta para a apresentação; "Entrar" e "Criar conta" levam
ao app. Assim a apresentação pode ser indexada por buscador e não carrega o
1,4 MB do curso.

**Estrutura, de cima para baixo:**

1. **Topo:** logo, "Entrar" à direita.
2. **Chamada:** "TOEFL iBT no formato 2026, em português." Uma linha embaixo:
   "A prova mudou em janeiro de 2026: 1h30, adaptativa, nota de 1 a 6. Este
   curso foi escrito para ela." Botão principal "Ver os planos", secundário
   "Fazer o diagnóstico grátis".
3. **O que tem dentro, em números que o build já conhece:** 10 módulos, 80
   lacunas de Complete the Words, 67 questões de Reading, 30 itens de Build a
   Sentence, 9 conjuntos de Speaking com áudio, 4 simulados com 62 questões,
   50 flashcards. Gerar do build, para não envelhecer.
4. **Três capturas de tela reais** (exercício respondido, simulado, painel).
5. **Para quem é cada plano**, lado a lado, com o Standard em destaque:

   | | Sprint | Standard | Premium |
   |---|---|---|---|
   | Acesso | 30 dias | 90 dias | Vitalício |
   | Preço | R$ 39,90 | R$ 89,90 | R$ 149,90 |
   | Para quem | Prova já marcada | Quer os 4 pilares com calma | Vai tentar mais de uma vez |
   | Selo | | "Mais escolhido" | |

   No celular os três viram cartões empilhados, Standard primeiro.
6. **Perguntas frequentes:** é oficial da ETS? (não); funciona no celular?;
   e se meu acesso vencer?; tem reembolso?.
7. **Rodapé:** termos, privacidade, contato.

**Decisões que só o dono toma:** se há diagnóstico grátis sem conta (hoje
tudo fica atrás do pagamento); política de reembolso; se o "mais escolhido"
pode ser dito antes de haver venda; e a colisão de nomes com os cronogramas
do M0, registrada no ROADMAP.

**Decidido em 2026-10-08:** diagnóstico grátis sem conta, com as 10 questões
do M0 e o resultado de banda; reembolso de 7 dias em todos os planos (direito
de arrependimento, art. 49 do CDC); selo "Recomendado" no Standard, e não
"Mais escolhido", que sem dado de venda seria afirmação falsa; e os
cronogramas do M0 passam a se chamar Intensivo (30 dias), Regular (60) e
Completo (90). As capturas de tela do item 4 ficaram de fora da primeira
versão.

### 6.2 Outros que esperam decisão

- **B5** barra lateral fixa em tela larga.
- **D4, D5** meta do dia ajustável; progresso medido por desempenho.
- **H3** trocar emoji por ícones de linha.
- **C6, C7** nota de Speaking e correção de redação (Etapas 5 e 3, pagas).
- **G6** hospedagem com compressão.
- **E5, F11** teste em aparelho e com leitor de tela.
