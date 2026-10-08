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
import shutil
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
  var m3 = document.getElementById("panel-mod3");
  return m3.querySelectorAll('.spk[data-mode="repeat"]').length === 5 &&
    m3.querySelectorAll('.spk[data-mode="repeat"] .spk-item').length === 35 &&
    m3.querySelectorAll('.spk[data-mode="interview"]').length === 4 &&
    m3.querySelectorAll('.spk[data-mode="interview"] .spk-item').length === 16;
});
// Writing e Speaking dos simulados do M7: audio, caixas de escrita e
// respostas-modelo fechadas ate o aluno pedir
check("m7_production_is_interactive", function(){
  var m7 = document.getElementById("panel-mod7");
  return m7.querySelectorAll('.spk[data-mode="repeat"] .spk-item').length === 10 &&
    m7.querySelectorAll('.spk[data-mode="interview"] .spk-item').length === 10 &&
    m7.querySelectorAll(".wbox").length === 4 && m7.querySelectorAll("details.reveal").length === 13;
});
check("m7_model_answers_start_closed", function(){
  return Array.prototype.every.call(document.querySelectorAll("#panel-mod7 details.reveal"), function(d){ return !d.open; });
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

// Alternativas embaralhadas na tela a cada sessao e a cada "Refazer"
(function(){
  function order(card, sel){ return Array.prototype.map.call(card.querySelectorAll(sel), function(o){ return o.dataset.letter; }).join(""); }
  function shown(card, sel){ return Array.prototype.map.call(card.querySelectorAll(sel), function(o){ return o.querySelector(".oletter").textContent; }).join(""); }
  var cards = Array.prototype.filter.call(document.querySelectorAll(".qcard"), function(c){ return !c.hasAttribute("data-noshuffle"); });
  check("shuffle_display_letters_stay_in_order", function(){
    return cards.every(function(c){ var s = shown(c, ".opt"); return s === "ABCDEF".slice(0, s.length); });
  });
  // com 4 alternativas, a chance de uma questao sair na ordem de origem e 1/24;
  // de 100+ questoes sairem TODAS na ordem de origem e desprezivel
  check("shuffle_changes_source_order_somewhere", function(){
    return cards.filter(function(c){ var o = order(c, ".opt"); return o !== o.split("").sort().join(""); }).length > cards.length / 2;
  });
  check("shuffle_keeps_scoring_by_source_letter", function(){
    return cards.filter(function(c){ return !c.dataset.multi; }).every(function(c){ return c.querySelectorAll('.opt[data-letter="' + c.dataset.correct + '"]').length === 1; });
  });
  check("shuffle_updates_letter_references", function(){
    return cards.every(function(c){
      var map = {};
      Array.prototype.forEach.call(c.querySelectorAll(".opt"), function(o){ map[o.dataset.letter] = o.querySelector(".oletter").textContent; });
      return Array.prototype.every.call(c.querySelectorAll(".optref"), function(r){ return r.textContent === "(" + map[r.dataset.ref] + ")"; });
    }) && document.querySelectorAll(".qcard .optref").length > 100;
  });
  check("shuffle_skips_insertion_items", function(){
    var fixed = document.querySelectorAll(".qcard[data-noshuffle]");
    return fixed.length >= 1 && Array.prototype.every.call(fixed, function(c){ var o = order(c, ".opt"); return o === o.split("").sort().join(""); });
  });
  // responder certo depois de embaralhar: clica na alternativa pela letra de origem
  var probe = cards[cards.length - 1], drill = probe.closest(".quiz-drill");
  probe.querySelector('.opt[data-letter="' + probe.dataset.correct + '"]').click();
  probe.querySelector(".qconfirm").click();
  check("shuffle_correct_answer_still_scores", function(){
    return probe.querySelector('.opt[data-letter="' + probe.dataset.correct + '"]').classList.contains("correct") &&
      !probe.querySelector(".opt.wrong");
  });
})();

// Treino no seu nivel: sessao sorteada entre exercicios da faixa do aluno
(function(){
  var box = document.getElementById("levelPractice");
  check("lvlp_exists_with_pool", function(){ return !!box && document.querySelectorAll("[data-level][data-lp-title]").length >= 40; });
  if(!box) return;
  var ORDER = ["A1","A2","B1","B2","C1","C2"];
  function seedDiag(nRight){
    var st = {};
    Array.prototype.forEach.call(document.querySelectorAll('.quiz-drill[data-drill="mod0-diag"] .qcard'), function(c, k){
      var wrong = ["A","B","C","D"].filter(function(L){ return L !== c.dataset.correct; })[0];
      st[c.dataset.num] = { picked: k < nRight ? c.dataset.correct : wrong, confirmed: true };
    });
    localStorage.setItem("toefl_quiz_mod0-diag_v1", JSON.stringify(st));
  }
  function rows(){ return Array.prototype.slice.call(document.querySelectorAll("#lvlpList li")); }
  function levelsFit(label){
    var me = ORDER.indexOf(label);
    return rows().every(function(li){
      var r = li.querySelector(".lvlp-meta").textContent.split(" · ")[0].split(/[–-]/);
      return ORDER.indexOf(r[0]) <= me && me <= ORDER.indexOf(r[r.length - 1]);
    });
  }
  seedDiag(5);  // 50% -> B1
  document.getElementById("lvlpShuffle").click();
  check("lvlp_b1_session_has_5_in_range", function(){
    return rows().length === 5 && document.getElementById("lvlpStatus").textContent.indexOf("Nível estimado: B1") === 0 && levelsFit("B1");
  });
  check("lvlp_session_mixes_skills", function(){
    var mods = {}; rows().forEach(function(li){ mods[li.querySelector(".lvlp-name").textContent.split(" · ")[0]] = 1; });
    return Object.keys(mods).length >= 3;
  });
  seedDiag(8);  // 80% -> C1
  document.getElementById("lvlpShuffle").click();
  check("lvlp_c1_session_in_range", function(){
    return rows().length === 5 && document.getElementById("lvlpStatus").textContent.indexOf("Nível estimado: C1") === 0 && levelsFit("C1");
  });
  var first = rows().map(function(li){ return li.querySelector(".lvlp-name").textContent; }).join("|"), changed = false;
  for(var t = 0; t < 6 && !changed; t++){
    document.getElementById("lvlpShuffle").click();
    changed = rows().map(function(li){ return li.querySelector(".lvlp-name").textContent; }).join("|") !== first;
  }
  check("lvlp_reshuffle_changes_session", function(){ return changed; });
  localStorage.removeItem("toefl_quiz_mod0-diag_v1");
})();

// Calculadora de score do M0: tabela 4.2 e media arredondada a meia banda
check("scalc_exists", function(){ return !!document.getElementById("scoreCalc") && document.querySelectorAll(".scalc-in").length === 4; });
(function(){
  function setPct(sec, v){ typeInto(document.getElementById("scalc-" + sec), v); }
  function bandOf(sec){ return document.querySelector('[data-band-for="' + sec + '"]').textContent; }
  if(!document.getElementById("scoreCalc")) return;
  setPct("reading", "20"); setPct("listening", "48"); setPct("writing", "49");
  check("scalc_total_waits_for_all_four", function(){ return document.getElementById("scalcTotal").textContent === "preencha as quatro seções"; });
  setPct("speaking", "86");
  check("scalc_bands_follow_table", function(){
    return bandOf("reading") === "banda 1,5 (A1)" && bandOf("listening") === "banda 3 (B1)" &&
      bandOf("writing") === "banda 3,5 (B1)" && bandOf("speaking") === "banda 6 (C2)";
  });
  // media de 1,5 + 3 + 3,5 + 6 = 3,5
  check("scalc_overall_is_mean_rounded_to_half", function(){ return document.getElementById("scalcTotal").textContent === "3,5 (B1)"; });
  setPct("speaking", "140");
  check("scalc_rejects_out_of_range", function(){ return bandOf("speaking") === "use de 0 a 100"; });
})();

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

// Painel de desempenho e meta do dia contam os exercicios novos. Ate aqui o
// teste ja fez: 1 texto de Complete the Words com 10/10 (o 2o foi refeito e
// nao conta), 2 itens de Build a Sentence (1 certo, 1 errado) e 1 bloco de
// simulado com exatamente 1 erro.
check("live_score_reading_counts_ctw", function(){
  var t = document.getElementById("liveScoreReadingBand").textContent;
  return t.indexOf("10/10 confirmadas") !== -1 || /\b1[01]\/1[01] confirmadas/.test(t);
});
check("live_score_writing_counts_bsq", function(){
  return document.getElementById("liveScoreWritingPct").textContent === "50%" &&
    document.getElementById("liveScoreWritingBand").textContent.indexOf("1/2 confirmadas de 30 no total") !== -1;
});
check("live_score_exam_counts_block", function(){
  var n = document.querySelector(".exam").querySelectorAll(".exam-item").length;
  return document.getElementById("liveScoreExamBand").textContent.indexOf((n - 1) + "/" + n + " confirmadas") !== -1;
});
check("daily_goal_counts_new_exercises", function(){
  var d = JSON.parse(localStorage.getItem("toefl_dailygoal_v1") || "{}");
  return d.count >= 3; // checkbox do inicio + texto de CTW + bloco de simulado
});

// Caixa de escrita: 6 de e-mail (7 min) + 6 de discussao (10 min, minimo 100)
var wboxes = document.querySelectorAll(".wbox");
check("wbox_12_boxes", function(){
  var m4 = document.getElementById("panel-mod4");
  return m4.querySelectorAll(".wbox").length === 12 && m4.querySelectorAll('.wbox[data-minutes="7"]').length === 6 &&
    m4.querySelectorAll('.wbox[data-minutes="10"][data-minwords="100"]').length === 6;
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
// fora do iOS e com reconhecimento de fala, o plano B nao aparece
check("mic_fallback_hidden_on_desktop", function(){ return document.getElementById("mrModeWrap").hidden && document.getElementById("mrNote").hidden; });

// PWA: manifesto no <head>, nada aparece sozinho, o botao de instalar surge
// com o evento do navegador e o aviso de versao nova abre e fecha. Aqui a
// pagina roda em file://, entao o service worker NAO pode ser registrado.
check("pwa_manifest_linked", function(){ return !!document.querySelector('link[rel="manifest"][href="manifest.json"]'); });
check("pwa_hidden_by_default", function(){
  return document.getElementById("pwaTools").hidden && document.getElementById("pwaInstall").hidden &&
         document.getElementById("pwaIosHint").hidden && document.getElementById("pwaUpdate").hidden;
});
check("pwa_no_sw_on_file", function(){ return window.__toeflPwa && window.__toeflPwa.canRegister === false; });
var bip = new Event("beforeinstallprompt", { cancelable: true });
var bipPrompted = false; bip.prompt = function(){ bipPrompted = true; };
window.dispatchEvent(bip);
check("pwa_install_button_appears", function(){
  return bip.defaultPrevented && !document.getElementById("pwaTools").hidden && !document.getElementById("pwaInstall").hidden;
});
document.getElementById("pwaInstall").click();
check("pwa_install_prompts_and_hides", function(){ return bipPrompted && document.getElementById("pwaInstall").hidden && document.getElementById("pwaTools").hidden; });
if(window.__toeflPwa) window.__toeflPwa.showUpdate(null);
check("pwa_update_bar_shows", function(){ return document.getElementById("pwaUpdate").hidden === false; });
document.getElementById("pwaUpdateLater").click();
check("pwa_update_bar_dismisses", function(){ return document.getElementById("pwaUpdate").hidden === true; });

// sem video cadastrado em app/videos.json, nenhum player aparece
check("video_none_without_registration", function(){ return document.querySelectorAll(".vid").length === 0; });

check("no_js_errors", function(){ return window.__errors.length === 0; });
results.__jsErrors = window.__errors;

document.title = JSON.stringify(results);
</script>
</body>
"""


# Segunda passada no navegador, fingindo um iPhone: user agent de iOS e um
# reconhecimento de fala de mentira, definidos ANTES do app.js rodar. Exercita
# o plano B do gravador (so gravar por padrao, opcao "So transcrever").
IOS_PRELUDE = r"""<script>
Object.defineProperty(navigator, "userAgent", { get: function(){ return "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1"; } });
window.__fakeRec = null;
window.webkitSpeechRecognition = function(){ window.__fakeRec = this; };
window.webkitSpeechRecognition.prototype.start = function(){ this.started = true; };
window.webkitSpeechRecognition.prototype.stop = function(){ this.stopped = true; if(this.onend) this.onend(); };
window.SpeechRecognition = undefined;
</script>"""

IOS_TEST_JS = r"""
<script>
window.__errors = [];
window.onerror = function(msg, src, line){ window.__errors.push(msg + " @" + line); };
var results = {};
function check(name, fn){
  try { results[name] = !!fn(); }
  catch(ex){ results[name] = false; results[name + "__error"] = ex.message; }
}
var $ = function(id){ return document.getElementById(id); };
check("ios_mic_mode_offered", function(){ return !$("mrModeWrap").hidden && !$("mrMode").checked && !$("mrMode").disabled; });
check("ios_mic_note_shown", function(){ return !$("mrNote").hidden && $("mrNote").textContent.indexOf("iPhone") !== -1; });
$("mrMode").checked = true;
$("mrMode").dispatchEvent(new Event("change", { bubbles: true }));
$("mrToggleBtn").click();
check("ios_mic_transcribe_only_starts", function(){
  return $("micRec").classList.contains("recording") && window.__fakeRec && window.__fakeRec.started &&
         $("mrStatus").textContent.indexOf("Transcrevendo") === 0 && $("mrMode").disabled;
});
if(window.__fakeRec && window.__fakeRec.onresult){
  window.__fakeRec.onresult({ resultIndex: 0, results: [{ 0: { transcript: "I would like to study abroad" }, isFinal: true, length: 1 }] });
}
check("ios_mic_transcript_shows_text", function(){ return !$("mrTranscript").hidden && $("mrTranscriptText").textContent === "I would like to study abroad"; });
$("mrToggleBtn").click();
check("ios_mic_transcribe_only_stops", function(){
  return !$("micRec").classList.contains("recording") && $("mrAudio").hidden && !$("mrClear").hidden &&
         !$("mrMode").disabled && $("mrToggleBtn").textContent.indexOf("Gravar") !== -1 &&
         $("mrTranscriptText").textContent === "I would like to study abroad";
});
// o iOS encerra o reconhecimento sozinho no silencio: a tela tem que sair do modo gravando
$("mrToggleBtn").click();
if(window.__fakeRec && window.__fakeRec.onend) window.__fakeRec.onend();
check("ios_mic_auto_end_resets_ui", function(){ return !$("micRec").classList.contains("recording") && !$("mrClear").hidden; });
// erro de permissao: mensagem clara e tela de volta ao normal
$("mrToggleBtn").click();
if(window.__fakeRec && window.__fakeRec.onerror) window.__fakeRec.onerror({ error: "not-allowed" });
check("ios_mic_permission_error_message", function(){ return !$("micRec").classList.contains("recording") && $("mrStatus").textContent.indexOf("negada") !== -1; });
check("ios_pwa_no_hint_on_file", function(){ return $("pwaIosHint").hidden; });
check("ios_no_js_errors", function(){ return window.__errors.length === 0; });
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
    # sys.executable, e nao "python": o do PATH pode ser outro interpretador,
    # sem o pacote markdown
    subprocess.run([sys.executable, "build_pipeline.py"], cwd=APP_DIR, check=True)
    subprocess.run([sys.executable, "build.py"], cwd=APP_DIR, check=True)


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


def pwa_checks():
    """Arquivos da PWA em artifact/: manifesto valido com os icones no lugar,
    service worker com a versao carimbada e pre-cache so de arquivo que existe
    (um arquivo faltando derruba a instalacao inteira do service worker)."""
    out = {}
    art = ARTIFACT.parent
    try:
        manifest = json.loads((art / "manifest.json").read_text(encoding="utf-8"))
        icons = manifest.get("icons", [])
        out["pwa_manifest_valid"] = (
            manifest.get("display") == "standalone" and bool(manifest.get("start_url"))
            and {"192x192", "512x512"} <= {i.get("sizes") for i in icons}
            and all((art / i["src"]).stat().st_size > 0 for i in icons)
        )
    except (OSError, ValueError, KeyError):
        out["pwa_manifest_valid"] = False

    sw_path = art / "sw.js"
    sw = sw_path.read_text(encoding="utf-8") if sw_path.exists() else ""
    out["pwa_sw_version_stamped"] = bool(re.search(r'var VERSION = "[0-9a-f]{12}";', sw))
    block = re.search(r"var PRECACHE = \[(.*?)\];", sw, re.S)
    urls = re.findall(r'"\./([^"]+)"', block.group(1)) if block else []
    out["pwa_sw_precache_files_exist"] = bool(urls) and all((art / u).exists() for u in urls)
    return out


def bank_checks():
    """Banco de questoes: todo item valida, e bank/items/migrado esta em dia
    com as fontes do site (migrate.py numa pasta temporaria gera os mesmos bytes)."""
    sys.path.insert(0, str(ROOT / "bank" / "tools"))
    import migrate
    import validate

    errors, _, ok = validate.validate_items(validate.load_items())
    out = {"bank_items_valid": not errors and len(ok) > 0}

    committed = ROOT / "bank" / "items" / "migrado"
    with tempfile.TemporaryDirectory() as tmp:
        migrate.run(Path(tmp))
        fresh = {p.name: p.read_bytes() for p in (Path(tmp) / "migrado").glob("*.json")}
    current = {p.name: p.read_bytes() for p in committed.glob("*.json")}
    out["bank_migrado_in_sync"] = fresh == current
    return out


# Terceira passada: um build de EXEMPLO, feito numa copia temporaria das
# fontes, com conteudo que o site de verdade ainda nao tem (videoaulas
# cadastradas). Serve para testar a infraestrutura sem deixar exemplo no ar:
# artifact/ e as fontes reais nao sao tocados.
FIXTURE_VIDEOS = {
    "videos": [
        {"id": "exemplo-abertura", "module": "mod3", "part": None, "title": "Aula de exemplo: abertura",
         "duration": "8 min", "provider": "youtube", "src": "abcdefghijk",
         "transcript": "Primeiro parágrafo da **transcrição** de exemplo."},
        {"id": "exemplo-parte2", "module": "mod3", "part": 2, "title": "Aula de exemplo: Parte 2",
         "provider": "file", "src": "https://example.invalid/aula.mp4",
         "captions": "https://example.invalid/aula.vtt"},
    ]
}

FIXTURE_TEST_JS = r"""
<script>
window.__errors = [];
window.onerror = function(msg, src, line){ window.__errors.push(msg + " @" + line); };
var results = {};
function check(name, fn){
  try { results[name] = !!fn(); }
  catch(ex){ results[name] = false; results[name + "__error"] = ex.message; }
}
// nada de rede no teste: o src do player fica so anotado, sem carregar
["HTMLIFrameElement", "HTMLMediaElement", "HTMLTrackElement"].forEach(function(cls){
  Object.defineProperty(window[cls].prototype, "src", {
    set: function(v){ this.setAttribute("data-test-src", v); },
    get: function(){ return this.getAttribute("data-test-src") || ""; }
  });
});
var m3 = document.querySelector('.panel[data-panel="mod3"]');
var vids = document.querySelectorAll(".vid");
var opener = m3.querySelector(".panel-inner > .vid");
var partVid = m3.querySelector(".section-card .vid");
check("video_two_rendered", function(){ return vids.length === 2 && opener && partVid && opener !== partVid; });
check("video_opener_before_first_part", function(){
  return opener.dataset.vid === "exemplo-abertura" && !!(opener.compareDocumentPosition(m3.querySelector(".section-card")) & Node.DOCUMENT_POSITION_FOLLOWING);
});
check("video_part_inside_its_part", function(){
  var card = partVid.closest(".section-card");
  return partVid.dataset.vid === "exemplo-parte2" && card.querySelector("h2 .htext").textContent.indexOf("PARTE 2") === 0 &&
         card.querySelector("h2").nextElementSibling === partVid;
});
check("video_lazy_no_player_before_click", function(){ return document.querySelectorAll(".vid iframe, .vid video").length === 0; });
check("video_transcript_collapsed", function(){
  var d = opener.querySelector("details.vid-transcript");
  return d && d.open === false && d.querySelector("strong").textContent === "transcrição" && !partVid.querySelector(".vid-transcript");
});
opener.querySelector(".vid-cover").click();
check("video_youtube_player_on_click", function(){
  var f = opener.querySelector(".vid-frame iframe");
  return f && f.src.indexOf("https://www.youtube-nocookie.com/embed/abcdefghijk?") === 0 && f.src.indexOf("cc_lang_pref=pt-BR") !== -1 &&
         opener.querySelector(".vid-cover").hidden && !opener.querySelector(".vid-frame").hidden;
});
partVid.querySelector(".vid-cover").click();
var player = partVid.querySelector(".vid-frame video");
check("video_file_player_with_captions", function(){
  var t = player && player.querySelector('track[kind="captions"]');
  return player.controls && player.src === "https://example.invalid/aula.mp4" && t && t.srclang === "pt-BR" && t.src === "https://example.invalid/aula.vtt";
});
check("video_counts_in_module_total", function(){ return m3.querySelectorAll(".pchk").length === m3.querySelectorAll(".section-card").length + 2; });
var pctBefore = document.getElementById("phPct-mod3").textContent;
var oc = opener.querySelector(".vid-chk");
oc.checked = true; oc.dispatchEvent(new Event("change", { bubbles: true }));
check("video_watched_counts_as_progress", function(){
  var saved = JSON.parse(localStorage.getItem("toefl_progress_v1") || "{}");
  return saved["mod3-video-exemplo-abertura"] === true && pctBefore === "0%" && document.getElementById("phPct-mod3").textContent !== "0%" &&
         opener.querySelector(".vid-done-label").textContent === "Aula assistida";
});
player.dispatchEvent(new Event("ended"));
check("video_file_marks_watched_at_end", function(){
  var saved = JSON.parse(localStorage.getItem("toefl_progress_v1") || "{}");
  return partVid.querySelector(".vid-chk").checked && saved["mod3-video-exemplo-parte2"] === true;
});
check("video_watched_does_not_finish_part", function(){ return !partVid.closest(".section-card").classList.contains("done"); });
check("fixture_no_js_errors", function(){ return window.__errors.length === 0; });
results.__jsErrors = window.__errors;
document.title = JSON.stringify(results);
</script>
</body>
"""


def build_fixture(work):
    """Builda o site de exemplo em `work` e devolve o index.html gerado."""
    for name in ("app", "consolidated", "legal"):
        shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns("__pycache__"))
    (work / "app" / "supabase_config.json").unlink(missing_ok=True)
    (work / "app" / "videos.json").write_text(json.dumps(FIXTURE_VIDEOS, ensure_ascii=False), encoding="utf-8")
    for script in ("build_pipeline.py", "build.py"):
        subprocess.run([sys.executable, script], cwd=work / "app", check=True, capture_output=True)
    return work / "artifact" / "index.html"


def run_browser_checks(test_js=TEST_JS, prelude="", source=None):
    html = (source or ARTIFACT).read_text(encoding="utf-8")
    html = html.replace("</body>", test_js)
    if prelude:
        html = html.replace("<head>", "<head>" + prelude, 1)

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
    ios = run_browser_checks(IOS_TEST_JS, IOS_PRELUDE)
    results["__jsErrors"] = (results.get("__jsErrors") or []) + (ios.pop("__jsErrors", None) or [])
    results.update(ios)
    with tempfile.TemporaryDirectory(prefix="itoefl_fixture_") as tmp:
        fixture = run_browser_checks(FIXTURE_TEST_JS, source=build_fixture(Path(tmp)))
    results["__jsErrors"] += fixture.pop("__jsErrors", None) or []
    results.update(fixture)
    results.update(legal_page_checks())
    results.update(pwa_checks())
    results.update(bank_checks())

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
