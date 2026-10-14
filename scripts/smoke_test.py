"""Suite de testes automatizados (smoke test) da plataforma iTOEFL.

Builda o site, abre o artifact resultante num Chrome headless com um script
de verificacao injetado, e reporta PASS/FAIL de cada checagem: gate de
login, progresso/meta diaria, painel, "Minha conta" (incluindo o formulario
de excluir conta), tema, certificado, botoes de pronuncia/audio, gravador de
voz, paginas legais, e ausencia de erro de JS ou mojibake. Nao substitui teste manual em navegador de verdade nem em
celular real (ver ROADMAP.md, Etapa 0.5), mas pega regressao
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

// ---- planos: escolha na tela de compra e validade do acesso ----
var planInputs = Array.prototype.slice.call(document.querySelectorAll("#planPick input[name=plan]"));
check("plans_three_options_standard_default", function(){
  var checked = planInputs.filter(function(i){ return i.checked; });
  return planInputs.map(function(i){ return i.value; }).join() === "sprint,standard,premium" &&
    checked.length === 1 && checked[0].value === "standard" &&
    document.getElementById("payBtn").textContent === "Comprar Standard: R$ 89,90";
});
check("plans_recommended_badge_only_on_standard", function(){
  var badges = document.querySelectorAll("#planPick .plan-badge");
  return badges.length === 1 && badges[0].textContent === "Recomendado" &&
    badges[0].closest(".plan-opt").querySelector("input").value === "standard" &&
    !/mais (escolhido|vendido)/i.test(document.body.textContent);
});
check("plans_button_follows_choice", function(){
  var btn = document.getElementById("payBtn"), out = [];
  ["sprint", "premium", "standard"].forEach(function(id){
    var input = document.querySelector('#planPick input[value="' + id + '"]');
    input.checked = true; input.dispatchEvent(new Event("change", { bubbles: true }));
    out.push(btn.textContent);
  });
  return out.join("|") === "Comprar Sprint: R$ 39,90|Comprar Premium: R$ 149,90|Comprar Standard: R$ 89,90";
});
check("plans_gate_states_refund_and_single_payment", function(){
  var t = document.querySelector("#payGate .pay-terms").textContent;
  return t.indexOf("7 dias") !== -1 && t.indexOf("sem renovação automática") !== -1;
});
var ACC = window.__toeflAccess, NOW = Date.UTC(2026, 9, 8, 12, 0, 0), DAY = 86400000;
check("access_none_without_purchase", function(){
  return !ACC.state(null, NOW).active && !ACC.state({ paid: false, expires_at: null }, NOW).active &&
    ACC.gateCopy(ACC.state(null, NOW)).title === "Libere seu acesso";
});
check("access_lifetime_without_expiry", function(){
  // linha antiga, sem as colunas dos planos, e Premium: as duas sem prazo
  var old = ACC.state({ paid: true }, NOW), prem = ACC.state({ paid: true, plan: "premium", expires_at: null }, NOW);
  return old.active && old.lifetime && prem.active && prem.lifetime &&
    ACC.text(prem, null).text === "Plano Premium: acesso vitalício liberado." && ACC.text(old, null).text === "Acesso vitalício liberado.";
});
check("access_active_until_expiry_with_days_left", function(){
  var st = ACC.state({ paid: true, plan: "standard", expires_at: new Date(NOW + 10 * DAY).toISOString() }, NOW);
  var line = ACC.text(st, null);
  return st.active && !st.lifetime && st.daysLeft === 10 && line.cls === "is-paid" &&
    line.text.indexOf("Plano Standard: acesso liberado até ") === 0 && line.text.indexOf("(faltam 10 dias)") !== -1 &&
    ACC.gateCopy(st).title === "Renovar ou mudar de plano";
});
check("access_last_week_is_flagged", function(){
  var st = ACC.state({ paid: true, plan: "sprint", expires_at: new Date(NOW + DAY / 2).toISOString() }, NOW);
  return st.active && st.daysLeft === 1 && ACC.text(st, null).cls === "is-ending" && ACC.text(st, null).text.indexOf("(falta 1 dia)") !== -1;
});
check("access_expired_blocks_and_says_so", function(){
  var st = ACC.state({ paid: true, plan: "sprint", expires_at: new Date(NOW - 1000).toISOString() }, NOW);
  var line = ACC.text(st, null), copy = ACC.gateCopy(st);
  return !st.active && st.expired && line.cls === "is-unpaid" && line.text.indexOf("O plano Sprint venceu em ") === 0 &&
    copy.title === "Seu acesso venceu" && copy.text.indexOf("progresso continua salvo") !== -1;
});
check("access_bad_date_stays_locked", function(){
  return !ACC.state({ paid: true, expires_at: "nao-e-data" }, NOW).active;
});
check("account_renew_button_starts_hidden", function(){
  var b = document.getElementById("accountRenew");
  return !!b && b.hidden === true;
});

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
    // 10 de Build a Sentence, 3 respostas-modelo de Writing e as 2 respostas de
    // digitacao do Complete the Words do Simulado 2 (um bloco so)
    m7.querySelectorAll(".wbox").length === 4 && m7.querySelectorAll("details.reveal").length === 14;
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

// cronometro: presets no tempo-base da ETS e na ordem da prova (docs/conferencia-formato-2026.md)
check("timer_presets_match_ets", function(){
  var mins = Array.prototype.map.call(document.querySelectorAll("#stPresets button"), function(b){ return b.dataset.min; });
  return mins.join(",") === "30,29,23,8,89" && document.getElementById("stDisplay").textContent === "30:00";
});

// sem video cadastrado em app/videos.json, nenhum player aparece
check("video_none_without_registration", function(){ return document.querySelectorAll(".vid").length === 0; });
// sem bloco de aprofundamento nos .md, o seletor de trilha fica escondido
check("trail_selector_hidden_without_blocks", function(){ return document.querySelectorAll("details.deep").length === 0 && document.getElementById("trailBox").hidden; });

// afirmacoes sobre a prova que a conferencia de 2026-10-08 derrubou
// (docs/conferencia-conteudo-2026-10.md) nao podem voltar ao texto
check("content_no_outdated_exam_claims", function(){
  var text = document.querySelector(".content-col").textContent;
  return ["ETS Test Browser", "decore 3 esqueletos", "segundos de preparação", "5 s de planejamento", "~42–71", "~20–41",
          "não é uma conversão oficial", "janela de tolerância", "reagendar sem custo", "celular fica fora", "TOEPO",
          "pausa de 10 minutos", "Fixação de Template"].every(function(s){ return text.indexOf(s) === -1; });
});
check("content_states_confirmed_exam_rules", function(){
  var m8 = document.getElementById("panel-mod8").textContent, m5 = document.getElementById("panel-mod5").textContent;
  return m8.indexOf("TOEFL Test App") !== -1 && m8.indexOf("4 envios") !== -1 && m8.indexOf("espelho de mão") !== -1 &&
    m5.indexOf("45 segundos") !== -1;
});
// numeros que a ETS publica com divergencia: o site nao cita valor de envio
// nem versao de Windows, aponta para a pagina oficial; e o M0 separa ponto
// bruto, banda e escala antiga
check("content_points_to_ets_for_changing_numbers", function(){
  var m8 = document.getElementById("panel-mod8"), m0 = document.getElementById("panel-mod0").textContent;
  return !!m8.querySelector('a[href*="ets.org/toefl/test-takers/ibt/register/at-home-requirements"]') &&
    !!m8.querySelector('a[href*="ets.org/toefl/test-takers/ibt/scores/send-scores"]') &&
    !/US\$\s?\d|Windows 1[01]/.test(m8.textContent) &&
    m0.indexOf("Três números que não se misturam") !== -1 && m0.indexOf("não é ponto bruto") !== -1;
});
// cronogramas do M0: Intensivo, Regular e Completo. Sprint, Standard e
// Premium sao so os planos de preco (decisao de 2026-10-08)
check("schedules_do_not_use_plan_names", function(){
  var m0 = document.getElementById("panel-mod0").textContent;
  return ["6.1 Intensivo: 30 Dias", "6.2 Regular: 60 Dias", "6.3 Completo: 90 Dias"].every(function(s){ return m0.indexOf(s) !== -1; }) &&
    !/(Sprint|Standard|Premium)/.test(m0) &&
    !/Cronograma (Sprint|Standard|Premium)/.test(document.body.textContent);
});

// acessibilidade estrutural: subsecoes operaveis por teclado, janelas com
// papel de dialogo, campos com rotulo, link de pular, ingles marcado
check("a11y_subsections_are_buttons_with_state", function(){
  var hs = document.querySelectorAll("h3.h3-toggle"), ok = hs.length > 200;
  Array.prototype.forEach.call(hs, function(h){
    var b = h.querySelector(":scope > .h3-btn");
    // o valor de aria-expanded e sincronizado por um observador assincrono:
    // aqui so a estrutura; o valor e conferido em real_keyboard_opens_subsections_and_dialogs
    if(!b || b.tagName !== "BUTTON" || !b.hasAttribute("aria-expanded")) ok = false;
  });
  return ok;
});
check("a11y_dialogs_have_role_and_name", function(){
  return ["certModal", "accountModal", "dashboardModal"].every(function(id){
    var m = document.getElementById(id);
    return m.getAttribute("role") === "dialog" && m.getAttribute("aria-modal") === "true" && !!m.getAttribute("aria-label");
  });
});
check("a11y_every_field_has_a_label", function(){
  return Array.prototype.every.call(document.querySelectorAll(".shell input:not([type=hidden]):not([type=file]), .shell textarea, .shell select"), function(i){
    return !!(i.getAttribute("aria-label") || i.closest("label") || (i.id && document.querySelector('label[for="' + i.id + '"]')));
  });
});
check("a11y_skip_link_and_current_module", function(){
  var s = document.querySelector("a.skip-link");
  return !!s && s.getAttribute("href") === "#mainArea" && document.body.firstElementChild === s &&
    document.querySelectorAll('.tabbtn[aria-current="page"]').length === 1;
});
check("a11y_english_content_is_marked", function(){
  var opts = document.querySelectorAll(".opt .otext"), en = document.querySelectorAll('.opt .otext[lang="en"]');
  return en.length > opts.length * 0.8 && document.querySelectorAll('.ctw-text[lang="en"]').length === 8 &&
    document.querySelectorAll('.spk-text[lang="en"]').length > 50 &&
    Array.prototype.every.call(document.querySelectorAll('[lang="en"]'), function(e){ return !/[ãõç]/.test(e.textContent); });
});

// fontes por <link> no <head> (com preconnect), nunca por @import no CSS
check("fonts_load_by_link_not_import", function(){
  var css = Array.prototype.map.call(document.querySelectorAll("style"), function(s){ return s.textContent; }).join("");
  return !!document.querySelector('head link[rel="stylesheet"][href*="fonts.googleapis.com"]') &&
    document.querySelectorAll('head link[rel="preconnect"]').length === 2 && css.indexOf("@import") === -1;
});
// erro de login que o servidor manda em ingles sai em portugues
check("auth_errors_are_in_portuguese", function(){
  var f = window.__toeflFriendlyError;
  return !!f && f("Invalid login credentials") === "E-mail ou senha incorretos." &&
    f("Email not confirmed").indexOf("Confirme") === 0 && f("email rate limit exceeded").indexOf("Muitas tentativas") === 0 &&
    f("TypeError: Failed to fetch").indexOf("Sem conexão") === 0 && f("algo novo").indexOf("Erro: ") === -1;
});
// a sequencia de dias aparece na gaveta, fora do Painel
check("streak_line_in_sidebar", function(){
  var t = document.getElementById("streakLine").textContent;
  return t.indexOf("1 dia de estudo seguido") === 0;
});

// "Marcar esta parte como concluida": o texto fica dentro do <label> da caixa
check("mark_done_label_wraps_text", function(){
  var all = document.querySelectorAll(".mark-done");
  return all.length > 50 && Array.prototype.every.call(all, function(m){ return !!m.querySelector("label.prog-check .pchk") && !!m.querySelector("label.prog-check .mark-done-label"); });
});

// ---- redação: regras compartilhadas com o servidor (supabase/functions/_shared/redacao.js) ----
// horário de Brasília = UTC-3: "sexta às 23h30" é sábado 02h30 em UTC
function brt(y, m, d, h, min){ return Date.UTC(y, m - 1, d, h + 3, min || 0); }
check("essay_due_friday_night_skips_weekend_and_tiradentes", function(){
  // sexta 17/04/2026 23h30: segunda 20 (1), terça 21 é Tiradentes, quarta 22 (2), quinta 23 (3)
  return redacaoPrevisao(brt(2026, 4, 17, 23, 30)) === "2026-04-23";
});
check("essay_due_friday_night_before_carnival", function(){
  // sexta 05/02/2027 23h: segunda 8 e terça 9 são Carnaval; quarta 10, quinta 11, sexta 12
  return redacaoPrevisao(brt(2027, 2, 5, 23, 0)) === "2027-02-12";
});
check("essay_due_uses_brasilia_date", function(){
  // quinta 15/10/2026 23h30 em Brasília já é sexta em UTC: o prazo conta da quinta
  return redacaoPrevisao(brt(2026, 10, 15, 23, 30)) === "2026-10-20";
});
check("essay_due_skips_good_friday_and_christmas", function(){
  return redacaoPrevisao(brt(2026, 4, 2, 10)) === "2026-04-08" && redacaoPrevisao(brt(2026, 12, 24, 10)) === "2026-12-30";
});
check("essay_holidays_fixed_and_movable", function(){
  var f26 = redacaoFeriados(2026), f27 = redacaoFeriados(2027);
  return ["2026-01-01", "2026-02-16", "2026-02-17", "2026-04-03", "2026-04-21", "2026-06-04", "2026-11-20", "2026-12-25"]
           .every(function(d){ return !!f26[d]; }) &&
         ["2027-02-08", "2027-02-09", "2027-03-26", "2027-05-27"].every(function(d){ return !!f27[d]; }) &&
         !f26["2026-04-22"] && Object.keys(f26).length === 13;
});
check("essay_cooldown_4_days", function(){
  var t = Date.UTC(2026, 9, 14, 15, 0), DAYMS = 86400000, h = [{ submitted_at: new Date(t).toISOString() }];
  var b1 = redacaoBloqueio(h, t + 3.9 * DAYMS), b2 = redacaoBloqueio(h, t + 4 * DAYMS), b0 = redacaoBloqueio([], t);
  return b1.bloqueado && b1.liberaEm === t + 4 * DAYMS && !b2.bloqueado && !b0.bloqueado && b0.liberaEm === null;
});
check("essay_final_score_rounds_and_caps", function(){
  function f(a, b, c, d){ return redacaoNotaFinal({ cumprimento: a, organizacao: b, gramatica: c, vocabulario: d }); }
  return f(4, 3, 3, 3) === 3.5 && f(4, 4, 4, 3) === 4 && f(2, 5, 5, 5) === 2.5 && f(2, 2, 2, 1) === 2 &&
         f(5, 5, 5, 5) === 5 && redacaoNivel(5) === "C1/C2 (banda 5,5 a 6)" && redacaoNivel(4.5) === "B2 alto/C1 (banda 4,5 a 5)" &&
         redacaoNivel(3.5) === "B2 (banda 4)" && redacaoNivel(2.5) === "B1 (banda 3 a 3,5)" && redacaoNivel(1) === "A2 (banda 2 a 2,5)" &&
         redacaoNivel(0.5) === "A1 ou sem resposta";
});
function essayGoodFeedback(){
  function crit(n){ return { nota: n, justificativa: "Frase de justificativa." }; }
  return {
    criterios: { cumprimento: crit(4), organizacao: crit(3.5), gramatica: crit(3), vocabulario: crit(4) },
    trechos: [{ original: "I am agree", correcao: "I agree", explicacao: "Agree já é verbo.", codigo: "W2" },
              { original: "very much people", correcao: "many people", explicacao: "Contável pede many.", codigo: null }],
    reescrita: { original: "I think it is good.", versao: "I would argue that it is beneficial." },
    prioridade: { texto: "Revise a concordância verbal.", modulo: "M4", parte: 3 }
  };
}
check("essay_feedback_accepts_exact_format", function(){ return redacaoValidaDevolutiva(essayGoodFeedback()).ok; });
check("essay_feedback_rejects_with_clear_messages", function(){
  function errs(mut){ var d = essayGoodFeedback(); mut(d); return redacaoValidaDevolutiva(d).erros.join(" | "); }
  return errs(function(d){ d.criterios.gramatica.nota = 6; }).indexOf("criterios.gramatica.nota: tem de ser um número de 0 a 5") === 0 &&
         errs(function(d){ d.criterios.vocabulario.nota = 3.3; }).indexOf("passos de 0.5") !== -1 &&
         errs(function(d){ delete d.reescrita; }) === 'falta o campo "reescrita".' &&
         errs(function(d){ d.nota_final = 4; }).indexOf("calculados pelo site") !== -1 &&
         errs(function(d){ for(var i = 0; i < 4; i++) d.trechos.push(d.trechos[0]); }).indexOf("no máximo 5") !== -1 &&
         errs(function(d){ d.trechos[0].codigo = "W9"; }).indexOf("trechos[1].codigo: use W1 a W6") === 0 &&
         errs(function(d){ d.prioridade.parte = 9; }) === "prioridade.parte: o M4 tem as Partes 1 a 7 (veio 9)." &&
         errs(function(d){ d.prioridade.modulo = "M9"; }).indexOf('use "M4" ou "M5"') !== -1 &&
         !redacaoValidaDevolutiva("texto solto").ok && !redacaoValidaDevolutiva(null).ok;
});

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
        out[key] = ("<h1>" in data and data.count("<h2>") >= 8 and 'href="index.html"' in data
                    and 'rel="icon"' in data and "@import" not in data)
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


def plans_checks():
    """Os tres planos: o que o site mostra (app/plans.json) bate com o que o
    servidor cobra (supabase/functions/_shared/plans.ts), o preco nunca vem
    do navegador, a migracao esta espelhada no schema.sql e os termos falam
    dos planos e do reembolso."""
    out = {}
    site = json.loads((APP_DIR / "plans.json").read_text(encoding="utf-8"))
    fn_dir = ROOT / "supabase" / "functions"
    shared = (fn_dir / "_shared" / "plans.ts").read_text(encoding="utf-8")
    server = [
        (m.group(1), m.group(2), None if m.group(3) == "null" else int(m.group(3)), int(m.group(4)))
        for m in re.finditer(r'\{ id: "(\w+)", name: "(\w+)", days: (null|\d+), priceCents: (\d+) \}', shared)
    ]
    out["plans_server_matches_site"] = len(server) == 3 and server == [
        (p["id"], p["name"], p["days"], p["price_cents"]) for p in site["plans"]
    ]
    out["plans_prices_are_the_decided_ones"] = server == [
        ("sprint", "Sprint", 30, 3990), ("standard", "Standard", 90, 8990), ("premium", "Premium", None, 14990),
    ]

    checkout = (fn_dir / "create-checkout" / "index.ts").read_text(encoding="utf-8")
    out["plans_checkout_price_comes_from_server"] = (
        "findPlan(planId)" in checkout and "unit_price: priceCents / 100" in checkout
        and "plan.priceCents * (100 - coupon.percent)" in checkout
        and not re.search(r"body\??\.(price|amount|unit_price|days)", checkout)
    )
    webhook = (fn_dir / "mp-webhook" / "index.ts").read_text(encoding="utf-8")
    out["plans_webhook_records_term"] = (
        'rpc("apply_payment"' in webhook and "p_days: ref.plan.days" in webhook
        and "parseReference(payment.external_reference)" in webhook
    )

    # o corpo da migracao (da primeira secao em diante) tem de estar igual no schema.sql
    migration = (ROOT / "supabase" / "migrations" / "20261008_planos.sql").read_text(encoding="utf-8")
    body = migration[migration.index("-- ============ entitlements: plano e validade"):]
    schema = (ROOT / "supabase" / "schema.sql").read_text(encoding="utf-8")
    out["plans_migration_mirrored_in_schema"] = body in schema and all(
        s in body for s in ("expires_at timestamptz", "create table if not exists payments",
                            "function public.apply_payment", "from public, anon, authenticated")
    )

    terms = (ARTIFACT.parent / "termos.html").read_text(encoding="utf-8")
    out["plans_terms_cover_plans_and_refund"] = (
        all(s in terms for s in ("Sprint", "Standard", "Premium", "30 dias", "90 dias", "Vitalício",
                                 "7 dias corridos", "artigo 49", "renovação automática"))
        and "REVISAR" not in terms
    )
    return out


def essay_server_checks():
    """Envio de redação no servidor: a migração está espelhada no schema.sql,
    nenhuma tabela nova aceita escrita do navegador, as regras do envio são
    conferidas na edge function (e não só no site), só corretor devolve, e
    nenhuma API de IA é chamada (modelo assistido, 2026-10-14)."""
    out = {}
    sb = ROOT / "supabase"
    migration = (sb / "migrations" / "20261014_redacoes.sql").read_text(encoding="utf-8")
    body = migration[migration.index("-- ============ redações: quem corrige"):]
    schema = (sb / "schema.sql").read_text(encoding="utf-8")
    out["essay_migration_mirrored_in_schema"] = body in schema

    policies = re.findall(r"create policy \"(\w+)\" on (\w+)\s+for (\w+)", migration)
    out["essay_db_no_client_write"] = (
        {(name, table, op) for name, table, op in policies}
        == {("admins_select_own", "admins", "select"), ("essays_select_own_or_admin", "essay_submissions", "select")}
        and "alter table admins enable row level security" in migration
        and "alter table essay_submissions enable row level security" in migration
        and "auth.uid() = user_id or public.is_admin()" in migration
        and re.search(r"revoke all on function public\.create_essay_submission\([^)]*\) from public, anon, authenticated", migration)
        and re.search(r"grant execute on function public\.create_essay_submission\([^)]*\) to service_role;", migration)
        and "on delete cascade" in migration.split("create table if not exists essay_submissions")[1].split(");")[0]
    )

    shared = (sb / "functions" / "_shared" / "redacao.js").read_text(encoding="utf-8")
    rules = {k: int(v) for k, v in re.findall(r"^\s+(intervaloDias|prazoDiasUteis|maxPalavras|maxCaracteres): (\d+)", shared, re.M)}
    out["essay_db_limits_match_rules"] = (
        rules == {"intervaloDias": 4, "prazoDiasUteis": 3, "maxPalavras": 600, "maxCaracteres": 5000}
        and "interval '4 days'" in migration and "between 1 and 5000" in migration and "between 1 and 600" in migration
        and "minutos: { email: 7, discussion: 10 }" in shared and "minPalavras: { email: 1, discussion: 100 }" in shared
    )

    submit = (sb / "functions" / "submit-essay" / "index.ts").read_text(encoding="utf-8")
    out["essay_submit_enforces_rules_on_server"] = all(s in submit for s in (
        'from "../_shared/redacao.js"', "redacaoContaPalavras(text)", "REDACAO_REGRAS.minPalavras",
        "REDACAO_REGRAS.maxCaracteres", "REDACAO_REGRAS.maxPalavras", 'from("entitlements")', "ent.expires_at",
        "redacaoBloqueio(", "redacaoPrevisao(now)", 'rpc("create_essay_submission"', "body.consent === true",
    )) and not re.search(r"body\.(words|word_count|due|due_on|status)\b", submit)

    review = (sb / "functions" / "review-essay" / "index.ts").read_text(encoding="utf-8")
    out["essay_review_admin_only_and_validated"] = (
        review.index('from("admins")') < review.index('body.action === "start"')
        and "redacaoValidaDevolutiva(feedback)" in review and "redacaoNotaFinal(notas)" in review
        and not re.search(r"body\.(final|final_score|level)\b", review)
    )
    mail = (sb / "functions" / "_shared" / "mail.ts").read_text(encoding="utf-8")
    out["essay_email_only_with_smtp"] = (
        "if (!smtpConfigured() || !to) return false;" in mail and "sendMail(" in review
        and not re.search(r"SMTP_PASS\s*=|password:\s*\"", mail)
    )
    functions_code = "\n".join(p.read_text(encoding="utf-8") for p in (sb / "functions").rglob("*.ts"))
    functions_code += shared
    out["essay_no_ai_api_called"] = not re.search(
        r"anthropic|openai|generativelanguage|api\.mistral|ANTHROPIC|OPENAI", functions_code)
    return out


def landing_checks():
    """Tela de apresentacao gerada: existe, e leve (nao carrega o curso), os
    numeros que anuncia sao os do site de verdade e o login aponta para ela."""
    out = {}
    path = ARTIFACT.parent / "apresentacao.html"
    if not path.exists():
        return {"landing_page_built": False}
    page = path.read_text(encoding="utf-8")
    index = ARTIFACT.read_text(encoding="utf-8")
    out["landing_page_built"] = (
        '<meta name="description"' in page and "@import" not in page and 'rel="icon"' in page
        and "panel-mod1" not in page and "ITOEFL_SUPABASE" not in page and len(page) < len(index) / 4
    )
    announced = [int(n) for n in re.findall(r'<span class="lp-stat-n">(\d+)</span>', page)]
    real = [
        len(re.findall(r'<section class="panel', index)),
        len(re.findall(r'class="ctw-in"', index)),
        len(re.findall(r'class="qcard"', index.split('id="panel-mod1"')[1].split('id="panel-mod2"')[0])),
        len(re.findall(r'class="qcard"', index.split('id="panel-mod2"')[1].split('id="panel-mod3"')[0])),
        len(re.findall(r'class="bsq-card', index.split('id="panel-mod4"')[1].split('id="panel-mod5"')[0])),
        len(re.findall(r'class="spk"', index.split('id="panel-mod3"')[1].split('id="panel-mod4"')[0])),
        len(re.findall(r'class="exam-item', index)),
        len(json.loads((APP_DIR / "vocab_kit.json").read_text(encoding="utf-8"))),
    ]
    out["landing_numbers_match_the_site"] = announced == real and all(n > 0 for n in real)
    out["landing_linked_from_login"] = 'href="apresentacao.html"' in index or "ITOEFL_SUPABASE" not in index
    return out


def deep_markup_checks():
    """Marcacao :::aprofundamento mal escrita tem que derrubar o build, nao
    sair calada no site."""
    sys.path.insert(0, str(APP_DIR))
    import build_pipeline as bp

    def fails(text):
        try:
            bp.to_html(text)
        except ValueError:
            return True
        return False

    good = bp.to_html("Antes.\n\n:::aprofundamento Título\nTexto.\n:::\n\nDepois.")
    return {
        "deep_markup_converts": '<details class="deep">' in good and ":::" not in good and "<p>Depois.</p>" in good,
        "deep_markup_rejects_broken": all(fails(t) for t in (
            ":::aprofundamento Sem fim\nTexto.",
            ":::aprofundamento Parte dentro\n## PARTE 9\n:::",
            ":::aprofundamento A\n:::aprofundamento B\nx\n:::\n:::",
            "Texto.\n:::\n",
            ":::aprofundamento Vazio\n\n:::",
            "- item\n\n    :::aprofundamento Na lista\n    x\n    :::",
        )),
    }


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


def content_review_checks():
    """Revisao de conteudo de 2026-10-13, rodada 1: o gabarito corrigido e as
    alternativas que deixavam o item com duas respostas nao podem voltar."""
    sys.path.insert(0, str(APP_DIR))
    import drills_data

    lists = [getattr(drills_data, n) for n in dir(drills_data) if n.startswith("MOD")]
    drills = {d["id"]: d for lst in lists for d in lst}
    items = [it for d in drills.values() for it in d["items"]]

    def item(drill_id, num):
        return next(it for it in drills[drill_id]["items"] if it["num"] == num)

    def answer(drill_id, num):
        it = item(drill_id, num)
        return it["options"][it["correct"]]

    def opts(drill_id, num):
        return set(item(drill_id, num)["options"].values())

    # distratores que eram resposta natural (Listen and Choose a Response) ou
    # segunda forma gramatical (lacunas do M1)
    banned = {
        ("mod1-a1", "2"): "arrives", ("mod1-a1", "3"): "planned", ("mod1-a1", "5"): "talked",
        ("mod1-a3", "3"): "complete", ("mod1-a5", "4"): "should",
        ("mod2-a", "A2"): "Tuesday's class was canceled, actually.",
        ("mod2-a", "A3"): "The deadline's not until Friday, right?",
        ("mod2-a", "A4"): "Campus is only ten minutes away.",
        ("mod2-a", "A9"): "We left at eight, same as always.",
        ("mod2-a", "A12"): "It's a very competitive program.",
    }
    out = {
        "drills_legacy_lists_gone": not hasattr(drills_data, "MOD1_DRILLS") and not hasattr(drills_data, "MOD2_DRILLS"),
        # "A,B,D" e o item de marcar tres (sai na rodada 2)
        "drills_keys_point_to_an_option": all(set(it["correct"].split(",")) <= set(it["options"])
                                              and len(set(it["options"].values())) == len(it["options"]) for it in items),
        "review_drill_a3_7_is_miss": answer("mod1-a3", "7") == "miss" and "lose a problem" in item("mod1-a3", "7")["explanation"],
        "review_drill_distractors_not_valid": all(text not in opts(*key) for key, text in banned.items()),
    }

    # Build a Sentence: a correcao so aceita a ordem do gabarito, entao bloco
    # movel que cabe em dois lugares vira texto fixo, e o bloco que sobra tem
    # de ser errado de verdade
    from build_sentence_data import BUILD_SENTENCE_ITEMS
    bs = {it["id"]: it for it in BUILD_SENTENCE_ITEMS}
    out["review_build_sentence_single_order"] = ("{this morning}" not in bs["bs17"]["pattern"]
                                                 and "this morning" in bs["bs17"]["pattern"]
                                                 and "will be" not in bs["bs22"].get("extra", []))

    kit = json.loads((APP_DIR / "vocab_kit.json").read_text(encoding="utf-8"))
    words = {w["w"]: w for w in (kit["words"] if isinstance(kit, dict) else kit)}
    out["review_vocab_consequential_gloss"] = not words["consequential"]["pt"].startswith("consequente")

    quiz = json.loads((APP_DIR / "quiz_mod0.json").read_text(encoding="utf-8"))
    questions = quiz["questions"] if isinstance(quiz, dict) else quiz
    q5 = next(q for q in questions if q["num"] == 5)
    out["review_diag_q5_not_called_ctw"] = "Complete the Words" not in q5["topic"]

    # M7: toda resposta-modelo de Build a Sentence usa exatamente as palavras
    # dos blocos (tres modelos pediam palavra que nao estava em bloco nenhum)
    def words(text):
        return sorted(re.findall(r"[a-z']+", text.lower()))

    m7 = (ROOT / "consolidated" / "modulo_7_simulados.md").read_text(encoding="utf-8")
    pairs = re.findall(r"`([^`\n]+ / [^`\n]+)`\n\*\*Resposta modelo:\*\* \*([^*\n]+)\*", m7)
    out["review_m7_build_models_use_the_chunks"] = (len(pairs) == 10 and all(
        words(chunks.replace("/", " ")) == words(model) for chunks, model in pairs))
    # a resposta nao vem impressa no enunciado nem como dica ao lado das opcoes
    out["review_m7_no_answer_in_prompt"] = all(s not in m7 for s in (
        '"confirmed")', '"logically")', "(D) decrease", "(C) mandated", "(considerando o contexto positivo"))
    out["review_m7_low_switching_costs"] = "Low switching costs, multi-homing" in m7

    # Texto dos modulos: trechos que ensinavam errado e foram corrigidos
    def module(n):
        return next((ROOT / "consolidated").glob(f"modulo_{n}_*.md")).read_text(encoding="utf-8")

    wrong = {
        0: ['formato "Complete the Words"', "o dobro do Writing", "Média das 4 bandas de seção (Reading"],
        1: ["**B** *lose*", '*"take a photo of me"*', "O CTW quase sempre oferece 4 formas"],
        2: ["mais curta e mais decisiva", "arrasta itens numa tabela", "**the 3rd** vs. **the 30th**"],
        3: ["o dobro do Writing", "rememBERED", "RE-mem-bered", "COMmunicate", "deMONstrate", "boca mais fechada",
            "| e-CO-no-my / e-co-NO-mic |"],
        4: ["Travessão (: )", "sem inversão e sem auxiliar", "information: and often it is not",
            "**The book that is on the shelf is mine.**"],
        6: ["| assumed | presumably |", "2 correlation *(repete", '*(neutro)*'],
        8: ['para sair do modo "leitura"'],
        9: ["| **graduate** | graduado (bacharel)", 'stress em "RON"', "(ð ausente)", "think through the hypothesis"],
    }
    out["review_modules_fixed_text_stays_fixed"] = all(s not in module(n) for n, bad in wrong.items() for s in bad)

    # M5: resposta-modelo de Academic Discussion nao fica abaixo do minimo de
    # 100 palavras que o M4 ensina
    m5 = module(5)
    models = [l for l in m5.splitlines() if l.startswith('> "While Maria raises') or l.startswith('> "While Lía is right')]
    out["review_m5_models_reach_100_words"] = len(models) == 2 and all(
        len(re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9'’-]*", l)) >= 100 for l in models)
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

# bloco de aprofundamento de exemplo, colado na copia temporaria do M3 logo
# antes desta subsecao (ou seja, dentro da PARTE 2, no fim da subsecao 2.1)
FIXTURE_DEEP_ANCHOR = "### 2.2 Estratégia para Listen and Repeat"
FIXTURE_DEEP_BLOCK = """:::aprofundamento Exemplo de aprofundamento
Parágrafo de **exemplo**, só para testar a infraestrutura.

#### Um subtítulo dentro do bloco

- primeiro item
- segundo item
:::

"""

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

// bloco de aprofundamento e seletor de trilha
var deeps = document.querySelectorAll("details.deep");
var deep = deeps[0];
var trailBox = document.getElementById("trailBox");
function trailBtn(name){ return trailBox.querySelector('.trail-btn[data-trail="' + name + '"]'); }
check("deep_example_rendered", function(){
  return deeps.length === 1 && m3.contains(deep) && deep.querySelector(".deep-title").textContent === "Exemplo de aprofundamento" &&
         deep.querySelector(".deep-body strong").textContent === "exemplo" && deep.querySelectorAll(".deep-body li").length === 2 &&
         !!deep.querySelector(".deep-body h4") && m3.textContent.indexOf(":::") === -1;
});
check("deep_inside_part_2_no_new_part", function(){
  return deep.closest(".section-card").querySelector("h2 .htext").textContent.indexOf("PARTE 2") === 0 &&
         m3.querySelectorAll(".section-card").length === 7;
});
check("trail_selector_shown_with_blocks", function(){ return trailBox.hidden === false && document.getElementById("trailHint").textContent.length > 0; });
check("trail_fast_is_default_and_closed", function(){
  return deep.open === false && trailBtn("rapida").classList.contains("active") && trailBtn("rapida").getAttribute("aria-pressed") === "true";
});
trailBtn("completa").click();
check("trail_complete_opens_blocks", function(){
  return deep.open === true && localStorage.getItem("toefl_trilha_v1") === "completa" && trailBtn("completa").classList.contains("active") &&
         !trailBtn("rapida").classList.contains("active");
});
trailBtn("rapida").click();
check("trail_fast_closes_blocks", function(){ return deep.open === false && localStorage.getItem("toefl_trilha_v1") === "rapida"; });
check("fixture_no_js_errors", function(){ return window.__errors.length === 0; });
results.__jsErrors = window.__errors;
document.title = JSON.stringify(results);
</script>
</body>
"""


def build_fixture(work):
    """Builda o site de exemplo em `work` e devolve o index.html gerado."""
    # supabase/functions/_shared: o build cola as regras de redação de lá
    for name in ("app", "consolidated", "legal", "supabase/functions/_shared"):
        shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns("__pycache__"))
    (work / "app" / "supabase_config.json").unlink(missing_ok=True)
    (work / "app" / "videos.json").write_text(json.dumps(FIXTURE_VIDEOS, ensure_ascii=False), encoding="utf-8")
    m3 = work / "consolidated" / "modulo_3_speaking.md"
    text = m3.read_text(encoding="utf-8")
    if text.count(FIXTURE_DEEP_ANCHOR) != 1:
        raise SystemExit(f"Fixture: nao achei {FIXTURE_DEEP_ANCHOR!r} no M3. Ajuste FIXTURE_DEEP_ANCHOR em scripts/smoke_test.py.")
    m3.write_text(text.replace(FIXTURE_DEEP_ANCHOR, FIXTURE_DEEP_BLOCK + FIXTURE_DEEP_ANCHOR), encoding="utf-8", newline="\n")
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
        try:
            result = subprocess.run(
                # --no-sandbox: com o sandbox ligado, o Chrome 155 headless às
                # vezes trava sem abrir nem uma página vazia (2026-10-14). A
                # página aberta aqui é sempre o próprio site, local.
                [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", f"--user-data-dir={profile}", "--dump-dom", uri],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90,
            )
        except subprocess.TimeoutExpired:
            # a passada leva uns 20 s, mas o Chrome desta máquina às vezes
            # demora bem mais para abrir: conta como tentativa perdida
            result = None
            continue
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
    results.update(plans_checks())
    results.update(essay_server_checks())
    results.update(landing_checks())
    results.update(deep_markup_checks())
    results.update(bank_checks())
    results.update(content_review_checks())

    # quarta passada: Chrome de verdade por http://127.0.0.1 (recarregar,
    # tela de celular, contraste, service worker). Ver scripts/smoke_browser.py
    print("Rodando a passada no Chrome de verdade (recarga, celular, contraste, service worker)...")
    import smoke_browser
    real, real_details = smoke_browser.run()
    results.update(real)
    for name, detail in real_details.items():
        results[name + "__error"] = detail

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
