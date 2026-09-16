"""Shared renderer for interactive quiz-drill widgets (select -> confirm -> reveal -> retry)."""


def render_quiz_drill(drill_id, title, objective, passage_html, items):
    cards = []
    for it in items:
        opts = "".join(
            f'<button class="opt" data-letter="{L}">'
            f'<span class="oletter">{L}</span><span class="otext">{txt}</span></button>'
            for L, txt in it["options"].items()
        )
        multi_attr = f' data-multi="{it["multi"]}"' if it.get("multi") else ""
        cards.append(f'''
<div class="qcard" data-correct="{it['correct']}" data-num="{it['num']}"{multi_attr}>
  <div class="qhead"><span class="qnum">{it['num']}</span></div>
  <p class="qprompt">{it['prompt']}</p>
  <div class="qopts">{opts}</div>
  <button class="qconfirm" type="button" hidden>Confirmar resposta</button>
  <div class="qfeedback" hidden>
    <p><strong>Explicação:</strong> {it['explanation']}</p>
  </div>
</div>''')
    passage_block = f'<div class="quiz-passage">{passage_html}</div>' if passage_html else ""
    heading = f'<h3>{title}</h3>' if title else ""
    return f'''
{heading}
<p class="quiz-objective">{objective}</p>
{passage_block}
<div class="quiz-drill" data-drill="{drill_id}">
  <div class="quiz-bar"><div class="quiz-bar-fill"></div></div>
  <p class="quiz-score">0 de {len(items)} respondidas</p>
  {"".join(cards)}
  <div class="quiz-summary" hidden>
    <span class="quiz-summary-text"></span>
    <button class="quiz-retry" type="button">Refazer este exercício</button>
  </div>
</div>'''
