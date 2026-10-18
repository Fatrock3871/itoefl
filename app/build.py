import json
from site_config import load_site_url

SITE_URL = load_site_url()
print("SITE_URL:", SITE_URL)

frag = json.load(open("module_fragments_final.json", encoding="utf-8"))

# marca iTOEFL: flor/redemoinho de 6 pétalas em tons de laranja, solta (sem
# halo branco, sem moldura quadrada em volta do símbolo, por pedido do
# usuário). Sem bolinha de destaque separada -- tentativa anterior de fazer
# uma bolinha "pular" da logo até o "i" foi removida a pedido do usuário
# (achou feia).
# --logo-deep, e não --accent-strong: o tom de texto foi escurecido por
# contraste (WCAG AA) e a logo não deve mudar junto.
_PETAL_COLORS = ["var(--accent-2)", "var(--accent)", "var(--logo-deep)",
                  "var(--accent)", "var(--accent-2)", "var(--logo-deep)"]
_PETAL_D = "M50,52 C34,48 26,34 30,18 C33,7 44,4 50,15 C56,4 67,7 70,18 C74,34 66,48 50,52 Z"
_PETAL_SCALE = 0.94
_petals = "".join(
    f'<path d="{_PETAL_D}" fill="{c}" '
    f'transform="translate(50,50) rotate({i * 60}) scale({_PETAL_SCALE}) translate(-50,-50)"/>'
    for i, c in enumerate(_PETAL_COLORS)
)
LOGO_SVG = (
    '<svg class="logo-mark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    f'{_petals}'
    '<circle cx="50" cy="51" r="5" fill="var(--logo-deep)"/>'
    '</svg>'
)

# fundo decorativo da tela de login/pagamento: ícones de linha soltos, tema
# "aprender um idioma / intercâmbio" (globo, avião, balão de fala, livro,
# fone, passaporte). Mesmo tratamento visual do antigo "iT" fantasma que
# substituem (stroke fino em var(--hair), sem preenchimento) -- textura de
# fundo, não deve competir com o card.
_BG_ICON_SVGS = {
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><line x1="3" y1="12" x2="21" y2="12"/>',
    "plane": '<path d="M22 2 11 13M22 2 15 22l-4-9-9-4 20-7Z"/>',
    "chat": '<path d="M4 4h16v12H8l-4 4V4Z"/><path d="M8 9h8M8 12.5h5"/>',
    "book": '<path d="M12 6c-2-1.5-6-1.5-9-.5v13c3-1 7-1 9 .5 2-1.5 6-1.5 9-.5v-13c-3-1-7-1-9 .5Z"/><path d="M12 6v13"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2" y="14" width="5" height="7" rx="2"/><rect x="17" y="14" width="5" height="7" rx="2"/>',
    "passport": '<rect x="5" y="2" width="14" height="20" rx="2"/><circle cx="12" cy="10" r="3.5"/><path d="M9 18h6"/>',
}
_BG_ICON_LAYOUT = [
    ("globe", "bgicon-1"), ("plane", "bgicon-2"), ("chat", "bgicon-3"),
    ("book", "bgicon-4"), ("headset", "bgicon-5"), ("passport", "bgicon-6"),
]
AUTH_BG_DECOR = '<div class="auth-gate-bg" aria-hidden="true">' + "".join(
    f'<svg class="bgicon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    f'stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round">{_BG_ICON_SVGS[name]}</svg>'
    for name, cls in _BG_ICON_LAYOUT
) + '</div>'

# links para as duas páginas legais (geradas no fim deste arquivo a partir de
# legal/*.md). Abrem em aba nova pra não tirar o aluno do meio do login/compra.
LEGAL_LINKS = (
    '<a href="termos.html" target="_blank" rel="noopener">Termos de Uso</a>'
    '<span aria-hidden="true"> · </span>'
    '<a href="privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>'
)

# fontes do Google: preconnect abre a conexão cedo e o <link> deixa o
# navegador buscar o CSS das fontes em paralelo com o resto da página (antes
# era um @import dentro do styles.css). Mesma lista de famílias e pesos.
FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Bricolage+Grotesque:ital,opsz,wght@0,12..96,400;0,12..96,500;0,12..96,600;0,12..96,700;0,12..96,800;1,12..96,700;1,12..96,800'
    '&amp;family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,600'
    '&amp;family=Baloo+2:wght@600;700;800&amp;display=swap">'
)

MODS = [
    ("mod0","00","Embarque & Diagnóstico","modulo_0_embarque.md",
     "Onde você está e para onde vai. Comece pelo diagnóstico de nivelamento."),
    ("mod1","01","Reading","modulo_1_reading.md",
     "Ler rápido e decidir item a item no formato adaptativo de Reading."),
    ("mod2","02","Listening","modulo_2_listening.md",
     "Decodificar o áudio na primeira passada: escuta ativa e anotação."),
    ("mod3","03","Speaking","modulo_3_speaking.md",
     "Fonética, prosódia e respostas por função para o SpeechRater."),
    ("mod4","04","Writing","modulo_4_writing.md",
     "Frases precisas, e-mail direto e educado e discussão acadêmica."),
    ("mod5","05","Registro & Retórica","modulo_5_registro.md",
     "A camada que separa 'correto' de 'banda alta': registro e densidade."),
    ("mod6","06","Vocabulário","modulo_6_vocabulary.md",
     "Reconhecer para ler; ativar para falar e escrever sob pressão."),
    ("mod7","07","Simulados","modulo_7_simulados.md",
     "Quatro simulados progressivos e a análise de erros que liga tudo."),
    ("mod8","08","Exam Day","modulo_8_examday.md",
     "As 24 horas antes e o protocolo seção a seção no dia da prova."),
    ("mod9","09","Brazilian Traps","modulo_9_braziliantraps.md",
     "O padrão de erro do brasileiro, mapeado e eliminado."),
]

nav_items = "\n".join(
    f'<button class="tabbtn" data-tab="{k}" data-title="{t}">'
    f'<span class="num-badge" data-n="{n}">{n}</span>'
    f'<span class="lbl">{t}</span>'
    f'<span class="pbadge" id="badge-{k}"></span></button>'
    for k, n, t, _, _tag in MODS
)

# mapa da jornada (roadmap fixo no topo do conteúdo)
JOURNEY_SHORT = {
    "mod0": "Embarque", "mod1": "Reading", "mod2": "Listening", "mod3": "Speaking",
    "mod4": "Writing", "mod5": "Registro", "mod6": "Vocabulário", "mod7": "Simulados",
    "mod8": "Exam Day", "mod9": "Traps",
}
journey_nodes = "\n".join(
    f'<button class="jnode" data-tab="{k}" data-title="{t}">'
    f'<span class="jdot" data-n="{n}">{n}</span>'
    f'<span class="jlbl">{JOURNEY_SHORT[k]}</span></button>'
    for k, n, t, _, _tag in MODS
)
journey = (
    '<nav class="journey" id="journey" aria-label="Mapa do curso">'
    '<button class="hamburger" id="sideToggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="sideRail">'
    '<span></span><span></span><span></span></button>'
    '<div class="journey-row">'
    # onde o aluno está (módulo e Parte), sempre à vista na barra do topo.
    # É um botão: clicar abre a gaveta, o que dá um rótulo ao menu.
    '<button type="button" class="journey-title" id="journeyTitle" aria-label="Abrir o menu de módulos">'
    '<span class="jt-mod" id="jtMod"></span><span class="jt-part" id="jtPart"></span></button>'
    '<div class="journey-tools">'
    '<div class="auth-box" id="authBox" hidden>'
    '<div id="authIn" hidden>'
    '<span class="auth-avatar-wrap">'
    '<button type="button" class="auth-avatar" id="authAvatar" aria-label="Alterar foto de perfil" title="Alterar foto de perfil">'
    '<img id="authAvatarImg" alt="" hidden>'
    '<span id="authAvatarLetter"></span>'
    '</button>'
    '<button type="button" class="auth-avatar-remove" id="authAvatarRemove" aria-label="Remover foto" title="Remover foto" hidden>✕</button>'
    '</span>'
    '<input type="file" id="authAvatarFile" accept="image/*" hidden>'
    '<span id="authEmail" class="auth-email"></span>'
    '<button type="button" id="dashboardBtn" class="account-gear" aria-label="Meu painel" title="Meu painel">📊</button>'
    '<button type="button" id="accountBtn" class="account-gear" aria-label="Minha conta" title="Minha conta">⚙️</button>'
    '<button type="button" id="authSignOut">Sair</button></div>'
    '<span id="authMsg" class="auth-msg" hidden></span></div>'
    '</div></div>'
    '</nav>'
)
side_jtrack = (
    '<p class="side-section-label">Mapa do curso</p>'
    f'<div class="jtrack-wrap"><div class="jtrack">{journey_nodes}</div></div>'
)

# videoaulas (app/videos.json): vídeo de Parte entra no fragmento, logo abaixo
# do <h2>; a aula de abertura entra abaixo do cabeçalho do módulo. Com a lista
# vazia, frag e o HTML saem iguais aos de antes.
import render_video
VIDEOS = render_video.load_videos()
frag, VIDEO_OPENERS = render_video.inject(frag, VIDEOS)
for _w in render_video.warnings(VIDEOS):
    print("AVISO:", _w)

# ---- conta grátis: a amostra (app/free_sample.json) ----
# O app.js lê a lista do JSON embutido e tranca o resto na conta logada sem
# acesso pago. Aqui só se confere a lista contra o conteúdo de verdade.
import re as _re_fs
with open("free_sample.json", encoding="utf-8") as _f:
    FREE_SAMPLE = json.load(_f)


def _fs_parts(mod):
    """HTML de cada Parte (do <h2> até o próximo) do fragmento do módulo."""
    return _re_fs.split(r"(?=<h2[\s>])", frag[mod])[1:]


if set(FREE_SAMPLE["partes"]) != {k for k, *_ in MODS}:
    raise SystemExit("free_sample.json: a lista de Partes tem de citar os 10 módulos")
for _mod, _open in FREE_SAMPLE["partes"].items():
    _parts = _fs_parts(_mod)
    _nums = range(1, len(_parts) + 1) if _open == "todas" else _open
    for _n in _nums:
        if not 1 <= _n <= len(_parts):
            raise SystemExit(f"free_sample.json: {_mod} não tem Parte {_n} (tem {len(_parts)})")
        if "data-exam=" in _parts[_n - 1]:
            raise SystemExit(f"free_sample.json: a Parte {_n} de {_mod} tem simulado, e simulado não entra na amostra")
_all_frag = "".join(frag.values())
for _ex in FREE_SAMPLE["exercicios"]:
    _hits = len(_re_fs.findall(r'data-(?:ctw|drill|spk|bsq)="' + _re_fs.escape(_ex["id"]) + '"', _all_frag))
    if _hits != 1:
        raise SystemExit(f"free_sample.json: exercício {_ex['id']} aparece {_hits} vez(es) no site, devia ser 1")
    if "itens" in _ex:
        _w = _all_frag.split(f'data-bsq="{_ex["id"]}"', 1)[1].split('class="quiz-summary"', 1)[0]
        if _ex["itens"] > _w.count('class="bsq-card"') or not _ex["rotulo"].startswith(f'{_ex["itens"]} '):
            raise SystemExit(f"free_sample.json: {_ex['id']} abre {_ex['itens']} itens, e o rótulo ou o widget não batem")
# o resumo é escrito à mão para soar natural; se a lista mudar de forma, o
# build para em vez de anunciar uma amostra que não é a de verdade
if FREE_SAMPLE["partes"] != {"mod0": "todas", **{k: [1] for k, *_ in MODS if k != "mod0"}}:
    raise SystemExit("free_sample.json: a amostra de Partes mudou. Reescreva FREE_SUMMARY em app/build.py")
_rot = [e["rotulo"] for e in FREE_SAMPLE["exercicios"]]
FREE_SUMMARY = ("o Módulo 0 inteiro, a Parte 1 de cada um dos outros nove módulos e um exercício de cada tipo ("
                + ", ".join(_rot[:-1]) + " e " + _rot[-1] + ")")
FREE_JSON = json.dumps({"partes": FREE_SAMPLE["partes"], "exercicios": FREE_SAMPLE["exercicios"],
                        "resumo": FREE_SUMMARY}, ensure_ascii=False).replace("</", "<\\/")

panels = "\n".join(
    f'<section class="panel" data-panel="{k}" id="panel-{k}" {"hidden" if k != "mod0" else ""}>'
    f'<div class="panel-inner">'
    f'<header class="panel-head"><span class="ph-num">{n}</span>'
    f'<span class="ph-text"><h1>{t}</h1>'
    '<div class="ph-progress">'
    f'<div class="ph-progress-label"><span>Seu progresso neste módulo</span><span class="ph-progress-pct" id="phPct-{k}">0%</span></div>'
    f'<div class="ph-progress-bar"><div class="ph-progress-fill" id="phFill-{k}"></div></div>'
    '</div>'
    f'<p>{tag}</p></span></header>'
    f'{VIDEO_OPENERS.get(k, "")}{frag[k]}</div></section>'
    for k, n, t, _, tag in MODS
)

CSS = open("styles.css", encoding="utf-8").read()
# level.js (resultado do diagnóstico -> banda e cronograma) vai na frente do
# app.js e do landing.js: as duas páginas fazem a mesma conta
LEVEL_JS = open("level.js", encoding="utf-8").read()
# regras do envio de redação: o mesmo arquivo que as edge functions importam.
# No site ele entra sem a palavra "export" (os nomes começam todos com
# "redacao" e viram globais).
import re as _re
REDACAO_JS = _re.sub(r"^export ", "", open("../supabase/functions/_shared/redacao.js", encoding="utf-8").read(), flags=_re.M)
if _re.search(r"^\s*(export|import)\b", REDACAO_JS, flags=_re.M):
    raise SystemExit("redacao.js: o arquivo compartilhado não pode ter import, nem export no meio da linha")
# app/redacao.js (tela do aluno e painel do corretor) vai depois do app.js:
# usa a ponte window.__toeflApp que o app.js monta no fim
JS = (LEVEL_JS + "\n" + REDACAO_JS + "\n" + open("app.js", encoding="utf-8").read() + "\n" +
      open("redacao.js", encoding="utf-8").read())

# tela de redação para correção: os títulos das Partes do M4 e do M5 servem
# ao link da "prioridade de estudo" da devolutiva
from render_redacao import render_essay_modal, render_review_modal, module_parts
ESSAY_PARTS = {
    "M4": module_parts(open("../consolidated/modulo_4_writing.md", encoding="utf-8").read()),
    "M5": module_parts(open("../consolidated/modulo_5_registro.md", encoding="utf-8").read()),
}
_essay_rules = open("../supabase/functions/_shared/redacao.js", encoding="utf-8").read()
if f'partes: {{ M4: {len(ESSAY_PARTS["M4"])}, M5: {len(ESSAY_PARTS["M5"])} }}' not in _essay_rules:
    raise SystemExit("redacao.js: REDACAO_REGRAS.partes não bate com o número de Partes do M4 e do M5")
essay_modal = render_essay_modal(ESSAY_PARTS) + render_review_modal()

# ---- Supabase (opcional): só entra se app/supabase_config.json existir e estiver preenchido ----
supa_url = supa_key = ""
try:
    with open("supabase_config.json", encoding="utf-8-sig") as _f:
        _cfg = json.load(_f)
    supa_url = (_cfg.get("url") or "").strip()
    supa_key = (_cfg.get("anonKey") or "").strip()
    if "SEU-PROJETO" in supa_url or "SUA-ANON" in supa_key:
        supa_url = supa_key = ""
except FileNotFoundError:
    pass
except (json.JSONDecodeError, OSError) as _e:
    print(f"supabase: config invalida ({_e}), seguindo offline")
# build de CI (Cloudflare Pages ligado ao repositório): o supabase_config.json
# não vai para o Git, então os mesmos dois valores públicos podem vir do ambiente
if not (supa_url and supa_key):
    import os as _os
    supa_url = _os.environ.get("SUPABASE_URL", "").strip()
    supa_key = _os.environ.get("SUPABASE_PUBLISHABLE_KEY", "").strip()

SUPA_HEAD = ""
if supa_url and supa_key:
    SUPA_HEAD = (
        f'<script>window.ITOEFL_SUPABASE={json.dumps({"url": supa_url, "anonKey": supa_key})};</script>\n'
        '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'
    )
    print("supabase: configurado")
else:
    print("supabase: nao configurado (modo offline)")

# gate de login: só bloqueia o conteúdo se houver como logar (Supabase
# configurado). Sem config, o app segue 100% offline como antes.
gate_hidden = "" if (supa_url and supa_key) else "hidden"
gate = (
    f'<div class="auth-gate" id="authGate" {gate_hidden}>'
    f'{AUTH_BG_DECOR}'
    '<div class="auth-gate-card">'
    '<div class="auth-gate-brand">'
    f'<span class="logo">{LOGO_SVG}</span>'
    f'<span class="btxt"><span class="name">iTOEFL</span></span>'
    '</div>'
    '<h2 id="authGateTitle">Entre para continuar</h2>'
    '<p id="authGateSubtitle"></p>'
    f'<p class="auth-free-note" id="authFreeNote">Ainda não tem conta? A conta grátis abre {FREE_SUMMARY}, '
    'sem prazo e sem cartão. <button type="button" class="auth-link" id="authFreeSignup">Criar conta grátis</button></p>'

    '<div class="auth-tabs" id="authTabs">'
    '<span class="auth-tab-indicator" id="authTabIndicator"></span>'
    '<button type="button" id="authTabLogin" class="auth-tab is-active">Entrar</button>'
    '<button type="button" id="authTabSignup" class="auth-tab">Criar conta</button>'
    '</div>'

    '<form class="auth-form" id="loginForm">'
    '<label class="auth-field"><span class="auth-label">E-mail</span>'
    '<span class="auth-input-wrap has-icon">'
    '<span class="auth-input-icon" aria-hidden="true">👤</span>'
    '<input type="email" id="loginEmail" class="auth-input" placeholder="voce@exemplo.com" autocomplete="email" required>'
    '</span></label>'
    '<label class="auth-field"><span class="auth-label">Senha</span>'
    '<span class="auth-input-wrap">'
    '<input type="password" id="loginPassword" class="auth-input" placeholder="••••••••" autocomplete="current-password" required>'
    '<button type="button" class="auth-eye" data-target="loginPassword" aria-label="Mostrar senha">👁</button>'
    '</span></label>'
    '<button type="submit" class="auth-gate-submit">Entrar</button>'
    '</form>'

    '<form class="auth-form" id="signupForm" hidden>'
    '<label class="auth-field"><span class="auth-label">E-mail</span>'
    '<input type="email" id="signupEmail" class="auth-input" placeholder="voce@exemplo.com" autocomplete="email" required></label>'
    '<label class="auth-field"><span class="auth-label">Senha</span>'
    '<span class="auth-input-wrap">'
    '<input type="password" id="signupPassword" class="auth-input" placeholder="mínimo 6 caracteres" autocomplete="new-password" required minlength="6">'
    '<button type="button" class="auth-eye" data-target="signupPassword" aria-label="Mostrar senha">👁</button>'
    '</span>'
    '<span class="auth-strength" id="signupStrength" hidden><span class="auth-strength-bar"><span id="signupStrengthFill"></span></span>'
    '<span class="auth-strength-label" id="signupStrengthLabel"></span></span>'
    '</label>'
    '<button type="submit" class="auth-gate-submit">Criar conta</button>'
    '<p class="auth-consent">Ao criar a conta, você concorda com os '
    '<a href="termos.html" target="_blank" rel="noopener">Termos de Uso</a> e com a '
    '<a href="privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</p>'
    '</form>'

    '<form class="auth-form" id="resetPasswordForm" hidden>'
    '<label class="auth-field"><span class="auth-label">Nova senha</span>'
    '<span class="auth-input-wrap">'
    '<input type="password" id="newPassword" class="auth-input" placeholder="mínimo 6 caracteres" autocomplete="new-password" required minlength="6">'
    '<button type="button" class="auth-eye" data-target="newPassword" aria-label="Mostrar senha">👁</button>'
    '</span></label>'
    '<button type="submit" class="auth-gate-submit">Salvar nova senha</button>'
    '</form>'

    '<div class="auth-links" id="authLinks">'
    '<button type="button" id="forgotPasswordLink" class="auth-link">Esqueci minha senha</button>'
    '</div>'

    '<div class="auth-gate-divider" id="authGateDivider"><span>ou</span></div>'
    '<div class="auth-gate-actions" id="authGateGoogleWrap">'
    '<button type="button" id="authSignInGoogle"><span class="auth-google-badge">G</span>Entrar com Google</button>'
    '</div>'

    '<span id="authGateMsg" class="auth-gate-msg" hidden></span>'
    '<p class="legal-links"><a href="apresentacao.html">Conhecer a plataforma e os planos</a></p>'
    f'<p class="legal-links">{LEGAL_LINKS}</p>'
    '</div>'
    '</div>'
)

# ---- os três planos de preço (app/plans.json) ----
# Só o que o site MOSTRA sai daqui. O valor cobrado e o prazo gravado saem de
# supabase/functions/_shared/plans.ts, no servidor; o smoke test reprova se os
# dois arquivos divergirem.
with open("plans.json", encoding="utf-8") as _f:
    _plans_cfg = json.load(_f)
PLANS = _plans_cfg["plans"]
REFUND_DAYS = _plans_cfg["refund_days"]
if [p["id"] for p in PLANS if p.get("recommended")] != ["standard"]:
    raise SystemExit("plans.json: o selo Recomendado tem de estar no Standard, e só nele (decisão de 2026-10-08)")


def brl(cents):
    """3990 -> 'R$ 39,90'"""
    return f"R$ {cents // 100},{cents % 100:02d}"


# o selo é "Recomendado" e nunca "mais escolhido" ou "mais vendido": sem dado
# de venda seria afirmação falsa
PLAN_BADGE = '<span class="plan-badge">Recomendado</span>'

plan_options = "".join(
    f'<label class="plan-opt"><input type="radio" name="plan" value="{p["id"]}" data-name="{p["name"]}" '
    f'data-price="{brl(p["price_cents"])}"{" checked" if p.get("recommended") else ""}>'
    '<span class="plan-opt-body">'
    f'<span class="plan-opt-name">{p["name"]}{PLAN_BADGE if p.get("recommended") else ""}</span>'
    f'<span class="plan-opt-access">{p["access"]}</span>'
    '</span>'
    f'<span class="plan-opt-price">{brl(p["price_cents"])}</span></label>'
    for p in PLANS
)
_plan_default = next(p for p in PLANS if p.get("recommended"))

# gate de pagamento: aparece depois do login se a conta não tem acesso em dia
# (nunca comprou, ou o plano venceu) e não é a conta admin, ver ADMIN_EMAIL em
# app.js. Os textos do título e do parágrafo são trocados pelo app.js conforme
# a situação (gateCopy). O preço mostrado aqui vem de plans.json.
pay_gate = (
    '<div class="auth-gate" id="payGate" hidden>'
    f'{AUTH_BG_DECOR}'
    '<div class="auth-gate-card">'
    '<div class="auth-gate-brand">'
    f'<span class="logo">{LOGO_SVG}</span>'
    f'<span class="btxt"><span class="name">iTOEFL</span></span>'
    '</div>'
    '<span class="auth-gate-kicker" id="payGateKicker">Acesso pago</span>'
    '<h2 id="payGateTitle">Libere seu acesso</h2>'
    '<p id="payGateText">Sua conta está conectada. O conteúdo completo fica disponível depois da compra.</p>'
    '<fieldset class="plan-pick" id="planPick">'
    '<legend class="auth-label">Escolha o plano</legend>'
    f'{plan_options}'
    '</fieldset>'
    '<div class="auth-field">'
    '<label class="auth-label" for="couponInput">Cupom de desconto (opcional)</label>'
    '<input type="text" class="auth-input" id="couponInput" autocomplete="off" placeholder="Ex.: LANCAMENTO20">'
    '</div>'
    '<div class="auth-gate-actions">'
    f'<button type="button" id="payBtn">Comprar {_plan_default["name"]}: {brl(_plan_default["price_cents"])}</button>'
    '</div>'
    f'<p class="pay-terms">Pagamento único, sem renovação automática. Você pode desistir em até {REFUND_DAYS} dias '
    'e receber o valor de volta.</p>'
    '<span id="payGateMsg" class="auth-gate-msg" hidden></span>'
    '<button type="button" id="payGateBack" class="pay-signout" hidden>Voltar para a plataforma</button>'
    '<button type="button" id="paySignOut" class="pay-signout">Sair desta conta</button>'
    f'<p class="legal-links">{LEGAL_LINKS}</p>'
    '</div>'
    '</div>'
)

# certificado de conclusão: nada oficial, só uma tela pra comemorar que
# terminou os 10 módulos — aparece a partir daí (ver app.js/updateBadges)
cert_modal = (
    '<div class="cert-modal" id="certModal" role="dialog" aria-modal="true" aria-label="Certificado de conclusão" hidden>'
    '<div class="cert-modal-backdrop" id="certModalBackdrop"></div>'
    '<div class="cert-card">'
    '<button type="button" class="cert-close" id="certClose" aria-label="Fechar">✕</button>'

    # passo 1: pede o nome completo antes de gerar (só na primeira vez --
    # depois fica salvo em profiles.display_name e este passo não aparece mais)
    '<div class="cert-name-step" id="certNameStep">'
    '<div class="cert-ornament">🎓</div>'
    '<p class="cert-kicker">Antes de gerar seu certificado</p>'
    '<h2 class="cert-step-title">Como seu nome deve aparecer?</h2>'
    '<p class="cert-step-hint">Use seu nome completo: é o que vai sair impresso no certificado.</p>'
    '<form id="certNameForm" class="cert-name-form">'
    '<input type="text" id="certNameInput" class="auth-input" placeholder="Nome completo" required maxlength="80">'
    '<button type="submit" class="cert-print">Gerar certificado</button>'
    '</form>'
    '</div>'

    # passo 2: o certificado em si
    '<div class="cert-view" id="certView" hidden>'
    '<div class="cert-frame">'
    '<div class="cert-ornament">🎓</div>'
    '<p class="cert-kicker">Certificado de Conclusão</p>'
    '<h2 class="cert-name" id="certName">Aluno(a) iTOEFL</h2>'
    '<p class="cert-body">concluiu com êxito a preparação completa para o <strong>TOEFL iBT</strong> '
    '(formato 2026) pela plataforma iTOEFL, percorrendo os 10 módulos: do diagnóstico de nivelamento '
    'ao protocolo do dia da prova.</p>'
    '<div class="cert-stats">'
    '<div class="cert-stat"><span class="cert-stat-label">Módulos concluídos</span><span class="cert-stat-value">10 de 10</span></div>'
    '<div class="cert-stat"><span class="cert-stat-label">Nível estimado</span><span class="cert-stat-value" id="certBand">—</span></div>'
    '<div class="cert-stat"><span class="cert-stat-label">Concluído em</span><span class="cert-stat-value" id="certDate">—</span></div>'
    '</div>'
    '</div>'
    '<p class="cert-disclaimer">Registra a conclusão do curso no iTOEFL. Não é documento oficial da ETS e não atesta nível de proficiência.</p>'
    '<div class="cert-actions">'
    '<button type="button" class="cert-edit-name" id="certEditName">Editar nome</button>'
    '<button type="button" class="cert-print" id="certPrint">🖨 Imprimir / salvar como PDF</button>'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
)

# tela "Minha conta": aparência, situação do acesso pago, troca de e-mail e
# senha, links legais e exclusão da conta. Reaproveita o shell do cert-modal (backdrop + card) e os
# estilos de .auth-form/.auth-input já usados no gate de login.
account_modal = (
    '<div class="account-modal" id="accountModal" role="dialog" aria-modal="true" aria-label="Minha conta" hidden>'
    '<div class="account-modal-backdrop" id="accountModalBackdrop"></div>'
    '<div class="account-card">'
    '<button type="button" class="account-close" id="accountClose" aria-label="Fechar">✕</button>'
    '<div class="account-head">'
    '<span class="account-head-icon">⚙️</span>'
    '<div><p class="account-kicker">Minha conta</p><h2 class="account-title">Configurações</h2></div>'
    '</div>'

    '<div class="account-section">'
    '<span class="account-section-label"><span class="account-section-icon">🎨</span>Aparência</span>'
    '<div class="auth-tabs" id="accountThemeTabs">'
    '<span class="auth-tab-indicator" id="accountThemeIndicator"></span>'
    '<button type="button" id="accountThemeLight" class="auth-tab">☀️ Claro</button>'
    '<button type="button" id="accountThemeDark" class="auth-tab">🌙 Escuro</button>'
    '</div>'
    '</div>'

    '<div class="account-section">'
    '<span class="account-section-label"><span class="account-section-icon">🎟️</span>Acesso</span>'
    '<p class="account-access" id="accountAccess">Verificando...</p>'
    '<button type="button" class="account-renew" id="accountRenew" hidden>Renovar ou mudar de plano</button>'
    '</div>'

    # redações para correção (app/redacao.js): o selo aparece quando há
    # devolutiva que o aluno ainda não abriu. "Painel do corretor" só aparece
    # para conta com linha na tabela `admins` do banco.
    '<div class="account-section">'
    '<span class="account-section-label"><span class="account-section-icon">✍️</span>Redações</span>'
    '<p class="account-access">Envie uma redação no tempo da prova e receba nota, nível e comentários em até 3 dias úteis.</p>'
    '<span class="essay-badge" id="accountEssayBadge" hidden></span>'
    '<button type="button" class="account-renew" id="accountEssay">Correção de redação</button>'
    '<button type="button" class="account-renew" id="accountReviewer" hidden>Painel do corretor</button>'
    '</div>'

    '<div class="account-section">'
    '<span class="account-section-label"><span class="account-section-icon">📧</span>E-mail</span>'
    '<form class="auth-form" id="accountEmailForm">'
    '<span class="auth-field">'
    '<input type="email" id="accountEmail" class="auth-input" required>'
    '<span class="auth-hint">Trocar o e-mail exige confirmar o link enviado pro endereço novo.</span>'
    '</span>'
    '<button type="submit" class="auth-gate-submit">Salvar e-mail</button>'
    '</form>'
    '</div>'

    '<div class="account-section">'
    '<span class="account-section-label"><span class="account-section-icon">🔑</span>Senha</span>'
    '<form class="auth-form" id="accountPasswordForm">'
    '<span class="auth-input-wrap">'
    '<input type="password" id="accountNewPassword" class="auth-input" placeholder="mínimo 6 caracteres" autocomplete="new-password" required minlength="6">'
    '<button type="button" class="auth-eye" data-target="accountNewPassword" aria-label="Mostrar senha">👁</button>'
    '</span>'
    '<button type="submit" class="auth-gate-submit">Salvar senha</button>'
    '</form>'
    '<span id="accountMsg" class="auth-gate-msg" hidden></span>'
    '</div>'

    # exclusão de conta: fica por último e fechada. Só abre o formulário
    # depois de um clique, e o envio exige digitar EXCLUIR (conferido de
    # novo no servidor, em supabase/functions/delete-account).
    '<div class="account-section account-danger">'
    '<span class="account-section-label"><span class="account-section-icon">🗑️</span>Excluir conta</span>'
    '<p class="account-danger-text">Apaga de vez sua conta, seu progresso, suas redações e o registro do seu pagamento. '
    'O acesso comprado é perdido e não dá pra desfazer.</p>'
    '<button type="button" class="account-danger-open" id="accountDeleteOpen">Quero excluir minha conta</button>'
    '<form class="auth-form" id="accountDeleteForm" hidden>'
    '<label class="auth-field"><span class="auth-label">Digite EXCLUIR para confirmar</span>'
    '<input type="text" id="accountDeleteConfirm" class="auth-input" autocomplete="off" autocapitalize="characters" spellcheck="false"></label>'
    '<div class="account-danger-actions">'
    '<button type="button" class="account-danger-cancel" id="accountDeleteCancel">Cancelar</button>'
    '<button type="submit" class="account-danger-submit" id="accountDeleteSubmit" disabled>Excluir conta de vez</button>'
    '</div>'
    '</form>'
    '<span id="accountDeleteMsg" class="auth-gate-msg" hidden></span>'
    '</div>'

    f'<p class="legal-links">{LEGAL_LINKS}</p>'
    '</div>'
    '</div>'
)

# painel: sequência de dias, banda estimada, progresso geral e pontos fracos
# -- tudo calculado em cima de dados que já existem em outros widgets (ver
# app.js, bloco "Painel (dashboard)"), sem nenhum conteúdo novo pra manter.
dashboard_modal = (
    '<div class="dash-modal" id="dashboardModal" role="dialog" aria-modal="true" aria-label="Painel de progresso" hidden>'
    '<div class="dash-modal-backdrop" id="dashboardModalBackdrop"></div>'
    '<div class="dash-card">'
    '<button type="button" class="dash-close" id="dashboardClose" aria-label="Fechar">✕</button>'
    '<div class="dash-head">'
    '<span class="dash-head-icon">📊</span>'
    '<div><p class="dash-kicker">Seu progresso</p><h2 class="dash-title">Painel</h2></div>'
    '</div>'

    '<div class="dash-stats-grid">'
    '<div class="dash-stat dash-stat-a">'
    '<span class="dash-stat-icon">🔥</span><span class="dash-stat-label">Sequência</span>'
    '<p class="dash-value" id="dashStreak">—</p>'
    '</div>'
    '<div class="dash-stat dash-stat-b">'
    '<span class="dash-stat-icon">✅</span><span class="dash-stat-label">Meta de hoje</span>'
    '<div class="op-bar dash-bar"><div class="op-fill" id="dashGoalFill"></div></div>'
    '<p class="dash-value dash-value-sm" id="dashGoalText"></p>'
    '</div>'
    '<div class="dash-stat dash-stat-a">'
    '<span class="dash-stat-icon">🎯</span><span class="dash-stat-label">Banda estimada</span>'
    '<p class="dash-value dash-value-sm" id="dashBand">—</p>'
    '</div>'
    '<div class="dash-stat dash-stat-b">'
    '<span class="dash-stat-icon">📈</span><span class="dash-stat-label">Progresso geral</span>'
    '<div class="op-bar dash-bar"><div class="op-fill" id="dashProgressFill"></div></div>'
    '<p class="dash-value dash-value-sm" id="dashProgressText"></p>'
    '</div>'
    '</div>'

    '<div class="dash-callout dash-callout-warn">'
    '<span class="dash-section-label"><span class="dash-section-icon">⚠️</span>Pontos fracos</span>'
    '<div id="dashWeakSpots" class="dash-weak-list"></div>'
    '</div>'

    '<div class="dash-callout dash-callout-accent">'
    '<span class="dash-section-label"><span class="dash-section-icon">🧭</span>Plano sugerido</span>'
    '<p class="dash-value" id="dashPlanText"></p>'
    '<button type="button" class="dash-plan-btn" id="dashPlanBtn" hidden>Ir para o módulo</button>'
    '</div>'
    '</div>'
    '</div>'
)

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>iTOEFL</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#ef5a1f">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="iTOEFL">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
{FONT_LINKS}
<style>
{CSS}
</style>
</head>
<body>
<a class="skip-link" href="#mainArea">Pular para o conteúdo</a>
{gate}
{pay_gate}
{cert_modal}
{account_modal}
{dashboard_modal}
{essay_modal}
<div class="shell">
  <div class="side-backdrop" id="sideBackdrop"></div>
  <aside class="side" id="sideRail">
    <div class="side-top">
      <div class="brand">
        <span class="logo">{LOGO_SVG}</span>
        <span class="btxt">
          <span class="name">iTOEFL</span>
          <span class="mark">Preparação independente</span>
        </span>
      </div>
      <button class="side-close" id="sideClose" type="button" aria-label="Fechar menu">✕</button>
    </div>
    <div class="overall-progress">
      <div class="op-label"><span>Progresso geral</span><span id="opPct">0%</span></div>
      <div class="op-bar"><div class="op-fill" id="opFill"></div></div>
      <div class="op-count" id="opCount"></div>
      <button type="button" class="resume-btn" id="resumeBtn" hidden>
        <span class="resume-ico" aria-hidden="true">↻</span>
        <span class="resume-txt">Continuar de onde parei<b id="resumeLabel"></b></span>
      </button>
    </div>
    <div class="daily-goal" id="dailyGoal">
      <div class="op-label"><span>🎯 Meta de hoje</span><span id="dgCount">0/1</span></div>
      <div class="op-bar"><div class="op-fill" id="dgFill"></div></div>
      <div class="op-count" id="streakLine"></div>
    </div>
    <div class="level-badge" id="levelBadge" hidden>
      <span class="level-badge-tag">Nível estimado (diagnóstico)</span>
      <span class="level-badge-band" id="levelBadgeBand"></span>
      <span class="level-badge-sched" id="levelBadgeSched"></span>
    </div>
    <button type="button" class="cert-btn" id="certBtn" hidden>Ver certificado de conclusão</button>
    {side_jtrack}
    <nav class="modnav" id="modnav" aria-label="Módulos">
      {nav_items}
    </nav>
    <div class="trail" id="trailBox" hidden>
      <p class="side-section-label">Trilha de estudo</p>
      <div class="trail-tabs" role="group" aria-label="Trilha de estudo">
        <button type="button" class="trail-btn" data-trail="rapida" aria-pressed="true">Rápida</button>
        <button type="button" class="trail-btn" data-trail="completa" aria-pressed="false">Completa</button>
      </div>
      <p class="trail-hint" id="trailHint"></p>
    </div>
    <div class="data-tools">
      <button type="button" id="dataExport">↓ Exportar progresso</button>
      <button type="button" id="dataImport">↑ Importar</button>
      <input type="file" id="dataFile" accept="application/json,.json" hidden>
      <span id="dataMsg" class="data-msg" hidden></span>
    </div>
    <div class="pwa-tools" id="pwaTools" hidden>
      <button type="button" class="pwa-install-btn" id="pwaInstall" hidden>⤓ Instalar app</button>
      <p class="pwa-ios-hint" id="pwaIosHint" hidden>No iPhone ou iPad: toque em <b>Compartilhar</b> e depois em <b>Adicionar à Tela de Início</b>.</p>
    </div>
    <button type="button" class="reset-btn" id="resetBtn">↺ Reiniciar todo o progresso</button>
    <div class="foot-note">Preparação independente baseada nas especificações da ETS vigentes desde 21/jan/2026. Não afiliada à ETS. Seu progresso é salvo neste navegador.
      <span class="legal-links">{LEGAL_LINKS}</span></div>
  </aside>

  <main id="mainArea" tabindex="-1">
    {journey}
    <div class="content-grid">
      <div class="content-col">
        <div class="fs-bar" id="freeBar" role="status">
          <p id="freeBarText">Conta grátis: você tem {FREE_SUMMARY}. O resto do curso aparece trancado.</p>
          <button type="button" class="fs-lock-btn" id="freeBarBtn">Ver os planos</button>
        </div>
        {panels}
      </div>
    </div>
  </main>
</div>

<div class="float-tools">
  <div id="micRec" class="mic-rec collapsed">
    <div class="mr-panel">
      <div class="mr-display" id="mrDisplay">00:00</div>
      <div class="mr-status" id="mrStatus">Grave sua resposta e ouça de volta.</div>
      <audio id="mrAudio" class="mr-audio" controls hidden></audio>
      <div class="mr-transcript" id="mrTranscript" hidden>
        <p class="mr-transcript-label">Transcrição automática (autoavaliação, pode errar):</p>
        <p id="mrTranscriptText"></p>
      </div>
      <label class="mr-mode" id="mrModeWrap" hidden><input type="checkbox" id="mrMode"> Só transcrever, sem gravar áudio</label>
      <p class="mr-note" id="mrNote" hidden></p>
      <div class="mr-controls">
        <button type="button" id="mrToggleBtn" class="st-primary">● Gravar</button>
        <button type="button" id="mrClear" hidden>Nova gravação</button>
      </div>
    </div>
    <button class="st-toggle" id="mrToggle" type="button" aria-label="Gravador de voz">
      <span>🎙</span>
    </button>
  </div>
  <div id="secTimer" class="sec-timer collapsed">
    <div class="st-panel">
      <div class="st-display" id="stDisplay">30:00</div>
      <div class="st-presets" id="stPresets">
        <button type="button" data-min="30" class="active">Reading 30 min</button>
        <button type="button" data-min="29">Listening 29 min</button>
        <button type="button" data-min="23">Writing 23 min</button>
        <button type="button" data-min="8">Speaking 8 min</button>
        <button type="button" data-min="89">Prova completa 89 min</button>
      </div>
      <div class="st-controls">
        <button type="button" id="stStart" class="st-primary">Iniciar</button>
        <button type="button" id="stReset">Zerar</button>
      </div>
    </div>
    <button class="st-toggle" id="stToggle" type="button" aria-label="Cronômetro de seção">
      <span id="stFace">⏱</span>
    </button>
  </div>
</div>

{SUPA_HEAD}
<div class="pwa-update" id="pwaUpdate" role="status" hidden>
  <span>Nova versão disponível.</span>
  <button type="button" id="pwaUpdateBtn">Recarregar</button>
  <button type="button" id="pwaUpdateLater" aria-label="Depois">Depois</button>
</div>
<script type="application/json" id="freeSample">{FREE_JSON}</script>
<script>
{JS}
</script>
</body>
</html>
'''

import os as _os
_os.makedirs("../artifact", exist_ok=True)  # num clone novo a pasta nao existe (artifact/ e gerado e fica fora do Git)
open("../artifact/index.html", "w", encoding="utf-8").write(html)
print("written", len(html))

# ---- páginas legais: legal/*.md -> artifact/<nome>.html ----
# Páginas próprias (não abas do app) porque precisam abrir sem login: o link
# vai na tela de cadastro, na tela de compra e na configuração do login com
# Google, que exige uma URL pública de política de privacidade.
import re as _re
import markdown as _md

LEGAL_PAGES = [
    ("termos", "Termos de Uso"),
    ("privacidade", "Política de Privacidade"),
]
# aplica o tema salvo antes de pintar a página, igual ao app (mesma chave)
_LEGAL_THEME_JS = (
    '(function(){try{var t=localStorage.getItem("toefl_theme_v1");'
    'if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();'
)
for _slug, _title in LEGAL_PAGES:
    _src = open(f"../legal/{_slug}.md", encoding="utf-8").read()
    _pending = _src.count("[PREENCHER")
    if _pending:
        print(f"AVISO: legal/{_slug}.md ainda tem {_pending} campo(s) [PREENCHER: ...], nao publicar assim")
    # trecho novo que ainda não passou por advogado é marcado na fonte com
    # <!-- REVISAR (advogado): ... -->. O comentário não vai para a página.
    _review = len(_re.findall(r"<!--\s*REVISAR.*?-->", _src, flags=_re.S))
    if _review:
        print(f"AVISO: legal/{_slug}.md tem {_review} trecho(s) marcado(s) REVISAR (advogado)")
    _src = _re.sub(r"<!--\s*REVISAR.*?-->\n?", "", _src, flags=_re.S)
    _body = _md.markdown(_src, extensions=["tables"])
    _page = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_title} · iTOEFL</title>
<link rel="canonical" href="{SITE_URL}/{_slug}">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<meta name="theme-color" content="#ef5a1f">
{FONT_LINKS}
<script>{_LEGAL_THEME_JS}</script>
<style>
{CSS}
</style>
</head>
<body class="legal-page">
<header class="legal-head">
  <a class="legal-brand" href="index.html"><span class="logo">{LOGO_SVG}</span><span class="name">iTOEFL</span></a>
  <a class="legal-back" href="index.html">Voltar para a plataforma</a>
</header>
<main class="legal-doc">
{_body}
</main>
<footer class="legal-foot">{LEGAL_LINKS}</footer>
</body>
</html>
'''
    open(f"../artifact/{_slug}.html", "w", encoding="utf-8").write(_page)
    print(f"written {_slug}.html", len(_page))

# ---- tela de apresentação: artifact/apresentacao.html ----
# Página pública, antes do login (seção 6.1 de
# docs/auditoria-plataforma-2026-10.md): o que a plataforma tem, o
# diagnóstico grátis sem conta, os três planos e as perguntas frequentes. É
# página própria, e não uma tela do app, para abrir sem carregar o curso
# inteiro. "Entrar" e "Criar conta" levam ao index.html.
#
# Regra de texto desta página: só entra o que dá para provar. Os números
# saem do próprio build, o selo é "Recomendado" (nunca "mais escolhido"), e
# não há promessa de nota nem contagem de alunos.

# as 10 questões do diagnóstico, já com as letras redistribuídas pelo
# pipeline: o mesmo HTML do Módulo 0, sem o rodapé de "refazer" (a página tem
# o próprio painel de resultado)
_diag = _re.search(r'<div class="quiz-drill" data-drill="mod0-diag">.*?(?=<div class="quiz-summary")', frag["mod0"], flags=_re.S)
if not _diag or _diag.group(0).count('class="qcard"') != 10:
    raise SystemExit("apresentacao: nao achei as 10 questoes do diagnostico no fragmento do M0")
DIAG_HTML = _diag.group(0) + "</div>"


def _count(mod, pattern):
    return len(_re.findall(pattern, frag[mod]))


LP_STATS = [
    (len(MODS), "módulos, do diagnóstico ao dia da prova"),
    (_count("mod1", r'class="ctw-in"'), "lacunas de Complete the Words para digitar"),
    (_count("mod1", r'class="qcard"'), "questões de Reading"),
    (_count("mod2", r'class="qcard"'), "questões de Listening"),
    (_count("mod4", r'class="bsq-card'), "itens de Build a Sentence"),
    (_count("mod3", r'class="spk"'), "conjuntos de Speaking para ouvir e responder"),
    (_count("mod7", r'class="exam-item'), "questões de simulado"),
    (len(json.load(open("vocab_kit.json", encoding="utf-8"))), "flashcards de vocabulário"),
]
if any(n <= 0 for n, _ in LP_STATS):
    raise SystemExit(f"apresentacao: contagem zerada em LP_STATS: {LP_STATS}")
lp_stats = "".join(f'<li><span class="lp-stat-n">{n}</span><span class="lp-stat-t">{t}</span></li>' for n, t in LP_STATS)

lp_plans = "".join(
    f'<article class="lp-plan{" is-recommended" if p.get("recommended") else ""}" data-plan="{p["id"]}">'
    f'{PLAN_BADGE if p.get("recommended") else ""}'
    f'<h3>{p["name"]}</h3>'
    f'<p class="lp-plan-price">{brl(p["price_cents"])}</p>'
    f'<p class="lp-plan-access">{p["access"]}</p>'
    f'<p class="lp-plan-for">{p["audience"]}</p>'
    f'<p class="lp-plan-detail">{p["detail"]}</p>'
    f'<a class="lp-btn{" lp-btn-main" if p.get("recommended") else ""}" href="index.html#criar-conta" '
    f'data-plan-pick="{p["id"]}">Escolher o {p["name"]}</a>'
    '</article>'
    for p in PLANS
)

LP_FAQ = [
    ("O iTOEFL é oficial da ETS?",
     "Não. É uma preparação independente, sem vínculo com a ETS. TOEFL e TOEFL iBT são marcas registradas da ETS. "
     "O material é original e segue o formato público da prova; não reproduz questões oficiais."),
    ("Existe garantia de nota?",
     "Não. Nenhum curso pode garantir. O resultado depende do seu estudo. O diagnóstico e as bandas mostradas na "
     "plataforma são estimativas de treino, não notas oficiais."),
    ("Funciona no celular?",
     "A plataforma é um site: abre no navegador do celular, do tablet e do computador, e o progresso acompanha a sua conta."),
    ("O pagamento é mensal?",
     "Não. Cada plano é pago uma vez só, pelo Mercado Pago. Não há renovação automática nem cobrança recorrente."),
    ("O que a conta grátis inclui?",
     f"{FREE_SUMMARY[0].upper() + FREE_SUMMARY[1:]}. Não tem prazo e não pede cartão. Os simulados, a correção de redação e "
     "o resto do curso são liberados por um plano. O que entra na conta grátis pode mudar, como dizem os Termos de Uso."),
    ("E se o meu acesso vencer?",
     "O curso completo volta a ficar trancado, mas a conta, o progresso e a amostra da conta grátis continuam. Se você comprar "
     "outro plano, retoma de onde parou. Quem renova antes de vencer soma os dias ao prazo que já tinha."),
    ("Tem reembolso?",
     f"Sim. Você pode desistir da compra em até {REFUND_DAYS} dias corridos e receber o valor inteiro de volta, sem precisar "
     "justificar. É o direito de arrependimento do artigo 49 do Código de Defesa do Consumidor, e vale para os três planos."),
    ("O que acontece com as respostas do diagnóstico grátis?",
     "Ficam guardadas só neste navegador, sem conta e sem envio para o servidor. Se você criar a conta neste mesmo navegador, "
     "o Módulo 0 já abre com o diagnóstico respondido."),
]
lp_faq = "".join(f'<details class="lp-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in LP_FAQ)

LANDING_JS = LEVEL_JS + "\n" + open("landing.js", encoding="utf-8").read()
_lp_desc = ("Preparação em português para o TOEFL iBT no formato 2026: 10 módulos, exercícios no molde da prova e simulados. "
            "Faça o diagnóstico grátis, sem criar conta.")
_landing = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>iTOEFL: preparação para o TOEFL iBT no formato 2026</title>
<meta name="description" content="{_lp_desc}">
<meta property="og:title" content="iTOEFL: preparação para o TOEFL iBT no formato 2026">
<meta property="og:description" content="{_lp_desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/apresentacao">
<link rel="canonical" href="{SITE_URL}/apresentacao">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<meta name="theme-color" content="#ef5a1f">
{FONT_LINKS}
<script>{_LEGAL_THEME_JS}</script>
<style>
{CSS}
</style>
</head>
<body class="lp-page">
<a class="skip-link" href="#lpMain">Pular para o conteúdo</a>
<header class="lp-top">
  <a class="legal-brand" href="apresentacao.html" aria-label="iTOEFL, início"><span class="logo">{LOGO_SVG}</span><span class="name">iTOEFL</span></a>
  <nav class="lp-nav" aria-label="Seções da página">
    <a href="#diagnostico">Diagnóstico grátis</a>
    <a href="#gratis">Conta grátis</a>
    <a href="#planos">Planos</a>
    <a href="#duvidas">Dúvidas</a>
  </nav>
  <a class="lp-btn lp-enter" href="index.html">Entrar</a>
</header>

<main id="lpMain" tabindex="-1">
<section class="lp-hero">
  <p class="lp-kicker">Formato vigente desde 21 de janeiro de 2026</p>
  <h1>TOEFL iBT no formato 2026, em português.</h1>
  <p class="lp-sub">A prova mudou em janeiro de 2026: menos de 1h30, Reading e Listening adaptativos, nota de 1 a 6.
  Este curso foi escrito para ela.</p>
  <div class="lp-cta">
    <a class="lp-btn lp-btn-main" href="#planos">Ver os planos</a>
    <a class="lp-btn" href="#diagnostico">Fazer o diagnóstico grátis</a>
  </div>
  <p class="lp-note">O diagnóstico tem 10 questões, leva cerca de 12 minutos e não pede conta.</p>
</section>

<section class="lp-section" aria-labelledby="lpInsideTitle">
  <h2 id="lpInsideTitle">O que tem dentro</h2>
  <ul class="lp-stats">{lp_stats}</ul>
  <div class="lp-feats">
    <div class="lp-feat"><h3>As quatro seções, no molde da prova</h3>
      <p>Reading, Listening, Writing e Speaking, com os tipos de tarefa de 2026: Complete the Words com digitação,
      Build a Sentence, Write an Email, Listen and Repeat, Take an Interview.</p></div>
    <div class="lp-feat"><h3>Explicação em português, treino em inglês</h3>
      <p>Cada questão corrigida mostra por que a resposta está certa e por que as outras estão erradas. Um módulo inteiro
      trata dos erros típicos de quem fala português.</p></div>
    <div class="lp-feat"><h3>Simulados e acompanhamento</h3>
      <p>Simulados progressivos com correção só na entrega, cronômetro por seção, gravador para o Speaking,
      registro de erros e progresso salvo na sua conta.</p></div>
  </div>
</section>

<section class="lp-section" id="diagnostico" aria-labelledby="lpDiagTitle">
  <h2 id="lpDiagTitle">Diagnóstico grátis, sem conta</h2>
  <p class="lp-lead">São as 10 questões do Teste de Nivelamento do Módulo 0: gramática, vocabulário e conectivos
  acadêmicos. Responda sem consulta, confirme cada resposta e veja no fim o seu nível estimado. É uma estimativa de
  treino, não uma nota oficial.</p>
  {DIAG_HTML}
  <div class="lp-result" id="lpResult" tabindex="-1" role="status" hidden>
    <p class="lp-result-score" id="lpResultScore"></p>
    <p class="lp-result-band" id="lpResultBand"></p>
    <p class="lp-result-desc" id="lpResultDesc"></p>
    <p class="lp-result-next">No curso, o caminho indicado para esse nível é o <strong id="lpResultSched"></strong>.
    A estimativa vem de 10 questões de gramática e vocabulário: serve para escolher por onde começar, não para prever a nota da prova.</p>
    <div class="lp-cta">
      <a class="lp-btn lp-btn-main" href="#planos">Ver os planos</a>
      <a class="lp-btn" href="index.html#criar-conta">Criar conta grátis</a>
      <button type="button" class="lp-btn" id="lpRetry">Refazer o diagnóstico</button>
    </div>
  </div>
</section>

<section class="lp-section" id="gratis" aria-labelledby="lpFreeTitle">
  <h2 id="lpFreeTitle">Comece com a conta grátis</h2>
  <p class="lp-lead">A conta grátis abre {FREE_SUMMARY}. Não tem prazo e não pede cartão. Os simulados, a correção de
  redação e o resto do curso são liberados por um plano. Se você fez o diagnóstico aqui, ele já aparece respondido na
  conta criada neste navegador.</p>
  <div class="lp-cta">
    <a class="lp-btn lp-btn-main" href="index.html#criar-conta">Criar conta grátis</a>
  </div>
</section>

<section class="lp-section" id="planos" aria-labelledby="lpPlansTitle">
  <h2 id="lpPlansTitle">Planos</h2>
  <p class="lp-lead">Os três planos dão acesso ao mesmo material. O que muda é por quanto tempo. Pagamento único,
  sem renovação automática.</p>
  <div class="lp-plans">{lp_plans}</div>
  <p class="lp-why">Por que o Standard é o recomendado: o cronograma de estudo que o curso indica para a maioria
  dos alunos tem 60 dias, e o mais longo tem 90. Os 90 dias do Standard cobrem os dois.</p>
  <p class="lp-refund"><strong>Reembolso em {REFUND_DAYS} dias.</strong> Em qualquer plano, você pode desistir da compra
  em até {REFUND_DAYS} dias corridos e receber o valor inteiro de volta, sem justificar (artigo 49 do Código de Defesa do
  Consumidor). Detalhes nos <a href="termos.html">Termos de Uso</a>.</p>
</section>

<section class="lp-section" id="duvidas" aria-labelledby="lpFaqTitle">
  <h2 id="lpFaqTitle">Perguntas frequentes</h2>
  <div class="lp-faq">{lp_faq}</div>
</section>
</main>

<footer class="lp-foot">
  <p>Preparação independente, baseada nas especificações públicas da prova. Não afiliada à ETS.
  TOEFL e TOEFL iBT são marcas registradas da ETS.</p>
  <p><a href="termos.html">Termos de Uso</a><span aria-hidden="true"> · </span><a href="privacidade.html">Política de Privacidade</a><span aria-hidden="true"> · </span><a href="termos.html">Contato (nos Termos de Uso)</a><span aria-hidden="true"> · </span><a href="index.html">Entrar</a></p>
</footer>
<script>
{LANDING_JS}
</script>
</body>
</html>
'''
open("../artifact/apresentacao.html", "w", encoding="utf-8").write(_landing)
print("written apresentacao.html", len(_landing))

# ---- PWA: manifesto, ícones e service worker com versão carimbada ----
# A versão é um hash de tudo que o service worker guarda em cache. Build com
# conteúdo igual gera sw.js igual (o navegador não acusa versão nova à toa);
# qualquer mudança gera sw.js diferente e dispara o aviso de nova versão.
# Os ícones são gerados por scripts/make_icons.py e ficam versionados.
import hashlib as _hashlib
import shutil as _shutil

_os.makedirs("../artifact/icons", exist_ok=True)
_shutil.copyfile("manifest.json", "../artifact/manifest.json")
for _icon in sorted(_os.listdir("icons")):
    if _icon.endswith(".png"):
        _shutil.copyfile(f"icons/{_icon}", f"../artifact/icons/{_icon}")

_h = _hashlib.sha256()
for _f in ["index.html", "termos.html", "privacidade.html", "manifest.json"] + \
        [f"icons/{i}" for i in sorted(_os.listdir("../artifact/icons"))]:
    _h.update(open(f"../artifact/{_f}", "rb").read())
_h.update(open("sw.js", "rb").read())  # mudou a lógica do service worker: versão nova também
_sw_version = _h.hexdigest()[:12]
_sw = open("sw.js", encoding="utf-8").read().replace("__BUILD_VERSION__", _sw_version)
open("../artifact/sw.js", "w", encoding="utf-8").write(_sw)
print("written sw.js, versao", _sw_version)

# ---- Hospedagem: _headers, robots e sitemap ----
# Tudo gerado aqui, nunca à mão em artifact/. _headers é o formato do
# Cloudflare Pages (e do Netlify). A Vercel (hospedagem do beta, decisão de
# 2026-10-18) lê as mesmas regras do vercel.json, na raiz do repositório, que
# não pode ser gerado porque a Vercel o lê antes do build: o smoke test
# reprova se os cabeçalhos dos dois divergirem. Sem _redirects de
# propósito: o Cloudflare serve index.html em / e redireciona /index.html
# para /, então reescrever a raiz para a apresentação deixaria o app inalcançável.
_CSP = "; ".join([
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: blob:",
    "media-src 'self' data: blob:",
    "connect-src 'self' https://*.supabase.co wss://*.supabase.co https://cdn.jsdelivr.net "
    "https://fonts.googleapis.com https://fonts.gstatic.com",
    "frame-src https://www.youtube-nocookie.com",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])
_HEADERS = f"""# Gerado por app/build.py. Nao editar.
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: microphone=(self), camera=(), geolocation=(), payment=()
  Strict-Transport-Security: max-age=31536000
  Content-Security-Policy: {_CSP}

# Paginas HTML ja saem do Cloudflare Pages com max-age=0 + revalidacao. O
# service worker e o manifesto tambem nao podem ficar em cache, senao a versao
# nova nao chega.
/sw.js
  Cache-Control: no-cache
/manifest.json
  Cache-Control: no-cache

# Icones so mudam quando o arquivo muda.
/icons/*
  Cache-Control: public, max-age=604800
"""
open("../artifact/_headers", "w", encoding="utf-8", newline="\n").write(_HEADERS)

open("../artifact/robots.txt", "w", encoding="utf-8", newline="\n").write(
    f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
open("../artifact/sitemap.xml", "w", encoding="utf-8", newline="\n").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE_URL}{_p}</loc></url>\n" for _p in ["/apresentacao", "/termos", "/privacidade"])
    + "</urlset>\n")
print("written _headers, robots.txt, sitemap.xml")
