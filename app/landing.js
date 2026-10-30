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

    // gabarito e explicações só depois da décima resposta, como no app
    function allDone(){
      return cards.every(function(c){ return state[c.dataset.num] && state[c.dataset.num].confirmed; });
    }
    function applyCard(card){
      var s = state[card.dataset.num];
      var key = card.dataset.correct;
      var opts = Array.prototype.slice.call(card.querySelectorAll(".opt"));
      var confirmBtn = card.querySelector(".qconfirm");
      var fb = card.querySelector(".qfeedback");
      var done = !!(s && s.confirmed);
      var note = card.querySelector(".qpending");
      if(done && !allDone()){
        opts.forEach(function(o){
          var on = s.picked === o.dataset.letter;
          o.disabled = true;
          o.classList.remove("correct", "wrong");
          o.classList.toggle("picked", on);
          o.setAttribute("aria-pressed", on ? "true" : "false");
          setTag(o, on ? "sua resposta" : "", "pending");
        });
        confirmBtn.hidden = true;
        fb.hidden = true;
        setVerdict(fb, null);
        if(!note){
          note = document.createElement("p");
          note.className = "qpending";
          note.setAttribute("role", "status");
          note.textContent = "Resposta guardada. O gabarito aparece no fim, depois da última questão.";
          card.appendChild(note);
        }
        return;
      }
      if(note) note.parentNode.removeChild(note);
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
        setVerdict(fb, ok ? "Você acertou." : "Quase. Você marcou (" + s.picked + "), mas a resposta é (" + key + ").", ok);
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
      document.getElementById("lpResultBand").textContent = "Nível estimado: banda " + band.code + " (" + band.label + ")";
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
        if(allDone()) cards.forEach(applyCard); else applyCard(card);
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

  // ---------- vídeo explicativo do topo (videos.json, chave "apresentacao") ----------
  // O player nasce no clique, como nas videoaulas do app: nada de fora
  // carrega antes disso.
  var video = document.getElementById("lpVideo");
  if(video){
    video.querySelector(".vid-cover").addEventListener("click", function(){
      var frame = video.querySelector(".vid-frame"), player;
      if(video.dataset.provider === "youtube"){
        player = document.createElement("iframe");
        player.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(video.dataset.src) +
          "?autoplay=1&rel=0&cc_load_policy=1&cc_lang_pref=pt-BR&hl=pt-BR";
        player.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen";
        player.allowFullscreen = true;
        player.referrerPolicy = "strict-origin-when-cross-origin";
        player.title = "Vídeo de apresentação";
      } else {
        player = document.createElement("video");
        player.controls = true; player.autoplay = true; player.playsInline = true; player.preload = "metadata";
        player.src = video.dataset.src;
        if(video.dataset.captions){
          var track = document.createElement("track");
          track.kind = "captions"; track.srclang = "pt-BR"; track.label = "Português";
          track.src = video.dataset.captions; track.default = true;
          player.appendChild(track);
        }
      }
      frame.appendChild(player);
      frame.hidden = false;
      video.querySelector(".vid-cover").hidden = true;
    });
  }

  window.__toeflLanding = { ready: true }; // gancho do smoke test
})();
