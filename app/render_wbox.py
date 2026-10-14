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
  <textarea class="wbox-text" id="wbox-{box_id}" aria-label="Sua resposta em inglês" lang="en" rows="9" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="sentences" placeholder="Escreva sua resposta aqui. Na prova não há corretor ortográfico."></textarea>
  <div class="wbox-foot">
    <span class="wbox-status">Salvo automaticamente neste navegador.</span>
    <button type="button" class="wbox-clear">Apagar texto</button>
  </div>
</div>'''


def render_essay_box():
    """A mesma caixa, na versão de prova da tela de redação para correção:
    sem botão de pausar nem de apagar, e sem data-wbox (o binder genérico do
    app.js não a pega; quem cuida dela é o app/redacao.js). Tempo e mínimo de
    palavras mudam conforme o tema e são preenchidos na hora."""
    return '''
<div class="wbox wbox-exam" id="essayBox">
  <div class="wbox-bar">
    <span class="wbox-clock" id="essayClock" role="timer" aria-live="off">00:00</span>
    <span class="wbox-count" id="essayCount">0 palavras</span>
    <span class="wbox-goal" id="essayGoal" hidden></span>
  </div>
  <textarea class="wbox-text" id="essayText" aria-label="Sua redação em inglês" lang="en" rows="11" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="sentences" maxlength="5000" placeholder="Escreva aqui. Na prova não há corretor ortográfico."></textarea>
  <div class="wbox-foot">
    <span class="wbox-status" id="essayBoxStatus">O cronômetro não pausa. O texto fica guardado neste aparelho até você enviar ou descartar.</span>
  </div>
</div>'''
