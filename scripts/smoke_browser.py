"""Passada do smoke test num Chrome de verdade, dirigido pelo DevTools.

As outras passadas do smoke_test.py injetam um script e leem o resultado com
--dump-dom: nao conseguem recarregar a pagina, mudar o tamanho da tela nem
esperar um service worker. Esta abre o site sem login (o mesmo do
scripts/build_teste.py) por http://127.0.0.1 e confere o que so aparece assim:

- o progresso de cada widget volta depois de recarregar;
- reiniciar o progresso apaga tudo, importar restaura;
- nenhuma pagina estoura na largura de um celular (375 px);
- contraste de texto WCAG AA no tema claro e no escuro;
- o service worker entrega a versao nova depois de um build novo e o site
  abre sem rede.

Chamado por scripts/smoke_test.py. Sozinho: python scripts\\smoke_browser.py
"""

import functools
import hashlib
import hmac
import http.server
import json
import os
import re
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_teste  # noqa: E402
from cdp import Browser  # noqa: E402


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def _serve(directory):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Quiet, directory=str(directory)))
    srv.handle_error = lambda *a: None  # o Chrome derruba conexoes ao fechar; nao e erro do teste
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


# Usa cada widget uma vez, como um aluno. Devolve a lista do que falhou.
ACT = r"""
(function(){
  var log = [];
  function type(el, v){ el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }
  function step(name, fn){ try { fn(); } catch(ex){ log.push(name + ": " + ex.message); } }
  step("diagnostico", function(){
    Array.prototype.forEach.call(document.querySelectorAll('.quiz-drill[data-drill="mod0-diag"] .qcard'), function(c, k){
      var want = k < 7 ? c.dataset.correct : ["A","B","C","D"].filter(function(L){ return L !== c.dataset.correct; })[0];
      c.querySelector('.opt[data-letter="' + want + '"]').click(); c.querySelector(".qconfirm").click();
    });
  });
  step("quiz M1", function(){
    var c = document.querySelector("#panel-mod1 .quiz-drill .qcard:not([data-multi])");
    var wrong = ["A","B","C","D"].filter(function(L){ return L !== c.dataset.correct; })[0];
    c.querySelector('.opt[data-letter="' + wrong + '"]').click(); c.querySelector(".qconfirm").click();
  });
  step("complete the words", function(){
    var ctw = document.querySelectorAll(".ctw");
    Array.prototype.forEach.call(ctw[0].querySelectorAll(".ctw-in"), function(i){ type(i, i.dataset.answer); });
    ctw[0].querySelector(".ctw-check").click();
    type(ctw[1].querySelector(".ctw-in"), "ab");
  });
  step("build a sentence", function(){
    var card = document.querySelector(".bsq-card");
    JSON.parse(card.dataset.answer).forEach(function(f){
      Array.prototype.filter.call(card.querySelectorAll(".bsq-bank .bsq-chip"), function(c){ return c.dataset.frag === f; })[0].click();
    });
    card.querySelector(".bsq-check").click();
  });
  step("caixa de escrita", function(){
    type(document.querySelector("#panel-mod4 .wbox .wbox-text"), "Dear Professor, this is a persistence test.");
    type(document.querySelector("#panel-mod7 .wbox .wbox-text"), "Mock exam text.");
  });
  step("speaking", function(){
    var it = document.querySelector('#panel-mod3 .spk[data-mode="repeat"] .spk-item');
    it.querySelector(".spk-show").click(); it.querySelector('.spk-mark[data-mark="ok"]').click();
    var it2 = document.querySelector('#panel-mod3 .spk[data-mode="interview"] .spk-item');
    it2.querySelector(".spk-show").click(); it2.querySelector(".spk-mark").click();
  });
  step("simulado", function(){
    var ex = document.querySelectorAll(".exam");
    Array.prototype.forEach.call(ex[0].querySelectorAll(".exam-item"), function(i){ i.querySelector('.exam-opt[data-letter="' + i.dataset.correct + '"]').click(); });
    ex[0].querySelector(".exam-submit").click();
    ex[1].querySelector(".exam-opt").click();
  });
  step("calculadora", function(){
    ["reading","listening","writing","speaking"].forEach(function(s, i){ type(document.getElementById("scalc-" + s), String(50 + i * 10)); });
  });
  step("flashcards", function(){
    var srs = document.querySelector(".srs");
    srs.querySelector(".srs-flip").click(); srs.querySelector('.srs-grades button[data-g="2"]').click();
  });
  step("registro de erros", function(){
    var el = document.querySelector('.errlog[data-errlog="mod1"]');
    el.querySelector(".errlog-drill").value = "Drill <b>A1</b> & teste";
    el.querySelector(".errlog-result").value = "3/5";
    el.querySelector(".errlog-code input").checked = true;
    el.querySelector(".errlog-form").dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
  });
  step("painel semanal", function(){ type(document.querySelector(".wd-input"), "72"); });
  step("progresso", function(){
    // clica no TEXTO de "Marcar esta parte como concluída", não na caixinha
    document.querySelector("#panel-mod0 .mark-done .mark-done-label").click();
    window.__toeflSetH3Done(document.querySelector("#panel-mod0 h3.h3-toggle"), true);
  });
  step("paginacao", function(){
    document.querySelector('.tabbtn[data-tab="mod1"]').click();
    document.querySelector("#panel-mod1 .part-next").click(); document.querySelector("#panel-mod1 .part-next").click();
  });
  return log;
})()
"""

# Tudo que o aluno ve do proprio progresso. Tem que sair igual depois de recarregar.
SNAP = r"""
(function(){
  function t(sel){ var e = document.querySelector(sel); return e ? (e.hidden ? "[oculto] " : "") + e.textContent.trim().replace(/\s+/g, " ").slice(0, 90) : null; }
  return {
    diag: t('.quiz-drill[data-drill="mod0-diag"] .quiz-summary-text'), nivel: t("#levelBadgeBand"), cronograma: t("#levelBadgeSched"),
    resultado: t("#diagResultTitle"), plano: t("#diagPlanGap"),
    quizM1: t("#panel-mod1 .quiz-drill .quiz-score"), erradasM1: document.querySelectorAll("#panel-mod1 .opt.wrong").length,
    ctw: t(".ctw .ctw-result"), ctwParcial: document.querySelectorAll(".ctw")[1].querySelector(".ctw-in").value,
    bsq: document.querySelector(".bsq-card").className, bsqScore: t(".bsq .quiz-score"),
    escritaM4: document.querySelector("#panel-mod4 .wbox .wbox-text").value, escritaM7: document.querySelector("#panel-mod7 .wbox .wbox-text").value,
    repeat: t('#panel-mod3 .spk[data-mode="repeat"] .spk-score'), entrevista: t('#panel-mod3 .spk[data-mode="interview"] .spk-score'),
    simulado: t(".exam .exam-result"), simuladoParcial: document.querySelectorAll(".exam")[1].querySelectorAll(".is-chosen").length,
    calculadora: t("#scalcTotal"), flashNovas: t(".srs-new"), flashDominadas: t(".srs-mastered"),
    erros: document.querySelectorAll('.errlog[data-errlog="mod1"] .errlog-entry').length,
    semanal: document.querySelector(".wd-input").value,
    parte: document.querySelector("#panel-mod0 .pchk").checked, selo: t("#badge-mod0"), geral: t("#opPct"), modulo: t("#phPct-mod0"),
    subsecoes: document.querySelectorAll(".h3-done").length, pagina: t("#panel-mod1 .part-pager-label"),
    aba: document.querySelector(".tabbtn.active").dataset.tab, meta: t("#dgCount"),
    desempenho: [t("#liveScoreReadingBand"), t("#liveScoreWritingBand"), t("#liveScoreExamBand")]
  };
})()
"""

# Abre tudo de um modulo (todas as Partes, subsecoes e blocos recolhidos) e
# lista o que passa da largura da tela sem estar dentro de uma area que rola.
OVERFLOW = r"""
(function(key){
  document.querySelector('.tabbtn[data-tab="' + key + '"]').click();
  var p = document.getElementById("panel-" + key);
  Array.prototype.forEach.call(p.querySelectorAll(".section-card"), function(c){ c.hidden = false; });
  Array.prototype.forEach.call(p.querySelectorAll(".h3-toggle"), function(h){ h.classList.remove("collapsed"); });
  Array.prototype.forEach.call(p.querySelectorAll(".h3-body"), function(h){ h.classList.remove("h3-collapsed"); });
  Array.prototype.forEach.call(p.querySelectorAll("details"), function(d){ d.open = true; });
  var vw = document.documentElement.clientWidth, bad = [];
  function scrolls(el){
    for(var a = el.parentElement; a && a !== document.body; a = a.parentElement){
      if(/(auto|scroll)/.test(getComputedStyle(a).overflowX)) return true;
    }
    return false;
  }
  Array.prototype.forEach.call(p.querySelectorAll("*"), function(el){
    var r = el.getBoundingClientRect();
    if(!r.width || !r.height || (r.right <= vw + 1 && r.left >= -1) || scrolls(el)) return;
    bad.push(el.tagName.toLowerCase() + "." + String(el.className).trim().split(/\s+/).join("."));
  });
  if(document.documentElement.scrollWidth > vw + 1) bad.push("pagina: " + document.documentElement.scrollWidth + " px");
  return bad.slice(0, 8);
})
"""

# Contraste de todo texto da pagina (WCAG AA: 4,5:1, ou 3:1 em texto grande).
# Ficam de fora: controle desabilitado, que a norma isenta; as telas de login
# e de compra, que este build nao tem; texto so de emoji ou simbolo; e o
# numero vazado do cabecalho do modulo, que e enfeite.
CONTRAST = r"""
(function(){
  function parse(c){
    var m = c.match(/rgba?\(([^)]+)\)/); if(!m) return null;
    var p = m[1].split(/[,\s\/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function blend(top, bot){ var a = top.a; return { r: top.r * a + bot.r * (1 - a), g: top.g * a + bot.g * (1 - a), b: top.b * a + bot.b * (1 - a), a: 1 }; }
  function lum(c){
    function f(v){ v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function ratio(a, b){ var l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); }
  function bgOf(el){
    var layers = [];
    for(var a = el; a; a = a.parentElement){
      var c = parse(getComputedStyle(a).backgroundColor);
      if(c && c.a > 0){ layers.push(c); if(c.a >= 0.999) break; }
    }
    var base = parse(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 };
    for(var i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return base;
  }
  var found = {};
  var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null), n;
  while((n = w.nextNode())){
    if(!/[A-Za-z0-9À-ÿ]/.test(n.nodeValue)) continue;
    var el = n.parentElement;
    if(!el || el.closest("script, style, .srs-data, svg, .auth-gate, .ph-num, button:disabled, input:disabled")) continue;
    var s = getComputedStyle(el);
    var fg = parse(s.color); if(!fg || fg.a === 0) continue;
    var bg = bgOf(el);
    var op = 1; for(var a = el; a; a = a.parentElement){ op *= parseFloat(getComputedStyle(a).opacity || 1); }
    fg = blend({ r: fg.r, g: fg.g, b: fg.b, a: fg.a * op }, bg);
    var size = parseFloat(s.fontSize), bold = parseInt(s.fontWeight, 10) >= 700;
    var need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
    var r = ratio(fg, bg);
    if(r < need){
      var sig = el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : "");
      if(!found[sig] || r < found[sig]) found[sig] = Math.round(r * 100) / 100;
    }
  }
  return Object.keys(found).map(function(k){ return k + " " + found[k]; }).slice(0, 10);
})()
"""

# Cabeçalho (itens 24, 29 e 31 de 2026-10-25): o botão do menu fica abaixo da
# faixa "Versão de teste", o ✕ da gaveta aberta não cai sobre a foto, o selo
# da meta e da sequência está no topo, e o número do módulo está colado ao título.
HEADER = r"""
(function(){
  function r(el){ return el.getBoundingClientRect(); }
  function hit(a, b){ return a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom; }
  window.scrollTo(0, 0);
  document.getElementById("authBox").hidden = false; document.getElementById("authIn").hidden = false;
  var beta = document.getElementById("betaBar"), ham = document.getElementById("sideToggle"), av = document.getElementById("authAvatar");
  var chip = document.getElementById("topChip"), panel = document.querySelector(".panel:not([hidden])");
  var o = { betaClear: !beta || r(ham).top >= r(beta).bottom, chipShown: !!chip && r(chip).width > 0 && r(chip).top < 120,
            chipClearOfAvatar: !hit(r(chip), r(av)), noOverlay: !document.querySelector(".auth-avatar-wrap button + button") };
  var num = panel.querySelector(".ph-num"), h1 = panel.querySelector(".panel-head h1");
  o.numNearTitle = Math.abs(r(num).top - r(h1).top) < 30 && r(h1).left - r(num).right < 40 && r(h1).left > r(num).right - 1;
  var rail = document.getElementById("sideRail");
  rail.style.transition = "none";
  ham.click();
  var close = document.getElementById("sideClose");
  o.closeClearOfAvatar = !hit(r(close), r(av)) && r(close).width > 0;
  close.click();
  rail.style.transition = "";
  document.getElementById("authBox").hidden = true;
  return o;
})()
"""

# Leitura e navegação na Parte (itens 14, 15, 26 e 30): texto com cerca de 70
# caracteres por linha; a coluna "Nesta Parte" (computador) ou a barra fina
# (celular) com as subseções, o ✓ das lidas mesmo fechadas, o botão único de
# concluir e a paginação que diz "Próxima Parte".
READING = r"""
(function(){
  document.querySelector('.tabbtn[data-tab="mod5"]').click();
  var cards = document.querySelectorAll("#panel-mod5 .section-card");
  window.__toeflShowPart.mod5(cards[1], { noScroll: true });
  var card = cards[1], rail = document.getElementById("partRail"), col = document.querySelector(".content-col");
  // caracteres por linha nos parágrafos longos que estão à vista
  Array.prototype.forEach.call(card.querySelectorAll(".h3-toggle.collapsed .h3-btn"), function(b){ b.click(); });
  var widths = [];
  Array.prototype.forEach.call(card.querySelectorAll(".h3-body > p"), function(p){
    var lh = parseFloat(getComputedStyle(p).lineHeight), lines = Math.round(p.getBoundingClientRect().height / lh);
    if(lines >= 3) widths.push(p.textContent.length / lines);
  });
  widths.sort(function(a, b){ return a - b; });
  var cpl = widths.length ? Math.round(widths[Math.floor(widths.length / 2)]) : 0;
  var h3s = card.querySelectorAll("h3.h3-toggle"), h = h3s[0];
  window.__toeflSetH3Done(h, true);
  if(!h.classList.contains("collapsed")) h.querySelector(".h3-btn").click();
  var dot = h.querySelector(".h3-done-dot");
  var rr = rail.getBoundingClientRect(), cr = col.getBoundingClientRect();
  var o = { cpl: cpl, items: document.querySelectorAll("#railToc .rail-sub").length, h3: h3s.length,
    railRight: rr.left >= cr.right - 1, sticky: getComputedStyle(rail).position === "sticky", railH: Math.round(rr.height),
    checkClosed: h.classList.contains("collapsed") && dot.getBoundingClientRect().width > 0,
    railCheck: document.querySelector("#railToc .rail-sub").classList.contains("is-done"),
    count: document.getElementById("railCount").textContent,
    pager: document.querySelector("#panel-mod5 .part-next").textContent,
    bottom: card.querySelector(".part-next-bottom").textContent,
    arrowNear: (function(){ var b = h.querySelector(".h3-btn"), t = b.querySelector(".h3-text").getBoundingClientRect(),
      c = b.querySelector(".h3-chevron").getBoundingClientRect(); return c.left - t.right < 16 && b.getBoundingClientRect().width > t.width; })(),
    sentence: card.querySelector("h2 .htext").textContent };
  var bodyShown = getComputedStyle(document.getElementById("railBody")).display !== "none";
  o.bodyShown = bodyShown;
  if(!bodyShown){ document.getElementById("railToggle").click(); o.opens = getComputedStyle(document.getElementById("railBody")).display !== "none"; document.getElementById("railToggle").click(); }
  // o botão único conclui a Parte (mesma caixa .pchk do fim dela)
  var chk = card.querySelector(".mark-done .pchk"), was = chk.checked;
  document.getElementById("railDone").click();
  o.doneWorks = chk.checked !== was && document.getElementById("railDone").getAttribute("aria-pressed") === String(chk.checked);
  document.getElementById("railDone").click();
  o.markDoneVisible = card.querySelector(".mark-done").getBoundingClientRect().height > 0;
  window.__toeflShowPart.mod5(cards[0], { noScroll: true }); // volta à Parte 1, como os outros testes esperam
  return o;
})()
"""

# Caixas explicativas (item 7): os 7 tipos existem, cada um com ícone e
# título; sem marcador fica neutra; texto de prova dentro de exercício não muda.
CALLOUTS = r"""
(function(){
  var types = ["dica", "atencao", "exemplo", "erro", "resumo", "ets", "modelo"], o = {};
  types.forEach(function(t){
    var b = document.querySelectorAll('.panel blockquote[data-callout="' + t + '"]');
    o[t] = b.length > 0 && Array.prototype.every.call(b, function(x){
      var h = x.querySelector(".callout-head"); return !!h && !!h.querySelector("svg use") && h === x.firstElementChild; });
  });
  var neutral = document.querySelectorAll(".panel blockquote.callout-neutro");
  o.neutral = neutral.length > 0 && !Array.prototype.some.call(neutral, function(x){ return !!x.querySelector(".callout-head"); });
  o.examUntouched = !document.querySelector(".quiz-drill blockquote.callout, .exam blockquote.callout");
  var tip = document.querySelector('.panel blockquote[data-callout="dica"]'), s = getComputedStyle(tip);
  o.light = parseFloat(s.borderLeftWidth) >= 3 && parseFloat(s.borderTopWidth) === 0;
  o.noLeadEmoji = !/^[☀-➿\uD83C-\uDBFF]/.test(tip.querySelector(".callout-head").nextSibling.textContent.trim());
  return o;
})()
"""

# Tabelas (itens 14 e 34): cabeçalho discreto; no celular, a tabela larga vira
# cartões que cabem na tela; a tabela do formato da prova tem selos e nota de rodapé.
TABLES = r"""
(function(){
  document.querySelector('.tabbtn[data-tab="mod0"]').click();
  var cards = document.querySelectorAll("#panel-mod0 .section-card");
  window.__toeflShowPart.mod0(cards[2], { noScroll: true });
  Array.prototype.forEach.call(cards[2].querySelectorAll(".h3-body"), function(b){ b.classList.remove("h3-collapsed"); });
  var t = Array.prototype.filter.call(cards[2].querySelectorAll("table.t-cards"), function(x){ return /Design/.test(x.textContent); })[0];
  var wrap = t.parentNode, th = t.querySelector("th"), td = t.querySelector("tbody td");
  var o = { tags: cards[2].querySelectorAll(".tag-design.is-adaptive").length + "/" + cards[2].querySelectorAll(".tag-design.is-linear").length,
    note: !!cards[2].querySelector(".table-note") && !/107 e 13/.test(t.closest(".h3-body").querySelector("table").textContent),
    thCase: getComputedStyle(th).textTransform, thVisible: th.getBoundingClientRect().height > 0,
    tdBlock: getComputedStyle(td).display, label: getComputedStyle(td, "::before").content,
    fits: wrap.scrollWidth <= wrap.clientWidth + 1 && t.getBoundingClientRect().right <= document.documentElement.clientWidth + 1,
    font: parseFloat(getComputedStyle(td).fontSize) };
  window.__toeflShowPart.mod0(cards[0], { noScroll: true });
  return o;
})()
"""

# Balão de tradução (item 18): abre pelo foco e pelo toque, fecha com Esc,
# toque de novo e saída do foco; desligado em exercício ainda não respondido
# e pelo interruptor "Traduções".
TRANSLATE = r"""
(function(){
  var tip = document.getElementById("trTip"), spans = document.querySelectorAll("#panel-mod0 .tr[data-tr]");
  var o = { count: spans.length, marked: Array.prototype.every.call(spans, function(s){
    return s.getAttribute("lang") === "en" && s.dataset.tr && s.getAttribute("tabindex") === "0"; }) };
  var s = spans[0];
  document.querySelector('.tabbtn[data-tab="mod0"]').click();
  window.__toeflShowPart.mod0(s.closest(".section-card"), { noScroll: true });
  var body = s.closest(".h3-body"); if(body) body.classList.remove("h3-collapsed");
  s.focus();
  // Chrome sem janela em primeiro plano não dispara o evento de foco sozinho
  if(!document.hasFocus()) s.dispatchEvent(new FocusEvent("focusin", { bubbles: true }));
  o.focusOpens = !tip.hidden && tip.textContent === s.dataset.tr && s.getAttribute("aria-describedby") === "trTip";
  s.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  o.escCloses = tip.hidden;
  s.blur();
  s.dispatchEvent(new PointerEvent("pointerdown", { pointerType: "touch", bubbles: true }));
  s.click(); o.tapOpens = !tip.hidden;
  s.dispatchEvent(new PointerEvent("pointerdown", { pointerType: "touch", bubbles: true }));
  s.click(); o.tapAgainCloses = tip.hidden;
  s.click(); document.body.click(); o.outsideCloses = tip.hidden;
  // dentro de uma questão do diagnóstico ainda sem resposta: desligado
  var q = document.querySelector('.quiz-drill[data-drill="mod0-diag"] .qcard:not(:has(.verdict)) .qprompt');
  var fake = document.createElement("span"); fake.className = "tr"; fake.dataset.tr = "teste"; fake.lang = "en"; fake.textContent = "test";
  q.appendChild(fake); window.__toeflTr.refresh(); window.__toeflTr.show(fake);
  o.offInExercise = tip.hidden && fake.classList.contains("tr-off") && !fake.hasAttribute("tabindex");
  fake.remove();
  var t = document.getElementById("trToggle"); t.checked = false; t.dispatchEvent(new Event("change", { bubbles: true }));
  window.__toeflTr.show(s);
  o.switchOff = tip.hidden && s.classList.contains("tr-off") && localStorage.getItem("toefl_tr_v1") === "off";
  t.checked = true; t.dispatchEvent(new Event("change", { bubbles: true }));
  o.switchOn = !s.classList.contains("tr-off");
  return o;
})()
"""

SW_STATE = """(async function(){
  var reg = await navigator.serviceWorker.getRegistration();
  return { controller: !!navigator.serviceWorker.controller, waiting: !!(reg && reg.waiting),
    bar: !document.getElementById("pwaUpdate").hidden, marker: document.documentElement.getAttribute("data-smoke"),
    panels: document.querySelectorAll(".panel").length };
})()"""

MODS = ["mod%d" % i for i in range(10)]
RESET_KEYS = ["toefl_progress", "toefl_h3progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_errlog_", "toefl_ctw_",
              "toefl_spk_", "toefl_write_", "toefl_exam_", "toefl_scorecalc", "toefl_weeklydash", "toefl_goal"]


# Tela de apresentacao: o que esta na pagina, o que estoura na largura e o
# que ela NAO pode dizer (nada que nao de para provar).
LANDING_STATE = r"""
(function(){
  var over = [], small = [];
  Array.prototype.forEach.call(document.querySelectorAll("body *"), function(e){
    var r = e.getBoundingClientRect();
    if(r.width && r.right > innerWidth + 1) over.push(e.tagName + "." + e.className);
  });
  Array.prototype.forEach.call(document.querySelectorAll(".lp-btn, .opt, .lp-faq-item summary"), function(e){
    var r = e.getBoundingClientRect();
    if(r.height && r.height < 44) small.push(e.textContent.trim().slice(0, 30) + ":" + Math.round(r.height));
  });
  var text = document.body.textContent;
  // "Mais escolhido" (selo do plano de 90 dias) foi decisão do dono em 2026-10-18
  var banned = [/mais (vendido|popular)/i, /milhares|centenas de alunos|\d+ alunos/i, /aprova[çc][ãa]o garantida/i,
                /garant(imos|e) (a |sua |uma )?(nota|aprova)/i, /nota garantida/i, /melhor curso/i, /n[úu]mero 1|#1/i, /oficial da ETS\./i];
  return {
    h1: document.querySelectorAll("h1").length,
    sections: Array.prototype.map.call(document.querySelectorAll("section[id]"), function(s){ return s.id; }),
    qcards: document.querySelectorAll("#diagnostico .qcard").length,
    enter: document.querySelector(".lp-enter").getAttribute("href"),
    start: document.querySelector(".lp-top .lp-start").getAttribute("href"),
    heroMain: document.querySelector(".lp-hero .lp-btn-main").getAttribute("href"),
    logo: Math.round(document.querySelector(".lp-top .logo").getBoundingClientRect().height),
    navFont: parseFloat(getComputedStyle(document.querySelector(".lp-nav a")).fontSize),
    kicker: (function(){ var s = getComputedStyle(document.querySelector(".lp-kicker"));
      return { size: parseFloat(s.fontSize), straight: s.transform === "none" }; })(),
    video: !!document.getElementById("lpVideo"),
    legal: !!document.querySelector('.lp-foot a[href="termos.html"]') && !!document.querySelector('.lp-foot a[href="privacidade.html"]'),
    faq: document.querySelectorAll(".lp-faq-item").length,
    resultHidden: document.getElementById("lpResult").hidden,
    refund: /7 dias corridos/.test(document.querySelector(".lp-refund").textContent) && /artigo 49/.test(document.querySelector(".lp-refund").textContent),
    plans: Array.prototype.map.call(document.querySelectorAll(".lp-plan"), function(p){
      var b = p.querySelector(".plan-badge");
      return { id: p.dataset.plan, price: p.querySelector(".lp-plan-price").textContent, badge: b ? b.textContent : "",
               note: p.querySelector(".lp-plan-note").textContent,
               top: Math.round(p.getBoundingClientRect().top + scrollY) };
    }),
    claims: banned.filter(function(re){ return re.test(text); }).map(String),
    docW: document.documentElement.scrollWidth, vw: innerWidth, over: over.slice(0, 6), smallTargets: small.slice(0, 6)
  };
})()
"""

# Tela de login aberta numa tela baixa: o cartão é mais alto que a janela, a
# tela rola até o fim e o título fica visível no começo (nada cortado em cima).
GATE_SCROLL = r"""
(function(){
  var g = document.getElementById("authGate");
  g.hidden = false;
  g.scrollTop = 0;
  function inView(el){ var r = el.getBoundingClientRect(); return r.height > 0 && r.top >= 0 && r.bottom <= innerHeight + 1; }
  var card = g.querySelector(".auth-gate-card");
  var o = { tall: card.getBoundingClientRect().height > innerHeight, topIn: inView(document.getElementById("authGateTitle")) };
  var google = document.getElementById("authSignInGoogle");
  var terms = g.querySelector('.legal-links a[href="termos.html"]');
  google.scrollIntoView({ block: "nearest" });
  o.googleIn = inView(google);
  terms.scrollIntoView({ block: "nearest" });
  o.termsIn = inView(terms);
  o.scrolled = g.scrollTop > 0;
  g.hidden = true;
  return o;
})()
"""

LANDING_ANSWER = r"""
(function(){
  Array.prototype.forEach.call(document.querySelectorAll("#diagnostico .qcard"), function(c, k){
    var want = k < 7 ? c.dataset.correct : ["A","B","C","D"].filter(function(L){ return L !== c.dataset.correct; })[0];
    c.querySelector('.opt[data-letter="' + want + '"]').click(); c.querySelector(".qconfirm").click();
  });
  var r = document.getElementById("lpResult");
  return { hidden: r.hidden, text: r.textContent.replace(/\s+/g, " ").trim(),
    verdicts: document.querySelectorAll("#diagnostico .verdict").length,
    saved: Object.keys(JSON.parse(localStorage.getItem("toefl_quiz_mod0-diag_v1") || "{}")).length };
})()
"""


# Teste de unidade do webhook do Stripe (supabase/functions/_shared/stripe.js),
# numa página servida por http://127.0.0.1 (o crypto.subtle só existe em
# contexto seguro). As assinaturas boas são calculadas aqui em Python, com
# hmac, e não pelo próprio código testado. O fluxo usa uma API do Stripe e um
# banco de mentira; o banco imita a regra de recompute_entitlement() da
# migração 20261018_stripe.sql (o SQL em si não roda aqui).
STRIPE_TEST = r"""
(async function(P){
  var out = {};
  var DAY = 86400000, NOW = P.now * 1000;
  var V = stripeVerifySignature;
  out.sig_good = await V(P.payload, P.goodHeader, P.secret, P.now);
  out.sig_bad = await V(P.payload, P.badHeader, P.secret, P.now);
  out.sig_tampered = await V(P.payload.replace("invoice.paid", "invoice.paiD"), P.goodHeader, P.secret, P.now);
  out.sig_wrong_secret = await V(P.payload, P.goodHeader, P.secret + "x", P.now);
  out.sig_old = await V(P.payload, P.oldHeader, P.secret, P.now);
  out.sig_empty = await V(P.payload, "", P.secret, P.now);
  out.sig_no_secret = await V(P.payload, P.goodHeader, "", P.now);

  // ---- banco de mentira: payments + billing, com a regra do SQL ----
  var payments = {}, billing = {}, canceled = [];
  function entitlement(user){
    var rows = Object.keys(payments).map(function(k){ return payments[k]; })
      .filter(function(r){ return r.user === user && r.status === "approved"; })
      .sort(function(a, b){ return a.approvedAt < b.approvedAt ? -1 : a.approvedAt > b.approvedAt ? 1 : 0; });
    if(!rows.length) return { paid: false, expires_at: null };
    var life = false, exp = null, subLast = false;
    rows.forEach(function(r){
      if(r.days == null){ life = true; return; }
      if(life) return;
      var base = Math.max(exp == null ? Date.parse(r.approvedAt) : exp, Date.parse(r.approvedAt));
      exp = base + r.days * DAY;
      subLast = r.periodEnd != null;
    });
    return { paid: true, expires_at: life ? null : new Date(exp + (subLast ? DAY : 0)).toISOString() };
  }
  function active(row){ return row.paid && (!row.expires_at || Date.parse(row.expires_at) > NOW); }
  var api = {};
  var deps = {
    get: function(path){ if(!api[path]) throw new Error("sem objeto " + path); return Promise.resolve(JSON.parse(JSON.stringify(api[path]))); },
    cancelSubscription: function(id){ canceled.push(id); return Promise.resolve(); },
    now: function(){ return new Date(NOW).toISOString(); },
    plan: function(id){ return { mensal: { id: "mensal", interval: "month", days: null }, "60dias": { id: "60dias", interval: null, days: 60 },
                                 "90dias": { id: "90dias", interval: null, days: 90 }, anual: { id: "anual", interval: null, days: 365 } }[id] || null; },
    findBilling: function(u){ return Promise.resolve(billing[u] ? { subscription_id: billing[u].subscription, subscription_status: billing[u].status } : null); },
    applyPayment: function(a){
      if(a.status === "approved"){ if(!payments[a.id]) payments[a.id] = JSON.parse(JSON.stringify(a)); }
      else if(payments[a.id]) payments[a.id].status = "refunded";
      return Promise.resolve();
    },
    applyBilling: function(a){
      var b = billing[a.user] || {};
      ["customer", "subscription", "status", "periodEnd"].forEach(function(k){ if(a[k] != null) b[k] = a[k]; });
      if(a.cancelAtPeriodEnd != null) b.cancel = a.cancelAtPeriodEnd;
      billing[a.user] = b;
      return Promise.resolve();
    }
  };
  function ev(type, id){ return { id: "evt_" + Math.random(), type: type, created: P.now, data: { object: { id: id } } }; }
  var U1 = "11111111-1111-4111-8111-111111111111", U2 = "22222222-2222-4222-8222-222222222222";
  var end1 = P.now + 30 * 86400;

  // ---- Mensal: checkout de assinatura, depois o invoice.paid repetido ----
  api["/v1/checkout/sessions/cs_m"] = { id: "cs_m", mode: "subscription", client_reference_id: U1, customer: "cus_1", subscription: "sub_1", metadata: { user_id: U1, plan_id: "mensal" } };
  api["/v1/subscriptions/sub_1"] = { id: "sub_1", status: "active", customer: "cus_1", cancel_at_period_end: false, current_period_end: end1, latest_invoice: "in_1", metadata: { user_id: U1, plan_id: "mensal" } };
  api["/v1/invoices/in_1"] = { id: "in_1", status: "paid", subscription: "sub_1", customer: "cus_1", amount_paid: 2990, status_transitions: { paid_at: P.now }, lines: { data: [{ period: { start: P.now, end: end1 } }] } };
  out.free_before = !active(entitlement(U1));
  await stripeHandleEvent(ev("checkout.session.completed", "cs_m"), deps);
  var e1 = entitlement(U1);
  out.monthly_grants = active(e1) && e1.expires_at === new Date((end1 * 1000) + DAY).toISOString() &&
    payments["stripe:in_1"].plan === "mensal" && payments["stripe:in_1"].amount === 29.9 && payments["stripe:in_1"].days === 30 &&
    billing[U1].status === "active" && billing[U1].customer === "cus_1" && billing[U1].subscription === "sub_1";
  await stripeHandleEvent(ev("invoice.paid", "in_1"), deps);
  await stripeHandleEvent(ev("invoice.paid", "in_1"), deps);
  out.monthly_idempotent = Object.keys(payments).length === 1 && entitlement(U1).expires_at === e1.expires_at;
  // o mês seguinte: fatura nova estende até o novo fim de período
  var end2 = end1 + 30 * 86400;
  api["/v1/invoices/in_2"] = { id: "in_2", status: "paid", subscription: "sub_1", amount_paid: 2990, lines: { data: [{ period: { start: end1, end: end2 } }] } };
  await stripeHandleEvent(ev("invoice.paid", "in_2"), deps);
  out.monthly_renews = entitlement(U1).expires_at === new Date(end2 * 1000 + DAY).toISOString();
  // fatura ainda não paga não dá acesso
  api["/v1/invoices/in_open"] = { id: "in_open", status: "open", subscription: "sub_1", amount_paid: 0, lines: { data: [] } };
  await stripeHandleEvent(ev("invoice.paid", "in_open"), deps);
  out.monthly_unpaid_ignored = !payments["stripe:in_open"];
  // cancelamento marcado para o fim do mês: o acesso fica
  api["/v1/subscriptions/sub_1"].cancel_at_period_end = true;
  await stripeHandleEvent(ev("customer.subscription.updated", "sub_1"), deps);
  out.monthly_cancel_keeps_access = billing[U1].cancel === true && active(entitlement(U1));
  // recusa de cobrança: só a situação muda
  api["/v1/subscriptions/sub_1"].status = "past_due";
  await stripeHandleEvent(ev("invoice.payment_failed", "in_open"), deps);
  out.monthly_failed_marks_past_due = billing[U1].status === "past_due" && active(entitlement(U1));
  // reembolso parcial não tira; total tira o mês e cancela a assinatura
  api["/v1/charges/ch_p"] = { id: "ch_p", refunded: false, invoice: "in_2", payment_intent: "pi_in2" };
  await stripeHandleEvent(ev("charge.refunded", "ch_p"), deps);
  out.refund_partial_keeps = payments["stripe:in_2"].status === "approved" && canceled.length === 0;
  api["/v1/charges/ch_2"] = { id: "ch_2", refunded: true, invoice: "in_2", payment_intent: "pi_in2" };
  await stripeHandleEvent(ev("charge.refunded", "ch_2"), deps);
  out.refund_total_revokes_month = payments["stripe:in_2"].status === "refunded" &&
    entitlement(U1).expires_at === e1.expires_at && canceled.join() === "sub_1";

  // ---- planos de dias (pagamento único): liberam e somam ao fim do acesso ----
  api["/v1/checkout/sessions/cs_v"] = { id: "cs_v", mode: "payment", payment_status: "paid", client_reference_id: U2, customer: "cus_2", payment_intent: "pi_v", amount_total: 5990, metadata: { user_id: U2, plan_id: "90dias" } };
  await stripeHandleEvent(ev("checkout.session.completed", "cs_v"), deps);
  await stripeHandleEvent(ev("checkout.session.completed", "cs_v"), deps);
  var e2 = entitlement(U2);
  out.days_plan_grants = active(e2) && e2.expires_at === new Date(NOW + 90 * DAY).toISOString() && payments["stripe:pi_v"].plan === "90dias" &&
    payments["stripe:pi_v"].days === 90 && payments["stripe:pi_v"].amount === 59.9 &&
    Object.keys(payments).filter(function(k){ return payments[k].user === U2; }).length === 1;
  // comprar outro plano com o acesso valendo soma os dias (90 + 60)
  api["/v1/checkout/sessions/cs_v2"] = { id: "cs_v2", mode: "payment", payment_status: "paid", client_reference_id: U2, payment_intent: "pi_v2", amount_total: 4990, metadata: { user_id: U2, plan_id: "60dias" } };
  await stripeHandleEvent(ev("checkout.session.completed", "cs_v2"), deps);
  out.days_plans_add_up = entitlement(U2).expires_at === new Date(NOW + 150 * DAY).toISOString();
  // a conta do Mensal (30 dias pagos) compra o Anual: 30 + 365, sem perder o mês
  api["/v1/checkout/sessions/cs_a"] = { id: "cs_a", mode: "payment", payment_status: "paid", client_reference_id: U1, payment_intent: "pi_a", amount_total: 12990, metadata: { user_id: U1, plan_id: "anual" } };
  await stripeHandleEvent(ev("checkout.session.completed", "cs_a"), deps);
  out.days_plan_adds_to_monthly = entitlement(U1).expires_at === new Date(NOW + 395 * DAY).toISOString() && canceled.join() === "sub_1";
  // aviso atrasado da assinatura velha não apaga a situação da conta
  api["/v1/subscriptions/sub_old"] = { id: "sub_old", status: "canceled", metadata: { user_id: U2 } };
  billing[U2] = { subscription: "sub_new", status: "active" };
  await stripeHandleEvent(ev("customer.subscription.deleted", "sub_old"), deps);
  out.old_subscription_does_not_overwrite = billing[U2].subscription === "sub_new" && billing[U2].status === "active";
  // reembolso de uma compra tira só os dias dela (sobram os 60 da outra)
  api["/v1/charges/ch_v"] = { id: "ch_v", refunded: true, invoice: null, payment_intent: "pi_v" };
  await stripeHandleEvent(ev("charge.refunded", "ch_v"), deps);
  out.days_refund_removes_only_that_purchase = entitlement(U2).expires_at === new Date(NOW + 60 * DAY).toISOString();

  // ---- o que não pode liberar nada ----
  var before = Object.keys(payments).length;
  api["/v1/checkout/sessions/cs_unpaid"] = { id: "cs_unpaid", mode: "payment", payment_status: "unpaid", client_reference_id: U2, payment_intent: "pi_u", metadata: { plan_id: "60dias" } };
  api["/v1/checkout/sessions/cs_nouser"] = { id: "cs_nouser", mode: "payment", payment_status: "paid", client_reference_id: "nao-e-uuid", payment_intent: "pi_n", metadata: { plan_id: "60dias" } };
  api["/v1/checkout/sessions/cs_wrongplan"] = { id: "cs_wrongplan", mode: "payment", payment_status: "paid", client_reference_id: U2, payment_intent: "pi_w", metadata: { plan_id: "mensal" } };
  await stripeHandleEvent(ev("checkout.session.completed", "cs_unpaid"), deps);
  await stripeHandleEvent(ev("checkout.session.completed", "cs_nouser"), deps);
  await stripeHandleEvent(ev("checkout.session.completed", "cs_wrongplan"), deps);
  out.bad_checkouts_grant_nothing = Object.keys(payments).length === before;
  return out;
})(%s)
"""


def _stripe_params():
    """Corpo de evento e cabeçalhos Stripe-Signature (bom, ruim e velho)."""
    secret = "whsec_teste_" + os.urandom(8).hex()
    now = int(time.time())
    payload = json.dumps({"id": "evt_1", "type": "invoice.paid", "data": {"object": {"id": "in_1"}}})

    def sig(t):
        return hmac.new(secret.encode(), f"{t}.{payload}".encode(), hashlib.sha256).hexdigest()
    return {
        "secret": secret, "now": now, "payload": payload,
        "goodHeader": f"t={now},v1={sig(now)}",
        "badHeader": f"t={now},v1={'0' * 64}",
        "oldHeader": f"t={now - 1000},v1={sig(now - 1000)}",
    }


def _write_stripe_page(site):
    src = (ROOT / "supabase" / "functions" / "_shared" / "stripe.js").read_text(encoding="utf-8")
    src = re.sub(r"^export ", "", src, flags=re.M)
    (site / "stripe_test.html").write_text(f'<!DOCTYPE html><html><head><link rel="icon" href="data:,"></head><body><script>\n{src}\n</script></body></html>',
                                           encoding="utf-8")


def run():
    """Devolve (resultados, detalhes): nome -> bool, e nome -> texto do que falhou."""
    out, why = {}, {}

    def check(name, ok, detail=""):
        out[name] = bool(ok)
        if not ok and detail:
            why[name] = str(detail)[:300]

    with tempfile.TemporaryDirectory(prefix="itoefl_real_") as tmp:
        site = build_teste.build(Path(tmp) / "site")

        # o build de teste tem que sair instalavel: manifesto, service worker
        # e todo arquivo que o service worker guarda
        sw_src = (site / "sw.js").read_text(encoding="utf-8") if (site / "sw.js").exists() else ""
        block = re.search(r"var PRECACHE = \[(.*?)\];", sw_src, re.S)
        urls = re.findall(r'"\./([^"]+)"', block.group(1)) if block else []
        missing = [u for u in urls + ["manifest.json", "sw.js"] if not (site / u).exists()]
        check("teste_build_is_installable", urls and not missing, f"faltando em _teste: {missing}")

        _write_stripe_page(site)
        srv, base = _serve(site)
        page = base + "/index.html"
        try:
            # webhook do Stripe: assinatura e fluxo de cada evento
            with Browser() as b:
                b.goto(base + "/stripe_test.html", settle=0.3)
                s = b.eval(STRIPE_TEST % json.dumps(_stripe_params()))
                s = s if isinstance(s, dict) else {}
                check("stripe_webhook_accepts_valid_signature", s.get("sig_good") is True, s)
                check("stripe_webhook_rejects_invalid_signature",
                      s and not any(s.get(k) for k in ("sig_bad", "sig_tampered", "sig_wrong_secret", "sig_old",
                                                       "sig_empty", "sig_no_secret")), s)
                check("stripe_flow_monthly_grants_access", s.get("free_before") and s.get("monthly_grants")
                      and s.get("monthly_renews") and s.get("monthly_unpaid_ignored"), s)
                check("stripe_flow_monthly_cancel_and_failure_keep_paid_month",
                      s.get("monthly_cancel_keeps_access") and s.get("monthly_failed_marks_past_due"), s)
                check("stripe_flow_days_plans_grant_access", s.get("days_plan_grants"), s)
                check("stripe_flow_purchases_add_days", s.get("days_plans_add_up") and s.get("days_plan_adds_to_monthly"), s)
                check("stripe_flow_idempotent", s.get("monthly_idempotent") and s.get("days_plan_grants"), s)
                check("stripe_flow_refund_revokes", s.get("refund_partial_keeps") and s.get("refund_total_revokes_month")
                      and s.get("days_refund_removes_only_that_purchase"), s)
                check("stripe_flow_rejects_bad_input", s.get("bad_checkouts_grant_nothing")
                      and s.get("old_subscription_does_not_overwrite"), s)
                check("stripe_test_no_js_errors", not b.errors, b.errors)

            with Browser() as b:
                b.goto(page, settle=0.5)
                b.eval('localStorage.setItem("toefl_theme_v1", "light")')
                b.reload(settle=1.2)
                check("real_no_js_errors_on_load", not b.errors, b.errors)
                # abrir o site nao e estudar: nada de sequencia, meta ou
                # alteracao pendente de sincronizacao so pela carga da pagina
                idle = b.eval('Object.keys(localStorage).filter(function(k){ return /^toefl_(streak|dailygoal|dirty|scorecalc)/.test(k); })')
                check("real_opening_the_site_marks_nothing", not idle, idle)
                head = b.eval(HEADER)
                check("header_no_overlap_desktop", all(head.values()), head)
                rd = b.eval(READING)
                check("reading_text_about_70_chars_per_line", 55 <= rd["cpl"] <= 80, rd)
                check("part_rail_desktop_column",
                      rd["railRight"] and rd["sticky"] and rd["bodyShown"] and rd["items"] == rd["h3"] > 0
                      and rd["doneWorks"] and not rd["markDoneVisible"], rd)
                check("subsection_read_check_when_closed",
                      rd["checkClosed"] and rd["railCheck"] and rd["count"].startswith("1 de ") and rd["arrowNear"], rd)
                check("pager_says_next_part_and_titles_in_sentence_case",
                      rd["pager"].startswith("Próxima Parte: ") and rd["bottom"].startswith("Próxima Parte: ")
                      and rd["sentence"] == "Parte 2: O atlas linguístico", rd)
                tr = b.eval(TRANSLATE)
                check("translation_balloon_opens_closes_and_is_off_in_exercises",
                      tr.pop("count") >= 5 and all(tr.values()), tr)
                co = b.eval(CALLOUTS)
                check("callouts_seven_types", all(co.values()), co)
                tb = b.eval(TABLES)
                check("tables_light_with_design_tags_and_footnote",
                      tb["tags"] == "3/3" and tb["note"] and tb["thCase"] == "none" and tb["thVisible"] and tb["tdBlock"] != "block", tb)
                b.eval('document.querySelector(\'.tabbtn[data-tab="mod0"]\').click()')
                b.reload(settle=1.2)

                # o diagnostico e a Parte 1 do M0: aluno novo cai nele, sem o
                # cartao "Comece aqui" por cima; em outra Parte do M0 o cartao
                # aparece e o botao leva de volta ao diagnostico
                start = b.eval(r"""(function(){
                  var c = document.getElementById("startCard");
                  var diagCard = document.querySelector('.quiz-drill[data-drill="mod0-diag"]').closest(".section-card");
                  var o = { firstIsDiag: !diagCard.hidden && document.getElementById("jtPart").textContent === "Parte 1 de 9",
                            hiddenOverDiag: c.hidden };
                  document.querySelector("#panel-mod0 .part-next").click();
                  o.shown = !c.hidden; o.go = c.querySelector(".start-go").textContent;
                  o.beforePager = c.nextElementSibling.classList.contains("part-pager");
                  c.querySelector(".start-go").click();
                  o.partOpen = !diagCard.hidden && document.getElementById("jtPart").textContent === "Parte 1 de 9" && c.hidden;
                  return o;
                })()""")
                check("real_diagnostic_is_part_1_without_start_card", start["firstIsDiag"] and start["hiddenOverDiag"], start)
                check("real_start_card_leads_to_diagnostic",
                      start["shown"] and start["go"] == "Fazer o diagnóstico agora" and start["beforePager"] and start["partOpen"], start)

                # diagnostico: 3 respostas confirmadas, nenhuma corrigida ainda
                pend = b.eval(r"""(function(){
                  var d = document.querySelector('.quiz-drill[data-drill="mod0-diag"]');
                  Array.prototype.slice.call(d.querySelectorAll(".qcard"), 0, 3).forEach(function(c){
                    c.querySelector('.opt[data-letter="' + c.dataset.correct + '"]').click(); c.querySelector(".qconfirm").click();
                  });
                  return { verdicts: d.querySelectorAll(".verdict").length, marked: d.querySelectorAll(".opt.correct, .opt.wrong").length,
                    explained: Array.prototype.filter.call(d.querySelectorAll(".qfeedback"), function(f){ return !f.hidden; }).length,
                    pending: d.querySelectorAll(".qpending").length, result: document.getElementById("diagResult").hidden };
                })()""")
                check("real_diagnostic_hides_key_until_the_end",
                      pend == {"verdicts": 0, "marked": 0, "explained": 0, "pending": 3, "result": True}, pend)

                failed = b.eval(ACT)
                # 7 de 10: resultado no lugar, com áreas, fortes e a melhorar
                res = b.eval(r"""(function(){
                  var d = document.querySelector('.quiz-drill[data-drill="mod0-diag"]'), r = document.getElementById("diagResult");
                  return { hidden: r.hidden, title: document.getElementById("diagResultTitle").textContent,
                    score: document.getElementById("diagScore").textContent, areas: r.querySelectorAll(".diag-area").length,
                    strong: document.getElementById("diagStrong").children.length, weak: document.getElementById("diagWeak").children.length,
                    verdicts: d.querySelectorAll(".verdict").length, pending: d.querySelectorAll(".qpending").length,
                    afterQuiz: !!(d.compareDocumentPosition(r) & Node.DOCUMENT_POSITION_FOLLOWING),
                    targets: document.querySelectorAll("#goalTarget option").length };
                })()""")
                check("real_diagnostic_result_screen",
                      not res["hidden"] and "B2" in res["title"] and "banda 4 a 4,5" in res["title"]
                      and res["score"].startswith("Você acertou 7 de 10.") and res["areas"] == 6 and res["strong"] >= 1
                      and res["weak"] >= 1 and res["verdicts"] == 10 and res["pending"] == 0 and res["afterQuiz"]
                      and res["targets"] == 12, res)
                goal = b.eval(r"""(function(){
                  function day(n){ var d = new Date(); d.setDate(d.getDate() + n); var p = function(x){ return (x < 10 ? "0" : "") + x; };
                    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()); }
                  var out = {};
                  document.getElementById("goalTarget").value = "5"; document.getElementById("goalDate").value = day(45);
                  document.getElementById("goalSave").click();
                  out.gap = document.getElementById("diagPlanGap").textContent; out.sched = document.getElementById("diagPlanSched").textContent;
                  out.saved = JSON.parse(localStorage.getItem("toefl_goal_v1"));
                  out.today = day(0);
                  document.getElementById("goalTarget").value = "6"; document.getElementById("goalDate").value = day(20);
                  document.getElementById("goalSave").click();
                  out.sched2 = document.getElementById("diagPlanSched").textContent;
                  document.getElementById("goalTarget").value = "5"; document.getElementById("goalDate").value = day(45);
                  document.getElementById("goalSave").click();
                  out.badge = document.getElementById("levelBadgeSched").textContent;
                  return out;
                })()""")
                check("real_goal_gives_distance_and_schedule",
                      "Você está em B2 (banda 4 a 4,5) e precisa de C1 (banda 5)." in goal["gap"] and "Faltam 45 dias" in goal["gap"]
                      and goal["sched"].startswith("Cronograma indicado: Intensivo, de 30 dias (Parte 6.1)")
                      and goal["saved"]["target"] == 5 and goal["saved"]["sched"] == 30 and goal["saved"]["start"] == goal["today"]
                      and goal["badge"].startswith("Cronograma Intensivo (30 dias)")
                      and "Plano de Emergência" in goal["sched2"], goal)
                # meta de hoje tirada do cronograma (Intensivo, 45 dias até a
                # prova): Partes de M0/M1 com minutos, prova e nível x meta
                today = b.eval(r"""(function(){
                  var o = { text: document.getElementById("todayText").textContent, meta: document.getElementById("todayMeta").textContent,
                            side: document.getElementById("dgText").textContent, next: document.getElementById("dgNext").textContent };
                  // 12 dias atrás no mesmo cronograma: a meta cresce com as atrasadas
                  var g = JSON.parse(localStorage.getItem("toefl_goal_v1"));
                  var d = new Date(); d.setDate(d.getDate() - 12); var p = function(x){ return (x < 10 ? "0" : "") + x; };
                  g.start = d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
                  localStorage.setItem("toefl_goal_v1", JSON.stringify(g));
                  window.__toeflRefreshPlan();
                  o.lateText = document.getElementById("todayText").textContent; o.lateNext = document.getElementById("dgNext").textContent;
                  o.lateItems = window.__toeflToday().items.length;
                  // volta ao plano de hoje
                  g.start = %s;
                  localStorage.setItem("toefl_goal_v1", JSON.stringify(g));
                  window.__toeflRefreshPlan();
                  document.getElementById("todayGo").click();
                  o.went = document.querySelector(".tabbtn.active").dataset.tab;
                  return o;
                })()""" % json.dumps(goal["today"]))
                check("real_today_goal_follows_schedule",
                      re.match(r"^Hoje: M[01] Parte \d", today["text"]) and re.search(r"\(\d+ min\)$", today["text"])
                      and not re.search(r"M0 Parte 1\b", today["text"])
                      and today["side"] == today["text"] and "Prova em 45 dias. Você: B2. Meta: C1 (banda 5)." in today["meta"]
                      and today["next"].startswith("Depois: ") and today["lateItems"] > 1 and "atrás do cronograma" in today["lateNext"]
                      and today["went"] in ("mod0", "mod1"), today)
                b.pump(1.2)  # a caixa de escrita salva com atraso
                start2 = b.eval('({ title: document.querySelector("#startCard .start-title").textContent,'
                                ' go: document.querySelector("#startCard .start-go").textContent })')
                b.eval('document.querySelector("#startCard .start-skip").click()')
                check("real_start_card_follows_diagnostic_and_dismisses",
                      "nível estimado B2" in start2["title"] and start2["go"] == "Ver o meu cronograma"
                      and b.eval('document.getElementById("startCard").hidden && localStorage.getItem("toefl_welcome_v1") === "1"'), start2)
                check("real_every_widget_responds", not failed, failed)
                before = b.eval(SNAP)
                check("real_mark_done_text_is_clickable", before["parte"] is True)
                check("real_band_label_uses_comma", "4–4,5" in (before["nivel"] or ""), before["nivel"])
                check("real_errlog_shows_typed_text_not_html", b.eval(
                    '(function(){ var c = document.querySelector(\'.errlog[data-errlog="mod1"] .errlog-entry-drill\');'
                    ' return !!c && c.textContent === "Drill <b>A1</b> & teste" && c.children.length === 0; })()'))
                check("real_no_mailto_links", b.eval('document.querySelectorAll(\'a[href^="mailto:"]\').length === 0'))

                # devolutiva em palavras, nao so em cor: questao errada do M1
                # (etiquetas e frase com as duas letras), questao certa do
                # diagnostico, bloco de simulado entregue e o que ainda falta
                fb = b.eval(r"""(function(){
                  function tags(card, sel){ return Array.prototype.map.call(card.querySelectorAll(sel + " .otag"), function(t){ return t.textContent; }).sort().join("|"); }
                  var wrong = document.querySelector("#panel-mod1 .opt.wrong").closest(".qcard");
                  var right = document.querySelector('.quiz-drill[data-drill="mod0-diag"] .qcard');
                  var v = wrong.querySelector(".verdict"), letters = (v.textContent.match(/\([A-F]\)/g) || []);
                  var ex = document.querySelectorAll(".exam");
                  return { wrongTags: tags(wrong, ".opt"), wrongVerdict: v.textContent, role: v.getAttribute("role"),
                    lettersMatch: letters.length === 2 &&
                      letters[0] === "(" + wrong.querySelector(".opt.wrong .oletter").textContent + ")" &&
                      letters[1] === "(" + wrong.querySelector(".opt.correct .oletter").textContent + ")",
                    rightTags: tags(right, ".opt"), rightVerdict: right.querySelector(".verdict").textContent,
                    examVerdicts: ex[0].querySelectorAll(".verdict.verdict-ok").length === ex[0].querySelectorAll(".exam-item").length,
                    examTags: ex[0].querySelectorAll(".otag-ok").length === ex[0].querySelectorAll(".exam-item").length,
                    openTags: ex[1].querySelectorAll(".otag, .verdict").length, left: ex[1].querySelector(".exam-left").textContent,
                    pressed: ex[1].querySelectorAll('.exam-opt[aria-pressed="true"]').length };
                })()""")
                check("real_feedback_says_right_or_wrong_in_words",
                      fb["wrongTags"] == "correta|sua resposta" and fb["wrongVerdict"].startswith("✗ Quase. Você marcou") and fb["lettersMatch"]
                      and fb["role"] == "status" and fb["rightTags"] == "sua resposta, correta" and fb["rightVerdict"] == "✓ Você acertou."
                      and fb["examVerdicts"] and fb["examTags"], fb)
                check("real_exam_shows_how_many_left", fb["openTags"] == 0 and fb["left"].startswith("Falta") and fb["pressed"] == 1, fb)
                small = b.eval('document.getElementById("liveScoreWritingBand").textContent')
                check("real_no_band_from_tiny_sample", small.startswith("Amostra pequena") and "Banda" not in small, small)

                # a data da meta e da sequencia e a do aparelho, nao a de UTC:
                # com o toISOString trocado, quem depender dele grava 1999
                dates = b.eval(
                    '(function(){ var real = Date.prototype.toISOString;'
                    ' Date.prototype.toISOString = function(){ return "1999-01-01T00:00:00.000Z"; };'
                    ' localStorage.removeItem("toefl_streak_v1"); localStorage.removeItem("toefl_dailygoal_v1");'
                    ' var c = document.querySelectorAll("#panel-mod0 .pchk")[1]; c.checked = true; c.dispatchEvent(new Event("change", { bubbles: true }));'
                    ' Date.prototype.toISOString = real;'
                    ' var d = new Date(), p = function(n){ return (n < 10 ? "0" : "") + n; };'
                    ' var local = d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());'
                    ' return { local: local, goal: JSON.parse(localStorage.getItem("toefl_dailygoal_v1")).date,'
                    '          streak: Object.keys(JSON.parse(localStorage.getItem("toefl_streak_v1")).days) }; })()')
                check("real_streak_and_goal_use_local_date",
                      dates["goal"] == dates["local"] and dates["streak"] == [dates["local"]], dates)

                # painel: abre com os dados acima e a meta em frase legivel
                dash = b.eval(
                    '(function(){ document.getElementById("authBox").hidden = false; document.getElementById("authIn").hidden = false;'
                    ' document.getElementById("dashboardBtn").click();'
                    ' var o = { goal: document.getElementById("dashGoalText").textContent, weak: document.getElementById("dashWeakSpots").textContent,'
                    '           band: document.getElementById("dashBand").textContent };'
                    ' document.getElementById("dashboardClose").click(); return o; })()')
                check("real_dashboard_reads_progress",
                      (dash["goal"].startswith("Hoje: ") or "Meta batida" in dash["goal"]) and "/1" not in dash["goal"]
                      and "R1" in dash["weak"] and "B2" in dash["band"], dash)

                # teclado: Enter no titulo de uma subsecao abre e fecha; a
                # janela do painel recebe o foco, fecha com Esc e devolve o foco
                kb = b.eval(r"""(function(){
                  document.querySelector('.tabbtn[data-tab="mod5"]').click();
                  var h = document.querySelectorAll("#panel-mod5 .section-card:not([hidden]) h3.h3-toggle")[1], btn = h.querySelector(".h3-btn");
                  var was = h.classList.contains("collapsed");
                  btn.focus();
                  var focused = document.activeElement === btn;
                  btn.click();   // Enter e Espaco num <button> viram click
                  var o = { focused: focused, toggled: h.classList.contains("collapsed") !== was };
                  return new Promise(function(res){ setTimeout(function(){
                    o.aria = btn.getAttribute("aria-expanded") === (h.classList.contains("collapsed") ? "false" : "true");
                    var opener = document.getElementById("dashboardBtn"); opener.focus(); opener.click();
                    setTimeout(function(){
                      var m = document.getElementById("dashboardModal");
                      o.focusIn = m.contains(document.activeElement);
                      m.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
                      setTimeout(function(){ o.closed = m.hidden; o.focusBack = document.activeElement === opener; res(o); }, 60);
                    }, 60);
                  }, 60); });
                })()""")
                check("real_keyboard_opens_subsections_and_dialogs",
                      all(kb.get(k) for k in ("focused", "toggled", "aria", "focusIn", "closed", "focusBack")), kb)

                # "continuar de onde parei" sem o ✓ da subsecao concluida
                b.eval('(function(){ var h = document.querySelector("#panel-mod0 h3.h3-done");'
                       ' localStorage.setItem("toefl_lastpos_v1", JSON.stringify({ mod: "mod0", id: h.id, title: h.textContent.trim() })); })()')
                before = b.eval(SNAP)
                b.reload(settle=1.2)
                after = b.eval(SNAP)
                diff = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
                check("real_progress_survives_reload", not diff, diff)
                label = b.eval('document.getElementById("resumeBtn").hidden ? null : document.getElementById("resumeLabel").textContent')
                check("real_resume_label_has_no_checkmark", bool(label) and "✓" not in label, label)
                check("real_start_card_stays_dismissed", b.eval('document.getElementById("startCard").hidden'))

                # gaveta: uma lista só dos 10 módulos, cada um com o progresso
                # (item 27; o "mapa do curso" repetia a lista)
                b.eval('document.getElementById("sideToggle").click()')
                b.pump(0.4)
                side = b.eval(r"""(function(){
                  var s = document.getElementById("sideRail"), tabs = s.querySelectorAll(".tabbtn");
                  return { lists: s.querySelectorAll(".modnav, .jtrack").length, tabs: tabs.length,
                    bars: s.querySelectorAll(".tabbtn .tab-bar-fill").length,
                    pct: Array.prototype.every.call(tabs, function(t){ return /\d+%/.test(t.querySelector(".pbadge").textContent); }),
                    visible: tabs[9].getBoundingClientRect().height > 0,
                    settingsClosed: !document.getElementById("sideSettings").open };
                })()""")
                check("sidebar_single_module_list_with_progress",
                      side == {"lists": 1, "tabs": 10, "bars": 10, "pct": True, "visible": True, "settingsClosed": True}, side)
                # texto de sincronização: logado, "Sincronizado na sua conta"
                sync = b.eval(r"""(function(){
                  var el = document.getElementById("syncNote"), o = { off: el.textContent };
                  window.__toeflSyncNote(true); o.on = el.textContent; window.__toeflSyncNote(false);
                  o.keys = ["toefl_goal_v1", "toefl_quiz_mod0-diag_v1", "toefl_dailygoal_v1", "toefl_streak_v1", "toefl_progress_v1",
                            "toefl_h3progress_v1"].every(window.__toeflIsSynced);
                  return o;
                })()""")
                check("sidebar_sync_text_for_logged_in",
                      sync["off"] == "Seu progresso é salvo neste navegador." and sync["on"].startswith("Sincronizado na sua conta")
                      and sync["keys"], sync)
                b.eval('document.getElementById("sideClose").click()')

                # reiniciar: só depois da segunda confirmação (item 28); apaga
                # todo o progresso e recarrega
                pid = b.eval('document.querySelector("#panel-mod0 .pchk").dataset.pid')
                steps = b.eval(r"""(function(){
                  function kept(){ return localStorage.getItem("toefl_progress_v1") !== null; }
                  document.getElementById("sideSettings").open = true;
                  var o = {};
                  document.getElementById("resetBtn").click(); o.first = kept() && !document.getElementById("resetConfirm").hidden;
                  document.getElementById("resetCancel").click(); o.cancel = kept() && document.getElementById("resetConfirm").hidden;
                  document.getElementById("resetBtn").click(); document.getElementById("resetYes").click();
                  o.second = kept() && document.getElementById("resetYes").textContent === "Apagar tudo agora";
                  return o;
                })()""")
                check("reset_needs_double_confirmation", steps == {"first": True, "cancel": True, "second": True}, steps)
                b.eval('document.getElementById("resetYes").click()')
                b.wait_for('localStorage.getItem("toefl_progress_v1") === null && document.readyState === "complete"', timeout=15)
                b.pump(1.5)
                left = b.eval('Object.keys(localStorage).filter(function(k){ return %s.some(function(p){ return k.indexOf(p) === 0; }); })' % json.dumps(RESET_KEYS))
                clean = b.eval('document.querySelectorAll(".pchk:checked, h3.h3-done").length === 0 && document.getElementById("opPct").textContent === "0%"')
                check("real_reset_clears_all_progress", not left and clean, left)

                # importar: restaura e deixa marcado para subir a nuvem
                backup = Path(tmp) / "backup.json"
                backup.write_text(json.dumps({"app": "iTOEFL", "data": {
                    "toefl_progress_v1": json.dumps({pid: True, "_ordem_m0": 2}), "toefl_sync_at": "2020-01-01T00:00:00Z", "outra_chave": "x"}}), encoding="utf-8")
                b.eval('localStorage.removeItem("toefl_dirty")')
                b.set_files("#dataFile", [backup])
                b.wait_for('!!document.querySelector("#panel-mod0 .pchk") && document.querySelector("#panel-mod0 .pchk").checked', timeout=15)
                imported = b.eval('({ checked: document.querySelector("#panel-mod0 .pchk").checked, dirty: localStorage.getItem("toefl_dirty"),'
                                  ' syncAt: localStorage.getItem("toefl_sync_at"), other: localStorage.getItem("outra_chave") })')
                check("real_import_restores_and_marks_dirty",
                      imported["checked"] and imported["dirty"] == "1" and imported["syncAt"] is None and imported["other"] is None, imported)

                # celular: nada estoura a largura, em nenhum modulo
                b.viewport(375, 812, mobile=True, scale=2)
                b.reload(settle=1.2)
                b.eval(ACT)
                over = {}
                for key in MODS:
                    bad = b.eval(OVERFLOW + "(" + json.dumps(key) + ")")
                    if bad:
                        over[key] = bad
                check("mobile_375_no_horizontal_overflow", not over, over)
                head = b.eval(HEADER)
                check("header_no_overlap_mobile", all(head.values()), head)
                rd = b.eval(READING)
                check("part_rail_mobile_thin_bar",
                      not rd["bodyShown"] and rd.get("opens") and rd["railH"] <= 80 and rd["items"] == rd["h3"] > 0
                      and rd["doneWorks"] and rd["markDoneVisible"], rd)
                tb = b.eval(TABLES)
                check("tables_readable_on_mobile_as_cards",
                      not tb["thVisible"] and tb["tdBlock"] == "block" and "Seção" in tb["label"]
                      and tb["fits"] and tb["font"] >= 14, tb)
                b.reload(settle=1.2)

                # barra do topo: gruda no alto, cobre o botao do menu (que
                # antes flutuava sobre o texto) e diz onde o aluno esta
                bar = b.eval(r"""(function(){
                  document.querySelector('.tabbtn[data-tab="mod1"]').click();
                  window.__toeflShowPart.mod1(document.querySelectorAll("#panel-mod1 .section-card")[2]);
                  window.scrollTo(0, 900);
                  var j = document.getElementById("journey").getBoundingClientRect(), h = document.getElementById("sideToggle").getBoundingClientRect();
                  return { top: Math.round(j.top), left: Math.round(j.left), right: Math.round(j.right), vw: document.documentElement.clientWidth,
                    covers: h.top >= j.top && h.bottom <= j.bottom && h.left >= j.left,
                    mod: document.getElementById("jtMod").textContent, part: document.getElementById("jtPart").textContent,
                    pager: document.querySelector("#panel-mod1 .part-pager-label").textContent, scrolled: window.scrollY > 300,
                    current: document.querySelector('.tabbtn[aria-current="page"]').dataset.tab };
                })()""")
                check("mobile_top_bar_sticks_and_names_the_place",
                      bar["scrolled"] and bar["top"] == 0 and bar["left"] <= 0 and bar["right"] >= bar["vw"] and bar["covers"]
                      and bar["mod"] == "01 · Reading" and bar["part"] == "Parte 3 de 7" and "PARTE 3" not in bar["pager"]
                      and bar["current"] == "mod1", bar)

                for theme in ("light", "dark"):
                    b.eval('document.documentElement.setAttribute("data-theme", %s)' % json.dumps(theme))
                    b.pump(0.3)
                    low = b.eval(CONTRAST)
                    check("contrast_aa_" + theme, not low, low)
                check("real_no_js_errors_after_use", not b.errors, b.errors)

            # tela de login em tela baixa: rola até o fim e o botão do Google e
            # o link dos Termos ficam alcançáveis (item 20 de 2026-10-25: o
            # cartão era centralizado com overflow:hidden e o fim sumia)
            with Browser() as b:
                for w, h, mobile in ((390, 600, True), (1280, 500, False)):
                    b.viewport(w, h, mobile=mobile)
                    b.goto(page, settle=0.8)
                    gate = b.eval(GATE_SCROLL)
                    check(f"login_gate_scrolls_{w}x{h}",
                          gate["tall"] and gate["scrolled"] and gate["googleIn"] and gate["termsIn"] and gate["topIn"], gate)

            # apresentacao antes do login: o script do <head> do app (com
            # Supabase configurado) manda quem nao tem sessao para a
            # apresentacao, e deixa passar quem tem sessao, quem veio por
            # "Entrar" e a volta do pagamento
            real_index = (ROOT / "artifact" / "index.html").read_text(encoding="utf-8")
            redir = re.search(r'<script id="landingRedirect">.*?</script>', real_index, re.S)
            check("landing_redirect_in_real_build", redir or "ITOEFL_SUPABASE" not in real_index,
                  "artifact/index.html tem Supabase e não tem o script landingRedirect")
            if redir:
                (site / "redirect_test.html").write_text(
                    '<!DOCTYPE html><html><head><link rel="icon" href="data:,">' + redir.group(0) + '</head><body>app</body></html>',
                    encoding="utf-8")
                with Browser() as b:
                    where = {}
                    for case, url, session in (("sem_sessao", "/redirect_test.html", False), ("com_sessao", "/redirect_test.html", True),
                                               ("entrar", "/redirect_test.html#entrar", False),
                                               ("pagamento", "/redirect_test.html?pay=success", False)):
                        b.goto(base + "/stripe_test.html", settle=0.2)
                        b.eval('localStorage.clear()' + ('; localStorage.setItem("sb-abc-auth-token", "{}")' if session else ""))
                        b.goto(base + url, settle=0.8)
                        where[case] = b.eval("location.pathname")
                    check("landing_before_login_for_visitors",
                          where == {"sem_sessao": "/apresentacao.html", "com_sessao": "/redirect_test.html",
                                    "entrar": "/redirect_test.html", "pagamento": "/redirect_test.html"}, where)

            # tela de apresentacao: pagina publica, antes do login
            with Browser() as b:
                b.goto(base + "/apresentacao.html", settle=0.5)
                b.eval('localStorage.clear(); localStorage.setItem("toefl_theme_v1", "light")')
                b.reload(settle=1.2)
                lp = b.eval(LANDING_STATE)
                check("landing_desktop_has_all_sections",
                      lp["h1"] == 1 and lp["sections"] == ["como-funciona", "diagnostico", "gratis", "planos", "duvidas"]
                      and lp["qcards"] == 10 and lp["enter"] == "index.html#entrar" and lp["legal"] and lp["faq"] >= 6
                      and lp["resultHidden"] and lp["docW"] <= lp["vw"] and not lp["over"], lp)
                # topo com presença: logo e menu maiores, "Começar grátis" como
                # ação principal, selo do formato legível e reto; sem vídeo
                # cadastrado, o espaço do vídeo não aparece
                check("landing_top_has_presence",
                      lp["start"] == "index.html#criar-conta" and lp["heroMain"] == "index.html#criar-conta"
                      and lp["logo"] >= 40 and lp["navFont"] >= 15 and lp["kicker"]["size"] >= 14 and lp["kicker"]["straight"]
                      and not lp["video"], lp)
                check("landing_four_plans_side_by_side_90_highlighted",
                      [p["id"] for p in lp["plans"]] == ["mensal", "60dias", "90dias", "anual"]
                      and [p["price"] for p in lp["plans"]] == ["R$ 29,90", "R$ 49,90", "R$ 59,90", "R$ 129,90"]
                      and [p["note"] for p in lp["plans"]] == ["por mês, renovação automática", "equivale a R$ 24,95/mês",
                                                               "equivale a R$ 19,97/mês", "equivale a R$ 10,83/mês"]
                      and [p["badge"] for p in lp["plans"]] == ["", "", "Mais escolhido", ""]
                      and len({p["top"] for p in lp["plans"]}) == 1 and lp["refund"], lp)
                check("landing_makes_no_unprovable_claims", not lp["claims"], lp["claims"])
                # 7 certas de 10: B2, cronograma Regular, e o estado fica na
                # mesma chave que o app le
                early = b.eval(r"""(function(){
                  Array.prototype.slice.call(document.querySelectorAll("#diagnostico .qcard"), 0, 3).forEach(function(c){
                    c.querySelector('.opt[data-letter="' + c.dataset.correct + '"]').click(); c.querySelector(".qconfirm").click();
                  });
                  return { verdicts: document.querySelectorAll("#diagnostico .verdict").length,
                    pending: document.querySelectorAll("#diagnostico .qpending").length };
                })()""")
                check("landing_diagnostic_hides_key_until_the_end", early == {"verdicts": 0, "pending": 3}, early)
                res = b.eval(LANDING_ANSWER)
                check("landing_free_diagnostic_gives_band",
                      "Você acertou 7 de 10." in res["text"] and "Nível estimado: banda 4–4,5 (B2)" in res["text"]
                      and "Cronograma Regular (60 dias)" in res["text"] and res["saved"] == 10 and res["verdicts"] == 10
                      and not res["hidden"], res)
                b.reload(settle=1)
                again = b.eval('(function(){ var r = document.getElementById("lpResult"); return { hidden: r.hidden, text: r.textContent }; })()')
                check("landing_diagnostic_survives_reload", not again["hidden"] and "B2" in again["text"], again)
                pick = b.eval('(function(){ var a = document.querySelector(\'.lp-plan[data-plan="60dias"] a\'); a.addEventListener("click", function(e){ e.preventDefault(); });'
                              ' a.click(); return { href: a.getAttribute("href"), saved: localStorage.getItem("toefl_plan_pick_v1") }; })()')
                check("landing_plan_click_carries_choice", pick == {"href": "index.html#criar-conta", "saved": "60dias"}, pick)
                for theme in ("light", "dark"):
                    b.eval('document.documentElement.setAttribute("data-theme", %s)' % json.dumps(theme))
                    b.pump(0.3)
                    low = b.eval(CONTRAST)
                    check("landing_contrast_aa_" + theme, not low, low)

                b.viewport(375, 812, mobile=True)
                b.reload(settle=1)
                lp = b.eval(LANDING_STATE)
                tops = {p["id"]: p["top"] for p in lp["plans"]}
                check("landing_mobile_375_fits_and_stacks_highlight_first",
                      lp["docW"] <= 375 and not lp["over"] and len(tops) == 4
                      and tops["90dias"] < tops["mensal"] < tops["60dias"] < tops["anual"] and lp["smallTargets"] == [], lp)
                check("landing_no_js_errors", not b.errors, b.errors)
                # o plano clicado la (60 dias) chega marcado na tela de compra do app
                b.goto(page, settle=1)
                carried = b.eval('(function(){ var p = document.querySelector("#planPick input:checked");'
                                 ' return { plan: p && p.value, btn: document.getElementById("payBtn").textContent }; })()')
                check("landing_choice_preselects_plan_in_app",
                      carried == {"plan": "60dias", "btn": "Comprar o plano 60 dias: R$ 49,90"}, carried)

            # service worker: navegador novo, sem cache nenhum
            with Browser() as b:
                b.goto(page, settle=0.5)
                took = b.wait_for("navigator.serviceWorker.controller !== null", timeout=25)
                check("sw_first_visit_takes_control", took)
                # build novo: conteudo e versao diferentes
                index = site / "index.html"
                index.write_text(index.read_text(encoding="utf-8").replace('<html lang="pt-BR"', '<html data-smoke="v2" lang="pt-BR"', 1), encoding="utf-8")
                sw = site / "sw.js"
                sw.write_text(re.sub(r'var VERSION = "[0-9a-f]+";', 'var VERSION = "aaaaaaaaaaaa";', sw.read_text(encoding="utf-8")), encoding="utf-8")
                b.reload(settle=0.5)
                b.wait_for('!document.getElementById("pwaUpdate").hidden', timeout=25)
                st = b.eval(SW_STATE)
                # ainda a versao antiga na tela, com o aviso: nao troca no meio do estudo
                check("sw_new_build_shows_update_bar", st["bar"] and st["waiting"] and st["marker"] is None, st)
                b.eval('document.getElementById("pwaUpdateBtn").click()')
                b.wait_for('document.documentElement.getAttribute("data-smoke") === "v2"', timeout=25)
                b.pump(0.8)
                st = b.eval(SW_STATE)
                check("sw_reload_button_serves_new_version", st["marker"] == "v2" and not st["bar"] and not st["waiting"], st)
                b.offline(True)
                try:
                    b.reload(settle=1)
                    st = b.eval(SW_STATE)
                    check("sw_site_opens_offline", st["panels"] == 10 and st["marker"] == "v2", st)
                finally:
                    b.offline(False)
        finally:
            srv.shutdown()
    return out, why


if __name__ == "__main__":
    results, details = run()
    for name in sorted(results):
        print(f"  [{'OK  ' if results[name] else 'FAIL'}] {name}")
        if name in details:
            print(f"         -> {details[name]}")
    sys.exit(0 if all(results.values()) else 1)
