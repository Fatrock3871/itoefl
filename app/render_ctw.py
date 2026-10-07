"""Renderiza o widget de Complete the Words no formato real da prova (M1).

Cada [[palavra]] do texto vira o começo da palavra impresso + um campo para o
aluno digitar o final. Ver ctw_data.py para a regra de corte.
"""

import html
import re

GAP_RE = re.compile(r"\[\[([A-Za-z]+)\]\]")
GAPS_PER_SET = 10


def split_word(word):
    """Começo que fica visível e final que o aluno digita."""
    keep = len(word) // 2
    return word[:keep], word[keep:]


def render_ctw(item):
    words = GAP_RE.findall(item["text"])
    if len(words) != GAPS_PER_SET:
        raise ValueError(f'{item["id"]}: esperava {GAPS_PER_SET} lacunas, achei {len(words)}')

    counter = {"n": 0}

    def gap(m):
        counter["n"] += 1
        n = counter["n"]
        pre, missing = split_word(m.group(1))
        size = len(missing)
        return (
            f'<span class="ctw-gap" data-word="{html.escape(m.group(1), quote=True)}">'
            f'<span class="ctw-pre">{html.escape(pre)}</span>'
            f'<input type="text" class="ctw-in" data-answer="{html.escape(missing, quote=True)}" '
            f'maxlength="{size}" size="{size}" style="width:{size + 0.9:.1f}ch" '
            f'autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" '
            f'aria-label="Lacuna {n}: faltam {size} letras depois de {html.escape(pre, quote=True)}">'
            f'<span class="ctw-fix" hidden></span></span>'
        )

    body = GAP_RE.sub(gap, html.escape(item["text"], quote=False))
    level = f'<span class="ctw-level">{html.escape(item["level"])}</span>' if item.get("level") else ""
    return f'''
<div class="ctw" data-ctw="{html.escape(item["id"], quote=True)}">
  <div class="ctw-head"><span class="ctw-title">{html.escape(item["title"])}</span>{level}</div>
  <p class="ctw-instr">Fill in the missing letters in the paragraph.</p>
  <p class="ctw-text">{body}</p>
  <div class="ctw-actions">
    <button type="button" class="ctw-check">Verificar</button>
    <button type="button" class="ctw-retry" hidden>Refazer este texto</button>
    <span class="ctw-result" hidden></span>
  </div>
  <p class="ctw-note" hidden>{html.escape(item["note"])}</p>
</div>'''


def render_ctw_group(items):
    return "".join(render_ctw(it) for it in items)
