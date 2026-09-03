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
      <span class="mark">Prep oficial</span>
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
    <div class="foot-note">Reconstruído sobre as especificações ETS vigentes desde 21/jan/2026. Seu progresso é salvo neste navegador.</div>
  </aside>

  <main id="mainArea">
    {panels}
  </main>
</div>

<script>
{JS}
</script>
'''

open("../artifact/index.html", "w", encoding="utf-8").write(html)
print("written", len(html))
