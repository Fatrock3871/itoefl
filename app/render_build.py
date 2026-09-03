"""Renderiza o widget interativo de Build a Sentence (Writing / M4)."""

import html
import json


def render_build_sentence(bsq_id, items):
    cards = []
    for i, it in enumerate(items, 1):
        chips = "".join(
            f'<button type="button" class="bsq-chip" data-frag="{html.escape(f, quote=True)}" '
            f'data-idx="{j}">{html.escape(f)}</button>'
            for j, f in enumerate(it["fragments"])
        )
        answer = json.dumps(it["answer"], ensure_ascii=False).replace("<", "\\u003c")
        cards.append(f'''
<div class="bsq-card" data-num="{i}" data-answer='{html.escape(answer, quote=True)}'
     data-sentence="{html.escape(it["sentence"], quote=True)}">
  <div class="bsq-head"><span class="bsq-num">{i}</span></div>
  <div class="bsq-build" data-role="build" aria-label="Frase montada"></div>
  <div class="bsq-bank" data-role="bank">{chips}</div>
  <button type="button" class="bsq-check" disabled>Verificar</button>
  <div class="bsq-feedback" hidden>
    <p class="bsq-model"></p>
    <p class="bsq-note">{html.escape(it["note"])}</p>
  </div>
</div>''')
    return f'''
<h3>Drill interativo — Build a Sentence</h3>
<p class="bsq-objective">Toque nos fragmentos para montar a frase na ordem correta. Toque num fragmento já colocado para devolvê-lo ao banco. Quando todos estiverem posicionados, confira.</p>
<div class="bsq" data-bsq="{bsq_id}">
  <div class="quiz-bar"><div class="quiz-bar-fill"></div></div>
  <p class="quiz-score">0 de {len(items)} verificadas</p>
  {"".join(cards)}
  <div class="quiz-summary" hidden>
    <span class="quiz-summary-text"></span>
    <button type="button" class="quiz-retry">Refazer este exercício</button>
  </div>
</div>'''
