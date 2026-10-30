"""Shared renderer for the "Registro de erros" mini-form (Protocolo de
Análise de Erros, Parte 7 de cada módulo M1-M6). Substitui o antigo template
de texto (preencher à mão em outro lugar) por um formulário que salva
histórico no próprio navegador (e sincroniza via Supabase quando logado,
como o resto do progresso)."""


def render_error_log(mod_key, codes):
    """codes: lista de tuplas (code, label), na ordem da tabela do módulo."""
    checkboxes = "".join(
        f'<label class="errlog-code"><input type="checkbox" value="{code}">'
        f'<span class="errlog-code-tag">{code}</span> {label}</label>'
        for code, label in codes
    )
    return f'''
<div class="errlog" data-errlog="{mod_key}">
  <p class="errlog-title">Registre esta sessão</p>
  <form class="errlog-form">
    <div class="errlog-row">
      <label class="errlog-field">Data<input type="date" class="errlog-date"></label>
      <label class="errlog-field">Exercício ou simulado<input type="text" class="errlog-drill" placeholder="ex.: Exercício A3"></label>
      <label class="errlog-field">Resultado<input type="text" class="errlog-result" placeholder="ex.: 5/8 acertos"></label>
    </div>
    <div class="errlog-codes">{checkboxes}</div>
    <button type="submit" class="errlog-submit">Registrar sessão</button>
  </form>
  <div class="errlog-history" hidden>
    <p class="errlog-history-title">Histórico desta sessão em diante <span class="errlog-freq"></span></p>
    <div class="errlog-list"></div>
  </div>
</div>'''
