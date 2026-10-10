// Tela de apresentação (artifact/apresentacao.html): o diagnóstico aberto sem
// conta e a escolha de plano. Página própria, sem o app.js: aqui não há
// login, sincronização nem progresso. O build.py cola o level.js (ToeflLevel)
// antes deste arquivo.
(function(){
  function safeGet(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }
  function safeSet(k, v){ try { localStorage.setItem(k, v); } catch(e){} }

  // ---------- diagnóstico: as 10 questões do M0 ----------
  // Mesma chave e mesmo formato do app ({ num: { picked, confirmed } }, pela
  // letra de data-letter). Assim quem faz o teste aqui e depois cria a conta
  // neste mesmo navegador encontra o diagnóstico já respondido no Módulo 0.
  var drill = document.querySelector('.quiz-drill[data-drill="mod0-diag"]');
  if(drill){
    var LS_KEY = "toefl_quiz_mod0-diag_v1";
    var state = {};
    try { state = JSON.parse(safeGet(LS_KEY) || "{}") || {}; } catch(e){ state = {}; }
    var cards = Array.prototype.slice.call(drill.querySelectorAll(".qcard"));
    var resultEl = document.getElementById("lpResult");

    // o texto das alternativas e a frase de cada questão são inglês
    cards.forEach(function(card){
      Array.prototype.forEach.call(card.querySelectorAll(".otext"), function(t){ t.setAttribute("lang", "en"); });
    });

    function save(){ safeSet(LS_KEY, JSON.stringify(state)); }

    function setTag(opt, text, kind){
      var tag = opt.querySelector(".otag");
      if(!text){ if(tag) tag.parentNode.removeChild(tag); return; }
      if(!tag){ tag = document.createElement("span"); opt.appendChild(tag); }
      tag.className = "otag otag-" + kind;
      tag.textContent = text;
    }
    function setVerdict(fb, text, ok){
      var v = fb.querySelector(".verdict");
      if(text === null){ if(v) v.parentNode.removeChild(v); return; }
      if(!v){
        v = document.createElement("p");
        v.setAttribute("role", "status");
        fb.insertBefore(v, fb.firstChild);
      }
      v.className = "verdict " + (ok ? "verdict-ok" : "verdict-bad");
      v.textContent = (ok ? "✓ " : "✗ ") + text;
    }

    function applyCard(card){
      var s = state[card.dataset.num];
      var key = card.dataset.correct;
      var opts = Array.prototype.slice.call(card.querySelectorAll(".opt"));
      var confirmBtn = card.querySelector(".qconfirm");
      var fb = card.querySelector(".qfeedback");
      var done = !!(s && s.confirmed);
      opts.forEach(function(o){
        var L = o.dataset.letter, picked = !!s && s.picked === L;
        o.disabled = done;
        o.classList.toggle("picked", picked && !done);
        o.classList.toggle("correct", done && L === key);
        o.classList.toggle("wrong", done && picked && L !== key);
        o.setAttribute("aria-pressed", picked ? "true" : "false");
        if(!done) setTag(o, "");
        else if(L === key) setTag(o, picked ? "sua resposta, correta" : "correta", "ok");
        else if(picked) setTag(o, "sua resposta", "bad");
        else setTag(o, "");
      });
      confirmBtn.hidden = done || !s;
      confirmBtn.disabled = !s || !s.picked;
      fb.hidden = !done;
      if(done){
        var ok = s.picked === key;
        setVerdict(fb, ok ? "Você acertou." : "Você marcou (" + s.picked + "). A correta é (" + key + ").", ok);
      } else {
        setVerdict(fb, null);
      }
    }

    function renderResult(){
      var total = cards.length, confirmed = 0, correct = 0;
      cards.forEach(function(card){
        var s = state[card.dataset.num];
        if(s && s.confirmed){ confirmed++; if(s.picked === card.dataset.correct) correct++; }
      });
      drill.querySelector(".quiz-bar-fill").style.width = Math.round(100 * confirmed / total) + "%";
      drill.querySelector(".quiz-score").textContent = confirmed + " de " + total + " respondidas";
      var finished = confirmed === total && total > 0;
      resultEl.hidden = !finished;
      if(!finished) return;
      var pct = Math.round(100 * correct / total);
      var band = ToeflLevel.band(pct);
      document.getElementById("lpResultScore").textContent = "Você acertou " + correct + " de " + total + ".";
      document.getElementById("lpResultBand").textContent = "Nível estimado: " + band.label + ", banda " + band.code;
      document.getElementById("lpResultDesc").textContent = band.desc.charAt(0).toUpperCase() + band.desc.slice(1) + ".";
      document.getElementById("lpResultSched").textContent = ToeflLevel.schedule(pct).split(" · ")[0];
    }

    cards.forEach(function(card){
      var num = card.dataset.num;
      Array.prototype.forEach.call(card.querySelectorAll(".opt"), function(o){
        o.addEventListener("click", function(){
          if(state[num] && state[num].confirmed) return;
          state[num] = { picked: o.dataset.letter, confirmed: false };
          save();
          applyCard(card);
        });
      });
      card.querySelector(".qconfirm").addEventListener("click", function(){
        var s = state[num];
        if(!s || !s.picked) return;
        s.confirmed = true;
        save();
        applyCard(card);
        renderResult();
        if(!resultEl.hidden) resultEl.focus();
      });
      applyCard(card);
    });

    document.getElementById("lpRetry").addEventListener("click", function(){
      state = {};
      save();
      cards.forEach(applyCard);
      renderResult();
      drill.scrollIntoView({ block: "start" });
    });

    renderResult();
  }

  // ---------- plano escolhido na tabela ----------
  // Guarda o plano clicado para a tela de compra do app já abrir com ele
  // marcado. Sobrevive ao cadastro e à volta do login com Google, que perdem
  // parâmetro de URL. É só uma preferência: o preço continua vindo do servidor.
  Array.prototype.forEach.call(document.querySelectorAll("[data-plan-pick]"), function(a){
    a.addEventListener("click", function(){ safeSet("toefl_plan_pick_v1", a.getAttribute("data-plan-pick")); });
  });

  window.__toeflLanding = { ready: true }; // gancho do smoke test
})();
