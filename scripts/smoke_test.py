"""Suite de testes automatizados (smoke test) da plataforma iTOEFL.

Builda o site, abre o artifact resultante num Chrome headless com um script
de verificacao injetado, e reporta PASS/FAIL de cada checagem: gate de
login, progresso/meta diaria, painel, "Minha conta" (incluindo o formulario
de excluir conta), tema, certificado, botoes de pronuncia/audio, gravador de
voz, paginas legais, e ausencia de erro de JS ou mojibake. Nao substitui teste manual em navegador de verdade nem em
celular real (ver ROADMAP.md, item 10 de qualidade), mas pega regressao
estrutural sem precisar testar tudo na mao a cada mudanca.

    python scripts\\smoke_test.py

Sai com codigo 0 se tudo passar, 1 se alguma checagem falhar.
"""

import json
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "app"
ARTIFACT = ROOT / "artifact" / "index.html"

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

# script injetado antes de </body> do artifact -- roda inteiramente no
# navegador; o resultado (um dict de nome -> bool) vira o <title> da
# pagina, que este script le de volta via --dump-dom
TEST_JS = r"""
<script>
window.__errors = [];
window.onerror = function(msg, src, line){ window.__errors.push(msg + " @" + line); };

var results = {};
function check(name, fn){
  try { results[name] = !!fn(); }
  catch(ex){ results[name] = false; results[name + "__error"] = ex.message; }
}

check("gate_visible_by_default", function(){
  return document.getElementById("authGate").hidden === false;
});

// simula estado logado (sem sessao real do Supabase)
document.getElementById("authGate").hidden = true;
var authBox = document.getElementById("authBox"); if(authBox) authBox.hidden = false;
var authIn = document.getElementById("authIn"); if(authIn) authIn.hidden = false;

["accountBtn", "dashboardBtn", "authSignOut"].forEach(function(id){
  check("topbar_" + id, function(){ return !!document.getElementById(id); });
});

check("checkbox_exists", function(){ return !!document.querySelector(".pchk"); });
var chk = document.querySelector(".pchk");
var dgBefore = document.getElementById("dgCount").textContent;
if(chk){ chk.checked = true; chk.dispatchEvent(new Event("change", { bubbles: true })); }
check("daily_goal_updates", function(){ return document.getElementById("dgCount").textContent !== dgBefore; });

var dashBtn = document.getElementById("dashboardBtn");
if(dashBtn) dashBtn.click();
check("dashboard_opens", function(){ return document.getElementById("dashboardModal").hidden === false; });
check("dashboard_streak_filled", function(){ return document.getElementById("dashStreak").textContent.length > 0; });
check("dashboard_weakspots_exists", function(){ return !!document.getElementById("dashWeakSpots"); });
var dashClose = document.getElementById("dashboardClose"); if(dashClose) dashClose.click();

var accBtn = document.getElementById("accountBtn");
if(accBtn) accBtn.click();
check("account_opens", function(){ return document.getElementById("accountModal").hidden === false; });
["accountEmailForm", "accountPasswordForm", "accountThemeTabs", "accountAccess", "accountDeleteForm"].forEach(function(id){
  check("account_" + id, function(){ return !!document.getElementById(id); });
});
// excluir conta: formulario fechado ate clicar, e o envio so libera com a
// palavra de confirmacao (nao envia nada de verdade aqui)
check("account_delete_starts_closed", function(){ return document.getElementById("accountDeleteForm").hidden === true; });
var delOpen = document.getElementById("accountDeleteOpen"); if(delOpen) delOpen.click();
check("account_delete_opens", function(){ return document.getElementById("accountDeleteForm").hidden === false; });
check("account_delete_submit_locked", function(){ return document.getElementById("accountDeleteSubmit").disabled === true; });
var delInput = document.getElementById("accountDeleteConfirm");
if(delInput){ delInput.value = "excluir"; delInput.dispatchEvent(new Event("input")); }
check("account_delete_submit_unlocks", function(){ return document.getElementById("accountDeleteSubmit").disabled === false; });
var delCancel = document.getElementById("accountDeleteCancel"); if(delCancel) delCancel.click();
check("account_delete_cancel_closes", function(){
  return document.getElementById("accountDeleteForm").hidden === true && document.getElementById("accountDeleteConfirm").value === "";
});
check("legal_links_exist", function(){
  return document.querySelectorAll('a[href="termos.html"]').length >= 4 && document.querySelectorAll('a[href="privacidade.html"]').length >= 4;
});
check("lock_message_removed", function(){ return !document.getElementById("lockMsg"); });
var accClose = document.getElementById("accountClose"); if(accClose) accClose.click();

var root = document.documentElement;
var themeDark = document.getElementById("accountThemeDark");
if(themeDark) themeDark.click();
check("theme_dark_applies", function(){ return root.getAttribute("data-theme") === "dark"; });
var themeLight = document.getElementById("accountThemeLight");
if(themeLight) themeLight.click();
check("theme_light_applies", function(){ return root.getAttribute("data-theme") === "light"; });

var certBtn = document.getElementById("certBtn");
if(certBtn){ certBtn.hidden = false; certBtn.click(); }
check("cert_opens", function(){ return certBtn ? document.getElementById("certModal").hidden === false : true; });
var certClose = document.getElementById("certClose"); if(certClose) certClose.click();

check("pronunciation_buttons_exist", function(){ return document.querySelectorAll(".panel table .speak-btn").length > 50; });
check("listening_item_speak_exists", function(){ return document.querySelectorAll(".quiz-item-speak").length > 0; });
check("listening_passage_speak_exists", function(){ return document.querySelectorAll(".quiz-passage-speak").length > 0; });

check("mic_recorder_exists", function(){ return !!document.getElementById("mrToggleBtn"); });
check("mic_transcript_exists", function(){ return !!document.getElementById("mrTranscript"); });

check("no_js_errors", function(){ return window.__errors.length === 0; });
results.__jsErrors = window.__errors;

document.title = JSON.stringify(results);
</script>
</body>
"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if path.exists():
            return str(path)
    raise SystemExit("Chrome nao encontrado nos caminhos esperados. Ajuste CHROME_CANDIDATES em scripts/smoke_test.py.")


def build():
    subprocess.run(["python", "build_pipeline.py"], cwd=APP_DIR, check=True)
    subprocess.run(["python", "build.py"], cwd=APP_DIR, check=True)


def mojibake_count():
    data = ARTIFACT.read_text(encoding="utf-8")
    return len(re.findall(r"â€.|Ã[^A-Za-z ]", data))


LEGAL_PAGES = ["termos.html", "privacidade.html"]


def legal_page_checks():
    """Paginas legais existem, tem conteudo e linkam de volta pro app."""
    out = {}
    for name in LEGAL_PAGES:
        path = ARTIFACT.parent / name
        key = "legal_page_" + name.split(".")[0]
        if not path.exists():
            out[key] = False
            continue
        data = path.read_text(encoding="utf-8")
        out[key] = ("<h1>" in data and data.count("<h2>") >= 8 and 'href="index.html"' in data)
    return out


def run_browser_checks():
    html = ARTIFACT.read_text(encoding="utf-8")
    html = html.replace("</body>", TEST_JS)

    tmp_dir = Path(tempfile.gettempdir())
    tmp_html = tmp_dir / f"itoefl_smoke_{uuid.uuid4().hex}.html"
    tmp_html.write_text(html, encoding="utf-8")
    profile = tmp_dir / f"itoefl_smoke_profile_{uuid.uuid4().hex}"

    chrome = find_chrome()
    uri = "file:///" + str(tmp_html).replace("\\", "/")

    result = None
    for _ in range(3):  # headless as vezes nao retorna saida na primeira tentativa (visto na sessao)
        result = subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--dump-dom", uri],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        if result.stdout.strip():
            break
    tmp_html.unlink(missing_ok=True)

    if not result or not result.stdout.strip():
        raise SystemExit("Chrome headless nao retornou saida apos 3 tentativas.")
    m = re.search(r"<title>(.*?)</title>", result.stdout, re.S)
    if not m:
        raise SystemExit("Nao encontrei <title> na saida do Chrome (dump-dom).")
    return json.loads(m.group(1))


def main():
    print("Buildando o site...")
    build()

    mb = mojibake_count()

    print("Rodando checagens no Chrome headless...")
    results = run_browser_checks()
    results.update(legal_page_checks())

    failed = []
    print()
    for key in sorted(results.keys()):
        if key.startswith("__") or key.endswith("__error"):
            continue
        ok = results[key]
        status = "OK  " if ok else "FAIL"
        print(f"  [{status}] {key}")
        if not ok:
            failed.append(key)
            err = results.get(key + "__error")
            if err:
                print(f"         -> {err}")

    print()
    mb_status = "OK  " if mb == 0 else "FAIL"
    print(f"  [{mb_status}] mojibake_count == 0 (achou {mb})")
    if mb:
        failed.append("mojibake_count")

    js_errors = results.get("__jsErrors") or []
    if js_errors:
        print(f"\n  Erros de JS capturados durante a execucao: {js_errors}")

    print()
    if failed:
        print(f"FALHOU: {len(failed)} checagem(ns): {', '.join(failed)}")
        sys.exit(1)
    print("Tudo passou.")
    sys.exit(0)


if __name__ == "__main__":
    main()
