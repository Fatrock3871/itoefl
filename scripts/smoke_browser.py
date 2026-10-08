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
import http.server
import json
import re
import sys
import tempfile
import threading
from pathlib import Path

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
    var h = document.querySelector("#panel-mod0 .h3chk"); h.checked = true; h.dispatchEvent(new Event("change", { bubbles: true }));
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

SW_STATE = """(async function(){
  var reg = await navigator.serviceWorker.getRegistration();
  return { controller: !!navigator.serviceWorker.controller, waiting: !!(reg && reg.waiting),
    bar: !document.getElementById("pwaUpdate").hidden, marker: document.documentElement.getAttribute("data-smoke"),
    panels: document.querySelectorAll(".panel").length };
})()"""

MODS = ["mod%d" % i for i in range(10)]
RESET_KEYS = ["toefl_progress", "toefl_h3progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_errlog_", "toefl_ctw_",
              "toefl_spk_", "toefl_write_", "toefl_exam_", "toefl_scorecalc", "toefl_weeklydash"]


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

        srv, base = _serve(site)
        page = base + "/index.html"
        try:
            with Browser() as b:
                b.goto(page, settle=0.5)
                b.eval('localStorage.setItem("toefl_theme_v1", "light")')
                b.reload(settle=1.2)
                check("real_no_js_errors_on_load", not b.errors, b.errors)
                # abrir o site nao e estudar: nada de sequencia, meta ou
                # alteracao pendente de sincronizacao so pela carga da pagina
                idle = b.eval('Object.keys(localStorage).filter(function(k){ return /^toefl_(streak|dailygoal|dirty|scorecalc)/.test(k); })')
                check("real_opening_the_site_marks_nothing", not idle, idle)

                failed = b.eval(ACT)
                b.pump(1.2)  # a caixa de escrita salva com atraso
                check("real_every_widget_responds", not failed, failed)
                before = b.eval(SNAP)
                check("real_mark_done_text_is_clickable", before["parte"] is True)
                check("real_band_label_uses_comma", "4–4,5" in (before["nivel"] or ""), before["nivel"])
                check("real_errlog_shows_typed_text_not_html", b.eval(
                    '(function(){ var c = document.querySelector(\'.errlog[data-errlog="mod1"] .errlog-entry-drill\');'
                    ' return !!c && c.textContent === "Drill <b>A1</b> & teste" && c.children.length === 0; })()'))
                check("real_no_mailto_links", b.eval('document.querySelectorAll(\'a[href^="mailto:"]\').length === 0'))

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
                      "Meta batida" in dash["goal"] and "/1" not in dash["goal"] and "R1" in dash["weak"] and "B2" in dash["band"], dash)

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

                # gaveta: o mapa do curso aparece (ja saiu com altura zero)
                b.eval('document.getElementById("sideToggle").click()')
                b.pump(0.4)
                check("real_sidebar_map_is_visible", b.eval(
                    '(function(){ var w = document.querySelector(".side .jtrack-wrap").getBoundingClientRect(); return w.height >= 30; })()'))
                b.eval('document.getElementById("sideClose").click()')

                # reiniciar: apaga todo o progresso e recarrega
                pid = b.eval('document.querySelector("#panel-mod0 .pchk").dataset.pid')
                b.eval('window.confirm = function(){ return true; }; document.getElementById("resetBtn").click()')
                b.wait_for('localStorage.getItem("toefl_progress_v1") === null && document.readyState === "complete"', timeout=15)
                b.pump(1.5)
                left = b.eval('Object.keys(localStorage).filter(function(k){ return %s.some(function(p){ return k.indexOf(p) === 0; }); })' % json.dumps(RESET_KEYS))
                clean = b.eval('document.querySelectorAll(".pchk:checked, .h3chk:checked").length === 0 && document.getElementById("opPct").textContent === "0%"')
                check("real_reset_clears_all_progress", not left and clean, left)

                # importar: restaura e deixa marcado para subir a nuvem
                backup = Path(tmp) / "backup.json"
                backup.write_text(json.dumps({"app": "iTOEFL", "data": {
                    "toefl_progress_v1": json.dumps({pid: True}), "toefl_sync_at": "2020-01-01T00:00:00Z", "outra_chave": "x"}}), encoding="utf-8")
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

                for theme in ("light", "dark"):
                    b.eval('document.documentElement.setAttribute("data-theme", %s)' % json.dumps(theme))
                    b.pump(0.3)
                    low = b.eval(CONTRAST)
                    check("contrast_aa_" + theme, not low, low)
                check("real_no_js_errors_after_use", not b.errors, b.errors)

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
