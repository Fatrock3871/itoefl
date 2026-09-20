"""Shared renderer for interactive quiz-drill widgets (select -> confirm -> reveal -> retry)."""


def render_quiz_drill(drill_id, title, objective, passage_html, items, listen=False):
    # listen=True (só M2, Listening): acrescenta um botão de ouvir em voz
    # alta (Web Speech API, sem áudio gravado) -- o item/passagem vira som
    # de verdade em vez de só transcrição lida em silêncio. Não mexe em M1
    # (Reading é treino de leitura silenciosa de propósito).
    item_listen_btn = (
        '<button type="button" class="speak-btn quiz-item-speak" aria-label="Ouvir">🔊</button>'
        if (listen and not passage_html) else ""
    )
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
  <p class="qprompt"><span class="qprompt-text">{it['prompt']}</span>{item_listen_btn}</p>
  <div class="qopts">{opts}</div>
  <button class="qconfirm" type="button" hidden>Confirmar resposta</button>
  <div class="qfeedback" hidden>
    <p><strong>Explicação:</strong> {it['explanation']}</p>
  </div>
</div>''')
    passage_listen_btn = (
        '<button type="button" class="speak-btn quiz-passage-speak">🔊 Ouvir áudio</button>'
        if (listen and passage_html) else ""
    )
    passage_block = (
        f'<div class="quiz-passage">{passage_listen_btn}<div class="quiz-passage-body">{passage_html}</div></div>'
        if passage_html else ""
    )
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
