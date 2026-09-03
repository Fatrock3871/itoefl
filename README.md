# iTOEFL

Plataforma de preparação para o TOEFL iBT (2026), cobrindo os módulos:

- Módulo 0 — Embarque e Diagnóstico
- Módulo 1 — Reading
- Módulo 2 — Listening
- Módulo 3 — Speaking
- Módulo 4 — Writing
- Módulo 7 — Simulados

## Estrutura

```
consolidated/     conteúdo de cada módulo em markdown (fonte de verdade do texto)
app/              scripts de build (build_pipeline.py, build.py), dados de quiz/drills, JS/CSS do site
artifact/         index.html gerado — o site estático final
supabase/         schema.sql (tabelas de conteúdo + progresso do aluno) e quiz_export.json (dados para popular o banco)
```

## Build

```bash
cd app
python3 build_pipeline.py   # reconstrói module_fragments_final.json a partir de consolidated/*.md
python3 build.py            # monta artifact/index.html a partir dos fragments
```

## Banco de dados (Supabase)

O schema em `supabase/schema.sql` cria:

- **Conteúdo** (leitura pública): `modules`, `quiz_questions`, `drills`, `drill_items`
- **Progresso do aluno** (RLS — cada usuário só vê/escreve os próprios dados): `profiles`, `module_progress`, `quiz_attempts`, `drill_attempts`

`supabase/quiz_export.json` contém os dados extraídos de `quiz_mod0.json` e `drills_data.py` prontos para popular as tabelas de quiz/drills.
