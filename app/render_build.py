"""Renderiza o widget interativo de Build a Sentence (Writing / M4).

Formato da prova: fala de contexto + resposta com trechos fixos e espaços a
preencher com os blocos do banco. Ver build_sentence_data.py.
"""

import html
import json
import re

CHUNK_RE = re.compile(r"\{([^{}]+)\}")


def parse_pattern(pattern):
    """Devolve (tokens, answer). tokens: lista de ("fixed", texto) e ("slot", i)."""
    tokens, answer, pos = [], [], 0
    for m in CHUNK_RE.finditer(pattern):
        fixed = pattern[pos:m.start()].strip()
        if fixed:
            tokens.append(("fixed", fixed))
        tokens.append(("slot", len(answer)))
        answer.append(m.group(1))
        pos = m.end()
    tail = pattern[pos:].strip()
    if tail:
        tokens.append(("fixed", tail))
    return tokens, answer


def render_build_sentence(bsq_id, items):
    cards = []
    for i, it in enumerate(items, 1):
        tokens, answer = parse_pattern(it["pattern"])
        bank = answer + list(it.get("extra", []))
        if len(set(bank)) != len(bank):
            raise ValueError(f'{it["id"]}: bloco repetido no banco')
        sentence = CHUNK_RE.sub(r"\1", it["pattern"])

        build = "".join(
            f'<span class="bsq-fixed{" bsq-punct" if re.fullmatch(r"[?.!,]+", val) else ""}">{html.escape(val)}</span>'
            if kind == "fixed" else f'<span class="bsq-slot" data-slot="{val}"></span>'
            for kind, val in tokens
        )
        chips = "".join(
            f'<button type="button" class="bsq-chip" data-frag="{html.escape(f, quote=True)}">{html.escape(f)}</button>'
            for f in bank
        )
        answer_json = json.dumps(answer, ensure_ascii=False).replace("<", "\\u003c")
        level = f'<span class="bsq-level">{html.escape(it["level"])}</span>' if it.get("level") else ""
        extra_hint = '<span class="bsq-extra-hint">Um bloco sobra.</span>' if it.get("extra") else ""
        cards.append(f'''
<div class="bsq-card" data-num="{i}" data-answer='{html.escape(answer_json, quote=True)}'
     data-sentence="{html.escape(sentence, quote=True)}">
  <div class="bsq-head"><span class="bsq-num">{i}</span>{level}{extra_hint}</div>
  <p class="bsq-context">{html.escape(it["context"])}</p>
  <div class="bsq-build" data-role="build" aria-label="Resposta a montar">{build}</div>
  <div class="bsq-bank" data-role="bank">{chips}</div>
  <button type="button" class="bsq-check" disabled>Verificar</button>
  <div class="bsq-feedback" hidden>
    <p class="bsq-model"></p>
    <p class="bsq-note">{html.escape(it["note"])}</p>
  </div>
</div>''')
    return f'''
<h3>Drill interativo: Build a Sentence no formato da prova</h3>
<p class="bsq-objective">Leia a fala e monte a resposta. Toque num bloco para colocá-lo no próximo espaço vazio; toque num bloco já colocado para devolvê-lo. As palavras impressas na resposta são fixas. Quando o item avisar que um bloco sobra, ele fica de fora.</p>
<div class="bsq" data-bsq="{bsq_id}">
  <div class="quiz-bar"><div class="quiz-bar-fill"></div></div>
  <p class="quiz-score">0 de {len(items)} verificadas</p>
  {"".join(cards)}
  <div class="quiz-summary" hidden>
    <span class="quiz-summary-text"></span>
    <button type="button" class="quiz-retry">Refazer este exercício</button>
  </div>
</div>'''
