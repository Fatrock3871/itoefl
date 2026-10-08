"""Gera bank/items/migrado/*.json a partir das fontes atuais do site.

    python bank/tools/migrate.py

Idempotente: a mesma fonte gera sempre os mesmos bytes, e arquivos antigos
da pasta migrado/ que não seriam mais gerados são apagados. Enquanto o site
continuar lendo de app/ e de consolidated/, ESTAS FONTES são a verdade: não
edite bank/items/migrado/ à mão, edite a fonte e rode de novo.

Fontes lidas (só leitura):
  app/quiz_mod0.json                 10 questões do diagnóstico (M0)
  app/drills_data.py                 *_ACTION_DRILLS_* de Reading (M1) e Listening (M2)
  app/ctw_data.py                    8 parágrafos de Complete the Words (M1)
  app/build_sentence_data.py         30 itens de Build a Sentence (M4)
  consolidated/modulo_7_simulados.md blocos de múltipla escolha com **Gabarito:**,
                                     lidos pelo mesmo parser do build (render_exam.py)

Letras: options e answer ficam com a letra de ORIGEM (antes do
rebalance.py). O campo source.build_map registra para que letra o build
leva cada alternativa, calculado chamando o próprio rebalance.py com a
mesma chave que o build usa.

Imprime a contagem origem vs. destino de cada fonte e falha se alguma não
bater.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app"
M7_MD = ROOT / "consolidated" / "modulo_7_simulados.md"
OUT_DEFAULT = ROOT / "bank" / "items"
SUBDIR = "migrado"

sys.path.insert(0, str(APP))

import rebalance  # noqa: E402

CEFR = ["A1", "A2", "B1", "B2", "C1", "C2"]

TASK_SECTION = {
    "Complete the Words": "reading", "Read in Daily Life": "reading",
    "Read an Academic Passage": "reading",
    "Listen and Choose a Response": "listening", "Listen to a Conversation": "listening",
    "Listen to an Announcement": "listening", "Listen to an Academic Talk": "listening",
    "Build a Sentence": "writing", "Grammar and Vocabulary": "general",
}

# lista de drills -> tipo de tarefa, se reproduz o formato da prova
DRILL_LISTS = [
    ("MOD1_ACTION_DRILLS_A", "Complete the Words", False),
    ("MOD1_ACTION_DRILLS_B", "Read in Daily Life", True),
    ("MOD1_ACTION_DRILLS_C", "Read an Academic Passage", True),
    ("MOD2_ACTION_DRILLS_A", "Listen and Choose a Response", True),
    ("MOD2_ACTION_DRILLS_B", "Listen to a Conversation", True),
    ("MOD2_ACTION_DRILLS_C", "Listen to an Announcement", True),
    ("MOD2_ACTION_DRILLS_D", "Listen to an Academic Talk", True),
]
# MOD1_DRILLS e MOD2_DRILLS ficam de fora: são importados mas não renderizados
# pelo build_pipeline.py, repetem parte dos Action Drills e reusam ids
# (mod2-d1 a mod2-d3). Ver bank/README.md, "Fora da migração".
LEGACY_LISTS = ["MOD1_DRILLS", "MOD2_DRILLS"]


def parse_level(level):
    """'A2–B1' -> ('A2', 'B1'); 'C1+' -> ('C1', 'C2'); None -> (None, None)."""
    if not level:
        return None, None
    parts = [p.strip() for p in re.split(r"[–-]", level) if p.strip()]
    lo, hi = parts[0], parts[-1]
    if hi.endswith("+"):
        hi = CEFR[min(CEFR.index(hi[:-1]) + 1, len(CEFR) - 1)]
    lo = lo.rstrip("+")
    if lo not in CEFR or hi not in CEFR:
        raise ValueError(f"nível CEFR não reconhecido: {level!r}")
    return lo, hi


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def letter_map(orig_opts, new_opts):
    """Mapa letra de origem -> letra no build, achado pelo texto da alternativa."""
    by_text = {}
    for new, txt in new_opts.items():
        by_text.setdefault(txt, []).append(new)
    mapping = {}
    for old, txt in orig_opts.items():
        cands = by_text.get(txt) or []
        if len(cands) != 1:
            raise ValueError(f"alternativa ambígua ou sumida no rebalanceamento: {txt!r}")
        mapping[old] = cands[0]
    if sorted(mapping.values()) != sorted(orig_opts):
        raise ValueError("mapa de letras não é uma permutação")
    return mapping


def build_maps(items, key, text_fields=("prompt", "explanation")):
    """Roda o rebalance.py como o build roda e devolve {num: mapa ou None}."""
    balanced = rebalance.rebalance_items(items, key, text_fields)
    out = {}
    for orig, new in zip(items, balanced):
        texts = list(orig["options"].values()) + [str(orig.get(f, "")) for f in text_fields]
        eligible = rebalance.eligible(list(orig["options"]), orig["correct"], texts) and not orig.get("multi")
        out[str(orig["num"])] = letter_map(orig["options"], new["options"]) if eligible else None
    return out


def item(**kw):
    base = {
        "id": None, "section": None, "task_type": None, "exam_format": True,
        "format": "mcq", "skill": None, "cefr_min": None, "cefr_max": None,
        "stimulus": None, "group": None, "prompt": None, "text_format": "plain",
        "options": None, "answer": None, "explanation": "", "hint": None,
        "trap_codes": [], "tags": [], "status": "rascunho",
        "source": None,
    }
    base.update(kw)
    if base["group"] is None:
        del base["group"]
    base["section"] = TASK_SECTION[base["task_type"]]
    return base


def source(file, ref, build_map=None):
    return {"kind": "migrado", "file": file, "ref": ref, "live_on_site": True,
            "answer_letter": "origem", "build_map": build_map}


def stim(content, kind="text", fmt="html", title=None):
    if not content or not content.strip():
        return None
    return {"kind": kind, "format": fmt, "title": title, "content": content.strip(), "audio_ref": None}


# ---------------------------------------------------------------- fontes

def from_quiz_mod0():
    data = json.loads((APP / "quiz_mod0.json").read_text(encoding="utf-8"))
    # mesma montagem do build_mod0() em build_pipeline.py, para o rebalance
    # receber exatamente o que o build recebe
    as_built = [{"num": q["num"], "prompt": f"Questão {q['num']} — {q['topic']}<br>{q['prompt']}",
                 "options": q["options"], "correct": q["correct"],
                 "explanation": f"<strong>Por que certa:</strong> {q['why_right']}<br>"
                                f"<strong>Por que as outras erram:</strong> {q['why_wrong']}"}
                for q in data]
    maps = build_maps(as_built, "mod0-diag")
    out = []
    for q, b in zip(data, as_built):
        out.append(item(
            id=f"mod0-diag.{q['num']}", task_type="Grammar and Vocabulary", exam_format=False,
            skill=q["topic"], group="mod0-diag", prompt=q["prompt"], text_format="html",
            options=dict(q["options"]), answer=q["correct"], explanation=b["explanation"],
            tags=["diagnostico"],
            source=source("app/quiz_mod0.json", f"num {q['num']}", maps[str(q["num"])]),
        ))
    return len(data), out


def from_drills():
    import drills_data
    origem, out = 0, []
    for list_name, task, exam_format in DRILL_LISTS:
        section = TASK_SECTION[task]
        for d in getattr(drills_data, list_name):
            origem += len(d["items"])
            maps = build_maps(d["items"], d["id"])
            lo, hi = parse_level(d.get("level"))
            shared = stim(d.get("passage_html"), "audio" if section == "listening" else "text",
                          "html", d.get("title"))
            for it in d["items"]:
                num = str(it["num"])
                prompt, stimulus = it["prompt"], shared
                if task == "Listen and Choose a Response" and stimulus is None:
                    # na prova a fala é ouvida, não lida: vira o estímulo de áudio
                    stimulus = stim(it["prompt"], "audio", "html")
                    prompt = "Choose the best response."
                multi = it.get("multi")
                answer = it["correct"].split(",") if multi else it["correct"]
                kw = dict(
                    id=f"{d['id']}.{num}".lower(), task_type=task, exam_format=exam_format,
                    cefr_min=lo, cefr_max=hi, stimulus=stimulus, group=d["id"],
                    prompt=prompt, text_format="html", options=dict(it["options"]),
                    answer=answer, explanation=it.get("explanation", ""),
                    format="multi_select" if multi else "mcq",
                    source=source("app/drills_data.py", f"{list_name}:{d['id']}#{num}", maps[num]),
                )
                if multi:
                    kw["select_count"] = int(multi)
                out.append(item(**kw))
    return origem, out


def from_ctw():
    from ctw_data import CTW_SETS
    gap_re = re.compile(r"\[\[([A-Za-z]+)\]\]")
    out, gaps = [], 0
    for s in CTW_SETS:
        words = gap_re.findall(s["text"])
        gaps += len(words)
        lo, hi = parse_level(s.get("level"))
        out.append(item(
            id=s["id"], task_type="Complete the Words", format="fill_words",
            cefr_min=lo, cefr_max=hi,
            stimulus=stim(s["text"], "text", "plain", s.get("title")),
            prompt="Fill in the missing letters to complete the words in the paragraph.",
            answer=words, explanation=s.get("note", ""),
            source=source("app/ctw_data.py", s["id"]),
        ))
    return len(CTW_SETS), out, gaps


def from_build_sentence():
    from build_sentence_data import BUILD_SENTENCE_ITEMS
    chunk_re = re.compile(r"\{([^{}]+)\}")
    out = []
    for it in BUILD_SENTENCE_ITEMS:
        answer = chunk_re.findall(it["pattern"])
        counter = iter(range(1, len(answer) + 1))
        template = chunk_re.sub(lambda m: "{" + str(next(counter)) + "}", it["pattern"])
        bank = sorted(answer + list(it.get("extra", [])), key=lambda s: (s.lower(), s))
        lo, hi = parse_level(it.get("level"))
        out.append(item(
            id=f"mod4-{it['id']}", task_type="Build a Sentence", format="build_sentence",
            cefr_min=lo, cefr_max=hi, group="m4build2",
            stimulus=stim(it["context"], "text", "plain"),
            prompt=template, options=bank, answer=answer, explanation=it.get("note", ""),
            tags=["sobra-um-bloco"] if it.get("extra") else [],
            source=source("app/build_sentence_data.py", it["id"]),
        ))
    return len(BUILD_SENTENCE_ITEMS), out


M7_TASKS = ["Complete the Words", "Read in Daily Life", "Read an Academic Passage",
            "Listen and Choose a Response", "Listen to a Conversation",
            "Listen to an Announcement", "Listen to an Academic Talk"]
SKILL_RE = re.compile(r"^\*\*QUESTÃO(?: \d+)? · ([^:*]+):\*\*")


def from_m7():
    """Usa o próprio convert_exam_blocks do build, trocando só o renderizador
    por um coletor. Assim a contagem é a mesma que o build confere."""
    import render_exam
    raw = M7_MD.read_text(encoding="utf-8")
    lines = raw.split("\n")
    captured = []
    real_rebalance = render_exam.rebalance_items

    def spy_rebalance(items, key, fields):
        balanced = real_rebalance(items, key, fields)
        captured.append({"key": key, "orig": [dict(it) for it in items], "balanced": balanced})
        return balanced

    saved = render_exam.rebalance_items, render_exam.render_exam
    render_exam.rebalance_items = spy_rebalance
    render_exam.render_exam = lambda exam_id, items: ""
    try:
        _, _, report = render_exam.convert_exam_blocks(raw, "mod7")
    finally:
        render_exam.rebalance_items, render_exam.render_exam = saved

    def last_before(idx, test):
        for k in range(idx - 1, -1, -1):
            if test(lines[k]):
                return k
        return -1

    out = []
    for block in captured:
        orig, balanced, key = block["orig"], block["balanced"], block["key"]
        first = orig[0]["start"]
        h = last_before(first, lambda l: l.startswith("####"))
        heading = lines[h].lstrip("#").strip()
        task = next((t for t in M7_TASKS if t.lower() in heading.lower()), None)
        if task is None:
            raise ValueError(f"M7 linha {h + 1}: tipo de tarefa não reconhecido em {heading!r}")
        section = TASK_SECTION[task]
        sim = last_before(first, lambda l: l.startswith("### ") and "SIMULADO" in l)
        sim_n = re.search(r"SIMULADO (\d)", lines[sim]).group(1)
        boundary = max(h, last_before(first, lambda l: l.startswith("**Gabarito:**")))
        preamble = "\n".join(lines[boundary + 1:first]).strip()
        own_pre = all(it.get("pre") for it in orig[1:]) and len(orig) > 1
        kind = "audio" if section == "listening" else "text"

        for it, new in zip(orig, balanced):
            opts = dict(it["options"])
            texts = list(opts.values()) + [str(it.get(f, "")) for f in ("prompt", "explanation", "note")]
            eligible = rebalance.eligible(list(opts), it["correct"], texts)
            bmap = letter_map(opts, dict(new["options"])) if eligible else None
            pre = "\n".join(it.get("pre", [])).strip()
            if own_pre:
                content = preamble if it is orig[0] else pre
            else:
                content = "\n\n".join(p for p in (preamble, pre) if p)
            sk = SKILL_RE.match(lines[it["start"]])
            out.append(item(
                id=f"{key}.{it['num']}", task_type=task,
                exam_format=task != "Complete the Words",
                skill=sk.group(1).strip() if sk else None, group=key,
                stimulus=stim(content, kind, "markdown", heading),
                prompt=it["prompt"].strip(), text_format="markdown", options=opts,
                answer=it["correct"], explanation=it.get("explanation", "") or "",
                hint=it.get("note") or None, tags=[f"simulado-{sim_n}"],
                source=source("consolidated/modulo_7_simulados.md", f"linha {it['start'] + 1}", bmap),
            ))

    pipeline = (APP / "build_pipeline.py").read_text(encoding="utf-8")
    expected = int(re.search(r"^M7_EXPECTED_ITEMS = (\d+)", pipeline, re.M).group(1))
    if report["items"] != expected:
        raise ValueError(f"M7: parser achou {report['items']} itens, build_pipeline espera {expected}")
    typed = len(re.findall(r"·\s*\d+\s+\*\*[^*]+\*\*", "\n".join(l for l in lines if l.startswith("**Gabarito:**"))))
    return report["items"], out, report["blocks"], typed


# ---------------------------------------------------------------- saída

def dump(items):
    return json.dumps(items, ensure_ascii=False, indent=2) + "\n"


def run(out_dir=OUT_DEFAULT, verbose=False):
    out_dir = Path(out_dir) / SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)

    report, all_items = [], []
    n, items = from_quiz_mod0()
    report.append({"fonte": "app/quiz_mod0.json", "origem": n, "destino": len(items)})
    all_items += items
    n, items = from_drills()
    report.append({"fonte": "app/drills_data.py (Action Drills M1 e M2)", "origem": n, "destino": len(items)})
    all_items += items
    n, items, gaps = from_ctw()
    report.append({"fonte": "app/ctw_data.py (parágrafos)", "origem": n, "destino": len(items)})
    report.append({"fonte": "app/ctw_data.py (lacunas)", "origem": gaps,
                   "destino": sum(len(i["answer"]) for i in items)})
    all_items += items
    n, items = from_build_sentence()
    report.append({"fonte": "app/build_sentence_data.py", "origem": n, "destino": len(items)})
    all_items += items
    n, items, blocks, typed = from_m7()
    report.append({"fonte": f"consolidated/modulo_7_simulados.md ({blocks} blocos)", "origem": n, "destino": len(items)})
    all_items += items

    files = {}
    for it in all_items:
        files.setdefault(f"{it['section']}-{slug(it['task_type'])}.json", []).append(it)
    for name, items in files.items():
        path = out_dir / name
        text = dump(items)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    for path in out_dir.glob("*.json"):
        if path.name not in files:
            path.unlink()

    if verbose:
        import drills_data
        legacy = sum(len(d["items"]) for name in LEGACY_LISTS for d in getattr(drills_data, name))
        print(f"{'fonte':<55} {'origem':>7} {'destino':>8}")
        for r in report:
            print(f"{r['fonte']:<55} {r['origem']:>7} {r['destino']:>8}")
        total_o = sum(r["origem"] for r in report if "lacunas" not in r["fonte"])
        total_d = sum(r["destino"] for r in report if "lacunas" not in r["fonte"])
        print(f"{'TOTAL de itens':<55} {total_o:>7} {total_d:>8}")
        print(f"\nArquivos em {out_dir.relative_to(ROOT) if out_dir.is_relative_to(ROOT) else out_dir}:")
        for name in sorted(files):
            print(f"  {name:<50} {len(files[name]):>4}")
        print(f"\nFora da migração: {legacy} itens de MOD1_DRILLS/MOD2_DRILLS (não renderizados pelo build);"
              f" {typed} itens de digitação do M7 sem alternativas.")
    bad = [r for r in report if r["origem"] != r["destino"]]
    if bad:
        raise SystemExit(f"contagem não bate: {bad}")
    return report


if __name__ == "__main__":
    run(verbose=True)
