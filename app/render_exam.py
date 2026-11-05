"""Blocos de simulado interativos do M7.

Diferente dos drills de M1/M2, aqui não há correção item a item: o aluno
responde o bloco inteiro e só vê acertos e explicações depois de entregar,
como numa prova.

As questões NÃO são redigitadas em Python. `convert_exam_blocks` lê o próprio
texto de consolidated/modulo_7_simulados.md, acha cada grupo de questões de
múltipla escolha seguido de uma linha "**Gabarito:** ..." e troca o grupo por
um marcador que o pipeline substitui pelo widget. O .md continua sendo a
fonte da verdade.
"""

import html
import re

import markdown as md

from rebalance import rebalance_items, tag_refs
from render_quiz import weak_area

ITEM_NUM_RE = re.compile(r"^(\d+)\. (.+)$")
ITEM_Q_RE = re.compile(r"^\*\*QUESTÃO(?: (\d+))?(?: · [^:*]+)?:\*\* ?(.*)$")
OPTION_LINE_RE = re.compile(r"^(?:- )?\(A\) ")
OPTION_RE = re.compile(r"\(([A-D])\)\s*(.*?)(?=\s+\([B-D]\)\s|$)")
NOTE_RE = re.compile(r"\s*\*\((nota:[^*]*)\)\*\s*$")
GABARITO_RE = re.compile(r"^\*\*Gabarito:\*\*\s*(.*)$")
PAIR_RE = re.compile(r"(\d+)-([A-D])\b")
SINGLE_RE = re.compile(r"^([A-D])\b(.*)$")


def inline(text):
    """Markdown de uma linha para HTML, sem o <p> em volta."""
    out = md.markdown(text.strip())
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def clean_expl(text):
    text = text.strip().strip("·;").strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    return text


def parse_gabarito(text):
    """'1-B (porque) · 2-C' ou só 'B (porque)'. Devolve {numero: (letra, explicacao)}."""
    pairs = list(PAIR_RE.finditer(text))
    if not pairs:
        m = SINGLE_RE.match(text.strip())
        return {1: (m.group(1), clean_expl(m.group(2)))} if m else {}
    out = {}
    for i, m in enumerate(pairs):
        end = pairs[i + 1].start() if i + 1 < len(pairs) else len(text)
        out[int(m.group(1))] = (m.group(2), clean_expl(text[m.end():end]))
    return out


def render_exam(exam_id, items):
    cards = []
    for it in items:
        opts = "".join(
            f'<button type="button" class="exam-opt" data-letter="{L}">'
            f'<span class="oletter">{L}</span><span class="otext">{inline(txt)}</span></button>'
            for L, txt in it["options"]
        )
        note = f'<span class="exam-hint">{tag_refs(inline(it["note"]))}</span>' if it.get("note") else ""
        expl = f'<p class="exam-expl" hidden>{tag_refs(inline(it["explanation"]))}</p>' if it.get("explanation") else ""
        pre = f'<div class="exam-pre">{md.markdown(chr(10).join(it["pre"]))}</div>' if it.get("pre") else ""
        weak = f' data-weak="{weak_area(it["prompt"])}"' if weak_area(it["prompt"]) else ""
        cards.append(f'''
  <div class="exam-item" data-num="{it["num"]}" data-correct="{it["correct"]}"{weak}>
    {pre}
    <p class="exam-prompt"><span class="exam-n">{it["num"]}</span><span class="exam-q">{inline(it["prompt"])}{note}</span></p>
    <div class="exam-opts">{opts}</div>
    {expl}
  </div>''')
    return f'''
<div class="exam" data-exam="{html.escape(exam_id, quote=True)}">
  {"".join(cards)}
  <div class="exam-actions">
    <button type="button" class="exam-submit" disabled>Entregar este bloco</button>
    <button type="button" class="exam-retry" hidden>Refazer este bloco</button>
    <span class="exam-result" hidden></span>
  </div>
</div>'''


def convert_exam_blocks(raw, id_prefix):
    """Devolve (texto com marcadores, {marcador: widget}, relatorio)."""
    lines = raw.split("\n")
    pending = []           # itens desde o último gabarito/título
    widgets, skipped = {}, []
    total_items = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            pending = []
            i += 1
            continue

        g = GABARITO_RE.match(line)
        if g:
            if pending:
                answers = parse_gabarito(g.group(1))
                nums = [it["num"] for it in pending]
                first, last = pending[0]["start"], pending[-1]["end"]
                owned = set()
                for it in pending:
                    owned.update(range(it["start"], it["end"] + 1))
                # questões sem número ("**QUESTÃO:**" repetido): numera na ordem
                if len(set(nums)) != len(nums) and len(nums) == len(answers):
                    for n, it in enumerate(pending, 1):
                        it["num"] = n
                    nums = [it["num"] for it in pending]
                # linhas soltas entre uma questão e outra: o que vem antes de
                # uma questão (ex.: a fala do áudio) é contexto dela; uma
                # "*(nota: ...)*" comenta a questão anterior e só aparece
                # depois da entrega, junto da explicação
                stray = []
                for k in range(first, last + 1):
                    if k in owned or not lines[k].strip():
                        continue
                    prev = [it for it in pending if it["end"] < k]
                    nxt = [it for it in pending if it["start"] > k]
                    if lines[k].lstrip().startswith("*(nota") and prev:
                        prev[-1].setdefault("after", []).append(lines[k].strip().strip("*"))
                    elif nxt:
                        nxt[0].setdefault("pre", []).append(lines[k])
                    else:
                        stray.append(k)
                if len(set(nums)) == len(nums) and set(nums) == set(answers) and not stray:
                    for it in pending:
                        it["correct"], it["explanation"] = answers[it["num"]]
                        if it.get("after"):
                            it["explanation"] = " ".join([it["explanation"]] + it["after"]).strip()
                    token = f"%%%EXAM_{len(widgets) + 1}%%%"
                    exam_id = f"{id_prefix}-b{len(widgets) + 1}"
                    # tira o vício de letra do gabarito (ver rebalance.py)
                    balanced = rebalance_items(
                        [dict(it, options=dict(it["options"])) for it in pending],
                        exam_id, ("prompt", "explanation", "note"))
                    for it in balanced:
                        it["options"] = list(it["options"].items())
                    widgets[token] = render_exam(exam_id, balanced)
                    total_items += len(pending)
                    lines[first:last + 1] = [token] + [""] * (last - first)
                    lines[i] = ""  # a linha do gabarito sai: a correção vem no widget
                else:
                    skipped.append((i + 1, nums, sorted(answers), len(stray)))
            pending = []
            i += 1
            continue

        m = ITEM_NUM_RE.match(line) or ITEM_Q_RE.match(line)
        if m:
            num = int(m.group(1)) if m.group(1) else 1
            prompt = m.group(2)
            j, options, note = i + 1, [], ""
            while j < len(lines) and (OPTION_LINE_RE.match(lines[j]) if not options else re.match(r"^(?:- )?\([B-D]\) ", lines[j])):
                opt_line = lines[j][2:] if lines[j].startswith("- ") else lines[j]
                nm = NOTE_RE.search(opt_line)
                if nm:
                    note = nm.group(1)
                    opt_line = opt_line[:nm.start()]
                options += [(L, t.strip()) for L, t in OPTION_RE.findall(opt_line)]
                j += 1
            letters = [L for L, _ in options]
            if letters in (["A", "B", "C", "D"], ["A", "B", "C"]):
                pending.append({"num": num, "prompt": prompt, "options": options, "note": note,
                                "start": i, "end": j - 1})
                i = j
                continue
        i += 1

    report = {"blocks": len(widgets), "items": total_items, "skipped": skipped}
    return "\n".join(lines), widgets, report
