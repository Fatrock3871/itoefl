"""Renderiza o widget de flashcards com revisao espacada (M6 — Kit de 50 palavras)."""

import json


def render_srs(deck_id, cards):
    # escapa apenas "<" para nao encerrar o <script> prematuramente; segue JSON valido
    data = json.dumps(cards, ensure_ascii=False).replace("<", "\\u003c")
    total = len(cards)
    return f'''
<div class="srs" data-srs="{deck_id}" data-total="{total}">
  <div class="srs-stats">
    <span class="srs-stat"><b class="srs-new">0</b> novas</span>
    <span class="srs-stat"><b class="srs-due">0</b> para revisar</span>
    <span class="srs-stat"><b class="srs-mastered">0</b> dominadas</span>
  </div>
  <p class="srs-progress">Sessão: <b class="srs-count">0</b> de <b class="srs-queued">0</b></p>
  <div class="srs-card">
    <div class="srs-face srs-front">
      <div class="srs-word"></div>
      <div class="srs-cat"></div>
      <button class="srs-flip" type="button">Mostrar significado</button>
    </div>
    <div class="srs-face srs-back" hidden>
      <div class="srs-word"></div>
      <p class="srs-pt"></p>
      <p class="srs-syn"></p>
      <p class="srs-ex"></p>
      <div class="srs-grades">
        <button type="button" data-g="0" class="srs-g0">Errei</button>
        <button type="button" data-g="1" class="srs-g1">Difícil</button>
        <button type="button" data-g="2" class="srs-g2">Fácil</button>
      </div>
    </div>
  </div>
  <div class="srs-done" hidden>
    <p class="srs-done-msg"></p>
    <button type="button" class="srs-restart">Revisar tudo de novo</button>
  </div>
  <script type="application/json" class="srs-data">{data}</script>
</div>'''
