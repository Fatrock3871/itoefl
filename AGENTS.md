# iTOEFL: instruções para agentes de IA

Este arquivo é lido por agentes que trabalham neste repositório (Hermes e
outros que seguem a convenção `AGENTS.md`). O Claude Code lê o `CLAUDE.md`.
Os dois valem juntos: o que está aqui não substitui o `CLAUDE.md`.

## Leia antes de qualquer coisa

1. `ROADMAP.md`, seção "Tudo que falta". É a lista única de pendências e a
   memória entre sessões. Cada item diz quem faz: **(U)** só o usuário,
   **(C)** código ou conteúdo, **(D)** decisão do usuário.
2. `CLAUDE.md`. Arquitetura, onde fica cada coisa, formato da prova, convenções.
3. `docs/ets-materiais-oficiais.md`, se a tarefa envolver exercício ou conteúdo.

## O que é o projeto

Plataforma de estudo para o TOEFL iBT no formato 2026, em português, para
brasileiros. Site estático gerado por Python a partir de Markdown, com
Supabase para login, sincronização e pagamento. Sem Node, sem framework.

## Papel de gerente do projeto

Se você está aqui para gerenciar, e não para programar, o seu trabalho é:

- **Manter o `ROADMAP.md` verdadeiro.** Marcar o que foi feito, registrar o
  que apareceu, nunca marcar como feito algo que não foi verificado.
- **Dizer qual é o próximo passo.** A Etapa 0 (publicar o site) bloqueia todo
  o resto. Enquanto ela estiver aberta, é ela que deve ser cobrada.
- **Lembrar o usuário das pendências (U).** Várias só ele resolve: trocar
  senhas expostas, validar a conta do gateway de pagamento, decidir
  hospedagem e preço, testar em celular.
- **Conferir a saúde do repositório.** `python scripts\smoke_test.py` tem que
  terminar com "Tudo passou". `git status` tem que estar limpo e em dia com
  `origin/main`.
- **Resumir, não repetir.** Relatório curto: o que mudou, o que está
  verificado, o que falta, qual decisão está esperando o usuário.

## Regras que valem para qualquer agente

- **Nunca editar arquivo gerado:** `artifact/*.html`, `app/module_fragments*.json`,
  `_teste/`. Edite a fonte e rode as duas builds.
- **Testar antes de commitar:** `python scripts\smoke_test.py`.
- **Commits pequenos, mensagem em português,** dizendo o que mudou e como foi
  verificado. Trabalhar em branch e abrir pull request quando houver mais de
  uma pessoa ou agente mexendo ao mesmo tempo.
- **Conteúdo da ETS não se copia nem se adapta de perto.** Só o formato.
- **Sem travessão como pausa em texto em português** (regra de estilo do
  usuário). Vírgula, dois-pontos ou frase curta. A regra não vale para o
  texto em inglês: em passagem, transcrição, resposta-modelo e exemplo, o
  travessão (—) é pontuação correta e fica. Nunca trocar travessão do inglês
  por ":" ou "·" (decisão de 2026-10-13).
- **Nenhum segredo no repositório.** `app/supabase_config.json` fica fora do Git.

## Só com autorização explícita do usuário

Estas ações são públicas, custam dinheiro ou não têm volta. Pergunte antes,
todas as vezes, mesmo que já tenha sido autorizado em outra ocasião:

- Publicar o site ou qualquer versão dele em endereço público.
- Rodar SQL no banco do Supabase ou publicar edge functions
  (`supabase functions deploy`).
- Mexer em preço, cupom, credenciais ou configuração do gateway de pagamento.
- Apagar dados, contas, branches ou histórico do Git (`push --force`, `reset --hard`).
- Tornar o repositório público ou convidar colaboradores.
- Qualquer coisa que gaste créditos de API de forma recorrente.

## Trabalho em dupla

O projeto tem duas pessoas: Pietro (conteúdo) e Gabriel (plataforma e pagamento).

- **A main é protegida.** Nada vai direto para ela. Tudo entra por pull request,
  revisado pela outra pessoa, com o teste automático
  (`.github/workflows/teste.yml`) verde.
- **Uma branch curta por tarefa,** com nome `nome/tarefa` (ex.: `gabriel/colaboracao`).
  Comece sempre de `git checkout main` e `git pull`, e envie a branch em 1 ou 2
  dias. Branch longa vira conflito.
- **Divisão por área.** Pietro: `consolidated/*.md` e os arquivos de dados
  (`app/*.json`, `app/*_data.py`, `bank/`). Gabriel: `app/app.js`, `supabase/` e
  o que envolve login e pagamento. Mexer na área do outro é possível, mas avise antes.
- **Antes de começar um item do `ROADMAP.md`,** escreva seu nome ao lado dele,
  para a outra pessoa não pegar o mesmo.
- **Arquivos que mais dão conflito:** `ROADMAP.md`, `CLAUDE.md` e `app/app.js`.
  Mudanças pequenas e `git pull` antes de editar.
- **Segredos só com o Pietro:** chaves do Stripe e chaves de servidor (Supabase
  `service_role`, secrets das functions). Gabriel trabalha só com a chave
  pública (ver `docs/publicar.md`). Nenhum segredo vai para o repositório.

## Quando dois agentes trabalham no mesmo repositório

Antes de mexer em arquivo: `git pull` e `git status`. Se houver mudança que
não é sua, não desfaça: avise o usuário. Ao terminar: build, smoke test,
commit na sua branch, push da branch (nunca da main), pull request, e uma
linha no `ROADMAP.md` dizendo o que foi feito.
