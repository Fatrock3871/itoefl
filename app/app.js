(function(){
  "use strict";
  // wrap tables so wide tables scroll inside themselves, not the page
  Array.prototype.slice.call(document.querySelectorAll(".panel table")).forEach(function(t){
    var wrap = document.createElement("div");
    wrap.className = "table-wrap";
    t.parentNode.insertBefore(wrap, t);
    wrap.appendChild(t);
  });

  var LS_PROGRESS = "toefl_progress_v1";
  var LS_THEME = "toefl_theme_v1";
  var LS_QUIZ = "toefl_quiz_mod0_v1";

  function safeGet(key){ try { return localStorage.getItem(key); } catch(e){ return null; } }
  function safeSet(key, val){ try { localStorage.setItem(key, val); } catch(e){} }

  // ---------- Theme ----------
  var root = document.documentElement;
  var themeBtn = document.getElementById("themeToggle");
  var themeIcon = document.getElementById("themeIcon");
  var themeLabel = document.getElementById("themeLabel");
  var themeStates = ["system", "light", "dark"];
  var themeIcons = {system:"🌗", light:"☀️", dark:"🌙"};
  var themeLabels = {system:"Sistema", light:"Claro", dark:"Escuro"};

  function applyTheme(mode){
    if(mode === "system"){ root.removeAttribute("data-theme"); }
    else { root.setAttribute("data-theme", mode); }
    themeIcon.textContent = themeIcons[mode];
    themeLabel.textContent = themeLabels[mode];
  }
  var savedTheme = safeGet(LS_THEME) || "system";
  applyTheme(savedTheme);
  themeBtn.addEventListener("click", function(){
    var cur = safeGet(LS_THEME) || "system";
    var next = themeStates[(themeStates.indexOf(cur)+1) % themeStates.length];
    safeSet(LS_THEME, next);
    applyTheme(next);
  });

  // ---------- Tabs ----------
  var tabBtns = Array.prototype.slice.call(document.querySelectorAll(".tabbtn"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  function showTab(key){
    tabBtns.forEach(function(b){ b.classList.toggle("active", b.dataset.tab === key); });
    panels.forEach(function(p){ p.hidden = p.dataset.panel !== key; });
    document.getElementById("mainArea").scrollTop = 0;
    safeSet("toefl_active_tab", key);
  }
  tabBtns.forEach(function(b){
    b.addEventListener("click", function(){ showTab(b.dataset.tab); });
  });
  var initialTab = safeGet("toefl_active_tab");
  if(initialTab && document.querySelector('.panel[data-panel="'+initialTab+'"]')){
    showTab(initialTab);
  } else {
    showTab("mod0");
  }

  // ---------- Progress checkboxes ----------
  var allChecks = Array.prototype.slice.call(document.querySelectorAll(".pchk"));
  var progressState = {};
  try { progressState = JSON.parse(safeGet(LS_PROGRESS) || "{}"); } catch(e){ progressState = {}; }

  function moduleKeyFromPid(pid){ return pid.split("-")[0]; }

  function updateBadges(){
    var byMod = {};
    allChecks.forEach(function(c){
      var mod = moduleKeyFromPid(c.dataset.pid);
      byMod[mod] = byMod[mod] || {total:0, done:0};
      byMod[mod].total++;
      if(progressState[c.dataset.pid]) byMod[mod].done++;
    });
    var totalAll = 0, doneAll = 0;
    Object.keys(byMod).forEach(function(mod){
      var b = byMod[mod];
      totalAll += b.total; doneAll += b.done;
      var badgeEl = document.getElementById("badge-"+mod);
      if(badgeEl) badgeEl.textContent = b.total ? Math.round(100*b.done/b.total)+"%" : "";
    });
    var pct = totalAll ? Math.round(100*doneAll/totalAll) : 0;
    document.getElementById("opPct").textContent = pct + "%";
    document.getElementById("opFill").style.width = pct + "%";
  }

  allChecks.forEach(function(c){
    var pid = c.dataset.pid;
    if(progressState[pid]){
      c.checked = true;
      c.closest(".prog-head").classList.add("done");
    }
    c.addEventListener("change", function(){
      progressState[pid] = c.checked;
      c.closest(".prog-head").classList.toggle("done", c.checked);
      safeSet(LS_PROGRESS, JSON.stringify(progressState));
      updateBadges();
    });
  });
  updateBadges();

  // ---------- Quiz widgets (select -> confirm -> reveal -> retry) ----------
  // Each .quiz-drill has data-drill="<id>" and its own localStorage key.
  var quizDrills = Array.prototype.slice.call(document.querySelectorAll(".quiz-drill"));

  quizDrills.forEach(function(drillEl){
    var drillId = drillEl.dataset.drill;
    var lsKey = "toefl_quiz_" + drillId + "_v1";
    var state = {}; // { num: { picked: "A", confirmed: true/false } }
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }

    var qcards = Array.prototype.slice.call(drillEl.querySelectorAll(".qcard"));

    function saveState(){ safeSet(lsKey, JSON.stringify(state)); }

    function renderSummary(){
      var total = qcards.length, confirmed = 0, correct = 0;
      qcards.forEach(function(card){
        var num = card.dataset.num;
        var s = state[num];
        if(s && s.confirmed){
          confirmed++;
          if(s.picked === card.dataset.correct) correct++;
        }
      });
      var bar = drillEl.querySelector(".quiz-bar-fill");
      var scoreEl = drillEl.querySelector(".quiz-score");
      var summary = drillEl.querySelector(".quiz-summary");
      if(bar) bar.style.width = (total ? Math.round(100*confirmed/total) : 0) + "%";
      if(scoreEl) scoreEl.textContent = confirmed + " de " + total + " respondidas";
      if(summary){
        if(confirmed === total && total > 0){
          summary.hidden = false;
          summary.querySelector(".quiz-summary-text").textContent =
            "Você acertou " + correct + " de " + total + ".";
        } else {
          summary.hidden = true;
        }
      }
    }

    function applyCardState(card){
      var num = card.dataset.num;
      var s = state[num];
      var opts = Array.prototype.slice.call(card.querySelectorAll(".opt"));
      var confirmBtn = card.querySelector(".qconfirm");
      var fb = card.querySelector(".qfeedback");
      if(!s){
        opts.forEach(function(o){ o.disabled = false; o.classList.remove("correct","wrong","picked"); });
        if(confirmBtn){ confirmBtn.hidden = true; confirmBtn.disabled = true; }
        if(fb) fb.hidden = true;
        return;
      }
      if(!s.confirmed){
        opts.forEach(function(o){
          o.disabled = false;
          o.classList.toggle("picked", o.dataset.letter === s.picked);
        });
        if(confirmBtn){ confirmBtn.hidden = false; confirmBtn.disabled = !s.picked; }
        if(fb) fb.hidden = true;
      } else {
        var correct = card.dataset.correct;
        opts.forEach(function(o){
          o.disabled = true;
          o.classList.remove("picked");
          if(o.dataset.letter === correct) o.classList.add("correct");
          else if(o.dataset.letter === s.picked) o.classList.add("wrong");
        });
        if(confirmBtn){ confirmBtn.hidden = true; }
        if(fb) fb.hidden = false;
      }
    }

    qcards.forEach(function(card){
      var num = card.dataset.num;
      var opts = Array.prototype.slice.call(card.querySelectorAll(".opt"));
      var confirmBtn = card.querySelector(".qconfirm");

      opts.forEach(function(o){
        o.addEventListener("click", function(){
          var s = state[num];
          if(s && s.confirmed) return; // already revealed, locked
          state[num] = { picked: o.dataset.letter, confirmed: false };
          saveState();
          applyCardState(card);
        });
      });

      if(confirmBtn){
        confirmBtn.addEventListener("click", function(){
          var s = state[num];
          if(!s || !s.picked) return;
          s.confirmed = true;
          saveState();
          applyCardState(card);
          renderSummary();
        });
      }

      applyCardState(card);
    });

    var retryBtn = drillEl.querySelector(".quiz-retry");
    if(retryBtn){
      retryBtn.addEventListener("click", function(){
        state = {};
        saveState();
        qcards.forEach(applyCardState);
        renderSummary();
      });
    }

    renderSummary();
  });

  // ---------- Cronômetro de seção ----------
  (function(){
    var wrap = document.getElementById("secTimer");
    if(!wrap) return;
    var display = document.getElementById("stDisplay");
    var presets = document.getElementById("stPresets");
    var startBtn = document.getElementById("stStart");
    var resetBtn = document.getElementById("stReset");
    var toggle = document.getElementById("stToggle");

    var LS_PRESET = "toefl_timer_preset";
    var minutes = parseInt(safeGet(LS_PRESET), 10);
    if(!minutes || minutes < 1) minutes = 28;
    var remaining = minutes * 60;   // segundos
    var tick = null;

    function fmt(s){
      var m = Math.floor(s / 60), r = s % 60;
      return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r;
    }
    function render(){ display.textContent = fmt(Math.max(0, remaining)); }
    function markPreset(){
      Array.prototype.forEach.call(presets.children, function(b){
        b.classList.toggle("active", parseInt(b.dataset.min, 10) === minutes);
      });
    }
    function stop(){
      if(tick){ clearInterval(tick); tick = null; }
      wrap.classList.remove("running");
      startBtn.textContent = "Iniciar";
    }
    function beep(){
      try{
        var Ctx = window.AudioContext || window.webkitAudioContext;
        if(!Ctx) return;
        var ac = new Ctx(), o = ac.createOscillator(), g = ac.createGain();
        o.connect(g); g.connect(ac.destination);
        o.type = "sine"; o.frequency.value = 880;
        g.gain.setValueAtTime(0.001, ac.currentTime);
        g.gain.exponentialRampToValueAtTime(0.2, ac.currentTime + 0.02);
        g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.6);
        o.start(); o.stop(ac.currentTime + 0.6);
      }catch(e){}
    }
    function finish(){
      stop();
      wrap.classList.add("done");
      beep();
      setTimeout(function(){ wrap.classList.remove("done"); }, 6000);
    }
    function start(){
      if(tick) return;
      if(remaining <= 0) remaining = minutes * 60;
      wrap.classList.remove("done");
      wrap.classList.add("running");
      startBtn.textContent = "Pausar";
      tick = setInterval(function(){
        remaining--;
        render();
        if(remaining <= 0) finish();
      }, 1000);
    }
    function reset(){
      stop();
      wrap.classList.remove("done");
      remaining = minutes * 60;
      render();
    }

    presets.addEventListener("click", function(e){
      var b = e.target.closest("button[data-min]");
      if(!b) return;
      minutes = parseInt(b.dataset.min, 10);
      safeSet(LS_PRESET, String(minutes));
      markPreset();
      reset();
    });
    startBtn.addEventListener("click", function(){ tick ? stop() : start(); });
    resetBtn.addEventListener("click", reset);
    toggle.addEventListener("click", function(){ wrap.classList.toggle("collapsed"); });

    markPreset();
    render();
  })();

  // ---------- Gravador de voz (Speaking) ----------
  (function(){
    var wrap = document.getElementById("micRec");
    if(!wrap) return;
    var display = document.getElementById("mrDisplay");
    var statusEl = document.getElementById("mrStatus");
    var audioEl = document.getElementById("mrAudio");
    var recBtn = document.getElementById("mrToggleBtn");
    var clearBtn = document.getElementById("mrClear");
    var toggle = document.getElementById("mrToggle");

    var rec = null, chunks = [], stream = null, elapsed = 0, tick = null, url = null;

    if(!navigator.mediaDevices || !window.MediaRecorder){
      recBtn.disabled = true;
      statusEl.textContent = "Gravação não suportada neste navegador.";
    }

    function fmt(s){
      var m = Math.floor(s / 60), r = s % 60;
      return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r;
    }
    function stopClock(){ if(tick){ clearInterval(tick); tick = null; } }
    function releaseStream(){
      if(stream){ stream.getTracks().forEach(function(t){ t.stop(); }); stream = null; }
    }
    function revoke(){ if(url){ URL.revokeObjectURL(url); url = null; } }

    function startRec(){
      navigator.mediaDevices.getUserMedia({ audio: true }).then(function(s){
        stream = s;
        revoke();
        audioEl.hidden = true;
        clearBtn.hidden = true;
        chunks = [];
        rec = new MediaRecorder(s);
        rec.ondataavailable = function(e){ if(e.data && e.data.size) chunks.push(e.data); };
        rec.onstop = function(){
          var blob = new Blob(chunks, { type: chunks[0] ? chunks[0].type : "audio/webm" });
          url = URL.createObjectURL(blob);
          audioEl.src = url;
          audioEl.hidden = false;
          clearBtn.hidden = false;
          statusEl.textContent = "Ouça e compare com o alvo.";
          releaseStream();
        };
        rec.start();
        elapsed = 0; display.textContent = "00:00";
        wrap.classList.add("recording");
        recBtn.textContent = "■ Parar";
        statusEl.textContent = "Gravando…";
        tick = setInterval(function(){ elapsed++; display.textContent = fmt(elapsed); }, 1000);
      }).catch(function(){
        statusEl.textContent = "Permissão de microfone negada.";
      });
    }
    function stopRec(){
      stopClock();
      wrap.classList.remove("recording");
      recBtn.textContent = "● Gravar";
      if(rec && rec.state !== "inactive") rec.stop();
      rec = null;
    }
    function clearRec(){
      revoke();
      audioEl.hidden = true; audioEl.removeAttribute("src");
      clearBtn.hidden = true;
      display.textContent = "00:00";
      statusEl.textContent = "Grave sua resposta e ouça de volta.";
    }

    recBtn.addEventListener("click", function(){
      if(wrap.classList.contains("recording")) stopRec(); else startRec();
    });
    clearBtn.addEventListener("click", clearRec);
    toggle.addEventListener("click", function(){ wrap.classList.toggle("collapsed"); });
  })();

  // ---------- Export / import de progresso ----------
  (function(){
    var expBtn = document.getElementById("dataExport");
    var impBtn = document.getElementById("dataImport");
    var fileInput = document.getElementById("dataFile");
    var msg = document.getElementById("dataMsg");
    if(!expBtn) return;

    var PREFIX = "toefl_";
    function flash(text, ok){
      msg.textContent = text;
      msg.style.color = ok === false ? "var(--danger)" : "var(--good)";
      msg.hidden = false;
      setTimeout(function(){ msg.hidden = true; }, 4000);
    }
    function collect(){
      var out = {};
      try{
        for(var i = 0; i < localStorage.length; i++){
          var k = localStorage.key(i);
          if(k && k.indexOf(PREFIX) === 0) out[k] = localStorage.getItem(k);
        }
      }catch(e){}
      return out;
    }

    expBtn.addEventListener("click", function(){
      var payload = { app: "iTOEFL", exported: new Date().toISOString(), data: collect() };
      var text = JSON.stringify(payload, null, 2);
      try{
        var blob = new Blob([text], { type: "application/json" });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "itoefl-progresso.json";
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
      }catch(e){}
      if(navigator.clipboard){
        navigator.clipboard.writeText(text).then(
          function(){ flash("Baixado + copiado para a área de transferência."); },
          function(){ flash("Arquivo baixado."); }
        );
      }else{
        flash("Arquivo baixado.");
      }
    });

    impBtn.addEventListener("click", function(){ fileInput.click(); });
    fileInput.addEventListener("change", function(){
      var f = fileInput.files && fileInput.files[0];
      if(!f) return;
      var reader = new FileReader();
      reader.onload = function(){
        try{
          var parsed = JSON.parse(reader.result);
          var data = parsed && parsed.data ? parsed.data : parsed;
          var n = 0;
          Object.keys(data).forEach(function(k){
            if(k.indexOf(PREFIX) === 0){ localStorage.setItem(k, data[k]); n++; }
          });
          flash(n + " itens importados. Recarregando…");
          setTimeout(function(){ location.reload(); }, 1200);
        }catch(e){
          flash("Arquivo inválido.", false);
        }
      };
      reader.readAsText(f);
      fileInput.value = "";
    });
  })();
})();
