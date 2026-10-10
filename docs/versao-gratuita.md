# Versão gratuita de teste: opções e recomendação

**Escrito em:** 2026-10-08
**Estado:** só plano. Nada daqui foi implementado. Espera decisão do dono
(item (D) no `ROADMAP.md`).

## 1. De onde se parte

O que já existe ou já foi decidido, e que qualquer versão gratuita tem de
respeitar:

- **Diagnóstico grátis sem conta.** As 10 questões do M0 estão abertas na
  tela de apresentação (`artifact/apresentacao.html`), com banda e
  cronograma indicado.
- **Três planos pagos** (Sprint 30 dias, Standard 90 dias, Premium
  vitalício), escritos em código e ainda não publicados
  (`docs/deploy-planos.md`).
- **Reembolso de 7 dias** em qualquer plano. Na prática já é um "teste sem
  risco" de acesso completo, só que exige pagar antes.
- **O bloqueio é só visual.** O curso inteiro (1,4 MB, 10 módulos, 86 Partes)
  vai embutido no `index.html`. Quem abre o código da página lê tudo, com ou
  sem conta. Este é o fato que mais pesa na escolha abaixo.

## 2. Os três modelos

### A. Degustação por tempo

Conta nova ganha acesso completo por 3 ou 7 dias. Depois cai na tela de
compra, como quem deixou o plano vencer.

| | |
|---|---|
| A favor | O aluno vê o produto inteiro. Mensagem simples ("7 dias grátis"). Reaproveita quase tudo que os planos já têm: prazo, contagem de dias, tela de acesso vencido. |
| Contra | Entrega o curso todo a qualquer e-mail. Com o conteúdo embutido no HTML, basta salvar a página durante o teste para ficar com tudo. Conta nova com outro e-mail renova o teste sem limite. Pede e-mail de aviso, que depende de SMTP próprio (pendência aberta na Etapa 0.2). Concorre com o Sprint: 7 dias grátis são um quarto do plano de 30 dias. |

### B. Freemium por conteúdo

Conta gratuita, sem prazo, vê uma amostra fixa. O resto aparece trancado, com
o convite para comprar.

Amostra sugerida (ajustável):

| O que | Por quê |
|---|---|
| **M0 inteiro** (9 Partes): diagnóstico, calculadora, cronogramas, plano de emergência | É o que orienta o aluno e mostra o método. Já é em parte público pelo diagnóstico. |
| **Parte 1 de M1, M2, M3 e M4** ("As regras do jogo" de cada seção) | Explica como cada seção funciona em 2026. É a parte mais informativa e a menos "exercício". |
| **Um exercício por seção:** 1 texto de Complete the Words (dos 8), 1 drill de Listening (dos 4), 1 cenário de Listen and Repeat (dos 9 conjuntos), 3 itens de Build a Sentence (dos 30) | Deixa o aluno sentir o formato de digitar, ouvir, repetir e montar frase. |
| **Parte 1 do M7** (a lógica dos simulados) e **nenhum simulado** | Os simulados são o que mais vale no fim do estudo. |
| **M5, M6, M8, M9:** só a Parte 1 de cada | Mostra que existem. |

Isso dá 18 Partes de 86, cerca de um quinto do texto, e uma fração bem
menor dos exercícios.

| | |
|---|---|
| A favor | Não tem relógio, então não tem e-mail de aviso, contador nem conta repetida para burlar: a amostra é a mesma para todo mundo. O aluno pode voltar quando quiser, e a conta gratuita vira lista de contatos. Não concorre com nenhum plano. |
| Contra | Exige bloqueio por Parte e por exercício, que hoje não existe (o bloqueio atual é tudo ou nada). Escolher a amostra é decisão de produto e precisa de manutenção quando o conteúdo muda. O aluno não vê os simulados. |

### C. Os dois combinados

Freemium permanente (B) e, uma vez por conta, um botão "liberar tudo por 3
dias" (A).

| | |
|---|---|
| A favor | A amostra segura o aluno indeciso; a degustação fecha a venda de quem quer ver os simulados antes de pagar. |
| Contra | Soma os custos dos dois, e herda o problema de exposição do modelo A. |

## 3. Como conversa com o que já existe

**Tela de apresentação e diagnóstico.** O funil fica em três degraus:
diagnóstico sem conta (já feito), conta gratuita com amostra, plano pago.
A tela de apresentação ganha um quarto cartão ou uma faixa "Comece grátis",
e o painel de resultado do diagnóstico passa a oferecer "Criar conta
gratuita" ao lado de "Ver os planos". O diagnóstico respondido lá já aparece
no M0 da conta nova (mesma chave de `localStorage`), o que dá continuidade.

**Três planos.** No freemium, quem compra só destranca o resto: nada muda
nos planos. Na degustação por tempo, o teste entra como um "plano" a mais no
extrato, com as perguntas que precisam de resposta: os dias de teste somam
ao plano comprado durante o teste, ou o plano começa do pagamento? (Sugestão:
não somam. O teste termina na compra.)

**Reembolso de 7 dias.** Continua valendo igual. Com degustação de 7 dias
mais reembolso de 7 dias, o aluno tem até 14 dias de acesso completo sem
custo. Com 3 dias, até 10. É motivo para preferir 3 dias, se houver
degustação.

## 4. O que muda no código e no banco

### Freemium por conteúdo (B)

| Onde | O quê |
|---|---|
| `app/free_sample.json` (novo) | A lista do que é aberto: por módulo, as Partes e os ids de exercício. Fonte única, lida pelo build. |
| `app/build_pipeline.py`, `app/build.py` | Marcar cada `.section-card` e cada widget com `data-free`. Falhar o build se a lista citar Parte que não existe. |
| `app/app.js` | Hoje `checkEntitlement()` esconde ou mostra a tela de compra inteira. Passa a existir um nível de acesso (`sem conta`, `gratuito`, `completo`). No gratuito, a tela de compra não cobre o site: cada Parte paga mostra um cartão "Parte do curso completo" com o botão de planos, e a navegação marca o que é trancado. |
| Progresso | Decidir se a porcentagem do módulo conta só as Partes abertas para a conta gratuita (sugestão: sim, senão o aluno gratuito nunca passa de 15%). O certificado continua exigindo o curso completo. |
| Banco | **Nada.** Conta sem linha em `entitlements` já é a conta gratuita. |
| Tela de apresentação | Texto e botão "Criar conta gratuita". |
| Smoke test | Conta gratuita vê exatamente a lista; conta paga vê tudo; nada trancado fica clicável. |

### Degustação por tempo (A)

| Onde | O quê |
|---|---|
| Banco | Reaproveita o que os planos criaram. O teste é uma linha em `payments` com `plan = 'teste'`, `amount = 0` e id fixo `teste-<id do usuário>`. Como o id é a chave da tabela, cada conta só consegue um teste. `entitlements` ganha o prazo pelo `recompute_entitlement()` de sempre. Falta decidir a regra de soma com planos pagos e ajustar a função. |
| `supabase/functions/start-trial` (nova) | Chamada pelo botão "Começar teste". Confere o login e chama `apply_payment` com o `service_role`. Precisa de deploy e de autorização do dono. |
| `app/app.js` | Botão de começar o teste na tela de compra; faixa "Seu teste termina em N dias" (o `accessState()` já calcula os dias); texto próprio na tela de acesso vencido ("Seu teste terminou"). |
| E-mail de aviso | Um dia antes do fim e no fim. Depende de SMTP próprio no Supabase (aberto na Etapa 0.2), de uma tarefa agendada (function agendada ou `pg_cron`) e de um texto. A Política de Privacidade precisa citar esse e-mail. |
| `legal/termos.md` | Seção sobre o teste: duração, uma vez por pessoa, sem cobrança automática no fim. |

### Os dois (C)

A soma das duas tabelas acima.

## 5. Proteção real: o que um teste grátis expõe

**Hoje, sem versão gratuita nenhuma, o conteúdo já está exposto.** O
`index.html` é público e traz os 10 módulos dentro. A tela de login e a de
compra são uma camada por cima. Ninguém precisa de conta para ler o código
da página.

O que cada modelo acrescenta a esse risco:

- **Freemium (B), como bloqueio visual:** tecnicamente nada. O que muda é que
  mais gente chega até o site com conta e vê cartões "trancado", o que
  convida a procurar. Quem procura acha.
- **Degustação (A):** além do acima, entrega o curso inteiro pela porta da
  frente, de forma legítima, por alguns dias. Não é preciso saber abrir o
  código: "Salvar página como" basta, e a cópia funciona offline porque o
  site foi feito para isso.

O que resolve, e em que grau:

| Medida | O que protege | Custo |
|---|---|---|
| **Build de amostra separado.** A conta gratuita abre um `amostra.html` gerado só com as Partes abertas. O conteúdo pago não está nesse arquivo. | A amostra deixa de carregar o curso pago. Mas o `index.html` completo continua público no mesmo servidor. | Baixo (o `scripts/build_teste.py` já gera um site alternativo). Sozinho não fecha a porta. |
| **Etapa 2: conteúdo servido do banco.** O HTML público traz só a casca; cada módulo é buscado depois do login, e a RLS só entrega a quem tem acesso em dia (`has_paid_access()` já olha o prazo). `supabase/schema-content-optional.sql` e `schema-bank.sql` são o começo disso. | Quem não pagou não recebe o conteúdo pago. É a única medida que torna o prazo dos planos e o bloqueio por Parte reais. | Alto: muda como o site carrega, o modo offline do PWA e o custo de banco. |
| **Nada resolve** a cópia por quem tem acesso legítimo | Aluno pagante ou em teste sempre pode copiar o que vê. Isso vale para qualquer curso online. | Só os Termos de Uso (item 8) tratam disso. |

**Consequência prática:** antes da Etapa 2, o freemium é honesto sobre o que
é (uma vitrine com cartões trancados) e a degustação por tempo é entregar o
produto. Depois da Etapa 2, os dois passam a ser bloqueios de verdade.

## 6. Riscos

**Abuso com várias contas.**
No freemium não há o que abusar: a amostra é igual para todos. Na
degustação, cada e-mail novo é um teste novo. O que reduz, sem eliminar:
religar "Confirm email" (pendência da Etapa 0.2), exigir login com Google
para o teste, guardar no aparelho que um teste já foi usado (fácil de
contornar), e captcha no cadastro. Nada disso segura quem quer de verdade, o
que é mais um motivo para o teste ser curto.

**Custo e limites do Supabase.**
Conta gratuita é usuário ativo do mesmo jeito: entra na contagem de usuários
do plano, ocupa uma linha de `user_state` (o progresso em JSON) e manda
e-mail de confirmação e de senha. Três pontos para conferir no painel antes
de abrir cadastro gratuito, porque os limites do plano grátis mudam: teto de
usuários ativos por mês, tamanho do banco, e o limite de envio de e-mail,
que já estourou só com testes. Cadastro aberto também atrai robô: captcha e
confirmação de e-mail passam a ser necessários, não opcionais.

**Efeito na receita.**
Amostra generosa demais reduz o motivo de comprar; teste longo demais
substitui o Sprint. Os dois se ajustam com medição, não com palpite.

**Suporte.** Mais contas, mais pedido de ajuda com login. Hoje não há canal
de suporte definido.

## 7. Como medir conversão

Sem ferramenta nova, com o que o banco já guarda:

```sql
-- contas criadas por semana e quantas compraram (qualquer plano)
select date_trunc('week', p.created_at) as semana,
       count(*) as contas,
       count(distinct pay.user_id) as compraram
from profiles p
left join payments pay on pay.user_id = p.id and pay.status = 'approved' and pay.plan <> 'teste'
group by 1 order by 1;
```

Com isso dá para acompanhar: taxa de conta para compra, dias entre criar a
conta e comprar, e qual plano quem veio do gratuito escolhe. Na degustação,
a linha `teste` em `payments` dá ainda "começou o teste" e "comprou durante
ou depois".

O que **não** dá para medir sem acrescentar algo: quantos visitam a tela de
apresentação, quantos terminam o diagnóstico sem conta e quais Partes
trancadas recebem clique. Para isso é preciso um contador de páginas que não
use cookie (há opções gratuitas) ou uma tabela de eventos própria. Qualquer
uma das duas entra na Política de Privacidade.

Meta para decidir se vale manter: definir antes de lançar. Sugestão de
partida, a rever com dado real: comparar a taxa de compra de quem criou conta
gratuita com a de quem foi direto para a compra, por quatro semanas.

## 8. Esforço e ordem

Estimativa em sessões de trabalho como as de hoje. São ordens de grandeza,
não promessa.

| Etapa | Depende de | Esforço |
|---|---|---|
| 1. Freemium visual: lista da amostra, bloqueio por Parte e por exercício, cartões trancados, progresso da conta gratuita, tela de apresentação, testes | Decisão sobre a amostra | 2 sessões |
| 2. Captcha no cadastro e "Confirm email" religado | Dono (painel do Supabase) e SMTP próprio | 1 sessão, mais os passos do dono |
| 3. Medição: a consulta acima e um contador de páginas | Decisão sobre a ferramenta | Meia sessão |
| 4. Etapa 2 do ROADMAP: conteúdo pago servido do banco | SQL e deploy autorizados | Várias sessões. Já é o próximo grande bloco do projeto. |
| 5. Degustação por tempo: function `start-trial`, regra de soma, faixa de dias, termos | Etapa 4 feita, para o teste não entregar o curso | 1 sessão, mais deploy |
| 6. E-mail de aviso do fim do teste | SMTP próprio e tarefa agendada | 1 sessão, mais deploy |

## 9. Recomendação

**Fazer o freemium por conteúdo (B) agora, e deixar a degustação por tempo
para depois da Etapa 2.**

Motivos, em ordem de peso:

1. **Exposição.** Com o curso inteiro dentro do HTML, degustação por tempo é
   dar o produto a qualquer e-mail. O freemium não piora o que já existe.
2. **Abuso.** No freemium não há teste para renovar com conta nova.
3. **Dependências.** O freemium não precisa de SQL, de function nova, de
   SMTP nem de tarefa agendada. A degustação precisa de quase todos.
4. **O teste sem risco já existe.** O reembolso de 7 dias cobre quem quer ver
   o curso inteiro antes de decidir, e o dono já decidiu oferecê-lo.
5. **Não concorre com o Sprint.**

Quando a Etapa 2 estiver pronta, vale reabrir a conversa sobre o modelo C,
com teste de **3 dias**, uma vez por conta: aí o prazo é cobrado pelo banco
e o teste deixa de ser uma cópia grátis.

## 10. O que o dono precisa decidir

1. Qual modelo: A, B, C, ou nenhum por enquanto.
2. Se B ou C: a amostra da seção 2 está boa, ou muda o quê?
3. Se A ou C: 3 ou 7 dias, e se os dias de teste somam ao plano comprado.
4. Conta gratuita conta progresso só sobre as Partes abertas?
5. Qual ferramenta de medição, se alguma, pode entrar no site.
