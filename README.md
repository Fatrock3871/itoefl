# iTOEFL

Plataforma de estudo para o TOEFL iBT no formato 2026, em português, para
candidatos brasileiros. Dez módulos (M0 a M9), site estático gerado por um
pipeline em Python a partir de Markdown, com login, sincronização de progresso
e pagamento via Supabase.

Preparação independente. Sem vínculo com a ETS.

## Comece por aqui

| Arquivo | Para quê |
|---|---|
| `ROADMAP.md` | O que falta fazer. A seção "Tudo que falta", no topo, é a lista única de pendências |
| `CLAUDE.md` | Arquitetura, convenções e o formato 2026 da prova. Leitura obrigatória antes de mexer |
| `docs/roadmap-expansao.md` | Plano das próximas frentes: app, videoaulas, banco de questões, correção por IA |
| `docs/supabase-setup.md` | Como configurar o backend |
| `docs/mercadopago-setup.md` | Como configurar o pagamento |

## Rodar na sua máquina

Requisitos: Python 3.13 e o pacote `markdown`. Não há Node.

```powershell
python -m pip install markdown
cd app
python build_pipeline.py     # consolidated/*.md  ->  app/module_fragments_final.json
python build.py              # fragmentos + CSS + JS  ->  artifact/index.html
cd ..
python scripts\serve.py      # abre http://localhost:8000/artifact/index.html
```

Sem configuração nenhuma o site sobe em **modo offline**: todo o conteúdo
aberto, progresso salvo só no navegador, sem login nem pagamento. É o
suficiente para trabalhar em conteúdo, estilo e widgets.

Para testar login, sincronização e pagamento, copie
`app/supabase_config.example.json` para `app/supabase_config.json` e preencha
com a URL e a chave pública do projeto Supabase. Peça os valores a quem
administra o projeto. Esse arquivo está no `.gitignore` e não deve ser
commitado.

## Regras que evitam retrabalho

- **Nunca edite arquivo gerado.** `artifact/index.html` e
  `app/module_fragments*.json` são sobrescritos a cada build e nem estão no
  repositório. Edite a fonte e rode as duas builds.
- **Onde fica cada coisa:**
  - Texto dos módulos: `consolidated/*.md`
  - Questões do diagnóstico: `app/quiz_mod0.json`
  - Drills de Reading e Listening: `app/drills_data.py`
  - Build a Sentence: `app/build_sentence_data.py`
  - Flashcards: `app/vocab_kit.json`
  - Comportamento: `app/app.js` e `app/render_*.py`
  - Estilo: `app/styles.css`
  - Banco e funções de servidor: `supabase/`
- **Teste antes de enviar:** `python scripts\smoke_test.py` builda o site e
  roda as checagens num Chrome headless. Precisa do Chrome instalado.
- **Idioma:** interface e explicações em português do Brasil. O conteúdo-alvo
  em inglês permanece em inglês.
- **Formato da prova:** vale o de 2026, descrito no `CLAUDE.md`. O material em
  `_archive/` é do formato antigo e não serve de referência.
- **Segredos:** nenhuma chave, token ou senha no repositório. Chaves de
  servidor ficam nos secrets do Supabase.

## Como contribuir

1. Crie uma branch a partir da principal.
2. Faça a mudança na fonte, rode as builds e o smoke test.
3. Abra um pull request descrevendo o que mudou e como foi verificado.
4. Ao concluir um item, marque-o no `ROADMAP.md`.
