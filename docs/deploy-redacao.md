# Ligar o envio de redação para correção: passo a passo para o dono

**Escrito em:** 2026-10-14
**Estado:** o código está pronto e commitado. **Nada foi executado fora do
repositório:** nenhum SQL rodou, nenhuma function foi publicada, nenhum
segredo foi configurado e nenhuma API de IA foi chamada ou configurada.

Cada passo abaixo é uma das ações que o `AGENTS.md` reserva ao dono. A ordem
importa: **SQL, depois a sua conta como corretora, depois as functions,
depois a conferência da versão publicada, depois o teste de ponta a ponta.**

## O que você precisa saber antes

- **Correção assistida.** O site não chama IA nenhuma. No painel do corretor,
  o botão "Copiar para a IA" copia um pedido pronto (enunciado, texto do
  aluno, rubrica e o formato JSON da devolutiva). Você cola na sua ferramenta
  de IA, traz o JSON de volta, confere, ajusta o que quiser e clica em
  "Devolver". Não há custo de API no site.
- **O texto do aluno vai como dado.** No pedido, ele fica entre marcadores
  `<redacao_do_aluno>` e a instrução manda não obedecer a nada escrito ali.
  Se o aluno escrever o próprio marcador, ele é trocado antes de copiar.
- **As functions nunca rodaram.** Esta máquina não tem Deno nem Node:
  `submit-essay` e `review-essay` foram revisadas por leitura e pelo smoke
  test (as regras de prazo, intervalo, nota e formato rodam no Chrome do
  teste, porque o site usa o mesmo arquivo). A primeira execução de verdade é
  o deploy. Por isso o teste do passo 6 não é opcional.
- **O site novo funciona com o banco antigo.** Sem a tabela de redações, a
  tela abre, mostra os temas e as regras e o histórico fica vazio; o envio
  falha com mensagem. Nada mais quebra.
- **As functions novas não funcionam sem o SQL do passo 1.**
- **Pré-requisitos:** o `supabase/schema.sql` e a migração
  `supabase/migrations/20261008_planos.sql` já rodaram (a function de envio
  confere `entitlements.expires_at`).

## As regras e onde elas moram

| Regra | Valor | Onde |
|---|---|---|
| Frequência | 1 envio a cada 4 dias, contados do último | `_shared/redacao.js` e, de novo, a função de banco `create_essay_submission` |
| Devolução | até 3 dias úteis, sem fim de semana nem feriado nacional (fixos, Carnaval, Sexta-feira Santa e Corpus Christi) | `_shared/redacao.js` (`redacaoPrevisao`) |
| Tempo | 7 min (e-mail) e 10 min (discussão), sem pausa | `_shared/redacao.js` e `app/redacao.js` |
| Tamanho | discussão com no mínimo 100 palavras; até 600 palavras e 5000 caracteres | `_shared/redacao.js` e as restrições da tabela |
| Quem envia | conta com acesso em dia (ou corretora) | `submit-essay` |
| Nota | 4 critérios de 0 a 5; final é a média arredondada ao meio ponto, com teto de 2,5 se o cumprimento for 2 ou menos | `_shared/redacao.js` (`redacaoNotaFinal`), recalculada no servidor na devolução |

`supabase/functions/_shared/redacao.js` é um arquivo só para o servidor e o
site: o `build.py` cola ele no `index.html`. Mudou uma regra ali, é preciso
rebuildar o site **e** publicar de novo as duas functions.

## Passo 1: rodar o SQL

1. Abra o Supabase, **SQL Editor > New query**.
2. Cole o conteúdo inteiro de `supabase/migrations/20261014_redacoes.sql` e
   clique em **Run**. Rodar duas vezes não estraga nada.
3. Confira:

   ```sql
   select tablename, rowsecurity from pg_tables
   where tablename in ('essay_submissions', 'admins');
   ```

   As duas linhas têm de aparecer com `rowsecurity = true`.

O que foi criado: a tabela `essay_submissions` (aluno lê só as suas; corretor
lê todas; ninguém escreve pelo navegador), a tabela `admins` (quem corrige) e
a função `create_essay_submission`, que só a function de envio pode chamar.

## Passo 2: marcar a sua conta como corretora

Ser corretor é ter uma linha na tabela `admins`. O site não tem como criar
essa linha: só o SQL Editor. Troque o e-mail e rode:

```sql
insert into admins (user_id)
select id from auth.users where email = 'SEU-EMAIL@exemplo.com'
on conflict do nothing;

select a.user_id, u.email from admins a join auth.users u on u.id = a.user_id;
```

A segunda consulta tem de mostrar a sua conta. Para tirar o papel depois:
`delete from admins where user_id = (select id from auth.users where email = '...');`

## Passo 3: publicar as duas functions

No terminal, na pasta do projeto (já ligada ao projeto do Supabase):

```powershell
supabase functions deploy submit-essay
supabase functions deploy review-essay
```

As duas usam a verificação de JWT padrão (não entram no `config.toml`): só
aluno logado chama. **Confira a versão publicada** em Dashboard > Edge
Functions > cada uma > aba Code: o deploy deste projeto já disse "sucesso"
sem atualizar o código. Na aba Code, `submit-essay` tem de importar
`../_shared/redacao.js`.

## Passo 4 (opcional): e-mail de aviso

Sem SMTP, o aluno é avisado só no site: selo "devolutiva nova" em Minha conta
e um ponto na engrenagem. Quando o SMTP próprio existir (pendência 0.2 do
ROADMAP), configure os segredos e o aviso por e-mail liga sozinho, sem novo
deploy:

```powershell
supabase secrets set SMTP_HOST=smtp.seuprovedor.com SMTP_PORT=465 SMTP_USER=usuario SMTP_PASS=senha SMTP_FROM="iTOEFL <nao-responda@seudominio.com>" SITE_URL=https://endereco-do-site
```

`SMTP_PORT` 465 usa TLS direto; 587 usa STARTTLS. O e-mail diz só que a
redação foi corrigida, a nota e o nível, com o link do site. Falha no e-mail
não desfaz a devolução: fica no log da `review-essay`.

## Passo 5: preencher o nome da ferramenta de IA

A política de privacidade tem dois campos `[PREENCHER: nome da ferramenta de
IA usada na correção]` (seção 4 e tabela de fornecedores). Preencha com a
ferramenta que você vai usar, rebuilde e passe as seções novas pelo advogado:
privacidade, seção 4; termos, seção 5 (as duas marcadas `REVISAR (advogado)`).

## Passo 6: teste de ponta a ponta

Use uma **segunda conta**, de aluno, com acesso liberado à mão (cortesia):

```sql
select public.apply_payment('manual-redacao-teste', '<uuid da conta de aluno>',
                            'standard', 90, 0, 'approved', now());
```

1. **Envio.** Na conta de aluno: M4, fim da Parte 4, "Escolher um tema" (ou
   Minha conta > Correção de redação). Escolha D1. A tela "antes de começar"
   mostra o objetivo e as 9 regras. Comece, escreva menos de 100 palavras e
   clique em "Terminar e revisar o envio": o envio fica travado com
   "Faltam N palavras". Volte ao texto, passe de 100, marque o consentimento
   e envie. Tem de aparecer a data prevista (3 dias úteis) e "Próximo envio
   liberado em DD/MM".
2. **Banco.** `select topic_id, word_count, status, due_on, consented_at from essay_submissions order by submitted_at desc limit 1;`
   Estado `na_fila`, `consented_at` preenchido.
3. **Intervalo.** Tente enviar de novo: a tela já bloqueia com "Próximo envio
   liberado em". O servidor também recusa.
4. **Sem acesso.** Numa terceira conta sem plano (ela fica na tela de
   compra), confirme que não há como chegar ao envio.
5. **Cronômetro.** Na sua conta corretora (que também pode enviar, para
   testar), comece um tema, feche a janela, espere e reabra: o tempo continuou
   correndo. Ao zerar, o texto trava. Descarte no fim.
6. **Correção.** Na sua conta: Minha conta > Painel do corretor. A redação
   aparece na fila, com o prazo. Abra (o estado vira `em_correcao`), clique em
   "Copiar para a IA", cole na sua ferramenta, traga o JSON, cole no campo e
   clique em "Conferir e preencher o formulário". Teste também colar um JSON
   quebrado: a mensagem diz o que está errado. Ajuste um campo, veja a nota
   final mudar e clique em "Devolver ao aluno".
7. **Aluno.** Na conta de aluno, recarregue: Minha conta mostra "1
   devolutiva nova" e a engrenagem tem um ponto. Abra a devolutiva: nota e
   nível, os 4 critérios, os trechos, a reescrita, a prioridade com o botão
   que abre a Parte certa, e o gráfico.
8. **Quem vê o quê.** A conta de aluno não tem o botão "Painel do corretor"
   e o histórico dela só lista as redações dela. Com duas contas de aluno, a
   segunda não vê a redação da primeira.
9. **Limpeza.** Apague os envios de teste e a cortesia:

   ```sql
   delete from essay_submissions where user_id = '<uuid da conta de aluno>';
   select public.apply_payment('manual-redacao-teste', null, null, null, null, 'refunded', null);
   ```

## Se algo der errado

- **"Não deu para registrar a redação agora"**: veja o log da
  `submit-essay` (Dashboard > Edge Functions > Logs). Causa mais provável: o
  SQL do passo 1 não rodou.
- **Painel do corretor não aparece**: confira a linha em `admins` (passo 2) e
  saia e entre de novo na conta.
- **Desligar o recurso sem apagar nada**: `delete from admins;` tira o
  painel, e `supabase functions delete submit-essay` impede novos envios. As
  redações já enviadas continuam no banco.
