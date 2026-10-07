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

// ---- exercicios no formato da prova (2026-10-07) ----
function typeInto(input, value){ input.value = value; input.dispatchEvent(new Event("input")); }

// Complete the Words: 8 textos de 10 lacunas; acertar tudo e errar tudo
var ctws = document.querySelectorAll(".ctw");
check("ctw_8_texts_80_gaps", function(){ return ctws.length === 8 && document.querySelectorAll(".ctw-in").length === 80; });
check("ctw_gap_sizes_match_answers", function(){
  return Array.prototype.every.call(document.querySelectorAll(".ctw-in"), function(i){
    var word = i.parentNode.dataset.word, pre = i.parentNode.querySelector(".ctw-pre").textContent;
    return pre + i.dataset.answer === word && parseInt(i.getAttribute("maxlength"), 10) === i.dataset.answer.length && pre.length >= 1;
  });
});
if(ctws.length >= 2){
  Array.prototype.forEach.call(ctws[0].querySelectorAll(".ctw-in"), function(i){ typeInto(i, i.dataset.answer.toUpperCase()); });
  ctws[0].querySelector(".ctw-check").click();
  check("ctw_all_right_scores_10", function(){ return ctws[0].querySelector(".ctw-result").textContent === "10 de 10 corretas" && ctws[0].querySelector(".ctw-note").hidden === false; });
  Array.prototype.forEach.call(ctws[1].querySelectorAll(".ctw-in"), function(i){ typeInto(i, "zz9"); });
  check("ctw_rejects_non_letters", function(){ return ctws[1].querySelector(".ctw-in").value.indexOf("9") === -1; });
  ctws[1].querySelector(".ctw-check").click();
  check("ctw_all_wrong_scores_0_and_shows_words", function(){
    var fixes = ctws[1].querySelectorAll(".ctw-fix");
    return ctws[1].querySelector(".ctw-result").textContent === "0 de 10 corretas" &&
      Array.prototype.every.call(fixes, function(f){ return !f.hidden && f.textContent === f.parentNode.dataset.word; });
  });
  ctws[1].querySelector(".ctw-retry").click();
  check("ctw_retry_clears", function(){ return ctws[1].querySelector(".ctw-in").value === "" && ctws[1].querySelector(".ctw-in").disabled === false; });
}

// Build a Sentence: 30 itens; montar certo (com bloco sobrando) e montar errado
var bsqCards = document.querySelectorAll(".bsq-card");
check("bsq_30_cards_with_context", function(){ return bsqCards.length === 30 && document.querySelectorAll(".bsq-context").length === 30; });
function bsqPlace(card, order){
  order.forEach(function(frag){
    var chip = Array.prototype.filter.call(card.querySelectorAll(".bsq-bank .bsq-chip"), function(c){ return c.dataset.frag === frag; })[0];
    if(chip) chip.click();
  });
}
check("bsq_slots_equal_answer_length", function(){
  return Array.prototype.every.call(bsqCards, function(c){ return c.querySelectorAll(".bsq-slot").length === JSON.parse(c.dataset.answer).length; });
});
if(bsqCards.length === 30){
  var extraCard = bsqCards[9]; // item 10 tem um bloco que sobra
  check("bsq_check_starts_disabled", function(){ return extraCard.querySelector(".bsq-check").disabled === true; });
  bsqPlace(extraCard, JSON.parse(extraCard.dataset.answer));
  check("bsq_extra_chunk_stays_in_bank", function(){ return extraCard.querySelectorAll(".bsq-bank .bsq-chip").length === 1 && extraCard.querySelector(".bsq-check").disabled === false; });
  extraCard.querySelector(".bsq-check").click();
  check("bsq_right_order_is_correct", function(){ return extraCard.classList.contains("correct"); });
  var wrongCard = bsqCards[1];
  bsqPlace(wrongCard, JSON.parse(wrongCard.dataset.answer).slice().reverse());
  wrongCard.querySelector(".bsq-check").click();
  check("bsq_wrong_order_is_wrong", function(){ return wrongCard.classList.contains("wrong") && wrongCard.querySelector(".bsq-feedback").hidden === false; });
}

// Speaking: 5 cenarios de 7 frases + 4 entrevistas de 4 perguntas, texto escondido
check("spk_sets_and_items", function(){
  return document.querySelectorAll('.spk[data-mode="repeat"]').length === 5 &&
    document.querySelectorAll('.spk[data-mode="repeat"] .spk-item').length === 35 &&
    document.querySelectorAll('.spk[data-mode="interview"]').length === 4 &&
    document.querySelectorAll('.spk[data-mode="interview"] .spk-item').length === 16;
});
check("spk_text_starts_hidden", function(){
  return Array.prototype.every.call(document.querySelectorAll(".spk-text"), function(t){ return t.hidden; });
});
var spk0 = document.querySelector('.spk[data-mode="repeat"]');
if(spk0){
  var it0 = spk0.querySelector(".spk-item");
  it0.querySelector(".spk-show").click();
  check("spk_show_reveals_text", function(){ return it0.querySelector(".spk-text").hidden === false && it0.querySelector(".spk-marks").hidden === false; });
  it0.querySelector('.spk-mark[data-mark="ok"]').click();
  check("spk_mark_updates_score", function(){ return spk0.querySelector(".spk-score").textContent === "1 de 7 repetidas sem erro"; });
}

// Simulados do M7: 19 blocos, 62 itens, correcao so na entrega
var exams = document.querySelectorAll(".exam");
check("exam_19_blocks_62_items", function(){ return exams.length === 19 && document.querySelectorAll(".exam-item").length === 62; });
check("exam_no_answer_key_left_as_text", function(){ return document.getElementById("panel-mod7").textContent.indexOf("Gabarito:") === -1; });
if(exams.length){
  var ex = exams[0], exItems = ex.querySelectorAll(".exam-item");
  check("exam_submit_starts_disabled", function(){ return ex.querySelector(".exam-submit").disabled === true; });
  Array.prototype.forEach.call(exItems, function(it, k){
    var want = k === 0 ? (it.dataset.correct === "A" ? "B" : "A") : it.dataset.correct; // erra so a primeira
    it.querySelector('.exam-opt[data-letter="' + want + '"]').click();
  });
  check("exam_no_feedback_before_submit", function(){
    return !ex.querySelector(".is-key") && !ex.querySelector(".is-right") && ex.querySelector(".exam-result").hidden === true;
  });
  ex.querySelector(".exam-submit").click();
  check("exam_grades_on_submit", function(){
    return ex.querySelector(".exam-result").textContent === (exItems.length - 1) + " de " + exItems.length + " corretas" &&
      exItems[0].classList.contains("is-wrong") && exItems[1].classList.contains("is-right");
  });
}

// Caixa de escrita: 6 de e-mail (7 min) + 6 de discussao (10 min, minimo 100)
var wboxes = document.querySelectorAll(".wbox");
check("wbox_12_boxes", function(){
  return wboxes.length === 12 && document.querySelectorAll('.wbox[data-minutes="7"]').length === 6 &&
    document.querySelectorAll('.wbox[data-minutes="10"][data-minwords="100"]').length === 6;
});
if(wboxes.length){
  var wb = document.querySelector('.wbox[data-minwords="100"]');
  typeInto(wb.querySelector(".wbox-text"), "one two  three\nfour");
  check("wbox_counts_words", function(){ return wb.querySelector(".wbox-count").textContent === "4 palavras" && !wb.querySelector(".wbox-goal").classList.contains("is-met"); });
  typeInto(wb.querySelector(".wbox-text"), new Array(101).join("word "));
  check("wbox_goal_met_at_100", function(){ return wb.querySelector(".wbox-count").textContent === "100 palavras" && wb.querySelector(".wbox-goal").classList.contains("is-met"); });
  wb.querySelector(".wbox-start").click();
  check("wbox_timer_starts", function(){ return wb.classList.contains("is-running") && wb.querySelector(".wbox-start").textContent === "Pausar"; });
  wb.querySelector(".wbox-start").click();
}
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
