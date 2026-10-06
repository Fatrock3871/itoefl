# Roadmap de expansão do iTOEFL

**Criado em:** 2026-10-05
**Escopo:** quatro frentes pedidas pelo usuário: (1) app para Android, Windows,
macOS e iOS; (2) didática, com videoaulas e aprofundamento; (3) banco de
questões e envio de redações com correção por agente; (4) conversação.
**Estado:** plano. Nada aqui foi construído ainda. O dia a dia continua no
`ROADMAP.md`, que aponta para este arquivo.

---

## 1. Ponto de partida

O que já existe e será reaproveitado:

- Site estático gerado por Python, um único `artifact/index.html` de cerca de
  1 MB com CSS, JS e os 10 módulos embutidos.
- Supabase com login (e-mail e Google), sincronização de progresso
  (`user_state`), controle de acesso pago (`entitlements`), cupons e duas edge
  functions (`create-checkout`, `mp-webhook`).
- 128 questões interativas (10 no M0, 67 no M1, 51 no M2), 10 itens de Build a
  Sentence e 50 flashcards.
- Gravador com transcrição e áudio sintético de Listening, ambos rodando no
  navegador, sem custo de API.

Três limites da arquitetura atual que as novas frentes vão bater:

1. **Tudo mora num HTML só.** Funciona para 128 questões. Não funciona para
   3.000 questões, áudios e redações. O banco precisa sair do HTML e ser
   servido sob demanda.
2. **O bloqueio de quem não pagou é uma camada visual.** O conteúdo vai
   embutido no HTML, então quem abre o código-fonte lê tudo. Para o curso de
   R$ 9,90 isso é aceitável. Para um banco de questões grande e para correção
   por IA (que custa dinheiro a cada uso), o controle tem que ser no servidor,
   via RLS e edge functions.
3. **Não há Node na máquina.** PWA não precisa de Node. O empacotamento para
   as lojas da Apple precisa, e a saída é rodar isso em CI (GitHub Actions),
   não na máquina do usuário.

---

## 2. Ordem das ondas

A ordem importa mais que cada item. Cada onda destrava a seguinte.

| Onda | Entrega | Depende de | Custo recorrente novo |
|---|---|---|---|
| 0 | Site publicado em https, pagamento confirmado, teste em celular real | Pendências do `ROADMAP.md` | Nenhum |
| 1 | App instalável (PWA) nas 4 plataformas + player de videoaula | Onda 0 | Nenhum |
| 2 | Banco de questões: estrutura, modo prática, primeiros 600 itens | Onda 0 | Baixo (geração de áudio, uma vez por item) |
| 3 | Envio de redações com correção por agente | Onda 2 + decisão de modelo de cobrança | Sim, por correção |
| 4 | Lojas: Play Store e Microsoft Store, depois App Store | Onda 1 estável | Taxas das lojas |
| 5 | Avaliação de Speaking e simulador de entrevista | Onda 3 | Sim, por resposta |
| 6 | Conversação em tempo real, simulados adaptativos | Onda 5 com uso comprovado | Sim, por minuto |

A Onda 0 não é opcional. Sem https não existe PWA, não existe loja e não
existe aluno de teste. Hoje ela é o item 1 do mapa de pendências.

As Ondas 1 e 2 podem andar em paralelo, porque não tocam nos mesmos arquivos.

---

## 3. Frente A: app em Android, Windows, macOS e iOS

### Recomendação

Um código só, o site atual, distribuído de três formas, nesta ordem. Não
reescrever em React Native nem Flutter: o produto é conteúdo mais formulários,
não há nada nele que peça interface nativa, e reescrever jogaria fora o
pipeline de build inteiro.

### A1. PWA (Onda 1)

Com um manifesto, um service worker e os ícones, o site passa a ser instalável
em todas as plataformas pedidas: Android (Chrome), Windows e macOS (Chrome e
Edge, e Safari no macOS recente), iOS (Compartilhar, Adicionar à Tela de
Início). Abre em janela própria, com ícone, e funciona offline.

O que entra no build:

- `app/manifest.json` (nome, cores, ícones 192 e 512, modo `standalone`).
- `app/sw.js`: guarda o `index.html` e as fontes em cache, com versão
  carimbada pelo `build.py` para o aluno receber a atualização na visita
  seguinte. Áudio e vídeo ficam fora do cache inicial.
- Aviso "nova versão disponível, recarregar" e botão "Instalar app" na sidebar.
- O `build.py` passa a copiar manifesto, service worker e ícones para
  `artifact/`.

Cuidados específicos:

- **iOS:** gravação de áudio funciona, mas o reconhecimento de fala do
  navegador é limitado. A transcrição do gravador precisa de um plano B no
  iPhone (mensagem clara hoje, transcrição no servidor na Onda 5).
- **Login com Google dentro de app instalado:** testar em cada plataforma. É o
  ponto que mais quebra.
- **Teste em aparelho físico:** Android e iPhone reais. Nunca foi feito, e é
  pendência antiga.

Critério de pronto: instalar nas 4 plataformas, logar, fazer um drill offline,
voltar online e ver o progresso sincronizado.

### A2. Play Store e Microsoft Store (Onda 4)

As duas aceitam o PWA empacotado, sem código novo. O PWABuilder (site da
Microsoft) gera os dois pacotes a partir da URL publicada, sem Node local.

- **Android:** pacote TWA, que é o próprio Chrome sem barra de endereço. Exige
  o arquivo `assetlinks.json` no domínio. Conta de desenvolvedor Google com
  taxa única. Conta pessoal nova passa por um período de teste fechado com um
  grupo de testadores antes de publicar, então vale abrir a conta cedo.
- **Windows:** pacote MSIX para a Microsoft Store.

### A3. App Store, iOS e macOS (Onda 4, por último)

É a parte cara e arriscada, por isso fica no fim.

- Exige conta Apple Developer (anuidade) e build em macOS. Sem Mac, o build
  roda em CI com runner macOS.
- Empacotamento com Capacitor (casca nativa em volta do mesmo site).
- A Apple rejeita app que é só um site embrulhado. Para passar, o app precisa
  de algo que justifique ser app: notificações de lembrete de estudo, offline
  de verdade, gravação nativa. As Ondas 1 a 3 entregam isso, e é mais um motivo
  para a App Store vir depois delas.
- **Pagamento:** Apple e Google têm regras próprias para venda de conteúdo
  digital dentro do app, e elas mudaram bastante nos últimos anos, inclusive
  no Brasil. Caminho seguro para começar: o app das lojas só faz login, e a
  compra acontece no site. Conferir a regra vigente na data da submissão antes
  de decidir qualquer coisa diferente disso.

Enquanto a App Store não sai, o usuário de iPhone e Mac já está atendido pelo
PWA da Onda 1.

---

## 4. Frente B: didática

### B1. Videoaulas (Onda 1)

Os vídeos já estão sendo gravados por fora. Falta a infraestrutura.

- **Fonte de dados:** `app/videos.json`, mapeando módulo e Parte para o vídeo
  (id, título, duração, legenda). Trocar de hospedagem vira troca de
  configuração, não de código.
- **Player:** um por módulo no `.panel-head` (aula de abertura) e um opcional
  no topo de cada Parte. Carregamento preguiçoso: só a capa aparece, o player
  de verdade carrega no clique, para não pesar a página.
- **Progresso:** "aula assistida" conta como item de conclusão, junto dos
  checkboxes que já existem.
- **Acessibilidade:** legenda em português e transcrição recolhível embaixo.
- **Hospedagem, recomendação:** começar com YouTube não listado, custo zero.
  O risco é o link vazar, o que pesa pouco com o curso a R$ 9,90. Migrar para
  um serviço com link assinado (Bunny Stream, Cloudflare Stream) quando o
  preço subir ou quando houver vídeo exclusivo de plano pago.

### B2. Estrutura fixa de cada Parte (Ondas 1 e 2)

Hoje cada Parte é texto mais drill. A proposta é um ciclo previsível em toda
Parte de todo módulo:

1. **Vídeo** curto (5 a 10 min): a ideia central.
2. **Essencial:** o texto atual, enxuto.
3. **Aprofundamento:** bloco recolhível, fechado por padrão, com a teoria
   densa (por que a regra existe, casos de borda, contraste com o português).
4. **Checkpoint:** 5 a 10 questões puxadas do banco, com as etiquetas daquela
   Parte.
5. **Registro de erros:** o formulário que já existe.

Isso resolve o dilema "material baseado em questões ou teoria densa" sem
escolher um: o aluno com pressa faz vídeo, essencial e checkpoint; o aluno
que quer profundidade abre o aprofundamento. Um seletor na sidebar ("trilha
rápida" ou "trilha completa") define o que vem aberto.

### B3. Produção do aprofundamento (Onda 2 em diante)

- Um módulo por sessão, na ordem de peso na prova: M3 (Speaking, 55 pontos
  brutos), M1, M2, M4, depois os transversais.
- Marcação nova nos `.md` de `consolidated/` para o bloco de aprofundamento, e
  o pipeline o transforma em seção recolhível.
- Mesma verificação por contagem de sempre: headings e tabelas antes e depois.
- Pendência antiga que vira pré-requisito: conferir os números do formato 2026
  contra o documento oficial da ETS antes de adensar a teoria em cima deles.

---

## 5. Frente C: banco de questões

### C1. Arquitetura (Onda 2)

- **Fonte da verdade:** arquivos JSON no repositório, em `bank/`, um por tipo
  de item. Versionados no Git, validados por script. Mesma filosofia do
  projeto: a fonte é arquivo, o resto é gerado.
- **Publicação:** um script envia o banco para uma tabela `items` no Supabase.
  A leitura é liberada por RLS só para quem tem `entitlements.paid`. É aqui que
  o conteúdo pago passa a ser protegido de verdade.
- **Tentativas:** tabela própria `attempts` (aluno, item, resposta, acerto,
  tempo, data). Não entram no blob `user_state`, que estouraria de tamanho.
- **Offline:** os itens já baixados ficam em cache no aparelho, e as tentativas
  feitas offline sobem quando a conexão volta.
- Os 128 itens atuais de `drills_data.py` migram para o mesmo formato, para o
  desempenho do aluno ser contado num lugar só.

Campos de cada item: id, seção, tipo de item (os 12 tipos do formato 2026),
habilidade testada, dificuldade em banda CEFR, estímulo (texto ou referência de
áudio), alternativas, gabarito, explicação em português, código de armadilha
(os R1 a R6, L1 a L6, W1 a W6 que o curso já usa), estado (rascunho, revisado,
publicado).

### C2. Linha de produção das questões

O gargalo do banco é qualidade, não código. Processo por lote:

1. **Geração** por IA, um tipo de item por vez, com a especificação de
   `docs/ets-blueprint-2026.md` e exemplos do próprio curso como referência.
   Conteúdo sempre original. Nunca copiar item oficial da ETS.
2. **Validação automática:** formato, uma única resposta correta, tamanho do
   texto, duplicata, vocabulário dentro da banda declarada.
3. **Revisão por um segundo agente** que tenta resolver o item sem ver o
   gabarito. Divergência manda o item de volta.
4. **Amostra humana:** o usuário revisa uma fração de cada lote. Lote com erro
   acima do limite combinado volta inteiro.
5. **Áudio de Listening:** gerado uma vez por item com voz neural, vozes e
   sotaques variados, guardado em storage. Substitui a voz do navegador, que
   varia por aparelho e soa artificial.
6. **Depois de publicado:** item com taxa de acerto anormal ou denunciado pelo
   aluno (botão "reportar questão") volta para revisão.

### C3. Metas de volume

| Marco | Total | Composição aproximada |
|---|---|---|
| Hoje | 138 | 128 de Reading e Listening + 10 Build a Sentence |
| v1 (Onda 2) | 600 | 200 Reading, 200 Listening, 150 Build a Sentence, 50 enunciados de Writing |
| v2 | 1.500 | + 200 frases de Listen and Repeat, 100 perguntas de Interview, reforço nos tipos com mais erro |
| v3 | 3.000+ | Volume suficiente para simulados adaptativos sem repetir item |

Build a Sentence é o tipo mais barato de escalar, porque a correção é
automática e o widget já existe.

### C4. O que o aluno ganha com o banco

- **Modo prática:** filtrar por seção, tipo, dificuldade e "só as que errei".
- **Caderno de erros automático:** todo erro entra numa fila de revisão
  espaçada, mesmo motor dos flashcards do M6.
- **Painel de desempenho:** acerto por tipo de item e por código de armadilha,
  com banda estimada por seção. Estende o painel que já existe no M0.
- **Simulados adaptativos (Onda 6):** montados do banco, com roteador e segundo
  estágio mais fácil ou mais difícil, como na prova real. Só vale a pena com o
  volume da v3.

---

## 6. Frente C: redações com correção por agente (Onda 3)

### Fluxo

1. O aluno escolhe a task (Write an Email ou Write for an Academic Discussion),
   recebe um enunciado do banco, escreve com cronômetro e contador de palavras.
2. Envia. A redação entra na tabela `submissions` com estado "em correção".
3. A edge function `grade-writing` confere acesso e cota, chama o agente com a
   rubrica daquela task e grava o resultado em `feedback`.
4. O aluno recebe, em geral em menos de um minuto: nota na escala da prova,
   banda CEFR estimada, nota por critério, o próprio texto com os erros
   marcados e explicados em português, os códigos de armadilha W1 a W6
   encontrados, e uma versão reescrita um nível acima para comparar.
5. Histórico de redações com gráfico de evolução.

### O que garante que a nota presta

- **Rubrica versionada no repositório,** construída em cima dos critérios
  oficiais de cada task, uma por task.
- **Conjunto de calibração:** redações de referência com nota conhecida, uma
  faixa de cada nível. Toda mudança de rubrica ou de modelo roda contra esse
  conjunto antes de ir ao ar. Sem isso não há como saber se a nota piorou.
- **Saída estruturada:** o agente devolve JSON com campos fixos, validado
  antes de gravar.
- **Painel de revisão para a equipe:** ver as correções, ajustar a nota quando
  discordar. Toda discordância vira caso novo do conjunto de calibração.
- **Transparência:** a nota aparece como estimativa de treino, não como nota
  oficial.

### Proteções

- Cota por aluno e limite de tamanho, no servidor.
- O texto do aluno entra como dado, nunca como instrução para o agente.
- A chave da API fica só na edge function.
- LGPD: consentimento no primeiro envio e exclusão das redações junto com a
  conta. "Excluir conta" já é pendência e passa a ser obrigatória aqui.

### Custo e modelo de cobrança

Cada correção custa centavos de API. O número exato sai de um piloto com 50
redações reais, medindo custo e qualidade com dois tamanhos de modelo. O
problema é estrutural: **acesso vitalício de R$ 9,90 não sustenta correção
ilimitada.** Antes de construir a Onda 3 é preciso escolher entre pacote de
créditos, assinatura mensal ou cota pequena incluída mais crédito avulso. A
decisão também define o que a troca de gateway de pagamento precisa suportar
(cobrança recorrente ou não), então as duas conversas devem acontecer juntas.

---

## 7. Frente D: Speaking e conversação

Dá para operacionalizar, em degraus de custo crescente. Cada degrau só é
construído se o anterior mostrar uso.

### D1. Listen and Repeat com nota (Onda 5)

O aluno ouve a frase, repete, o áudio sobe para o servidor. Um serviço de
avaliação de pronúncia devolve precisão por palavra e por fonema, fluência e
completude. O retorno mostra exatamente qual palavra saiu errada. É o maior
bloco do Speaking (7 dos 11 itens), a correção é objetiva e o custo por
resposta é baixo. Melhor relação entre esforço e valor de toda esta frente.

### D2. Simulador de Take an Interview (Onda 5)

Por turnos, não em tempo real: o entrevistador (voz sintética) faz a pergunta,
o aluno grava a resposta no tempo da prova, o áudio é transcrito no servidor e
o agente avalia com a rubrica de Speaking, combinando com as métricas de
pronúncia do D1. Reproduz o formato da prova, que também é por turnos, e
reaproveita toda a infraestrutura das redações (fila, cota, rubrica,
calibração, painel de revisão).

### D3. Entrevista com perguntas de seguimento (Onda 5 ou 6)

O mesmo simulador, mas o agente escolhe a pergunta seguinte com base no que o
aluno respondeu. Ainda por turnos, com alguns segundos de espera entre um e
outro. Já dá a sensação de conversa sem o custo do tempo real.

### D4. Conversa por voz em tempo real (Onda 6)

Parceiro de conversação com voz contínua, cenários (campus, entrevista,
discussão acadêmica) e relatório ao final. É tecnicamente viável hoje, mas
cobrado por minuto, o que só fecha a conta num plano de assinatura. Fica por
último de propósito: é o recurso mais caro, o menos ligado à nota da prova e o
que mais depende de o modelo de cobrança já estar resolvido.

### D5. Gente de verdade (sem data)

Comunidade de alunos e encontros ao vivo periódicos. Não é código, é operação.
Vale como diferencial de retenção depois que houver base de alunos.

---

## 8. Decisões que dependem do usuário

Nenhuma trava as Ondas 0, 1 e 2. Todas travam alguma coisa depois.

| Decisão | Trava | Recomendação |
|---|---|---|
| Modelo de cobrança da correção por IA | Onda 3 | Curso vitalício como está + assinatura ou créditos para correção e conversação |
| Gateway de pagamento (discussão aberta em 2026-09-24) | Onda 3 | Decidir junto com o item acima, porque assinatura muda o requisito |
| Hospedagem dos vídeos | Onda 1 | YouTube não listado agora, migrar depois |
| Quem revisa a amostra humana do banco e quanto por lote | Onda 2 | O usuário, 10% de cada lote no começo |
| Conta Apple Developer e acesso a um Mac | Onda 4 | Adiar até o PWA e a Play Store estarem validados |
| Abrir conta de desenvolvedor Google | Onda 4 | Abrir cedo, por causa do período de teste obrigatório |

---

## 9. Próximo passo concreto

1. Fechar a Onda 0: publicar em https, concluir o pagamento de teste, testar
   em um Android e um iPhone reais.
2. Onda 1, primeira sessão: manifesto, service worker e ícones no build.
3. Onda 1, segunda sessão: `videos.json` e o player, com o primeiro vídeo
   real que o usuário mandar.
4. Onda 2, primeira sessão: formato do item, script de validação e migração
   dos 128 itens atuais, com contagem declarada antes e depois.
