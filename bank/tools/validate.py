"""Valida o banco de questões (bank/items/**/*.json).

    python bank/tools/validate.py            # valida bank/items
    python bank/tools/validate.py <pasta>    # valida outra pasta

Só stdlib. Confere cada item contra bank/schema/item.schema.json (com um
validador próprio que cobre o subconjunto de JSON Schema usado lá) e depois
as regras que o schema não expressa: ids únicos, resposta entre as opções,
tipo de tarefa compatível com a seção, faixa CEFR em ordem, lacunas do
Complete the Words batendo com as respostas. Imprime um resumo com as
contagens por seção e por tipo de tarefa.

Sai com código 1 se houver erro. Avisos (explicação vazia, item sem CEFR,
explicação citando letra que não existe) não mudam o código de saída.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

BANK = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BANK / "schema" / "item.schema.json"
ITEMS_DIR = BANK / "items"

CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

SECTION_TASKS = {
    "reading": {"Complete the Words", "Read in Daily Life", "Read an Academic Passage"},
    "listening": {"Listen and Choose a Response", "Listen to a Conversation",
                  "Listen to an Announcement", "Listen to an Academic Talk"},
    "writing": {"Build a Sentence", "Write an Email", "Write for an Academic Discussion"},
    "speaking": {"Listen and Repeat", "Take an Interview"},
    "general": {"Grammar and Vocabulary"},
}

GAP_RE = re.compile(r"\[\[([A-Za-z]+)\]\]")
SLOT_RE = re.compile(r"\{(\d+)\}")
REF_RE = re.compile(r"\(([A-H])\)")
LETTER_RE = re.compile(r"^[A-H]$")


# ---------------------------------------------------------------- schema

def load_schema(path=SCHEMA_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


_TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def _resolve(schema, root):
    while "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"$ref não suportado: {ref}")
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        schema = node
    return schema


def check_schema(value, schema, root=None, path="item"):
    """Devolve a lista de erros (strings) de `value` contra `schema`."""
    root = root if root is not None else schema
    schema = _resolve(schema, root)
    errors = []

    types = schema.get("type")
    if types is not None:
        types = [types] if isinstance(types, str) else types
        if not any(_TYPES[t](value) for t in types):
            return [f"{path}: tipo {type(value).__name__}, esperado {'/'.join(types)}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: valor {value!r} fora de {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: esperado {schema['const']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: texto vazio ou curto demais")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} não casa com {schema['pattern']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} menor que {schema['minimum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: menos de {schema['minItems']} elementos")
        if "items" in schema:
            for i, v in enumerate(value):
                errors += check_schema(v, schema["items"], root, f"{path}[{i}]")

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: falta o campo obrigatório {key!r}")
        extra = schema.get("additionalProperties", True)
        for key, v in value.items():
            if key in props:
                errors += check_schema(v, props[key], root, f"{path}.{key}")
            elif extra is False:
                errors.append(f"{path}: campo desconhecido {key!r}")
            elif isinstance(extra, dict):
                errors += check_schema(v, extra, root, f"{path}.{key}")
    return errors


# ---------------------------------------------------------------- regras

def _check_rules(it):
    """Regras de conteúdo de um item que já passou no schema."""
    errors, warnings = [], []
    fmt, opts, ans = it["format"], it["options"], it["answer"]

    if it["task_type"] not in SECTION_TASKS[it["section"]]:
        errors.append(f"task_type {it['task_type']!r} não pertence à seção {it['section']!r}")

    lo, hi = it["cefr_min"], it["cefr_max"]
    if (lo is None) != (hi is None):
        errors.append("cefr_min e cefr_max: ou os dois preenchidos ou os dois null")
    elif lo is None:
        warnings.append("sem faixa cefr declarada")
    elif CEFR_ORDER.index(lo) > CEFR_ORDER.index(hi):
        errors.append(f"cefr_min {lo} maior que cefr_max {hi}")

    if fmt in ("mcq", "multi_select"):
        if not isinstance(opts, dict) or len(opts) < 2:
            errors.append("mcq/multi_select precisa de options como objeto com 2+ letras")
            return errors, warnings
        bad = [k for k in opts if not LETTER_RE.match(k)]
        if bad:
            errors.append(f"letras de alternativa inválidas: {bad}")
        if any(not isinstance(v, str) or not v.strip() for v in opts.values()):
            errors.append("alternativa vazia")
        if fmt == "mcq":
            if not isinstance(ans, str) or ans not in opts:
                errors.append(f"resposta {ans!r} não está entre as opções {list(opts)}")
            if "select_count" in it:
                errors.append("select_count só vale em multi_select")
        else:
            if not isinstance(ans, list) or not ans or any(a not in opts for a in ans):
                errors.append(f"resposta {ans!r} tem letra fora das opções {list(opts)}")
            elif len(set(ans)) != len(ans):
                errors.append("resposta com letra repetida")
            if it.get("select_count") != (len(ans) if isinstance(ans, list) else None):
                errors.append(f"select_count {it.get('select_count')} difere do número de respostas")
        cited = set(REF_RE.findall(it["explanation"] or "")) | set(REF_RE.findall(it["hint"] or ""))
        for letter in sorted(cited - set(opts)):
            warnings.append(f"explicação cita ({letter}), que não é alternativa do item")

    elif fmt == "fill_words":
        stim = it["stimulus"]
        if opts is not None:
            errors.append("fill_words não tem options (use null)")
        if not stim:
            errors.append("fill_words precisa de stimulus com as lacunas [[palavra]]")
        else:
            gaps = GAP_RE.findall(stim["content"])
            if not isinstance(ans, list) or ans != gaps:
                errors.append(f"resposta não bate com as lacunas do texto: {len(gaps)} lacunas, resposta {ans!r}")

    elif fmt == "build_sentence":
        if not isinstance(opts, list) or not isinstance(ans, list) or not ans:
            errors.append("build_sentence precisa de options e answer como listas")
            return errors, warnings
        if len(set(opts)) != len(opts):
            errors.append("bloco repetido em options")
        missing = [a for a in ans if a not in opts]
        if missing:
            errors.append(f"resposta tem bloco fora das opções: {missing}")
        slots = [int(n) for n in SLOT_RE.findall(it["prompt"])]
        if slots != list(range(1, len(ans) + 1)):
            errors.append(f"prompt tem {len(slots)} espaços {{n}}, resposta tem {len(ans)} blocos")

    if not (it["explanation"] or "").strip():
        warnings.append("explicação vazia")
    return errors, warnings


def validate_items(entries, schema=None):
    """entries: lista de (arquivo, item). Devolve (erros, avisos, itens válidos)."""
    schema = schema or load_schema()
    errors, warnings, ok = [], [], []
    seen = {}
    for fname, it in entries:
        label = f"{fname}:{it.get('id', '?') if isinstance(it, dict) else '?'}"
        errs = check_schema(it, schema)
        if errs:
            errors += [f"{label}: {e}" for e in errs]
            continue
        if it["id"] in seen:
            errors.append(f"{label}: id duplicado (já usado em {seen[it['id']]})")
        else:
            seen[it["id"]] = fname
        e, w = _check_rules(it)
        errors += [f"{label}: {x}" for x in e]
        warnings += [f"{label}: {x}" for x in w]
        if not e:
            ok.append(it)
    return errors, warnings, ok


def load_items(folder=ITEMS_DIR):
    """Lê todos os .json da pasta (recursivo). Cada arquivo é uma lista de itens."""
    entries = []
    folder = Path(folder)
    for path in sorted(folder.rglob("*.json")):
        rel = path.relative_to(folder).as_posix()
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{rel}: o arquivo deve ser uma lista de itens")
        entries += [(rel, it) for it in data]
    return entries


def summarize(items):
    by_section = Counter(it["section"] for it in items)
    by_task = Counter((it["section"], it["task_type"], it["format"]) for it in items)
    by_status = Counter(it["status"] for it in items)
    lines = [f"Itens válidos: {len(items)}", "", "Por seção:"]
    lines += [f"  {s:<10} {n:>4}" for s, n in sorted(by_section.items())]
    lines += ["", "Por tarefa (seção / tipo / formato):"]
    lines += [f"  {s:<10} {t:<32} {f:<15} {n:>4}" for (s, t, f), n in sorted(by_task.items())]
    lines += ["", "Por status: " + ", ".join(f"{s} {n}" for s, n in sorted(by_status.items()))]
    gaps = sum(len(it["answer"]) for it in items if it["format"] == "fill_words")
    if gaps:
        lines.append(f"Lacunas de Complete the Words (dentro dos itens fill_words): {gaps}")
    return "\n".join(lines)


def main(argv):
    folder = Path(argv[1]) if len(argv) > 1 else ITEMS_DIR
    entries = load_items(folder)
    errors, warnings, ok = validate_items(entries)
    print(f"Arquivos lidos em {folder}: {len({f for f, _ in entries})}, itens: {len(entries)}")
    print(summarize(ok))
    if warnings:
        kinds = Counter(w.split(": ", 2)[-1] if "cita" not in w else "explicação cita letra inexistente"
                        for w in warnings)
        print(f"\nAvisos: {len(warnings)}")
        for k, n in kinds.most_common():
            print(f"  {n:>4} x {k}")
    if errors:
        print(f"\nERROS: {len(errors)}")
        for e in errors:
            print("  " + e)
        return 1
    print("\nNenhum erro.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
