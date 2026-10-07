"""Redistribui a letra correta das questões de múltipla escolha.

Medido em 2026-10-07: nos dados de origem, a resposta certa era "B" em 66% a
81% dos itens de quase todos os drills (e "C" em 7 das 10 questões do
diagnóstico). Quem marcasse sempre a mesma letra tirava nota de aprovado, o
que invalidava o diagnóstico e o painel de desempenho.

Em vez de reescrever centenas de itens à mão, a ordem das alternativas é
trocada aqui, na hora do build, de forma determinística (o mesmo item sai
sempre igual). As explicações citam alternativas como "(B)"; essas citações
são remapeadas junto. Ficam de fora os itens em que a letra tem significado
próprio: múltipla seleção e questões de inserção com marcadores [■A].
"""

import hashlib
import random
import re

REF_RE = re.compile(r"\(([A-D])\)")


def remap_refs(text, mapping):
    """Troca cada "(X)" pela nova letra daquela alternativa."""
    if not text:
        return text
    return REF_RE.sub(lambda m: f"({mapping.get(m.group(1), m.group(1))})", text)


def tag_refs(text):
    """Envolve cada "(X)" num <span> que o app.js atualiza quando embaralha
    as alternativas na tela (ver shuffleChoices em app.js)."""
    if not text:
        return text
    return REF_RE.sub(lambda m: f'<span class="optref" data-ref="{m.group(1)}">({m.group(1)})</span>', text)


def fixed_order(*texts):
    """Itens em que a letra tem significado próprio (inserção com [■A]) não
    podem ser embaralhados na tela."""
    return any("■" in (t or "") for t in texts)


def _seed(key):
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:12], 16)


def eligible(letters, correct, texts):
    if len(str(correct)) != 1 or correct not in letters:
        return False
    return not any("■" in t for t in texts)


def plan_targets(count, letters, key):
    """Sequência de letras-alvo com distribuição igual, em ordem embaralhada."""
    rng = random.Random(_seed(key))
    pool = (letters * (count // len(letters) + 1))[:count]
    rng.shuffle(pool)
    return pool


def permute(letters, correct, target, key):
    """Mapa letra antiga -> letra nova que leva `correct` para `target`."""
    rng = random.Random(_seed(key))
    others_old = [L for L in letters if L != correct]
    others_new = [L for L in letters if L != target]
    rng.shuffle(others_old)
    mapping = dict(zip(others_old, others_new))
    mapping[correct] = target
    return mapping


def rebalance_items(items, key, text_fields=("prompt", "explanation")):
    """Itens no formato dos drills: {"options": {letra: texto}, "correct": letra, ...}.
    Devolve uma lista nova; não altera a original."""
    out = [dict(it) for it in items]
    todo = [it for it in out
            if eligible(list(it["options"]), it["correct"],
                        list(it["options"].values()) + [str(it.get(f, "")) for f in text_fields])
            and not it.get("multi")]
    if not todo:
        return out
    letters = list(todo[0]["options"])
    targets = plan_targets(len(todo), letters, key)
    for it, target in zip(todo, targets):
        own = list(it["options"])
        if target not in own:
            target = own[_seed(key + str(it["num"])) % len(own)]
        mapping = permute(own, it["correct"], target, f'{key}:{it["num"]}')
        it["options"] = {new: it["options"][old] for old, new in sorted(mapping.items(), key=lambda kv: kv[1])}
        it["correct"] = target
        for f in text_fields:
            if f in it:
                it[f] = remap_refs(it[f], mapping)
    return out
