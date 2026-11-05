// Banco de questões por nível CEFR (app/banco_niveis.json, 30 por nível).
// Duas páginas usam: o app (diagnóstico adaptativo e "Questões para o seu
// nível" no Painel) e a apresentação (diagnóstico adaptativo sem conta). O
// build.py cola este arquivo depois do level.js e antes do app.js e do
// landing.js. As regras estão também no CLAUDE.md.
//
// Diagnóstico adaptativo: começa no B1. Acertou, a próxima é do nível de
// cima; errou, do nível de baixo (entre A1 e C2). Termina com 12 questões se
// as 4 últimas ficaram em no máximo 2 níveis vizinhos, senão com 15. O nível
// final é a média, arredondada, do nível demonstrado nas 6 últimas: o da
// questão quando acertou, um abaixo quando errou.
//
// Recomendação: rodadas de 10 questões, 7 do nível do aluno e 3 do nível de
// cima (no C2, as 10 do C2), primeiro as nunca respondidas. Só as do nível
// do aluno contam para mudar de nível: com 15 respostas seguidas do nível,
// 80% ou mais de acerto sobe um nível e menos de 40% desce um. A conta
// começa de novo depois de cada mudança. Na conta grátis, só as 5 primeiras
// questões do nível do aluno.
var ToeflBanco = (function(){
  var LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"];
  var B = {
    LEVELS: LEVELS,
    // % equivalente de cada nível na régua do ToeflLevel.band (level.js)
    PCT: { A1: 15, A2: 35, B1: 50, B2: 65, C1: 80, C2: 95 },
    START: "B1", MIN: 12, MAX: 15,
    WINDOW: 15, UP: 0.8, DOWN: 0.4, SESSION: 10, SESSION_UP: 3, FREE_ITEMS: 5,
    // habilidade da questão -> área do diagnóstico (DIAG_AREAS do build_pipeline.py)
    HAB_DIAG: { gramatica: "gramatica", vocabulario: "vocabulario", conectivos: "conectivos", leitura: "compreensao", registro: "registro" }
  };
  function idx(l){ return LEVELS.indexOf(l); }
  function clamp(i){ return Math.max(0, Math.min(LEVELS.length - 1, i)); }
  B.up = function(l){ return LEVELS[clamp(idx(l) + 1)]; };
  B.down = function(l){ return LEVELS[clamp(idx(l) - 1)]; };
  B.byId = function(items){ var m = {}; items.forEach(function(it){ m[it.id] = it; }); return m; };
  B.load = function(){
    var el = document.getElementById("bancoNiveis");
    try { return el ? JSON.parse(el.textContent) : []; } catch(e){ return []; }
  };

  // ---------- diagnóstico adaptativo ----------
  // ans: [{ id, lvl, p (índice marcado), ok }]
  B.adaptLevel = function(ans){
    if(!ans.length) return B.START;
    var last = ans[ans.length - 1];
    return last.ok ? B.up(last.lvl) : B.down(last.lvl);
  };
  B.adaptDone = function(ans){
    if(ans.length >= B.MAX) return true;
    if(ans.length < B.MIN) return false;
    var last = ans.slice(-4).map(function(a){ return idx(a.lvl); });
    return Math.max.apply(null, last) - Math.min.apply(null, last) <= 1;
  };
  B.adaptNext = function(items, ans, rnd){
    if(B.adaptDone(ans)) return null;
    var lvl = B.adaptLevel(ans), used = {}, byId = B.byId(items);
    ans.forEach(function(a){ used[a.id] = true; });
    var recent = ans.slice(-2).map(function(a){ return byId[a.id] && byId[a.id].habilidade; });
    var pool = items.filter(function(it){ return it.nivel === lvl && !used[it.id]; });
    var fresh = pool.filter(function(it){ return recent.indexOf(it.habilidade) === -1; });
    var from = fresh.length ? fresh : pool;
    if(!from.length) return null;
    return from[Math.floor((rnd || Math.random)() * from.length) % from.length];
  };
  // { level, pct, correct, total, areas: { <área do diagnóstico>: {ok, n} } }
  B.adaptResult = function(items, ans){
    // nível demonstrado em cada uma das 6 últimas: o da questão se acertou,
    // um abaixo se errou (quem acerta B2 e erra C1 fica no B2)
    var byId = B.byId(items), tail = ans.slice(-6).map(function(a){ return a.ok ? idx(a.lvl) : idx(a.lvl) - 1; });
    var mean = tail.length ? tail.reduce(function(s, x){ return s + x; }, 0) / tail.length : idx(B.START);
    var level = LEVELS[clamp(Math.round(mean))], areas = {}, correct = 0;
    ans.forEach(function(a){
      var it = byId[a.id], k = it ? B.HAB_DIAG[it.habilidade] : "outros";
      areas[k] = areas[k] || { ok: 0, n: 0 };
      areas[k].n++;
      if(a.ok){ areas[k].ok++; correct++; }
    });
    return { level: level, pct: B.PCT[level], correct: correct, total: ans.length, areas: areas };
  };

  // ---------- recomendação e subida de nível ----------
  // st: { level, base, win: [1 ou 0, das respostas do nível], ans: { id: {p, ok, n} }, hist: [{from, to}], set, pos }
  B.practiceInit = function(st, diagLevel){
    st = st && typeof st === "object" ? st : {};
    if(!st.ans) st.ans = {};
    if(!st.win) st.win = [];
    if(!st.hist) st.hist = [];
    // diagnóstico novo com outro nível: o nível do banco recomeça dele
    if(diagLevel && st.base !== diagLevel){ st.base = diagLevel; st.level = diagLevel; st.win = []; st.set = null; }
    if(idx(st.level) < 0) st.level = diagLevel || B.START;
    return st;
  };
  B.practiceRecord = function(st, item, p){
    var ok = p === item.correta;
    st.ans[item.id] = { p: p, ok: ok, n: ((st.ans[item.id] && st.ans[item.id].n) || 0) + 1 };
    var changed = null;
    if(item.nivel === st.level){
      st.win.push(ok ? 1 : 0);
      if(st.win.length > B.WINDOW) st.win.shift();
      if(st.win.length === B.WINDOW){
        var rate = st.win.reduce(function(s, x){ return s + x; }, 0) / B.WINDOW;
        var to = rate >= B.UP ? B.up(st.level) : rate < B.DOWN ? B.down(st.level) : st.level;
        if(to !== st.level){ changed = { from: st.level, to: to }; st.hist.push(changed); st.level = to; st.win = []; st.set = null; }
      }
    }
    return { ok: ok, changed: changed };
  };
  // quanto falta: { level, next, prev, n, ok, need (acertos para subir nas 15), window }
  B.practiceProgress = function(st){
    var ok = st.win.reduce(function(s, x){ return s + x; }, 0);
    return { level: st.level, next: idx(st.level) < LEVELS.length - 1 ? B.up(st.level) : null,
      prev: idx(st.level) > 0 ? B.down(st.level) : null, n: st.win.length, ok: ok,
      need: Math.ceil(B.UP * B.WINDOW), window: B.WINDOW };
  };
  // ids da próxima rodada
  B.practiceSet = function(items, st, free, rnd){
    rnd = rnd || Math.random;
    var lvl = st.level;
    if(free) return items.filter(function(it){ return it.nivel === lvl; }).slice(0, B.FREE_ITEMS).map(function(it){ return it.id; });
    function pick(level, n){
      var pool = items.filter(function(it){ return it.nivel === level; }).map(function(it){
        var a = st.ans[it.id];
        return { id: it.id, k: (a ? a.n : 0) + rnd() * 0.5 };
      });
      pool.sort(function(x, y){ return x.k - y.k; });
      return pool.slice(0, n).map(function(x){ return x.id; });
    }
    var upN = lvl === "C2" ? 0 : B.SESSION_UP;
    var own = pick(lvl, B.SESSION - upN), up = upN ? pick(B.up(lvl), upN) : [];
    // as de cima entram espalhadas: depois da 2ª, da 5ª e da 7ª do nível
    var out = [];
    own.forEach(function(id, i){ out.push(id); if((i === 1 || i === 4 || i === 6) && up.length) out.push(up.shift()); });
    return out.concat(up);
  };

  // ---------- tela de uma questão (adaptativo e Painel) ----------
  B.paras = function(text){
    var box = document.createElement("div");
    box.className = "bk-prompt";
    box.setAttribute("lang", "en");
    String(text).split(/\n+/).forEach(function(t){
      if(!t.trim()) return;
      var p = document.createElement("p"); p.textContent = t; box.appendChild(p);
    });
    return box;
  };
  var LETTERS = ["A", "B", "C", "D"];
  // monta a questão em root; onConfirm(p) quando o aluno confirma
  B.renderItem = function(root, it, head, onConfirm){
    root.innerHTML = "";
    var card = document.createElement("div");
    card.className = "bk-card";
    card.dataset.id = it.id;
    var h = document.createElement("p"); h.className = "bk-head"; h.textContent = head;
    card.appendChild(h);
    card.appendChild(B.paras(it.enunciado));
    var list = document.createElement("div"); list.className = "bk-opts"; list.setAttribute("role", "group");
    var picked = null;
    var confirm = document.createElement("button");
    confirm.type = "button"; confirm.className = "bk-confirm"; confirm.textContent = "Confirmar resposta"; confirm.disabled = true;
    it.alternativas.forEach(function(a, i){
      var b = document.createElement("button");
      b.type = "button"; b.className = "bk-opt"; b.dataset.i = String(i); b.setAttribute("aria-pressed", "false");
      var l = document.createElement("span"); l.className = "bk-letter"; l.textContent = LETTERS[i];
      var t = document.createElement("span"); t.className = "bk-text"; t.setAttribute("lang", "en"); t.textContent = a;
      b.appendChild(l); b.appendChild(t);
      b.addEventListener("click", function(){
        picked = i;
        Array.prototype.forEach.call(list.children, function(o){
          var on = o === b; o.classList.toggle("is-picked", on); o.setAttribute("aria-pressed", on ? "true" : "false");
        });
        confirm.disabled = false;
      });
      list.appendChild(b);
    });
    confirm.addEventListener("click", function(){ if(picked !== null) onConfirm(picked); });
    card.appendChild(list);
    card.appendChild(confirm);
    root.appendChild(card);
    return card;
  };
  // correção de uma questão já respondida: alternativas marcadas e explicação
  B.renderFeedback = function(card, it, p){
    Array.prototype.forEach.call(card.querySelectorAll(".bk-opt"), function(o){
      var i = +o.dataset.i;
      o.disabled = true;
      o.classList.toggle("is-right", i === it.correta);
      o.classList.toggle("is-wrong", i === p && p !== it.correta);
      var text = i === it.correta ? (i === p ? "sua resposta, correta" : "correta") : i === p ? "sua resposta" : "";
      if(text){ var tag = document.createElement("span"); tag.className = "bk-tag"; tag.textContent = text; o.appendChild(tag); }
    });
    var c = card.querySelector(".bk-confirm"); if(c) c.hidden = true;
    var fb = document.createElement("div"); fb.className = "bk-fb";
    var v = document.createElement("p"); v.setAttribute("role", "status");
    var ok = p === it.correta;
    v.className = "bk-verdict " + (ok ? "is-ok" : "is-bad");
    v.textContent = ok ? "✓ Você acertou." : "✗ Quase. Você marcou (" + LETTERS[p] + "), mas a resposta é (" + LETTERS[it.correta] + ").";
    var ex = document.createElement("p"); ex.className = "bk-exp"; ex.textContent = it.explicacao;
    fb.appendChild(v); fb.appendChild(ex);
    if(!ok && it.distratores && it.distratores[p] && it.distratores[p] !== "correta"){
      var why = document.createElement("p"); why.className = "bk-exp"; why.textContent = "Sobre a sua: " + it.distratores[p];
      fb.appendChild(why);
    }
    card.appendChild(fb);
    return fb;
  };

  // Diagnóstico adaptativo numa caixa. opts: { root, items, get(), set(state), onDone(result), onReset(), rnd }
  // state: { mode: "adapt", ans: [...], done, at }
  B.mountAdaptive = function(opts){
    var root = opts.root, items = opts.items, byId = B.byId(items);
    function state(){ var s = opts.get() || {}; if(!Array.isArray(s.ans)) s.ans = []; return s; }
    function render(){
      var s = state();
      if(s.done){ renderDone(s); return; }
      var it = B.adaptNext(items, s.ans, opts.rnd);
      if(!it){ s.done = true; opts.set(s); renderDone(s); if(opts.onDone) opts.onDone(B.adaptResult(items, s.ans)); return; }
      B.renderItem(root, it, "Questão " + (s.ans.length + 1) + ". O teste tem de " + B.MIN + " a " + B.MAX + " questões e se ajusta às suas respostas.", function(p){
        var cur = state();
        cur.ans.push({ id: it.id, lvl: it.nivel, p: p, ok: p === it.correta });
        cur.mode = "adapt";
        if(B.adaptDone(cur.ans)){ cur.done = true; cur.at = new Date().toISOString().slice(0, 10); }
        opts.set(cur);
        render();
        if(cur.done && opts.onDone) opts.onDone(B.adaptResult(items, cur.ans));
        var first = root.querySelector(".bk-head, .bk-done-title");
        if(first && first.focus){ first.setAttribute("tabindex", "-1"); first.focus({ preventScroll: true }); }
      });
    }
    function renderDone(s){
      var r = B.adaptResult(items, s.ans);
      root.innerHTML = "";
      var box = document.createElement("div"); box.className = "bk-done";
      var t = document.createElement("p"); t.className = "bk-done-title";
      t.textContent = "Diagnóstico adaptativo concluído: nível estimado " + r.level + ". Você acertou " + r.correct + " de " + r.total + ".";
      box.appendChild(t);
      var key = document.createElement("details"); key.className = "bk-key";
      var sum = document.createElement("summary"); sum.textContent = "Ver o gabarito, questão por questão";
      key.appendChild(sum);
      s.ans.forEach(function(a, i){
        var it = byId[a.id]; if(!it) return;
        var slot = document.createElement("div"); key.appendChild(slot);
        var card = B.renderItem(slot, it, "Questão " + (i + 1) + ", nível " + it.nivel, function(){});
        B.renderFeedback(card, it, a.p);
      });
      box.appendChild(key);
      var again = document.createElement("button"); again.type = "button"; again.className = "bk-again";
      again.textContent = "Refazer o diagnóstico adaptativo";
      again.addEventListener("click", function(){
        opts.set({ mode: "adapt", ans: [], done: false });
        render();
        if(opts.onReset) opts.onReset();
      });
      box.appendChild(again);
      root.appendChild(box);
    }
    render();
    return { render: render };
  };

  // Escolha do modo no começo do diagnóstico. opts: { root, current() ("rapido" | "adapt" | ""), choose(mode) }
  B.mountChooser = function(opts){
    var root = opts.root;
    root.innerHTML =
      '<p class="dm-q">Como você quer fazer o diagnóstico?</p>' +
      '<div class="dm-opts">' +
      '<button type="button" class="dm-opt" data-mode="rapido"><span class="dm-t">Diagnóstico rápido (10 questões fixas)</span>' +
      '<span class="dm-d">Cerca de 12 minutos. As mesmas 10 questões para todo mundo, com o gabarito no fim.</span></button>' +
      '<button type="button" class="dm-opt" data-mode="adapt"><span class="dm-t">Diagnóstico adaptativo</span>' +
      '<span class="dm-d">De 12 a 15 questões, cerca de 15 minutos. Começa no B1 e sobe ou desce conforme você acerta ou erra. Assim o nível CEFR sai mais preciso.</span></button>' +
      '</div>';
    function paint(){
      var cur = opts.current();
      Array.prototype.forEach.call(root.querySelectorAll(".dm-opt"), function(b){
        var on = b.dataset.mode === cur;
        b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }
    Array.prototype.forEach.call(root.querySelectorAll(".dm-opt"), function(b){
      b.addEventListener("click", function(){ opts.choose(b.dataset.mode); paint(); });
    });
    paint();
    return { paint: paint };
  };

  return B;
})();
