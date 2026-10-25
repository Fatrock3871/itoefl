import html as html_lib
import json
import re
import markdown as md
from render_quiz import render_quiz_drill
from render_srs import render_srs
from render_build import render_build_sentence
from render_errorlog import render_error_log
from render_weeklydash import render_weekly_dashboard
from drills_data import (
    MOD1_ACTION_DRILLS_A, MOD1_ACTION_DRILLS_B, MOD1_ACTION_DRILLS_C,
    MOD2_ACTION_DRILLS_A, MOD2_ACTION_DRILLS_B, MOD2_ACTION_DRILLS_C, MOD2_ACTION_DRILLS_D,
)
from build_sentence_data import BUILD_SENTENCE_ITEMS
from ctw_data import CTW_SETS
from render_ctw import render_ctw_group
from speaking_data import LISTEN_REPEAT_SETS, INTERVIEW_SETS
from render_speaking import render_speaking_group, render_speaking_set
from render_exam import convert_exam_blocks
from rebalance import rebalance_items
from render_wbox import render_wbox, EMAIL_MINUTES, DISCUSSION_MINUTES, DISCUSSION_MIN_WORDS
from render_redacao import render_essay_cta

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

# Módulo 0, Parte 5.1: mesmas 10 linhas do template estático de
# acompanhamento semanal, agora alimentando a tabela interativa
# (render_weeklydash.py) em vez de células em branco pra preencher à mão.
WEEKLY_DASH_METRICS = [
    ("complete_words", "% acerto: Complete the Words", "≥85%"),
    ("read_daily_academic", "% acerto: Read in Daily Life / Academic Passage", "≥80%"),
    ("listen_choose", "% acerto: Listen and Choose a Response", "≥85%"),
    ("listen_conv_announce_talk", "% acerto: Listen to Conversation/Announcement/Academic Talk", "≥80%"),
    ("build_sentence", "% acerto: Build a Sentence", "≥90%"),
    ("write_email", "Nota qualitativa: Write an Email (1–5)", "≥4.5"),
    ("write_discussion", "Nota qualitativa: Write for an Academic Discussion (1–5)", "≥4.5"),
    ("listen_repeat", "% fidelidade: Listen and Repeat", "≥90%"),
    ("take_interview", "Nota qualitativa: Take an Interview (1–5)", "≥4.5"),
    ("cefr_band", "Banda CEFR geral estimada", "5.0–6.0"),
    ("study_hours", "Horas de estudo deliberado na semana", "conforme cronograma"),
]


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


# Bloco de aprofundamento (docs/roadmap-expansao.md, seção B2): teoria densa
# que fica recolhida até o aluno abrir, ou que já vem aberta na "trilha
# completa" (seletor na sidebar, app.js). Marcação nos .md de consolidated/:
#
#     :::aprofundamento Por que o router pesa tanto
#     Texto em Markdown normal: parágrafos, listas, tabelas, ####.
#     :::
#
# As duas linhas de cerca ficam sozinhas, coladas na margem. O título é
# opcional. Dentro do bloco não entra título de Parte nem de subseção (#, ##,
# ###), porque são eles que montam o progresso e o accordion, e não entra
# outro bloco de aprofundamento.
DEEP_OPEN_RE = re.compile(r"^:::aprofundamento[ \t]*(.*)$")
DEEP_CLOSE_RE = re.compile(r"^:::[ \t]*$")


def render_deep(title, inner_html):
    title_html = f'<span class="deep-title">{html_lib.escape(title)}</span>' if title else ""
    return ('<details class="deep"><summary><span class="deep-kicker">Aprofundamento</span>'
            f'{title_html}</summary><div class="deep-body">{inner_html}</div></details>')


def extract_deep_blocks(text):
    """Tira os blocos :::aprofundamento do Markdown, deixando no lugar um
    parágrafo-marcador. Devolve (texto, {marcador: html do bloco})."""
    out, blocks, buf, title, start = [], {}, None, "", 0
    for n, line in enumerate(text.split("\n"), 1):
        if line[:1] in " \t>" and line.lstrip(" \t>").startswith(":::aprofundamento"):
            raise ValueError(f"aprofundamento: a cerca fica colada na margem, fora de lista e de citação (linha {n} do trecho)")
        opening = DEEP_OPEN_RE.match(line)
        if buf is None:
            if opening:
                buf, title, start = [], opening.group(1).strip(), n
            elif DEEP_CLOSE_RE.match(line):
                raise ValueError(f"aprofundamento: ':::' sem abertura (linha {n} do trecho)")
            else:
                out.append(line)
        elif opening:
            raise ValueError(f"aprofundamento: bloco dentro de bloco (linha {n} do trecho)")
        elif DEEP_CLOSE_RE.match(line):
            body = "\n".join(buf)
            if re.search(r"^#{1,3} ", body, flags=re.M):
                raise ValueError(f"aprofundamento {title!r}: use #### dentro do bloco, não #, ## ou ###")
            if not body.strip():
                raise ValueError(f"aprofundamento {title!r}: bloco vazio")
            token = f"@@APROFUNDAMENTO-{len(blocks)}@@"
            blocks[token] = render_deep(title, fix_checklists(md.markdown(body, extensions=MD_EXT)))
            out += ["", token, ""]
            buf = None
        else:
            buf.append(line)
    if buf is not None:
        raise ValueError(f"aprofundamento {title!r}: faltou a linha ':::' de fechamento (aberto na linha {start} do trecho)")
    return "\n".join(out), blocks


def to_html(text):
    text, deep = extract_deep_blocks(text)
    out = fix_checklists(md.markdown(text, extensions=MD_EXT))
    for token, block in deep.items():
        if out.count(f"<p>{token}</p>") != 1:
            raise ValueError("aprofundamento: o bloco precisa ficar fora de lista, tabela e citação")
        out = out.replace(f"<p>{token}</p>", block)
    return out


# O `markdown` puro (nossa única dependência, CLAUDE.md) não entende a
# sintaxe de task-list do GFM ("- [ ] item") — sem uma extensão de terceiro,
# "[ ] item" vira texto literal dentro do <li>, colchetes e tudo. Os
# checklists de saída de cada módulo usam exatamente essa sintaxe, então
# toda `<li>[ ] texto</li>` saía quebrada. Em vez de adicionar uma
# dependência nova só pra isso, um post-processo simples troca o `[ ]`/`[x]`
# literal por uma checkbox de verdade depois da conversão.
CHECKLIST_RE = re.compile(r"<li>\[([ xX])\]\s*(.*?)</li>")


def fix_checklists(html):
    def repl(m):
        checked = " checked" if m.group(1).lower() == "x" else ""
        return f'<li class="checklist-item"><label><input type="checkbox" disabled{checked}><span>{m.group(2)}</span></label></li>'
    return CHECKLIST_RE.sub(repl, html)


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

    # Parte 5.1: troca a tabela estática de acompanhamento semanal (células
    # em branco pra preencher à mão -- não faz sentido numa página web sem
    # nenhum jeito de digitar nela) pela versão interativa: input por
    # semana/métrica, salvo sozinho em localStorage.
    before_wd, after_wd = slice_lines(
        after,
        "| Métrica | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Meta |",
        "> ⚡ **Regra de ouro do dashboard:**",
    )
    after = before_wd + "\n\n" + render_weekly_dashboard(WEEKLY_DASH_METRICS) + "\n\n" + after_wd

    html_before = to_html(before)
    html_after = to_html(after)

    quiz_json = json.load(open("quiz_mod0.json", encoding="utf-8"))
    items = [{
        "num": q["num"], "prompt": f"Questão {q['num']}: {q['topic']}<br>{q['prompt']}",
        "options": q["options"], "correct": q["correct"],
        "explanation": f"<strong>Por que certa:</strong> {q['why_right']}<br><strong>Por que as outras erram:</strong> {q['why_wrong']}",
    } for q in quiz_json]
    # 7 das 10 respostas do diagnóstico eram "C" na origem (ver rebalance.py)
    items = rebalance_items(items, "mod0-diag")
    widget = render_quiz_drill(
        "mod0-diag", None,
        "Teste de Nivelamento Express: 10 questões de gramática, vocabulário e conectivos acadêmicos. Responda, confirme cada resposta para ver o gabarito, e refaça quando quiser.",
        None, items,
    )

    # painel "Seu desempenho real até agora" (Parte 4, depois de 4.3): soma os
    # acertos dos Action Drills interativos de M1/M2 (JS calcula em tempo real,
    # sem input manual) -- injeta antes da Parte 5 (o dashboard semanal,
    # interativo desde a mudança acima)
    live_score = (
        '<div class="live-score-panel" id="liveScorePanel">'
        '<p class="live-score-title">Seu desempenho real até agora, calculado automaticamente a partir dos '
        'exercícios que você já respondeu, sem precisar somar nada à mão.</p>'
        '<div class="live-score-grid">'
        '<div class="live-score-item"><span class="live-score-label">Reading</span>'
        '<span class="live-score-pct" id="liveScoreReadingPct">—</span>'
        '<span class="live-score-band" id="liveScoreReadingBand">Responda aos Action Drills do Módulo 1 para calcular</span></div>'
        '<div class="live-score-item"><span class="live-score-label">Listening</span>'
        '<span class="live-score-pct" id="liveScoreListeningPct">—</span>'
        '<span class="live-score-band" id="liveScoreListeningBand">Responda aos Action Drills do Módulo 2 para calcular</span></div>'
        '<div class="live-score-item"><span class="live-score-label">Writing · Build a Sentence</span>'
        '<span class="live-score-pct" id="liveScoreWritingPct">—</span>'
        '<span class="live-score-band" id="liveScoreWritingBand">Faça o drill interativo do Módulo 4 para calcular</span></div>'
        '<div class="live-score-item"><span class="live-score-label">Simulados</span>'
        '<span class="live-score-pct" id="liveScoreExamPct">—</span>'
        '<span class="live-score-band" id="liveScoreExamBand">Entregue um bloco de simulado do Módulo 7 para calcular</span></div>'
        '</div></div>'
    )
    # treino por nível: o app.js sorteia, a cada sessão, exercícios do site
    # cuja faixa CEFR inclui o nível estimado do aluno (ver "Treino no seu
    # nível" em app.js). Não cria questão nova: escolhe entre as que existem.
    level_practice = (
        '<div class="lvlp" id="levelPractice">'
        '<p class="lvlp-title">Treino no seu nível</p>'
        '<p class="lvlp-status" id="lvlpStatus">Termine as 10 questões do diagnóstico (Parte 3) para liberar uma sessão '
        'de exercícios escolhidos para o seu nível.</p>'
        '<ol class="lvlp-list" id="lvlpList"></ol>'
        '<button type="button" class="lvlp-shuffle" id="lvlpShuffle" hidden>Sortear outra sessão</button>'
        '</div>'
    )
    idx = html_after.find("<h2>PARTE 5")
    if idx != -1:
        html_after = html_after[:idx] + live_score + level_practice + html_after[idx:]

    # calculadora de score (Parte 4): entra logo antes de "4.3 Score Geral
    # Estimado". Usa a mesma tabela de 4.2; a conta é feita no app.js.
    calc_rows = "".join(
        f'<label class="scalc-row"><span class="scalc-name">{name}</span>'
        f'<input type="number" class="scalc-in" id="scalc-{key}" data-section="{key}" min="0" max="100" step="1" inputmode="numeric" placeholder="%">'
        f'<span class="scalc-band" data-band-for="{key}">sem dado</span></label>'
        for key, name in (("reading", "Reading"), ("listening", "Listening"), ("writing", "Writing"), ("speaking", "Speaking"))
    )
    score_calc = (
        '<div class="scalc" id="scoreCalc">'
        '<p class="scalc-title">Calculadora: digite o seu percentual de acerto em cada seção</p>'
        f'<div class="scalc-grid">{calc_rows}</div>'
        '<p class="scalc-total"><span>Banda geral estimada</span><strong id="scalcTotal">preencha as quatro seções</strong></p>'
        '<p class="scalc-note">Estimativa de treino pela tabela acima. A banda geral é a média das quatro, '
        'arredondada à meia banda mais próxima, como na prova. Não é nota oficial.</p>'
        '</div>'
    )
    idx = html_after.find("<h3>4.3")
    if idx == -1:
        raise ValueError("M0: não achei a seção 4.3 para encaixar a calculadora")
    html_after = html_after[:idx] + score_calc + html_after[idx:]

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
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), rebalance_items(d["items"], d["id"]), level=d.get("level"))
        for d in MOD1_ACTION_DRILLS_A
    )
    # Grupo A (2026-10-07): primeiro os textos no formato real da prova
    # (digitar o final das palavras, sem alternativas); depois os drills de
    # múltipla escolha que já existiam, agora apresentados como o que são:
    # treino de gramática e collocation, não o formato da tarefa.
    html_a = (
        to_html(before_a)
        + "<h3>Grupo A: Complete the Words no formato da prova</h3>"
        + '<p class="ctw-group-intro">Oito parágrafos, 10 lacunas cada, do B1 ao C1+. Em cada lacuna o começo da '
          'palavra está impresso e você digita o final. O campo aceita exatamente o número de letras que falta. '
          'Alvo: 3 minutos por texto.</p>'
        + render_ctw_group(CTW_SETS)
        + "<h3>Grupo A2: gramática e collocation em contexto (treino de base)</h3>"
        + '<p class="ctw-group-intro">Estes cinco textos <strong>não</strong> estão no formato da prova: aqui a lacuna '
          'é uma palavra inteira e há alternativas. Servem para treinar a decisão gramatical e de collocation que '
          'está por trás de cada lacuna do Grupo A.</p>'
        + widgets_a
    )

    # PARTE 5, Grupo B: troca os 5 textos curtos pelos widgets
    before_b, rest = slice_lines(rest, "### GRUPO B: READ IN DAILY LIFE", "### GRUPO C: READ AN ACADEMIC PASSAGE")
    widgets_b = "".join(
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), rebalance_items(d["items"], d["id"]), level=d.get("level"))
        for d in MOD1_ACTION_DRILLS_B
    )
    html_b = to_html(before_b) + "<h3>Grupo B: Read in Daily Life, exercícios interativos</h3>" + widgets_b

    # PARTE 5, Grupo C: troca as 3 passagens acadêmicas pelos widgets
    before_c, rest = slice_lines(rest, "### GRUPO C: READ AN ACADEMIC PASSAGE", "## PARTE 6: GABARITO COMENTADO")
    widgets_c = "".join(
        render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), rebalance_items(d["items"], d["id"]), level=d.get("level"))
        for d in MOD1_ACTION_DRILLS_C
    )
    html_c = to_html(before_c) + "<h3>Grupo C: Read an Academic Passage, exercícios interativos</h3>" + widgets_c

    # PARTE 6: remove as 3 tabelas de gabarito redundantes (a explicação já
    # aparece inline em cada widget acima); mantém o Score Consolidado
    before_g, rest = slice_lines(rest, "### GRUPO A: Complete the Words", "### GRUPO B: Read in Daily Life")
    _, rest = slice_lines(rest, "### GRUPO B: Read in Daily Life", "### GRUPO C: Read an Academic Passage")
    _, rest = slice_lines(rest, "### GRUPO C: Read an Academic Passage", "### SCORE CONSOLIDADO DOS DRILLS")

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
            render_quiz_drill(d["id"], d["title"], d["objective"], d.get("passage_html"), rebalance_items(d["items"], d["id"]), listen=True, level=d.get("level"))
            for d in drills
        )
        return to_html(before) + f"<h3>{label}, exercícios interativos</h3>" + widgets, rest

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
    _, rest = slice_lines(rest, "### GRUPO D: Listen to an Academic Talk", "### SCORE CONSOLIDADO")

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


def swap_placeholder(html_out, name, widget):
    """Troca o parágrafo '%%%NAME%%%' (deixado no .md) pelo widget."""
    token = f"<p>%%%{name}%%%</p>"
    if html_out.count(token) != 1:
        raise ValueError(f"placeholder %%%{name}%%% deveria aparecer 1 vez, achei {html_out.count(token)}")
    return html_out.replace(token, widget)


# cada enunciado de Write an Email / Academic Discussion do M4 é um parágrafo
# que começa com "Email N:" ou "Discussion N:" em negrito; a caixa de escrita
# entra logo depois dele
WBOX_PROMPT_RE = re.compile(r"(<p><strong>(Email|Discussion) (\d+):.*?</p>)", re.DOTALL)


def add_writing_boxes(html_out):
    count = {"Email": 0, "Discussion": 0}

    def repl(m):
        kind, num = m.group(2), m.group(3)
        count[kind] += 1
        if kind == "Email":
            box = render_wbox(f"mod4-email{num}", EMAIL_MINUTES)
        else:
            box = render_wbox(f"mod4-disc{num}", DISCUSSION_MINUTES, DISCUSSION_MIN_WORDS)
        return m.group(1) + box

    out = WBOX_PROMPT_RE.sub(repl, html_out)
    return out, count


# ---------- Módulo 3: markdown + conjuntos de Speaking + registro de erros ----------
def build_mod3():
    html_out = build_with_errlog(f"{SRC}/modulo_3_speaking.md", "mod3")
    # conjuntos no formato da prova: o .md marca o lugar com um placeholder
    html_out = swap_placeholder(html_out, "SPK_REPEAT", render_speaking_group(LISTEN_REPEAT_SETS, "repeat"))
    html_out = swap_placeholder(html_out, "SPK_INTERVIEW", render_speaking_group(INTERVIEW_SETS, "interview"))
    return html_out


# ---------- Módulo 4: markdown + Build a Sentence + registro de erros ----------
def build_mod4():
    raw = open(f"{SRC}/modulo_4_writing.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)
    before, after = split_registro_block(raw)
    errlog = render_error_log("mod4", ERRLOG_CODES["mod4"])
    html_out = to_html(before) + errlog + to_html(after)

    html_out, boxes = add_writing_boxes(html_out)
    if boxes != {"Email": 6, "Discussion": 6}:
        raise ValueError(f"esperava 6 caixas de e-mail e 6 de discussão, achei {boxes}")

    # id novo (m4build2): os itens mudaram de formato em 2026-10-07, então o
    # estado salvo do widget antigo (m4build) não se aplica a estes
    widget = render_build_sentence("m4build2", BUILD_SENTENCE_ITEMS)
    html_out = swap_placeholder(html_out, "BUILD_SENTENCE", widget)
    # chamada para o envio de redação (a tela em si fica no shell, build.py)
    return swap_placeholder(html_out, "REDACAO", render_essay_cta())


# ---------- Módulo 7: simulados com blocos interativos ----------
# Os blocos de múltipla escolha dos Simulados 2 e 3 viram widgets de prova
# (resposta do bloco inteiro, correção só na entrega). As questões continuam
# no .md: render_exam.convert_exam_blocks lê o texto e o gabarito de lá.
M7_EXPECTED_BLOCKS = 19
M7_EXPECTED_ITEMS = 59  # 62 até 2026-10-18: passagens do S2 e do S3 com 5 perguntas, conversa com 2


# Writing e Speaking dos simulados: o texto do .md continua igual; aqui, já
# em HTML, cada seção ganha o que precisa para ser feita na tela.
M7_SECTION_RE = re.compile(r"(?=<h[234]>)")
M7_MODEL_BLOCK_RE = re.compile(
    r"<p><strong>Resposta[- ]modelo[^<]*</strong>[^<]*</p>\s*<blockquote>.*?</blockquote>", re.DOTALL)
M7_MODEL_INLINE_RE = re.compile(r"<strong>Resposta modelo:</strong>\s*(<em>.*?</em>)", re.DOTALL)
M7_EXPECTED_PRODUCTION = {"repeat": 2, "interview": 2, "wbox": 4, "model_inline": 10, "model_block": 3}


def _reveal(label, inner):
    return f'<details class="reveal"><summary>{label}</summary>{inner}</details>'


def _list_texts(segment):
    """Textos dos itens da primeira lista numerada da seção, sem marcação."""
    m = re.search(r"<ol>(.*?)</ol>", segment, re.DOTALL)
    if not m:
        return None, []
    texts = []
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.DOTALL):
        li = re.sub(r"^\s*<strong>\([^)]*\)</strong>\s*", "", li.strip())  # rótulo "(Opinião)"
        txt = html_lib.unescape(re.sub(r"<[^>]+>", "", li)).strip().strip('"“”').strip()
        texts.append(txt)
    return m, texts


def enhance_m7_production(html_out):
    count = {k: 0 for k in M7_EXPECTED_PRODUCTION}
    out = []
    for seg in M7_SECTION_RE.split(html_out):
        head = re.match(r"<h4>(.*?)</h4>", seg)
        title = re.sub(r"<[^>]+>", "", head.group(1)) if head else ""

        if title.startswith("Listen and Repeat") or title.startswith("Take an Interview"):
            mode = "repeat" if title.startswith("Listen") else "interview"
            m, texts = _list_texts(seg)
            if m and texts:
                count[mode] += 1
                n = count[mode]
                widget = render_speaking_set({
                    "id": f"mod7-{mode}{n}",
                    "level": "A2–C2",
                    "title": ("Listen and Repeat" if mode == "repeat" else "Take an Interview") + " do simulado",
                    "scenario": ("Listen to each sentence once and repeat it. Repeat only once."
                                 if mode == "repeat" else
                                 "An interviewer will ask you questions. Answer each one as fully as you can in the time allowed."),
                    "items": texts,
                }, mode)
                seg = seg[:m.start()] + widget + seg[m.end():]

        elif title.startswith("Build a Sentence"):
            seg, n = M7_MODEL_INLINE_RE.subn(lambda mm: _reveal("Ver resposta", mm.group(1)), seg)
            count["model_inline"] += n

        elif title.startswith("Write an Email") or title.startswith("Write for an Academic Discussion"):
            seg, n = M7_MODEL_BLOCK_RE.subn(lambda mm: _reveal("Ver resposta-modelo", mm.group(0)), seg)
            count["model_block"] += n
            count["wbox"] += 1
            if title.startswith("Write an Email"):
                box = render_wbox(f'mod7-email{count["wbox"]}', EMAIL_MINUTES)
            else:
                box = render_wbox(f'mod7-disc{count["wbox"]}', DISCUSSION_MINUTES, DISCUSSION_MIN_WORDS)
            # a caixa entra antes da primeira resposta-modelo; sem modelo, no
            # fim da seção (antes de um <hr>, se houver)
            cut = seg.find('<details class="reveal">')
            if cut == -1:
                cut = seg.rfind("<hr")
                if cut == -1:
                    cut = len(seg)
            seg = seg[:cut] + box + seg[cut:]
        out.append(seg)
    return "".join(out), count


def build_mod7():
    raw = open(f"{SRC}/modulo_7_simulados.md", encoding="utf-8").read()
    raw = strip_title_banner(raw)
    raw, widgets, report = convert_exam_blocks(raw, "mod7")
    if report["skipped"] or report["blocks"] != M7_EXPECTED_BLOCKS or report["items"] != M7_EXPECTED_ITEMS:
        raise ValueError(
            f"M7: esperava {M7_EXPECTED_BLOCKS} blocos e {M7_EXPECTED_ITEMS} itens interativos, "
            f"achei {report}. Se o .md mudou de propósito, atualize as constantes."
        )
    html_out = to_html(raw)
    for token, widget in widgets.items():
        html_out = swap_placeholder(html_out, token.strip("%"), widget)
    html_out, production = enhance_m7_production(html_out)
    if production != M7_EXPECTED_PRODUCTION:
        raise ValueError(f"M7 Writing/Speaking: esperava {M7_EXPECTED_PRODUCTION}, achei {production}")
    return html_out


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
        "mod2": build_mod2(),  # Grupos A/B/C/D (Action Drills) interativos, 36 itens
        "mod3": build_mod3(),  # formulário de registro de erros (Parte 7)
        "mod4": build_mod4(),  # Build a Sentence + registro de erros
        "mod5": build_mod5(),  # formulário de registro de erros (Parte 9)
        "mod6": build_mod6(),  # SRS + registro de erros (Parte 11)
        "mod7": build_mod7(),  # blocos de simulado interativos, 59 itens
        "mod8": build_plain(f"{SRC}/modulo_8_examday.md"),
        "mod9": build_plain(f"{SRC}/modulo_9_braziliantraps.md"),
    }
    final = {k: add_progress_hooks(v, k) for k, v in frag.items()}
    json.dump(final, open("module_fragments_final.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("built:", {k: len(v) for k, v in final.items()})
    print("leftover %%% placeholders:", any("%%%" in v for v in final.values()))
    stray = [k for k, v in final.items() if ":::aprofundamento" in v or "@@APROFUNDAMENTO" in v]
    if stray:
        raise ValueError(f"aprofundamento: marcação não convertida em {stray} (bloco dentro de questão de simulado ou de widget?)")
    print("blocos de aprofundamento:", {k: v.count('<details class="deep">') for k, v in final.items() if '<details class="deep">' in v} or 0)


if __name__ == "__main__":
    main()
