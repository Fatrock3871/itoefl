"""Renderiza os conjuntos de Speaking do M3: Listen and Repeat e Take an Interview.

Nos dois o aluno ouve antes de ver: o texto fica escondido até ele pedir.
mode "repeat": ouvir, repetir e marcar se saiu igual.
mode "interview": ouvir a pergunta e responder com contagem regressiva.
"""

import html

INTERVIEW_SECONDS = 45


def render_speaking_set(item, mode):
    rows = []
    for i, text in enumerate(item["items"], 1):
        if mode == "repeat":
            marks = (
                '<span class="spk-marks" hidden>'
                '<button type="button" class="spk-mark" data-mark="ok">Repeti igual</button>'
                '<button type="button" class="spk-mark" data-mark="miss">Errei algo</button>'
                '</span>'
            )
        else:
            marks = (
                '<span class="spk-clock" hidden></span>'
                '<span class="spk-marks" hidden>'
                '<button type="button" class="spk-mark" data-mark="ok">Respondi</button>'
                '</span>'
            )
        rows.append(f'''
  <div class="spk-item" data-num="{i}" data-text="{html.escape(text, quote=True)}">
    <span class="spk-num">{i}</span>
    <div class="spk-body">
      <div class="spk-controls">
        <button type="button" class="spk-play">▶ Ouvir</button>
        <button type="button" class="spk-show">Mostrar texto</button>
        {marks}
      </div>
      <p class="spk-text" hidden>{html.escape(text)}</p>
    </div>
  </div>''')
    seconds = f' data-seconds="{INTERVIEW_SECONDS}"' if mode == "interview" else ""
    return f'''
<div class="spk" data-spk="{html.escape(item["id"], quote=True)}" data-mode="{mode}"{seconds} data-level="{html.escape(item["level"], quote=True)}" data-lp-title="{'Listen and Repeat' if mode == 'repeat' else 'Take an Interview'} · {html.escape(item["title"], quote=True)}">
  <div class="spk-head"><span class="spk-title">{html.escape(item["title"])}</span><span class="spk-score"></span></div>
  <p class="spk-scenario">{html.escape(item["scenario"])}</p>
  {"".join(rows)}
  <div class="spk-foot">
    <span class="spk-nosound" hidden>Este navegador não tem voz sintética. Use "Mostrar texto" e leia a frase uma vez antes de repetir.</span>
    <button type="button" class="spk-retry" hidden>Refazer este conjunto</button>
  </div>
</div>'''


def render_speaking_group(items, mode):
    return "".join(render_speaking_set(it, mode) for it in items)
