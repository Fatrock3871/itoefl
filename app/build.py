import json

frag = json.load(open("module_fragments_final.json", encoding="utf-8"))

# marca iTOEFL: flor/redemoinho de 6 pétalas em tons de laranja, desenhada
# em SVG (vetorial, sem depender de arquivo externo) para substituir o
# antigo selo "iT" chapado. Cada pétala é a mesma curva repetida a cada 60°;
# a variação de tom entre var(--accent)/--accent-2/--accent-strong dá o
# efeito de profundidade sem precisar de gradiente por pétala.
_PETAL_COLORS = ["var(--accent-2)", "var(--accent)", "var(--accent-strong)",
                  "var(--accent)", "var(--accent-2)", "var(--accent-strong)"]
_PETAL_D = "M50,52 C34,48 26,34 30,18 C33,7 44,4 50,15 C56,4 67,7 70,18 C74,34 66,48 50,52 Z"
LOGO_SVG = (
    '<svg class="logo-mark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    + "".join(
        f'<path d="{_PETAL_D}" fill="{c}" transform="rotate({i * 60} 50 50)"/>'
        for i, c in enumerate(_PETAL_COLORS)
    )
    + '<circle cx="50" cy="52" r="6" fill="var(--accent-strong)"/>'
    + '</svg>'
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
     "Frases precisas, e-mail navegacional e discussão acadêmica."),
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

panels = "\n".join(
    f'<section class="panel" data-panel="{k}" id="panel-{k}" {"hidden" if k != "mod0" else ""}>'
    f'<div class="panel-inner">'
    f'<header class="panel-head"><span class="ph-num">{n}</span>'
    f'<span class="ph-text"><h1>{t}</h1>'
    '<p class="ph-progress-hint">Seu progresso: conclua 70% para avançar</p>'
    f'<p>{tag}</p></span></header>'
    f'{frag[k]}</div></section>'
    for k, n, t, _, tag in MODS
)

CSS = open("styles.css", encoding="utf-8").read()
JS = open("app.js", encoding="utf-8").read()

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
    '<span class="btxt"><span class="name">iTOEFL</span></span>'
    '</div>'
    '<h2 id="authGateTitle">Entre para continuar</h2>'
    '<p id="authGateSubtitle"></p>'

    '<div class="auth-tabs" id="authTabs">'
    '<span class="auth-tab-indicator" id="authTabIndicator"></span>'
    '<button type="button" id="authTabLogin" class="auth-tab is-active">Entrar</button>'
    '<button type="button" id="authTabSignup" class="auth-tab">Criar conta</button>'
    '</div>'

    '<form class="auth-form" id="loginForm">'
    '<label class="auth-field"><span class="auth-label">Nome de usuário</span>'
    '<input type="text" id="loginUsername" class="auth-input" placeholder="seu_usuario" autocomplete="username" required></label>'
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
    '<label class="auth-field"><span class="auth-label">Nome de usuário</span>'
    '<input type="text" id="signupUsername" class="auth-input" placeholder="seu_usuario" autocomplete="username" required pattern="[A-Za-z0-9_]{3,20}">'
    '<span class="auth-hint" id="signupUsernameHint">Letras, números e _, de 3 a 20 caracteres</span></label>'
    '<label class="auth-field"><span class="auth-label">Senha</span>'
    '<span class="auth-input-wrap">'
    '<input type="password" id="signupPassword" class="auth-input" placeholder="mínimo 6 caracteres" autocomplete="new-password" required minlength="6">'
    '<button type="button" class="auth-eye" data-target="signupPassword" aria-label="Mostrar senha">👁</button>'
    '</span>'
    '<span class="auth-strength" id="signupStrength" hidden><span class="auth-strength-bar"><span id="signupStrengthFill"></span></span>'
    '<span class="auth-strength-label" id="signupStrengthLabel"></span></span>'
    '</label>'
    '<button type="submit" class="auth-gate-submit">Criar conta</button>'
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
    '<button type="button" id="forgotUsernameLink" class="auth-link">Esqueci meu usuário</button>'
    '</div>'

    '<div class="auth-gate-divider" id="authGateDivider"><span>ou</span></div>'
    '<div class="auth-gate-actions" id="authGateGoogleWrap">'
    '<button type="button" id="authSignInGoogle"><span class="auth-google-badge">G</span>Entrar com Google</button>'
    '</div>'

    '<span id="authGateMsg" class="auth-gate-msg" hidden></span>'
    '</div>'
    '</div>'
)

# gate de pagamento: some depois do login se a conta ainda não pagou (e não é
# a conta admin, ver ADMIN_EMAIL em app.js). Preço aqui é só o texto do botão
# -- o valor de verdade é cobrado pelo PRICE_BRL em
# supabase/functions/create-checkout/index.ts; mudar um sem o outro deixa o
# texto do botão errado.
pay_gate = (
    '<div class="auth-gate" id="payGate" hidden>'
    f'{AUTH_BG_DECOR}'
    '<div class="auth-gate-card">'
    '<div class="auth-gate-brand">'
    f'<span class="logo">{LOGO_SVG}</span>'
    '<span class="btxt"><span class="name">iTOEFL</span></span>'
    '</div>'
    '<span class="auth-gate-kicker">Acesso pago</span>'
    '<h2>Libere seu acesso</h2>'
    '<p>Sua conta está conectada, mas o conteúdo completo da plataforma só libera depois da compra.</p>'
    '<div class="auth-gate-actions">'
    '<button type="button" id="payBtn">Comprar acesso: R$ 197 (vitalício)</button>'
    '</div>'
    '<span id="payGateMsg" class="auth-gate-msg" hidden></span>'
    '<button type="button" id="paySignOut" class="pay-signout">Sair desta conta</button>'
    '</div>'
    '</div>'
)

# certificado de conclusão: nada oficial, só uma tela pra comemorar que
# terminou os 10 módulos — aparece a partir daí (ver app.js/updateBadges)
cert_modal = (
    '<div class="cert-modal" id="certModal" hidden>'
    '<div class="cert-modal-backdrop" id="certModalBackdrop"></div>'
    '<div class="cert-card">'
    '<button type="button" class="cert-close" id="certClose" aria-label="Fechar">✕</button>'
    '<div class="cert-ornament">🎓</div>'
    '<p class="cert-kicker">Certificado de Conclusão</p>'
    '<h2 class="cert-name" id="certName">Aluno(a) iTOEFL</h2>'
    '<p class="cert-body">concluiu a preparação completa para o <strong>TOEFL iBT</strong> '
    '(formato 2026) pela plataforma iTOEFL: os 10 módulos, do diagnóstico ao protocolo do dia da prova.</p>'
    '<p class="cert-date" id="certDate"></p>'
    '<p class="cert-disclaimer">Não é um certificado oficial da ETS, é só um jeito de comemorar que você terminou.</p>'
    '<button type="button" class="cert-print" id="certPrint">🖨 Imprimir / salvar como PDF</button>'
    '</div>'
    '</div>'
)

# tela "Minha conta": trocar usuário e senha depois de criar a conta -- até
# aqui só dava pra recuperar (esqueci senha/usuário), não pra trocar por
# escolha própria. Reaproveita o shell do cert-modal (backdrop + card) e os
# estilos de .auth-form/.auth-input já usados no gate de login.
account_modal = (
    '<div class="account-modal" id="accountModal" hidden>'
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
    '<span class="account-section-label"><span class="account-section-icon">👤</span>Nome de usuário</span>'
    '<form class="auth-form" id="accountUsernameForm">'
    '<span class="auth-field">'
    '<input type="text" id="accountUsername" class="auth-input" required pattern="[A-Za-z0-9_]{3,20}">'
    '<span class="auth-hint" id="accountUsernameHint">Letras, números e _, de 3 a 20 caracteres</span>'
    '</span>'
    '<button type="submit" class="auth-gate-submit">Salvar usuário</button>'
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
    '</div>'

    '<span id="accountMsg" class="auth-gate-msg" hidden></span>'
    '</div>'
    '</div>'
)

# painel: sequência de dias, banda estimada, progresso geral e pontos fracos
# -- tudo calculado em cima de dados que já existem em outros widgets (ver
# app.js, bloco "Painel (dashboard)"), sem nenhum conteúdo novo pra manter.
dashboard_modal = (
    '<div class="dash-modal" id="dashboardModal" hidden>'
    '<div class="dash-modal-backdrop" id="dashboardModalBackdrop"></div>'
    '<div class="dash-card">'
    '<button type="button" class="dash-close" id="dashboardClose" aria-label="Fechar">✕</button>'
    '<div class="dash-head">'
    '<span class="dash-head-icon">📊</span>'
    '<div><p class="dash-kicker">Seu progresso</p><h2 class="dash-title">Painel</h2></div>'
    '</div>'

    '<div class="dash-section">'
    '<span class="dash-section-label"><span class="dash-section-icon">🔥</span>Sequência</span>'
    '<p class="dash-value" id="dashStreak">—</p>'
    '</div>'

    '<div class="dash-section">'
    '<span class="dash-section-label"><span class="dash-section-icon">✅</span>Meta de hoje</span>'
    '<div class="op-bar dash-bar"><div class="op-fill" id="dashGoalFill"></div></div>'
    '<p class="dash-value" id="dashGoalText"></p>'
    '</div>'

    '<div class="dash-section">'
    '<span class="dash-section-label"><span class="dash-section-icon">🎯</span>Banda estimada</span>'
    '<p class="dash-value" id="dashBand">—</p>'
    '</div>'

    '<div class="dash-section">'
    '<span class="dash-section-label"><span class="dash-section-icon">📈</span>Progresso geral</span>'
    '<div class="op-bar dash-bar"><div class="op-fill" id="dashProgressFill"></div></div>'
    '<p class="dash-value" id="dashProgressText"></p>'
    '</div>'

    '<div class="dash-section">'
    '<span class="dash-section-label"><span class="dash-section-icon">⚠️</span>Pontos fracos</span>'
    '<div id="dashWeakSpots" class="dash-weak-list"></div>'
    '</div>'

    '<div class="dash-section">'
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
<style>
{CSS}
</style>
</head>
<body>
{gate}
{pay_gate}
{cert_modal}
{account_modal}
{dashboard_modal}
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
    {side_jtrack}
    <div class="overall-progress">
      <div class="op-label"><span>Progresso geral</span><span id="opPct">0%</span></div>
      <div class="op-bar"><div class="op-fill" id="opFill"></div></div>
      <div class="op-count" id="opCount"></div>
    </div>
    <div class="daily-goal" id="dailyGoal">
      <div class="op-label"><span>🎯 Meta de hoje</span><span id="dgCount">0/1</span></div>
      <div class="op-bar"><div class="op-fill" id="dgFill"></div></div>
    </div>
    <div class="level-badge" id="levelBadge" hidden>
      <span class="level-badge-tag">Nível estimado (diagnóstico)</span>
      <span class="level-badge-band" id="levelBadgeBand"></span>
      <span class="level-badge-sched" id="levelBadgeSched"></span>
    </div>
    <button type="button" class="cert-btn" id="certBtn" hidden>Ver certificado de conclusão</button>
    <nav class="modnav" id="modnav">
      {nav_items}
    </nav>
    <div class="lock-msg" id="lockMsg" hidden></div>
    <div class="data-tools">
      <button type="button" id="dataExport">↓ Exportar progresso</button>
      <button type="button" id="dataImport">↑ Importar</button>
      <input type="file" id="dataFile" accept="application/json,.json" hidden>
      <span id="dataMsg" class="data-msg" hidden></span>
    </div>
    <button type="button" class="reset-btn" id="resetBtn">↺ Reiniciar todo o progresso</button>
    <div class="foot-note">Preparação independente baseada nas especificações ETS vigentes desde 21/jan/2026. Não afiliada à ETS. Seu progresso é salvo neste navegador.</div>
  </aside>

  <main id="mainArea">
    {journey}
    <div class="content-grid">
      <div class="content-col">{panels}</div>
      <aside class="rail" id="rail">
        <p class="rail-title">Nesta parte</p>
        <nav class="rail-toc" id="railToc"></nav>
      </aside>
    </div>
  </main>
</div>

<div class="float-tools">
  <div id="micRec" class="mic-rec collapsed">
    <div class="mr-panel">
      <div class="mr-display" id="mrDisplay">00:00</div>
      <div class="mr-status" id="mrStatus">Grave sua resposta e ouça de volta.</div>
      <audio id="mrAudio" class="mr-audio" controls hidden></audio>
      <div class="mr-controls">
        <button type="button" id="mrToggleBtn" class="st-primary">● Gravar</button>
        <button type="button" id="mrClear" hidden>Nova</button>
      </div>
    </div>
    <button class="st-toggle" id="mrToggle" type="button" aria-label="Gravador de voz">
      <span>🎙</span>
    </button>
  </div>
  <div id="secTimer" class="sec-timer collapsed">
    <div class="st-panel">
      <div class="st-display" id="stDisplay">28:00</div>
      <div class="st-presets" id="stPresets">
        <button type="button" data-min="28" class="active">Reading 28′</button>
        <button type="button" data-min="18">Listening 18′</button>
        <button type="button" data-min="8">Speaking 8′</button>
        <button type="button" data-min="23">Writing 23′</button>
        <button type="button" data-min="85">Prova completa 85′</button>
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
<script>
{JS}
</script>
</body>
</html>
'''

open("../artifact/index.html", "w", encoding="utf-8").write(html)
print("written", len(html))
