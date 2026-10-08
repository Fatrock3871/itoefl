"""Renderiza o "Weekly Performance Dashboard" do Módulo 0, Parte 5.1 como
tabela interativa (input por semana/métrica, salvo em localStorage) em vez
do antigo template de texto com células vazias pra preencher à mão -- numa
página web, uma tabela sem nenhum jeito de digitar nela não faz sentido."""


def _plain(label):
    """Texto do rótulo sem marcação, pronto para ir num atributo."""
    import html
    import re
    return html.escape(re.sub(r"<[^>]+>", "", label), quote=True)


def render_weekly_dashboard(metrics):
    """metrics: lista de (key, label, meta)."""
    head_weeks = "".join(f"<th>Semana {w}</th>" for w in range(1, 5))
    rows = "".join(
        f'<tr><td class="wd-metric">{label}</td>'
        + "".join(
            f'<td><input type="text" class="wd-input" data-metric="{key}" data-week="w{w}" '
            # rótulo para leitor de tela: a célula sozinha não diz o que é
            f'aria-label="{_plain(label)}, semana {w}" '
            f'inputmode="decimal" autocomplete="off" placeholder="—"></td>'
            for w in range(1, 5)
        )
        + f'<td class="wd-meta">{meta}</td></tr>'
        for key, label, meta in metrics
    )
    return f'''
<div class="weekly-dash" id="weeklyDash">
  <div class="table-wrap"><table class="wd-table">
    <thead><tr><th>Métrica</th>{head_weeks}<th>Meta</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="wd-hint">Preenche esse quadro toda semana, sempre no mesmo dia da semana. Os valores ficam salvos automaticamente neste navegador (e sincronizam se você estiver logado). O que importa aqui não é o número isolado. É a tendência.</p>
</div>'''
