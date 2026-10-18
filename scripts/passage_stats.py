"""Tamanho das passagens de Read an Academic Passage e dos áudios de Listening.

Conta palavras e perguntas de cada texto, nas duas fontes onde eles moram:
app/drills_data.py (os drills do M1 e do M2, que o site mostra) e
consolidated/*.md (a cópia dos drills no M1 e no M2, e os simulados do M7).

    python scripts/passage_stats.py     lista tudo e marca o que passa do limite

O smoke test usa os mesmos números (passage_checks em scripts/smoke_test.py).
Limites, pelo formato de 2026 (docs/ets-materiais-oficiais.md, seção 3):
passagem acadêmica com até 230 palavras e até 5 perguntas; conversa e anúncio
com até 2 perguntas; fala acadêmica com até 4.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAX_WORDS = {"academic": 230}
MAX_QUESTIONS = {"academic": 5, "conversation": 2, "announcement": 2, "talk": 4}

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’.\-][A-Za-z0-9]+)*")
SPEAKER_RE = re.compile(r"\b(?:Narrator|Speaker|Professor|Student|Advisor|Librarian|Faculty Coordinator|Man|Woman):")
QUESTION_RE = re.compile(r"\*\*(QUESTÃO|[A-D]\d\.\d)")

# lista de drills_data.py -> tipo de tarefa
DRILL_LISTS = {
    "MOD1_ACTION_DRILLS_C": "academic",
    "MOD2_ACTION_DRILLS_B": "conversation",
    "MOD2_ACTION_DRILLS_C": "announcement",
    "MOD2_ACTION_DRILLS_D": "talk",
}
MD_LISTEN_HEADINGS = {
    "listen to a conversation": "conversation",
    "listen to an announcement": "announcement",
    "listen to an academic talk": "talk",
}


def count_words(text):
    """Palavras do texto em inglês, sem tags, marcação, narrador e rótulo de quem fala."""
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    text = re.sub(r"\*\*?|\[■[A-D]\]", " ", text)
    text = SPEAKER_RE.sub(" ", text)
    return len(WORD_RE.findall(text))


def from_drills():
    sys.path.insert(0, str(ROOT / "app"))
    import drills_data

    out = []
    for name, kind in DRILL_LISTS.items():
        for d in getattr(drills_data, name):
            body = d["passage_html"] or ""
            # tira o título (<p><strong>PASSAGE: ...</strong></p>) e a linha do narrador
            body = re.sub(r"<p><strong>PASSAGE[^<]*</strong></p>", "", body)
            body = re.sub(r"<p><em>Narrator:[^<]*</em></p>", "", body)
            out.append({"source": "app/drills_data.py", "id": d["id"], "kind": kind,
                        "words": count_words(body), "questions": len(d["items"])})
    return out


def from_markdown():
    """Passagens (**PASSAGE...**) e transcrições (**TRANSCRIÇÃO** no M7, fala
    depois do *Narrator:* no M2), cada uma com as perguntas que vêm logo depois."""
    out = []
    for md in sorted((ROOT / "consolidated").glob("modulo_*.md")):
        lines = md.read_text(encoding="utf-8").split("\n")
        group = ""  # último título: diz se a transcrição é conversa, anúncio ou fala
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#"):
                title = line.lstrip("#").strip().lower()
                # no M2 o tipo está no "### GRUPO X", não no "#### DRILL" logo acima
                if not title.startswith("drill"):
                    group = title
            kind = None
            if line.startswith("**PASSAGE"):
                kind = "academic"
            elif line.startswith("**TRANSCRIÇÃO") or line.startswith("*Narrator:"):
                kind = next((k for h, k in MD_LISTEN_HEADINGS.items() if h in group), None)
            if not kind:
                i += 1
                continue
            text = [line] if line.startswith("**TRANSCRIÇÃO") else []
            j = i + 1
            # o texto vai até a primeira pergunta
            while j < len(lines) and not QUESTION_RE.match(lines[j]) and not lines[j].startswith(("#", "---")):
                text.append(lines[j])
                j += 1
            questions = 0
            while j < len(lines) and not lines[j].startswith(("**Gabarito", "**PASSAGE", "**TRANSCRIÇÃO", "#", "---")):
                questions += bool(QUESTION_RE.match(lines[j]))
                j += 1
            body = re.sub(r"^\*\*TRANSCRIÇÃO[^*]*\*\*", "", "\n".join(text).strip())
            out.append({"source": f"consolidated/{md.name}", "id": f"linha {i + 1}", "kind": kind,
                        "words": count_words(body), "questions": questions})
            i = j
    return out


def all_texts():
    return from_drills() + from_markdown()


def problems(texts=None):
    bad = []
    for t in texts if texts is not None else all_texts():
        limit = MAX_WORDS.get(t["kind"])
        if limit and t["words"] > limit:
            bad.append(f"{t['source']} {t['id']}: {t['words']} palavras (teto {limit})")
        if t["questions"] > MAX_QUESTIONS[t["kind"]]:
            bad.append(f"{t['source']} {t['id']}: {t['questions']} perguntas ({t['kind']}, teto {MAX_QUESTIONS[t['kind']]})")
        if t["questions"] == 0:
            bad.append(f"{t['source']} {t['id']}: nenhuma pergunta achada depois do texto")
    return bad


def main():
    texts = all_texts()
    print(f"{'fonte':<38} {'id':<11} {'tipo':<13} {'palavras':>8} {'perguntas':>9}")
    for t in texts:
        print(f"{t['source']:<38} {t['id']:<11} {t['kind']:<13} {t['words']:>8} {t['questions']:>9}")
    bad = problems(texts)
    print(f"\n{len(texts)} textos; {len(bad)} fora do limite")
    for b in bad:
        print("  -", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
