import json
import re
import markdown as md
from render_quiz import render_quiz_drill
from render_srs import render_srs
from render_build import render_build_sentence
from render_errorlog import render_error_log
from drills_data import (
    MOD1_DRILLS, MOD2_DRILLS,
    MOD1_ACTION_DRILLS_A, MOD1_ACTION_DRILLS_B, MOD1_ACTION_DRILLS_C,
    MOD2_ACTION_DRILLS_A, MOD2_ACTION_DRILLS_B, MOD2_ACTION_DRILLS_C, MOD2_ACTION_DRILLS_D,
)
from build_sentence_data import BUILD_SENTENCE_ITEMS

SRC = "../consolidated"

# Item 10 da review de UX (2026-09-16): o "Registro" de cada Protocolo de
# Análise de Erros (Parte 7 de M1-M4, Parte 9/Seção 11 de M5/M6) era um
# template de texto pra preencher à mão em outro lugar. Vira um mini-
# formulário (render_errorlog.render_error_log) com o histórico salvo no
# navegador. Códigos abaixo = mesma tabela de cada módulo, só copiados pro
# Python pra virar checkbox. M7 fica de fora (protocolo de triagem próprio,
# mais elaborado — decisão de design à parte, junto com o resto do M7).
ERRLOG_CODES = {
    "mod1": [
        ("R1", "Não entendi a pergunta"), ("R2", "Caí num distrator"),
        ("R3", "Lacuna de gramática (CTW)"), ("R4", "Lacuna de vocabulário / collocation"),
        ("R5", "Tempo"), ("R6", "Desatenção / releitura"),
    ],
    "mod2": [
        ("L1", "Não decodifiquei o áudio"), ("L2", "Não entendi a pergunta"),
        ("L3", "Caí num distrator"), ("L4", "Anotação errada"),
        ("L5", "Vocabulário"), ("L6", "Atenção / fim do áudio"),
    ],
    "mod3": [
        ("S1", "Fonema / segmento"), ("S2", "Acento de palavra"),
        ("S3", "Ritmo / acento de frase"), ("S4", "Fluência"),
        ("S5", "Gramática sob pressão"), ("S6", "Estrutura da resposta"),
    ],
    "mod4": [
        ("W1", "Estrutura de frase"), ("W2", "Gramática de verbo"),
        ("W3", "Artigo / preposição / word form"), ("W4", "Registro"),
        ("W5", "Conteúdo / prompt"), ("W6", "Léxico"),
    ],
    "mod5": [
        ("RG1", "Over-formality / cerimônia"), ("RG2", "Register clash"),
        ("RG3", "Sofisticação sem controle"), ("RG4", "Repetição lexical"),
        ("RG5", "Conector impreciso ou ausente"), ("RG6", "Densidade plana"),
    ],
    "mod6": [
        ("V1", "Forma errada da palavra"), ("V2", "Colocação errada"),
        ("V3", "Falso cognato"), ("V4", "Registro trocado"),
        ("V5", "Overreach (usou palavra que não controla)"), ("V6", "Sinônimo impreciso"),
    ],
}


def split_registro_block(raw):
    """Corta o template antigo de 'Registro' (preencher à mão) do resto do
    texto -- tanto o formato de bloco de código (M1-M4) quanto o de tabela
    semanal (M5/M6). Retorna (before, after); se não achar, (raw, "")."""
    fenced = re.search(r"\*\*Registro \([^)]*\):\*\*\n\n```\n.*?\n```", raw, re.DOTALL)
    if fenced:
        return raw[:fenced.start()], raw[fenced.end():]
    table = re.search(r"### Registro semanal\n\n\|.*\n(?:\|.*\n)+", raw)
    if table:
        return raw[:table.start()], raw[table.end():]
    return raw, ""
MD_EXT = ["tables", "fenced_code", "sane_lists"]


def to_html(text):
    return md.markdown(text, extensions=MD_EXT)


def strip_title_banner(text):
    """Cut everything before the first '## PARTE 1' (or '## PARTE') heading."""
    m = re.search(r"^## PARTE 1", text, flags=re.M)
    if m:
        return text[m.start():]
    m = re.search(r"^## PARTE", text, flags=re.M)
    return text[m.start():] if m else text


def slice_lines(text, start_marker, end_marker):
    """Return (before, cut, after) split on line-start markers."""
    lines = text.split("\n")
    start_idx = next(i for i, l in enumerate(lines) if l.startswith(start_marker))
    end_idx = next(i for i, l in enumerate(lines) if l.startswith(end_marker))
    before = "\n".join(lines[:start_idx])
    after = "\n".join(lines[end_idx:])
    return before, after


# ---------- Módulo 0: diagnostic quiz ----------
def build_mod0():
    raw = open(f"{SRC}/modulo_0_embarque.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)
    before, after = slice_lines(raw, "### 3.2 As 10 Questões", "## PARTE 4")
    html_before = to_html(before)
    html_after = to_html(after)

    quiz_json = json.load(open("quiz_mod0.json", encoding="utf-8"))
    items = [{
        "num": q["num"], "prompt": f"Questão {q['num']} — {q['topic']}<br>{q['prompt']}",
        "options": q["options"], "correct": q["correct"],
        "explanation": f"<strong>Por que certa:</strong> {q['why_right']}<br><strong>Por que as outras erram:</strong> {q['why_wrong']}",
    } for q in quiz_json]
    widget = render_quiz_drill(
        "mod0-diag", None,
        "Teste de Nivelamento Express — 10 questões de gramática, vocabulário e conectivos acadêmicos. Responda, confirme cada resposta para ver o gabarito, e refaça quando quiser.",
        None, items,
    )

    # painel "Seu desempenho real até agora" (Parte 4, depois de 4.3): soma os
    # acertos dos Action Drills interativos de M1/M2 (JS calcula em tempo real,
    # sem input manual) — injeta antes da Parte 5, que hoje é preenchida à mão
    live_score = (
        '<div class="live-score-panel" id="liveScorePanel">'
        '<p class="live-score-title">Seu desempenho real até agora — calculado automaticamente a partir dos '
        'Action Drills que você já respondeu nos Módulos 1 e 2, sem precisar somar nada à mão.</p>'
        '<div class="live-score-grid">'
        '<div class="live-score-item"><span class="live-score-label">Reading</span>'
        '<span class="live-score-pct" id="liveScoreReadingPct">—</span>'
        '<span class="live-score-band" id="liveScoreReadingBand">Responda os Action Drills do Módulo 1 para calcular</span></div>'
        '<div class="live-score-item"><span class="live-score-label">Listening</span>'
        '<span class="live-score-pct" id="liveScoreListeningPct">—</span>'
        '<span class="live-score-band" id="liveScoreListeningBand">Responda os Action Drills do Módulo 2 para calcular</span></div>'
        '</div></div>'
    )
    idx = html_after.find("<h2>PARTE 5")
    if idx != -1:
        html_after = html_after[:idx] + live_score + html_after[idx:]

    return html_before + widget + html_after


# ---------- Módulo 1: Reading drills ----------
# NOTA (2026-09-16): build_mod1() foi reescrita pra estrutura atual do módulo
# (7 partes, "PARTE 5: ACTION DRILLS"). A versão anterior fatiava em
# "PARTE 3: ACTION DRILLS", um marcador que não existe mais desde que o
# módulo foi renumerado/expandido — main() usava build_plain() nesse meio
# tempo, então nada disso rodava. Primeira fatia convertida: Grupo A
# (Complete the Words, 32 itens). Grupos B e C seguem estáticos por ora.
def build_mod1():
    raw = open(f"{SRC}/modulo_1_reading.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)

    # PARTE 5, Grupo A: troca o texto estático das 5 lacunas pelos widgets
    before_a, rest = slice_lines(raw, "### GRUPO A: COMPLETE THE WORDS", "### GRUPO B: READ IN DAILY LIFE")
    widgets_a = "".join(
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), d["items"])
        for d in MOD1_ACTION_DRILLS_A
    )
    html_a = to_html(before_a) + "<h3>Grupo A: Complete the Words — exercícios interativos</h3>" + widgets_a

    # PARTE 5, Grupo B: troca os 5 textos curtos pelos widgets
    before_b, rest = slice_lines(rest, "### GRUPO B: READ IN DAILY LIFE", "### GRUPO C: READ AN ACADEMIC PASSAGE")
    widgets_b = "".join(
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), d["items"])
        for d in MOD1_ACTION_DRILLS_B
    )
    html_b = to_html(before_b) + "<h3>Grupo B: Read in Daily Life — exercícios interativos</h3>" + widgets_b

    # PARTE 5, Grupo C: troca as 3 passagens acadêmicas pelos widgets
    # (C3.7 é múltipla seleção — "multi": 3 no item, suportado pelo widget)
    before_c, rest = slice_lines(rest, "### GRUPO C: READ AN ACADEMIC PASSAGE", "## PARTE 6: GABARITO COMENTADO")
    widgets_c = "".join(
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), d["items"])
        for d in MOD1_ACTION_DRILLS_C
    )
    html_c = to_html(before_c) + "<h3>Grupo C: Read an Academic Passage — exercícios interativos</h3>" + widgets_c

    # PARTE 6: remove as 3 tabelas de gabarito redundantes (a explicação já
    # aparece inline em cada widget acima); mantém o Score Consolidado
    before_g, rest = slice_lines(rest, "### GRUPO A: Complete the Words", "### GRUPO B: Read in Daily Life")
    _, rest = slice_lines(rest, "### GRUPO B: Read in Daily Life", "### GRUPO C: Read an Academic Passage")
    _, rest = slice_lines(rest, "### GRUPO C: Read an Academic Passage", "### 📊 SCORE CONSOLIDADO DOS DRILLS")

    # PARTE 7: troca o template de "Registro" (preencher à mão) pelo
    # formulário que salva histórico
    before_r, after_r = split_registro_block(rest)
    errlog = render_error_log("mod1", ERRLOG_CODES["mod1"])
    html_rest = to_html(before_g) + to_html(before_r) + errlog + to_html(after_r)

    return html_a + html_b + html_c + html_rest


# ---------- Módulo 2: Listening drills ----------
# NOTA (2026-09-16): mesma reescrita de build_mod1() — a versão anterior
# fatiava em "PARTE 3: ACTION DRILLS", marcador que não existe mais (Action
# Drills é Parte 5 na estrutura atual, 4 grupos A-D).
def build_mod2():
    raw = open(f"{SRC}/modulo_2_listening.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)

    def swap_group(rest, start_marker, end_marker, label, drills):
        before, rest = slice_lines(rest, start_marker, end_marker)
        widgets = "".join(
            render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), d["items"])
            for d in drills
        )
        return to_html(before) + f"<h3>{label} — exercícios interativos</h3>" + widgets, rest

    rest = raw
    html_a, rest = swap_group(rest, "### GRUPO A: LISTEN AND CHOOSE A RESPONSE", "### GRUPO B: LISTEN TO A CONVERSATION", "Grupo A: Listen and Choose a Response", MOD2_ACTION_DRILLS_A)
    html_b, rest = swap_group(rest, "### GRUPO B: LISTEN TO A CONVERSATION", "### GRUPO C: LISTEN TO AN ANNOUNCEMENT", "Grupo B: Listen to a Conversation", MOD2_ACTION_DRILLS_B)
    html_c, rest = swap_group(rest, "### GRUPO C: LISTEN TO AN ANNOUNCEMENT", "### GRUPO D: LISTEN TO AN ACADEMIC TALK", "Grupo C: Listen to an Announcement", MOD2_ACTION_DRILLS_C)
    html_d, rest = swap_group(rest, "### GRUPO D: LISTEN TO AN ACADEMIC TALK", "## PARTE 6: GABARITO COMENTADO", "Grupo D: Listen to an Academic Talk", MOD2_ACTION_DRILLS_D)

    # PARTE 6: remove as 4 tabelas de gabarito redundantes (a explicação já
    # aparece inline em cada widget acima); mantém o Score Consolidado
    before_g, rest = slice_lines(rest, "### GRUPO A: Listen and Choose a Response", "### GRUPO B: Listen to a Conversation")
    _, rest = slice_lines(rest, "### GRUPO B: Listen to a Conversation", "### GRUPO C: Listen to an Announcement")
    _, rest = slice_lines(rest, "### GRUPO C: Listen to an Announcement", "### GRUPO D: Listen to an Academic Talk")
    _, rest = slice_lines(rest, "### GRUPO D: Listen to an Academic Talk", "### 📊 SCORE CONSOLIDADO")

    # PARTE 7: troca o template de "Registro" (preencher à mão) pelo
    # formulário que salva histórico
    before_r, after_r = split_registro_block(rest)
    errlog = render_error_log("mod2", ERRLOG_CODES["mod2"])
    html_rest = to_html(before_g) + to_html(before_r) + errlog + to_html(after_r)

    return html_a + html_b + html_c + html_d + html_rest


# ---------- Módulos 7, 8, 9: plain markdown (no MC quiz) ----------
def build_plain(path):
    raw = open(path, encoding="utf-8").read()
    raw = strip_title_banner(raw)
    return to_html(raw)


def build_with_errlog(path, mod_key):
    """M3 e M5 não têm outro widget além do formulário de registro de erros."""
    raw = open(path, encoding="utf-8").read()
    raw = strip_title_banner(raw)
    before, after = split_registro_block(raw)
    errlog = render_error_log(mod_key, ERRLOG_CODES[mod_key])
    return to_html(before) + errlog + to_html(after)


# ---------- Módulo 3: markdown + formulário de registro de erros ----------
def build_mod3():
    return build_with_errlog(f"{SRC}/modulo_3_speaking.md", "mod3")


# ---------- Módulo 4: markdown + Build a Sentence + registro de erros ----------
def build_mod4():
    raw = open(f"{SRC}/modulo_4_writing.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)
    before, after = split_registro_block(raw)
    errlog = render_error_log("mod4", ERRLOG_CODES["mod4"])
    html_out = to_html(before) + errlog + to_html(after)

    widget = render_build_sentence("m4build", BUILD_SENTENCE_ITEMS)
    # injeta logo antes do heading "Drill 2 ... Write an Email"
    idx = html_out.find("Drill 2")
    if idx == -1:
        return html_out + widget
    h3 = html_out.rfind("<h3", 0, idx)
    if h3 == -1:
        h3 = idx
    return html_out[:h3] + widget + "\n" + html_out[h3:]


# ---------- Módulo 5: markdown + formulário de registro de erros ----------
def build_mod5():
    return build_with_errlog(f"{SRC}/modulo_5_registro.md", "mod5")


# ---------- Módulo 6: markdown + SRS + registro de erros ----------
def build_mod6():
    raw = open(f"{SRC}/modulo_6_vocabulary.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)
    before, after = split_registro_block(raw)
    errlog = render_error_log("mod6", ERRLOG_CODES["mod6"])
    html_out = to_html(before) + errlog + to_html(after)

    cards = json.load(open("vocab_kit.json", encoding="utf-8"))
    widget = render_srs("kit50", cards)
    # injeta o widget de flashcards logo após o Kit de 50 palavras (Parte 8),
    # antes dos drills de vocabulário (Parte 9) -- NOTA: esse marcador era
    # "<h2>SEÇÃO 9" e ficou obsoleto (silenciosamente!) quando M6 trocou pra
    # "PARTE" nesta mesma sessão; sem o achado aqui, o widget cairia sempre
    # no fallback (fim do módulo) em vez do lugar certo.
    idx = html_out.find("<h2>PARTE 9")
    if idx == -1:
        return html_out + widget
    return html_out[:idx] + widget + "\n" + html_out[idx:]


def add_progress_hooks(html, modkey):
    counter = {"i": 0}

    def repl(m):
        tag, text = m.group(1), m.group(2)
        counter["i"] += 1
        pid = f"{modkey}-{counter['i']}"
        return (f'<{tag} id="{pid}h" class="prog-head">'
                f'<label class="prog-check"><input type="checkbox" data-pid="{pid}" class="pchk"><span class="box"></span></label>'
                f'<span class="htext">{text}</span></{tag}>')
    # apenas h2 (uma marca de progresso por Parte/Seção, não por subseção)
    return re.sub(r"<(h2)>(.*?)</\1>", repl, html)


def main():
    frag = {
        "mod0": build_mod0(),
        "mod1": build_mod1(),  # Grupos A/B/C (Action Drills) interativos, 67 itens
        "mod2": build_mod2(),  # Grupos A/B/C/D (Action Drills) interativos, 51 itens
        "mod3": build_mod3(),  # formulário de registro de erros (Parte 7)
        "mod4": build_mod4(),  # Build a Sentence + registro de erros
        "mod5": build_mod5(),  # formulário de registro de erros (Parte 9)
        "mod6": build_mod6(),  # SRS + registro de erros (Parte 11)
        "mod7": build_plain(f"{SRC}/modulo_7_simulados.md"),
        "mod8": build_plain(f"{SRC}/modulo_8_examday.md"),
        "mod9": build_plain(f"{SRC}/modulo_9_braziliantraps.md"),
    }
    final = {k: add_progress_hooks(v, k) for k, v in frag.items()}
    json.dump(final, open("module_fragments_final.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("built:", {k: len(v) for k, v in final.items()})
    print("leftover %%% placeholders:", any("%%%" in v for v in final.values()))


if __name__ == "__main__":
    main()
