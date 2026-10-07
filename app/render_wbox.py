"""Renderiza a caixa de escrita do M4: campo de texto com cronômetro e
contador de palavras, um por enunciado de Write an Email e de Write for an
Academic Discussion. O texto fica salvo no navegador (e sincroniza com a conta).
"""

EMAIL_MINUTES = 7
DISCUSSION_MINUTES = 10
DISCUSSION_MIN_WORDS = 100


def render_wbox(box_id, minutes, min_words=0):
    goal = f' data-minwords="{min_words}"' if min_words else ""
    target = f'<span class="wbox-goal">mínimo {min_words} palavras</span>' if min_words else ""
    return f'''
<div class="wbox" data-wbox="{box_id}" data-minutes="{minutes}"{goal}>
  <div class="wbox-bar">
    <button type="button" class="wbox-start">Iniciar {minutes} min</button>
    <span class="wbox-clock">{minutes:02d}:00</span>
    <span class="wbox-count">0 palavras</span>
    {target}
  </div>
  <textarea class="wbox-text" id="wbox-{box_id}" rows="9" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="sentences" placeholder="Escreva sua resposta aqui. Na prova não há corretor ortográfico."></textarea>
  <div class="wbox-foot">
    <span class="wbox-status">Salvo automaticamente neste navegador.</span>
    <button type="button" class="wbox-clear">Apagar texto</button>
  </div>
</div>'''
