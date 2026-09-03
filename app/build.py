import json

frag = json.load(open("module_fragments_final.json", encoding="utf-8"))

MODS = [
    ("mod0","00","Embarque & Diagnóstico","modulo_0_embarque.md"),
    ("mod1","01","Reading","modulo_1_reading.md"),
    ("mod2","02","Listening","modulo_2_listening.md"),
    ("mod3","03","Speaking","modulo_3_speaking.md"),
    ("mod4","04","Writing","modulo_4_writing.md"),
    ("mod5","05","Registro & Retórica","modulo_5_registro.md"),
    ("mod6","06","Vocabulário","modulo_6_vocabulary.md"),
    ("mod7","07","Simulados","modulo_7_simulados.md"),
    ("mod8","08","Exam Day","modulo_8_examday.md"),
    ("mod9","09","Brazilian Traps","modulo_9_braziliantraps.md"),
]

nav_items = "\n".join(
    f'<button class="tabbtn" data-tab="{k}"><span class="num">{n}</span>{t}<span class="pbadge" id="badge-{k}"></span></button>'
    for k, n, t, _ in MODS
)

panels = "\n".join(
    f'<section class="panel" data-panel="{k}" id="panel-{k}" {"hidden" if k != "mod0" else ""}>'
    f'<div class="panel-inner">{frag[k]}</div></section>'
    for k, n, t, _ in MODS
)

CSS = open("styles.css", encoding="utf-8").read()
JS = open("app.js", encoding="utf-8").read()

html = f'''<title>iTOEFL</title>
<style>
{CSS}
</style>

<div class="shell">
  <aside class="side">
    <div class="brand">
      <span class="mark">Preparação independente</span>
      <span class="name">iTOEFL</span>
    </div>
    <div class="overall-progress">
      <div class="op-label"><span>Progresso geral</span><span id="opPct">0%</span></div>
      <div class="op-bar"><div class="op-fill" id="opFill"></div></div>
    </div>
    <nav class="modnav" id="modnav">
      {nav_items}
    </nav>
    <button class="themetoggle" id="themeToggle" type="button" aria-label="Alternar tema">
      <span id="themeIcon">🌗</span><span id="themeLabel">Sistema</span>
    </button>
    <div class="data-tools">
      <button type="button" id="dataExport">↓ Exportar progresso</button>
      <button type="button" id="dataImport">↑ Importar</button>
      <input type="file" id="dataFile" accept="application/json,.json" hidden>
      <span id="dataMsg" class="data-msg" hidden></span>
    </div>
    <div class="foot-note">Preparação independente baseada nas especificações ETS vigentes desde 21/jan/2026. Não afiliada à ETS. Seu progresso é salvo neste navegador.</div>
  </aside>

  <main id="mainArea">
    {panels}
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

<script>
{JS}
</script>
'''

open("../artifact/index.html", "w", encoding="utf-8").write(html)
print("written", len(html))
