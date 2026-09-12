import json

frag = json.load(open("module_fragments_final.json", encoding="utf-8"))

MODS = [
    ("mod0","00","Embarque & Diagnóstico","modulo_0_embarque.md",
     "Onde você está e para onde vai. Comece pelo diagnóstico de nivelamento."),
    ("mod1","01","Reading","modulo_1_reading.md",
     "Ler rápido e decidir item a item no formato adaptativo de Reading."),
    ("mod2","02","Listening","modulo_2_listening.md",
     "Decodificar o áudio na primeira passada: escuta ativa e anotação."),
    ("mod3","03","Speaking","modulo_3_speaking.md",
     "Fonética, prosódia e respostas por função para o SpeechRater."),
    ("mod4","04","Writing","modulo_4_writing.md",
     "Frases precisas, e-mail navegacional e discussão acadêmica."),
    ("mod5","05","Registro & Retórica","modulo_5_registro.md",
     "A camada que separa 'correto' de 'banda alta': registro e densidade."),
    ("mod6","06","Vocabulário","modulo_6_vocabulary.md",
     "Reconhecer para ler; ativar para falar e escrever sob pressão."),
    ("mod7","07","Simulados","modulo_7_simulados.md",
     "Quatro simulados progressivos e a análise de erros que liga tudo."),
    ("mod8","08","Exam Day","modulo_8_examday.md",
     "As 24 horas antes e o protocolo seção a seção no dia da prova."),
    ("mod9","09","Brazilian Traps","modulo_9_braziliantraps.md",
     "O padrão de erro do brasileiro, mapeado e eliminado."),
]

nav_items = "\n".join(
    f'<button class="tabbtn" data-tab="{k}" data-title="{t}">'
    f'<span class="num-badge" data-n="{n}">{n}</span>'
    f'<span class="lbl">{t}</span>'
    f'<span class="pbadge" id="badge-{k}"></span></button>'
    for k, n, t, _, _tag in MODS
)

# mapa da jornada (roadmap fixo no topo do conteúdo)
JOURNEY_SHORT = {
    "mod0": "Embarque", "mod1": "Reading", "mod2": "Listening", "mod3": "Speaking",
    "mod4": "Writing", "mod5": "Registro", "mod6": "Vocabulário", "mod7": "Simulados",
    "mod8": "Exam Day", "mod9": "Traps",
}
journey_nodes = "\n".join(
    f'<button class="jnode" data-tab="{k}" data-title="{t}">'
    f'<span class="jdot" data-n="{n}">{n}</span>'
    f'<span class="jlbl">{JOURNEY_SHORT[k]}</span></button>'
    for k, n, t, _, _tag in MODS
)
journey = (
    '<nav class="journey" id="journey" aria-label="Mapa da jornada">'
    '<div class="journey-row">'
    '<div class="journey-left">'
    '<button class="hamburger" id="sideToggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="sideRail">'
    '<span></span><span></span><span></span></button>'
    '<p class="journey-title">Sua jornada: conclua 70% para avançar</p>'
    '</div>'
    '<div class="journey-tools">'
    '<button class="themetoggle" id="themeToggle" type="button" aria-label="Alternar tema">'
    '<span id="themeIcon">🌗</span><span id="themeLabel">Sistema</span></button>'
    '<div class="auth-box" id="authBox" hidden>'
    '<button type="button" id="authSignIn">Entrar para sincronizar</button>'
    '<div id="authIn" hidden>'
    '<span class="auth-avatar" id="authAvatar" aria-hidden="true"></span>'
    '<span id="authEmail" class="auth-email"></span>'
    '<button type="button" id="authSignOut">Sair</button></div>'
    '<span id="authMsg" class="auth-msg" hidden></span></div>'
    '</div></div>'
    f'<div class="jtrack-wrap"><div class="jtrack">{journey_nodes}</div></div>'
    '</nav>'
)

panels = "\n".join(
    f'<section class="panel" data-panel="{k}" id="panel-{k}" {"hidden" if k != "mod0" else ""}>'
    f'<div class="panel-inner">'
    f'<header class="panel-head"><span class="ph-num">{n}</span>'
    f'<span class="ph-text"><h1>{t}</h1><p>{tag}</p></span></header>'
    f'{frag[k]}</div></section>'
    for k, n, t, _, tag in MODS
)

CSS = open("styles.css", encoding="utf-8").read()
JS = open("app.js", encoding="utf-8").read()

# ---- Supabase (opcional): só entra se app/supabase_config.json existir e estiver preenchido ----
supa_url = supa_key = ""
try:
    with open("supabase_config.json", encoding="utf-8-sig") as _f:
        _cfg = json.load(_f)
    supa_url = (_cfg.get("url") or "").strip()
    supa_key = (_cfg.get("anonKey") or "").strip()
    if "SEU-PROJETO" in supa_url or "SUA-ANON" in supa_key:
        supa_url = supa_key = ""
except FileNotFoundError:
    pass
except (json.JSONDecodeError, OSError) as _e:
    print(f"supabase: config invalida ({_e}) — seguindo offline")

SUPA_HEAD = ""
if supa_url and supa_key:
    SUPA_HEAD = (
        f'<script>window.ITOEFL_SUPABASE={json.dumps({"url": supa_url, "anonKey": supa_key})};</script>\n'
        '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'
    )
    print("supabase: configurado")
else:
    print("supabase: nao configurado (modo offline)")

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>iTOEFL</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="shell">
  <div class="side-backdrop" id="sideBackdrop"></div>
  <aside class="side" id="sideRail">
    <div class="side-top">
      <div class="brand">
        <span class="logo">iT</span>
        <span class="btxt">
          <span class="name">iTOEFL</span>
          <span class="mark">Preparação independente</span>
        </span>
      </div>
      <button class="side-close" id="sideClose" type="button" aria-label="Fechar menu">✕</button>
    </div>
    <div class="overall-progress">
      <div class="op-label"><span>Progresso geral</span><span id="opPct">0%</span></div>
      <div class="op-bar"><div class="op-fill" id="opFill"></div></div>
      <div class="op-count" id="opCount"></div>
    </div>
    <div class="level-badge" id="levelBadge" hidden>
      <span class="level-badge-tag">Nível estimado (diagnóstico)</span>
      <span class="level-badge-band" id="levelBadgeBand"></span>
      <span class="level-badge-sched" id="levelBadgeSched"></span>
    </div>
    <nav class="modnav" id="modnav">
      {nav_items}
    </nav>
    <div class="lock-msg" id="lockMsg" hidden></div>
    <div class="data-tools">
      <button type="button" id="dataExport">↓ Exportar progresso</button>
      <button type="button" id="dataImport">↑ Importar</button>
      <input type="file" id="dataFile" accept="application/json,.json" hidden>
      <span id="dataMsg" class="data-msg" hidden></span>
    </div>
    <div class="foot-note">Preparação independente baseada nas especificações ETS vigentes desde 21/jan/2026. Não afiliada à ETS. Seu progresso é salvo neste navegador.</div>
  </aside>

  <main id="mainArea">
    {journey}
    <div class="content-grid">
      <div class="content-col">{panels}</div>
      <aside class="rail" id="rail">
        <p class="rail-title">Nesta parte</p>
        <nav class="rail-toc" id="railToc"></nav>
      </aside>
    </div>
  </main>
</div>

<div class="float-tools">
  <div id="micRec" class="mic-rec collapsed">
    <div class="mr-panel">
      <div class="mr-display" id="mrDisplay">00:00</div>
      <div class="mr-status" id="mrStatus">Grave sua resposta e ouça de volta.</div>
      <audio id="mrAudio" class="mr-audio" controls hidden></audio>
      <div class="mr-controls">
        <button type="button" id="mrToggleBtn" class="st-primary">● Gravar</button>
        <button type="button" id="mrClear" hidden>Nova</button>
      </div>
    </div>
    <button class="st-toggle" id="mrToggle" type="button" aria-label="Gravador de voz">
      <span>🎙</span>
    </button>
  </div>
  <div id="secTimer" class="sec-timer collapsed">
    <div class="st-panel">
      <div class="st-display" id="stDisplay">28:00</div>
      <div class="st-presets" id="stPresets">
        <button type="button" data-min="28" class="active">Reading 28′</button>
        <button type="button" data-min="18">Listening 18′</button>
        <button type="button" data-min="8">Speaking 8′</button>
        <button type="button" data-min="23">Writing 23′</button>
        <button type="button" data-min="85">Prova completa 85′</button>
      </div>
      <div class="st-controls">
        <button type="button" id="stStart" class="st-primary">Iniciar</button>
        <button type="button" id="stReset">Zerar</button>
      </div>
    </div>
    <button class="st-toggle" id="stToggle" type="button" aria-label="Cronômetro de seção">
      <span id="stFace">⏱</span>
    </button>
  </div>
</div>

{SUPA_HEAD}
<script>
{JS}
</script>
</body>
</html>
'''

open("../artifact/index.html", "w", encoding="utf-8").write(html)
print("written", len(html))
