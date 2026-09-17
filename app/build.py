import json

frag = json.load(open("module_fragments_final.json", encoding="utf-8"))

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
    '<button class="themetoggle" id="themeToggle" type="button" aria-label="Alternar tema">'
    '<span id="themeIcon">☀️</span><span id="themeLabel">Claro</span></button>'
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
    '<span class="auth-gate-ghost">iT</span>'
    '<div class="auth-gate-card">'
    '<div class="auth-gate-brand">'
    '<span class="logo">iT</span>'
    '<span class="btxt"><span class="name">iTOEFL</span><span class="mark">Preparação independente</span></span>'
    '</div>'
    '<span class="auth-gate-kicker" id="authGateKicker">Acesso à plataforma</span>'
    '<h2 id="authGateTitle">Entre para continuar</h2>'
    '<p id="authGateSubtitle">Seu progresso fica salvo na sua conta e sincroniza entre dispositivos.</p>'

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
    '<span class="auth-gate-ghost">iT</span>'
    '<div class="auth-gate-card">'
    '<div class="auth-gate-brand">'
    '<span class="logo">iT</span>'
    '<span class="btxt"><span class="name">iTOEFL</span><span class="mark">Preparação independente</span></span>'
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
<div class="shell">
  <div class="side-backdrop" id="sideBackdrop"></div>
  <aside class="side" id="sideRail">
    <div class="side-top">
      <div class="brand">
        <span class="logo">iT</span>
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
