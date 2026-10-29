"""Renderiza a tela de envio de redação para correção (Etapa 3, versão
assistida): a escolha entre os 10 temas, a tela "antes de começar" com todas
as regras, a escrita com cronômetro sem pausa, a confirmação do envio, o
histórico com devolutiva e gráfico, e o painel do corretor.

O comportamento fica em app/redacao.js; as regras que valem de verdade, em
supabase/functions/_shared/redacao.js (servidor e site). Aqui só o HTML e os
textos.
"""

import html
import json
import re

from redacao_data import (
    EMAIL_TOPICS, DISCUSSION_TOPICS, TOPICS,
    INTERVALO_DIAS, PRAZO_DIAS_UTEIS, MINUTOS, MIN_PALAVRAS_DISCUSSAO,
)
from render_wbox import render_essay_box
from icons import icon

TASK_NAME = {"email": "Write an Email", "discussion": "Write for an Academic Discussion"}

# Rubrica do iTOEFL, alinhada aos critérios da ETS (decisão de 2026-10-13).
# Mostrada ao aluno antes de começar e copiada no texto que vai para a IA.
RUBRICA = [
    {"id": "cumprimento", "nome": "Cumprimento da tarefa",
     "avalia": "E-mail: os 3 pontos pedidos, propósito claro, destinatário certo. Discussão: posição clara, "
               "responde à pergunta do professor, dialoga com um colega.",
     "5": "Tudo cumprido e desenvolvido.", "3": "Cumpre quase tudo, algum ponto raso ou faltando.",
     "1": "Fora do tema ou pontos ausentes."},
    {"id": "organizacao", "nome": "Organização e coesão",
     "avalia": "Ordem lógica, frases e parágrafos ligados, conectores naturais.",
     "5": "Fluxo natural, sem saltos.", "3": "Organizado, conectores repetitivos.", "1": "Ideias soltas."},
    {"id": "gramatica", "nome": "Gramática",
     "avalia": "Precisão e variedade de estruturas.",
     "5": "Variada e quase sem erros.", "3": "Erros que não atrapalham.", "1": "Erros que atrapalham o sentido."},
    {"id": "vocabulario", "nome": "Vocabulário e registro",
     "avalia": "Precisão, variedade, registro adequado (e-mail formal e cortês; discussão acadêmica).",
     "5": "Preciso, variado, registro certo.", "3": "Adequado, repetitivo.", "1": "Limitado ou registro errado."},
]

# códigos de erro do M4 (Parte 7, protocolo de análise de erros de Writing)
CODIGOS = {
    "W1": "Estrutura de frase", "W2": "Gramática de verbo", "W3": "Artigo, preposição ou forma da palavra",
    "W4": "Registro", "W5": "Conteúdo e enunciado", "W6": "Léxico",
}

REGRAS = [
    f"<b>Tempo:</b> {MINUTOS['email']} minutos no Write an Email e {MINUTOS['discussion']} minutos no Write for an "
    "Academic Discussion, os tempos da prova. O cronômetro começa quando você clica em Começar e não pausa, "
    "nem se você fechar a janela ou recarregar a página.",
    "<b>Tempo esgotado:</b> quando o cronômetro zera, o texto trava. Aí você decide se envia ou descarta.",
    "<b>Tamanho:</b> no e-mail não há mínimo oficial; o recomendado é de 80 a 150 palavras. Na discussão, "
    f"o envio só libera a partir de {MIN_PALAVRAS_DISCUSSAO} palavras.",
    f"<b>Frequência:</b> 1 redação a cada {INTERVALO_DIAS} dias, contados do seu último envio.",
    f"<b>Devolução:</b> em até {PRAZO_DIAS_UTEIS} dias úteis (de segunda a sexta, sem feriados nacionais). "
    "A data prevista aparece na hora do envio.",
    "<b>Devolutiva:</b> nota de 0 a 5, nível estimado, a nota de cada um dos 4 critérios com uma frase de "
    "justificativa, até 5 trechos do seu texto corrigidos e explicados em português, uma ou duas frases suas "
    "reescritas um nível acima e uma prioridade de estudo.",
    "<b>Correção:</b> feita pela nossa equipe com apoio de ferramenta de IA e revisada por uma pessoa. A nota "
    "é uma estimativa de treino, não a nota oficial da ETS.",
    "<b>Privacidade:</b> no primeiro envio pedimos o seu consentimento. O texto é analisado com ferramenta de "
    "IA de terceiros, sem os seus dados pessoais, e é apagado junto com a sua conta.",
    "<b>Quem pode enviar:</b> todo aluno com plano em dia.",
]

AVISO = (
    f"Você tem {MINUTOS['email']} minutos (e-mail) ou {MINUTOS['discussion']} minutos (discussão), como na prova. "
    f"O cronômetro não pausa. Você pode enviar 1 redação a cada {INTERVALO_DIAS} dias, e a devolutiva chega em "
    f"até {PRAZO_DIAS_UTEIS} dias úteis, com nota de 0 a 5, nível estimado e comentários. A correção é feita pela "
    "nossa equipe com apoio de IA e é uma estimativa de treino, não a nota oficial."
)

CONSENTIMENTO = (
    "Autorizo que esta e as próximas redações que eu enviar sejam analisadas pela equipe do iTOEFL com apoio "
    "de ferramenta de inteligência artificial de terceiros. Só o texto e o enunciado são enviados à ferramenta, "
    "sem nome, e-mail ou outro dado pessoal. As redações ficam guardadas na minha conta e são apagadas quando "
    "eu excluir a conta."
)

e = html.escape


def module_parts(md_text):
    """Títulos das Partes de um módulo, na ordem ('## PARTE N: TÍTULO')."""
    found = re.findall(r"^## PARTE (\d+)\s*[:·]\s*(.+?)\s*$", md_text, flags=re.M | re.I)
    nums = [int(n) for n, _ in found]
    if nums != list(range(1, len(nums) + 1)):
        raise ValueError(f"Partes fora de ordem: {nums}")
    return [t for _, t in found]


def prompt_text(t):
    """O enunciado em texto puro, como vai no pedido à IA."""
    if "points" in t:
        lines = [f"To: {t['to']}", f"Subject: {t['subject']}", "", t["situation"], "",
                 "In your email, do the following:"] + [f"- {p}" for p in t["points"]]
    else:
        lines = [f"Course: {t['course']}", f"{t['professor']}: {t['question']}", ""] + \
                [f"{name}: {post}" for name, post in t["students"]]
    return "\n".join(lines)


def prompt_html(t):
    if "points" in t:
        pts = "".join(f"<li>{e(p)}</li>" for p in t["points"])
        body = (
            f'<p class="essay-prompt-situation">{e(t["situation"])}</p>'
            '<p>In your email, do the following:</p>'
            f'<ul class="essay-prompt-points">{pts}</ul>'
            '<div class="essay-mailhead">'
            f'<p><span>To:</span> {e(t["to"])}</p>'
            f'<p><span>Subject:</span> {e(t["subject"])}</p>'
            '</div>'
        )
    else:
        posts = "".join(
            f'<div class="essay-post"><p class="essay-post-name">{e(name)}</p><p>{e(text)}</p></div>'
            for name, text in t["students"]
        )
        body = (
            '<p class="essay-prompt-intro">Your professor has posted a question for the class. Read it and your '
            "classmates' posts, then write a post of your own: state your opinion, support it, and add something "
            f'new to the discussion. A strong post has at least {MIN_PALAVRAS_DISCUSSAO} words.</p>'
            f'<div class="essay-post essay-post-prof"><p class="essay-post-name">{e(t["professor"])} · {e(t["course"])}</p>'
            f'<p>{e(t["question"])}</p></div>'
            f'{posts}'
        )
    task = "email" if "points" in t else "discussion"
    return (f'<div class="essay-prompt" data-topic="{t["id"]}" lang="en" hidden>'
            f'<p class="essay-prompt-task">{TASK_NAME[task]}</p>{body}</div>')


def _topic_button(t, task):
    return (
        f'<button type="button" class="essay-topic" data-topic="{t["id"]}">'
        f'<span class="essay-topic-id">{t["id"]}</span>'
        f'<span class="essay-topic-body"><b>{e(t["titulo"])}</b>'
        f'<span class="essay-topic-goal">{e(t["objetivo"])}</span></span></button>'
    )


def topics_json(parts):
    data = {
        "topics": [
            {"id": t["id"], "task": "email" if "points" in t else "discussion", "titulo": t["titulo"],
             "objetivo": t["objetivo"], "enunciado": prompt_text(t)}
            for t in TOPICS
        ],
        "rubrica": RUBRICA,
        "codigos": CODIGOS,
        "partes": parts,
    }
    # </script> dentro do JSON fecharia a tag antes da hora
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_essay_cta():
    """Chamada no M4 para a tela de redação."""
    return (
        '<div class="essay-cta">'
        '<p class="essay-cta-kicker">Correção de redação</p>'
        f'<p>Escreva um e-mail ou uma discussão no tempo da prova e receba nota de 0 a 5, nível estimado e '
        f'comentários em até {PRAZO_DIAS_UTEIS} dias úteis. Você pode enviar 1 redação a cada {INTERVALO_DIAS} dias.</p>'
        '<button type="button" class="essay-open">Escolher um tema</button>'
        '</div>'
    )


def _field(label, control):
    return f'<label class="review-field"><span class="auth-label">{label}</span>{control}</label>'


def render_review_modal():
    """Painel do corretor. Fica escondido para todo mundo: o app/redacao.js só
    o abre para conta com linha na tabela `admins` (e o banco e a function
    review-essay conferem de novo, então mostrar a tela não dá poder nenhum)."""
    notas = '<option value="">escolha</option>' + "".join(
        f'<option value="{n / 2:g}">{str(n / 2).replace(".0", "").replace(".", ",")}</option>' for n in range(11))
    crit = "".join(
        f'<fieldset class="review-set"><legend>{e(c["nome"])}</legend>'
        + _field("Nota", f'<select data-crit="{c["id"]}" data-key="nota">{notas}</select>')
        + _field("Justificativa (1 frase)", f'<input type="text" data-crit="{c["id"]}" data-key="justificativa" maxlength="1500">')
        + '</fieldset>'
        for c in RUBRICA
    )
    codigos = '<option value="">sem código</option>' + "".join(
        f'<option value="{k}">{k} · {e(v)}</option>' for k, v in CODIGOS.items())
    trechos = "".join(
        f'<fieldset class="review-set"><legend>Trecho {i}</legend>'
        + _field("Original (copiado do aluno)", f'<input type="text" data-trecho="{i}" data-key="original" lang="en" maxlength="1500">')
        + _field("Correção (em inglês)", f'<input type="text" data-trecho="{i}" data-key="correcao" lang="en" maxlength="1500">')
        + _field("Explicação (em português)", f'<input type="text" data-trecho="{i}" data-key="explicacao" maxlength="1500">')
        + _field("Código", f'<select data-trecho="{i}" data-key="codigo">{codigos}</select>')
        + '</fieldset>'
        for i in range(1, 6)
    )
    return f'''
<div class="account-modal essay-modal" id="reviewModal" role="dialog" aria-modal="true" aria-label="Painel do corretor" hidden>
<div class="account-modal-backdrop" id="reviewBackdrop"></div>
<div class="account-card essay-card">
<button type="button" class="account-close" id="reviewClose" aria-label="Fechar">{icon("close")}</button>
<div class="account-head"><span class="account-head-icon">{icon("pen")}</span>
<div><p class="account-kicker">Equipe</p><h2 class="account-title">Painel do corretor</h2></div></div>

<section class="essay-view" id="reviewList">
<p class="essay-status" id="reviewStatus" role="status">Carregando a fila...</p>
<div class="essay-history" id="reviewQueue"></div>
<div class="essay-actions"><button type="button" class="essay-secondary" id="reviewReload">Atualizar a fila</button></div>
</section>

<section class="essay-view" id="reviewDetail" hidden>
<button type="button" class="essay-secondary" id="reviewBack">Voltar à fila</button>
<p class="essay-kicker review-meta" id="reviewMeta"></p>
<details class="essay-rubric"><summary>Enunciado que o aluno viu</summary><pre class="review-pre" id="reviewPrompt" lang="en"></pre></details>
<h4 class="essay-h4">Texto do aluno</h4>
<pre class="review-pre" id="reviewText" lang="en"></pre>
<div class="essay-actions review-left"><button type="button" class="essay-primary" id="reviewCopy">Copiar para a IA</button></div>
<p class="essay-msg" id="reviewCopyMsg" role="status" hidden></p>
<textarea class="review-paste" id="reviewPromptBox" aria-label="Texto para a IA" rows="6" readonly hidden></textarea>
{_field("Cole aqui o JSON devolvido pela IA", '<textarea class="review-paste" id="reviewPaste" rows="6" spellcheck="false"></textarea>')}
<div class="essay-actions review-left"><button type="button" class="essay-secondary" id="reviewApply">Conferir e preencher o formulário</button></div>
<ul class="review-errors" id="reviewErrors" role="alert" hidden></ul>
<form class="review-form" id="reviewForm">
<h4 class="essay-h4">1 e 2. Notas por critério</h4>{crit}
<h4 class="essay-h4">3. Trechos (até 5; deixe em branco os que não usar)</h4>{trechos}
<h4 class="essay-h4">4. Reescrita um nível acima</h4>
{_field("Frase original do aluno", '<textarea data-reescrita="original" rows="2" lang="en"></textarea>')}
{_field("Versão um nível acima", '<textarea data-reescrita="versao" rows="2" lang="en"></textarea>')}
<h4 class="essay-h4">5. Prioridade de estudo</h4>
{_field("Texto da prioridade", '<input type="text" data-prioridade="texto" maxlength="1500">')}
{_field("Módulo", '<select data-prioridade="modulo"><option value="M4">M4</option><option value="M5">M5</option></select>')}
{_field("Parte", '<input type="number" data-prioridade="parte" min="1" max="10" step="1">')}
</form>
<p class="review-final" id="reviewFinal" role="status"></p>
<div class="essay-actions"><button type="button" class="essay-primary" id="reviewReturn" disabled>Devolver ao aluno</button></div>
<p class="essay-msg" id="reviewMsg" role="status" hidden></p>
</section>
</div>
</div>'''


def render_essay_modal(parts):
    rules = "".join(f"<li>{r}</li>" for r in REGRAS)
    rubric = "".join(
        f'<li><b>{e(c["nome"])}:</b> {e(c["avalia"])} 5: {e(c["5"])} 3: {e(c["3"])} 1: {e(c["1"])}</li>'
        for c in RUBRICA
    )
    emails = "".join(_topic_button(t, "email") for t in EMAIL_TOPICS)
    discs = "".join(_topic_button(t, "discussion") for t in DISCUSSION_TOPICS)
    prompts = "".join(prompt_html(t) for t in TOPICS)
    return f'''
<div class="account-modal essay-modal" id="essayModal" role="dialog" aria-modal="true" aria-label="Correção de redação" hidden>
<div class="account-modal-backdrop" id="essayBackdrop"></div>
<div class="account-card essay-card">
<button type="button" class="account-close" id="essayClose" aria-label="Fechar">{icon("close")}</button>
<div class="account-head"><span class="account-head-icon">{icon("pen")}</span>
<div><p class="account-kicker">Writing</p><h2 class="account-title" id="essayTitle">Correção de redação</h2></div></div>
<script type="application/json" id="essayData">{topics_json(parts)}</script>

<section class="essay-view" id="essayHome">
<p class="essay-status" id="essayStatus" role="status"></p>
<h3 class="essay-h">Write an Email · {MINUTOS["email"]} minutos</h3>
<div class="essay-topics">{emails}</div>
<h3 class="essay-h">Write for an Academic Discussion · {MINUTOS["discussion"]} minutos</h3>
<div class="essay-topics">{discs}</div>
<h3 class="essay-h">Suas redações</h3>
<div class="essay-chart" id="essayChart" hidden></div>
<div class="essay-history" id="essayHistory"><p class="essay-empty">Nenhuma redação enviada ainda.</p></div>
</section>

<section class="essay-view" id="essayBrief" hidden>
<p class="essay-kicker" id="essayBriefKicker"></p>
<h3 class="essay-h" id="essayBriefTitle"></h3>
<p class="essay-goal"><b>Objetivo deste tema:</b> <span id="essayBriefGoal"></span></p>
<p class="essay-warn">{AVISO}</p>
<h4 class="essay-h4">Regras do envio</h4>
<ul class="essay-rules" id="essayRules">{rules}</ul>
<details class="essay-rubric"><summary>Como a nota é dada</summary>
<p>Quatro critérios, cada um de 0 a 5. A nota final é a média, arredondada para o meio ponto mais próximo. Se o
cumprimento da tarefa ficar em 2 ou menos, a nota final não passa de 2,5.</p>
<ul>{rubric}</ul></details>
<p class="essay-block" id="essayBriefBlock" hidden></p>
<div class="essay-actions">
<button type="button" class="essay-secondary" id="essayBriefBack">Voltar aos temas</button>
<button type="button" class="essay-primary" id="essayStart">Começar: o cronômetro dispara</button>
</div>
</section>

<section class="essay-view" id="essayWrite" hidden>
<div class="essay-prompts">{prompts}</div>
{render_essay_box()}
<p class="essay-locked" id="essayLocked" role="status" hidden>Tempo esgotado. O texto travou: agora você decide se envia ou descarta.</p>
<div class="essay-actions">
<button type="button" class="essay-secondary" id="essayDiscard">Descartar esta redação</button>
<button type="button" class="essay-primary" id="essayFinish">Terminar e revisar o envio</button>
</div>
</section>

<section class="essay-view" id="essayConfirm" hidden>
<h3 class="essay-h">Confirmar o envio</h3>
<dl class="essay-summary">
<dt>Tema</dt><dd id="essaySumTopic"></dd>
<dt>Palavras</dt><dd id="essaySumWords"></dd>
<dt>Tempo usado</dt><dd id="essaySumTime"></dd>
<dt>Devolutiva prevista</dt><dd id="essaySumDue"></dd>
<dt>Próximo envio</dt><dd id="essaySumNext"></dd>
</dl>
<p class="essay-block" id="essayMinMsg" hidden></p>
<label class="essay-consent" id="essayConsentWrap" hidden><input type="checkbox" id="essayConsent">
<span>{CONSENTIMENTO} <a href="privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</span></label>
<div class="essay-actions">
<button type="button" class="essay-secondary" id="essayConfirmDiscard">Descartar</button>
<button type="button" class="essay-secondary" id="essayConfirmBack">Voltar ao texto</button>
<button type="button" class="essay-primary" id="essaySend">Enviar para correção</button>
</div>
<p class="essay-msg" id="essaySendMsg" role="status" hidden></p>
</section>

<section class="essay-view" id="essayDone" hidden>
<h3 class="essay-h">Redação enviada</h3>
<p id="essayDoneText"></p>
<div class="essay-actions"><button type="button" class="essay-primary" id="essayDoneBack">Ver minhas redações</button></div>
</section>

<section class="essay-view" id="essayFeedback" hidden>
<button type="button" class="essay-secondary" id="essayFeedbackBack">Voltar às redações</button>
<div id="essayFeedbackBody"></div>
</section>
</div>
</div>'''
