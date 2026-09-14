(function(){
  "use strict";
  // wrap tables so wide tables scroll inside themselves, not the page
  Array.prototype.slice.call(document.querySelectorAll(".panel table")).forEach(function(t){
    var wrap = document.createElement("div");
    wrap.className = "table-wrap";
    t.parentNode.insertBefore(wrap, t);
    wrap.appendChild(t);
  });

  // agrupa o conteudo de cada modulo em cards por secao (um card por H2),
  // ao estilo "unit card" de plataformas de curso, em vez de texto corrido.
  // O check de "concluir" sai do topo do H2 e vai para o fim do card: só faz
  // sentido marcar como lido depois de ler, não antes de começar.
  Array.prototype.forEach.call(document.querySelectorAll(".panel-inner"), function(container){
    var kids = Array.prototype.slice.call(container.children);
    var frag = document.createDocumentFragment();
    var current = null;
    var pendingCheck = null;

    function finalizeSection(){
      if(current && pendingCheck){
        var wrap = document.createElement("div");
        wrap.className = "mark-done";
        var labelSpan = document.createElement("span");
        labelSpan.className = "mark-done-label";
        labelSpan.textContent = "Marcar esta parte como concluída";
        wrap.appendChild(pendingCheck);
        wrap.appendChild(labelSpan);
        current.appendChild(wrap);
      }
      pendingCheck = null;
    }

    kids.forEach(function(node){
      if(node.tagName === "H2"){
        finalizeSection();
        current = document.createElement("div");
        current.className = "section-card";
        frag.appendChild(current);
        var checkLabel = node.querySelector(".prog-check");
        if(checkLabel){
          checkLabel.parentNode.removeChild(checkLabel);
          pendingCheck = checkLabel;
        }
        current.appendChild(node);
      } else if(current){
        current.appendChild(node);
      } else {
        frag.appendChild(node); // conteudo raro antes do primeiro H2
      }
    });
    finalizeSection();
    container.innerHTML = "";
    container.appendChild(frag);
  });

  var LS_PROGRESS = "toefl_progress_v1";
  var LS_THEME = "toefl_theme_v1";
  var LS_QUIZ = "toefl_quiz_mod0_v1";

  // chaves que sincronizam com o Supabase (progresso real do aluno).
  // ficam de fora: toefl_theme_v1, toefl_active_tab, toefl_timer_preset, toefl_sync_*
  var SYNC_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_avatar"];
  function isSyncedKey(key){
    if(!key || key.indexOf("toefl_") !== 0) return false;
    for(var i = 0; i < SYNC_PREFIXES.length; i++){
      if(key.indexOf(SYNC_PREFIXES[i]) === 0) return true;
    }
    return false;
  }
  var onSyncedWrite = null; // atribuído pelo módulo de sync quando logado

  function safeGet(key){ try { return localStorage.getItem(key); } catch(e){ return null; } }
  function safeSet(key, val){
    try { localStorage.setItem(key, val); } catch(e){}
    if(isSyncedKey(key)){
      try { localStorage.setItem("toefl_dirty", "1"); } catch(e){}
      if(onSyncedWrite){ try { onSyncedWrite(); } catch(e){} }
    }
  }

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

  // ---------- Barra lateral: menu em gaveta (aberta sob demanda) ----------
  // Por padrão fica fechada (só o botão de 3 traços aparece) — não ocupa espaço.
  var sideRail = document.getElementById("sideRail");
  var sideBackdrop = document.getElementById("sideBackdrop");
  var hamburgerBtn = document.getElementById("sideToggle");
  var sideCloseBtn = document.getElementById("sideClose");

  function setSidebarOpen(open){
    if(sideRail) sideRail.classList.toggle("open", open);
    if(sideBackdrop) sideBackdrop.classList.toggle("show", open);
    if(hamburgerBtn) hamburgerBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("menu-open", open);
  }
  if(hamburgerBtn){
    hamburgerBtn.addEventListener("click", function(){
      setSidebarOpen(!(sideRail && sideRail.classList.contains("open")));
    });
  }
  if(sideCloseBtn){ sideCloseBtn.addEventListener("click", function(){ setSidebarOpen(false); }); }
  if(sideBackdrop){ sideBackdrop.addEventListener("click", function(){ setSidebarOpen(false); }); }
  document.addEventListener("keydown", function(e){
    if(e.key === "Escape") setSidebarOpen(false);
  });

  // ---------- Tabs + progressão sequencial ----------
  // A ordem de desbloqueio segue a ordem em que os botões aparecem na sidebar
  // (a mesma ordem em que app/build.py monta MODS) — sem duplicar a lista aqui.
  var tabBtns = Array.prototype.slice.call(document.querySelectorAll(".tabbtn"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  var modOrder = tabBtns.map(function(b){ return b.dataset.tab; });
  var modPct = {}; // preenchido por updateBadges()
  var lockMsgEl = document.getElementById("lockMsg");
  var lockMsgTimer = null;

  var UNLOCK_PCT = 70; // % do módulo anterior necessário para liberar o próximo

  // % de questões respondidas nos widgets interativos do módulo (quiz e
  // Build a Sentence). Módulo sem widget de questão retorna 100 (não bloqueia
  // por essa via; só o checklist de 70% vale nesse caso).
  function moduleQuizPct(key){
    var panel = document.querySelector('.panel[data-panel="' + key + '"]');
    if(!panel) return 100;
    var total = 0, done = 0;
    Array.prototype.forEach.call(panel.querySelectorAll(".quiz-drill"), function(d){
      var st = {};
      try { st = JSON.parse(safeGet("toefl_quiz_" + d.dataset.drill + "_v1") || "{}"); } catch(e){}
      var cards = d.querySelectorAll(".qcard");
      total += cards.length;
      Array.prototype.forEach.call(cards, function(c){
        if(st[c.dataset.num] && st[c.dataset.num].confirmed) done++;
      });
    });
    Array.prototype.forEach.call(panel.querySelectorAll(".bsq"), function(b){
      var st = {};
      try { st = JSON.parse(safeGet("toefl_bsq_" + b.dataset.bsq + "_v1") || "{}"); } catch(e){}
      var cards = b.querySelectorAll(".bsq-card");
      total += cards.length;
      Array.prototype.forEach.call(cards, function(c){
        if(st[c.dataset.num] && st[c.dataset.num].checked) done++;
      });
    });
    if(!total) return 100; // este módulo não tem widget de questão
    return Math.round(100 * done / total);
  }

  function isUnlocked(key){
    var idx = modOrder.indexOf(key);
    if(idx <= 0) return true;
    var prev = modOrder[idx - 1];
    return (modPct[prev] || 0) >= UNLOCK_PCT && moduleQuizPct(prev) >= 100;
  }

  function showLockMessage(key){
    if(!lockMsgEl) return;
    var idx = modOrder.indexOf(key);
    var prevBtn = idx > 0 ? tabBtns[idx - 1] : null;
    var prevTitle = prevBtn ? prevBtn.dataset.title : "o módulo anterior";
    var prev = idx > 0 ? modOrder[idx - 1] : null;
    var prevPct = prev ? (modPct[prev] || 0) : 0;
    var quizPct = prev ? moduleQuizPct(prev) : 100;
    var msg = "Conclua pelo menos " + UNLOCK_PCT + "% de \"" + prevTitle + "\" (você está em " + prevPct + "%).";
    if(quizPct < 100){
      msg += " Falta responder todas as questões dos exercícios interativos (" + quizPct + "% feito).";
    }
    lockMsgEl.textContent = msg;
    lockMsgEl.hidden = false;
    if(lockMsgTimer) clearTimeout(lockMsgTimer);
    lockMsgTimer = setTimeout(function(){ lockMsgEl.hidden = true; }, 6000);
  }

  var journeyNodes = Array.prototype.slice.call(document.querySelectorAll(".jnode"));

  // ---------- Índice lateral ("Nesta parte") ----------
  var railToc = document.getElementById("railToc");
  function populateRailToc(key){
    if(!railToc) return;
    railToc.innerHTML = "";
    var panel = document.querySelector('.panel[data-panel="' + key + '"]');
    if(!panel) return;
    var heads = Array.prototype.slice.call(panel.querySelectorAll("h2[id]"));
    heads.forEach(function(h){
      var label = h.querySelector(".htext");
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = label ? label.textContent : h.textContent;
      a.addEventListener("click", function(e){
        e.preventDefault();
        h.scrollIntoView({behavior:"smooth", block:"start"});
      });
      railToc.appendChild(a);
    });
  }

  function showTab(key){
    tabBtns.forEach(function(b){ b.classList.toggle("active", b.dataset.tab === key); });
    journeyNodes.forEach(function(j){
      var on = j.dataset.tab === key;
      j.classList.toggle("current", on);
      if(on && j.scrollIntoView){ j.scrollIntoView({inline:"center", block:"nearest"}); }
    });
    panels.forEach(function(p){ p.hidden = p.dataset.panel !== key; });
    window.scrollTo(0, 0);
    var ma = document.getElementById("mainArea"); if(ma) ma.scrollTop = 0;
    safeSet("toefl_active_tab", key);
    if(lockMsgEl) lockMsgEl.hidden = true;
    setSidebarOpen(false); // navegar fecha a gaveta, que não deve ocupar espaço
    populateRailToc(key);
  }
  function navTo(key){
    if(!isUnlocked(key)){ showLockMessage(key); return; }
    showTab(key);
  }
  tabBtns.forEach(function(b){
    b.addEventListener("click", function(){ navTo(b.dataset.tab); });
  });
  journeyNodes.forEach(function(j){
    j.addEventListener("click", function(){ navTo(j.dataset.tab); });
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
    var totalAll = 0, doneAll = 0, modsDone = 0;
    Object.keys(byMod).forEach(function(mod){
      var b = byMod[mod];
      totalAll += b.total; doneAll += b.done;
      var pctMod = b.total ? Math.round(100 * b.done / b.total) : 0;
      modPct[mod] = pctMod;
      if(pctMod >= 100) modsDone++;
      var badgeEl = document.getElementById("badge-"+mod);
      if(badgeEl) badgeEl.textContent = b.total ? pctMod+"%" : "";
    });
    var pct = totalAll ? Math.round(100*doneAll/totalAll) : 0;
    document.getElementById("opPct").textContent = pct + "%";
    document.getElementById("opFill").style.width = pct + "%";
    var opCount = document.getElementById("opCount");
    if(opCount) opCount.innerHTML = "<b>" + modsDone + "</b> de " + modOrder.length + " módulos concluídos";

    // reflete no estado visual da sidebar: concluído (✓), atual, ou bloqueado (🔒)
    tabBtns.forEach(function(b){
      var key = b.dataset.tab;
      var badgeEl = b.querySelector(".num-badge");
      var done = (modPct[key] || 0) >= 100;
      var unlocked = isUnlocked(key);
      b.classList.toggle("done", done);
      b.classList.toggle("locked", !unlocked);
      if(badgeEl){
        badgeEl.textContent = done ? "✓" : (unlocked ? badgeEl.dataset.n : "🔒");
      }
    });
    // mapa da jornada: done (✓) / reached (linha preenchida) / locked (🔒)
    journeyNodes.forEach(function(j){
      var key = j.dataset.tab;
      var done = (modPct[key] || 0) >= 100;
      var unlocked = isUnlocked(key);
      j.classList.toggle("done", done);
      j.classList.toggle("reached", unlocked);
      j.classList.toggle("locked", !unlocked);
      var dot = j.querySelector(".jdot");
      if(dot) dot.textContent = done ? "✓" : (unlocked ? dot.dataset.n : "🔒");
    });
  }

  allChecks.forEach(function(c){
    var pid = c.dataset.pid;
    if(progressState[pid]){
      c.checked = true;
      var doneCard = c.closest(".section-card");
      if(doneCard) doneCard.classList.add("done");
    }
    c.addEventListener("change", function(){
      progressState[pid] = c.checked;
      var card = c.closest(".section-card");
      if(card) card.classList.toggle("done", c.checked);
      var lbl = c.closest(".mark-done");
      if(lbl){
        var t = lbl.querySelector(".mark-done-label");
        if(t) t.textContent = c.checked ? "Parte concluída" : "Marcar esta parte como concluída";
      }
      safeSet(LS_PROGRESS, JSON.stringify(progressState));
      updateBadges();
    });
  });
  updateBadges();

  // ---------- Nivelamento: o diagnóstico (M0) calibra o resto do curso ----------
  // Mesma tabela % -> banda CEFR do Módulo 0, Parte 4.2. O gate de avanço do
  // diagnóstico exige só responder as 10 (ver isUnlocked/moduleQuizPct) --
  // nunca um mínimo de acertos. O que os acertos FAZEM é isto aqui: estimar
  // a banda de entrada e recomendar um dos 3 cronogramas do Módulo 0, Parte 6.
  function cefrBandFromPct(pct){
    if(pct <= 20) return {code:"1–1.5", label:"A1", desc:"fundamentos ausentes"};
    if(pct <= 40) return {code:"2–2.5", label:"A2", desc:"fundamentos parciais"};
    if(pct <= 55) return {code:"3–3.5", label:"B1", desc:"base funcional, muitos gaps de precisão"};
    if(pct <= 70) return {code:"4–4.5", label:"B2", desc:"consistência intermediária-avançada"};
    if(pct <= 85) return {code:"5–5.5", label:"C1", desc:"alta consistência, poucos erros sistemáticos"};
    return {code:"6", label:"C2", desc:"domínio quase completo"};
  }
  function scheduleFromPct(pct){
    if(pct <= 55) return "Cronograma Premium (90 dias) · Módulo 0, Parte 6.3";
    if(pct <= 70) return "Cronograma Standard (60 dias) · Módulo 0, Parte 6.2";
    return "Cronograma Sprint (30 dias) · Módulo 0, Parte 6.1";
  }
  function updateLevelBadge(correct, total){
    var badge = document.getElementById("levelBadge");
    var bandEl = document.getElementById("levelBadgeBand");
    var schedEl = document.getElementById("levelBadgeSched");
    if(!badge || !total) return;
    var pct = Math.round(100 * correct / total);
    var band = cefrBandFromPct(pct);
    if(bandEl) bandEl.textContent = "Banda " + band.code + " (" + band.label + ") · " + correct + "/" + total + " acertos";
    if(schedEl) schedEl.textContent = scheduleFromPct(pct);
    badge.hidden = false;
  }

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
      if(drillId === "mod0-diag" && confirmed === total && total > 0){
        updateLevelBadge(correct, total);
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
      msg.style.color = ok === false ? "var(--danger)" : "var(--accent)";
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

  // ---------- Build a Sentence — widget interativo (M4) ----------
  Array.prototype.forEach.call(document.querySelectorAll(".bsq"), function(root){
    var bsqId = root.dataset.bsq;
    var lsKey = "toefl_bsq_" + bsqId + "_v1";
    var cards = Array.prototype.slice.call(root.querySelectorAll(".bsq-card"));
    var state = {};
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }
    function persist(){ safeSet(lsKey, JSON.stringify(state)); }

    function shuffle(nodes){
      for(var i = nodes.length - 1; i > 0; i--){
        var j = Math.floor(Math.random() * (i + 1));
        nodes[i].parentNode.insertBefore(nodes[i], nodes[j]);
      }
    }
    function frags(zone){
      return Array.prototype.map.call(zone.querySelectorAll(".bsq-chip"),
        function(c){ return c.dataset.frag; });
    }

    function renderSummary(){
      var total = cards.length, checked = 0, right = 0;
      cards.forEach(function(card){
        var s = state[card.dataset.num];
        if(s && s.checked){ checked++; if(s.ok) right++; }
      });
      var fill = root.querySelector(".quiz-bar-fill");
      var score = root.querySelector(".quiz-score");
      var summary = root.querySelector(".quiz-summary");
      if(fill) fill.style.width = (total ? Math.round(100 * checked / total) : 0) + "%";
      if(score) score.textContent = checked + " de " + total + " verificadas";
      if(summary){
        if(checked === total && total > 0){
          summary.hidden = false;
          summary.querySelector(".quiz-summary-text").textContent =
            "Você montou " + right + " de " + total + " corretamente.";
        }else{ summary.hidden = true; }
      }
    }

    cards.forEach(function(card){
      var num = card.dataset.num;
      var correct;
      try { correct = JSON.parse(card.dataset.answer); } catch(e){ correct = []; }
      var build = card.querySelector('[data-role="build"]');
      var bank = card.querySelector('[data-role="bank"]');
      var checkBtn = card.querySelector(".bsq-check");
      var fb = card.querySelector(".bsq-feedback");
      var model = card.querySelector(".bsq-model");
      var allChips = Array.prototype.slice.call(card.querySelectorAll(".bsq-chip"));

      function updateCheckBtn(){
        checkBtn.disabled = bank.querySelector(".bsq-chip") !== null;
      }
      function lock(){
        allChips.forEach(function(c){ c.disabled = true; });
        checkBtn.hidden = true;
      }
      function reveal(ok){
        card.classList.add(ok ? "correct" : "wrong");
        model.textContent = (ok ? "✓ " : "Resposta: ") + (card.dataset.sentence || correct.join(" "));
        fb.hidden = false;
        lock();
      }

      allChips.forEach(function(chip){
        chip.addEventListener("click", function(){
          if(chip.disabled) return;
          if(chip.parentNode === bank) build.appendChild(chip);
          else bank.appendChild(chip);
          updateCheckBtn();
          state[num] = { order: frags(build), checked: false };
          persist();
        });
      });

      checkBtn.addEventListener("click", function(){
        var assembled = frags(build);
        var ok = assembled.length === correct.length &&
          assembled.every(function(f, i){ return f === correct[i]; });
        state[num] = { order: assembled, checked: true, ok: ok };
        persist();
        reveal(ok);
        renderSummary();
      });

      // restaura estado salvo
      var s = state[num];
      if(s && s.order && s.order.length){
        var pool = allChips.slice();
        s.order.forEach(function(f){
          for(var k = 0; k < pool.length; k++){
            if(pool[k].dataset.frag === f){ build.appendChild(pool[k]); pool.splice(k, 1); break; }
          }
        });
        updateCheckBtn();
        if(s.checked) reveal(!!s.ok);
      }else{
        shuffle(allChips);
      }
    });

    var retry = root.querySelector(".quiz-retry");
    if(retry){
      retry.addEventListener("click", function(){
        state = {}; persist();
        location.reload();
      });
    }
    renderSummary();
  });

  // ---------- Flashcards com revisão espaçada (M6) ----------
  Array.prototype.forEach.call(document.querySelectorAll(".srs"), function(root){
    var deckId = root.dataset.srs;
    var lsKey = "toefl_srs_" + deckId + "_v1";
    var cards;
    try { cards = JSON.parse(root.querySelector(".srs-data").textContent); }
    catch(e){ return; }

    var DAY = 86400000;
    var INTERVAL_DAYS = [0, 1, 3, 7, 16, 30]; // por box (0..5)
    var byWord = {};
    cards.forEach(function(c){ byWord[c.w] = c; });

    var state = {};
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }
    function persist(){ safeSet(lsKey, JSON.stringify(state)); }

    var cardEl = root.querySelector(".srs-card");
    var frontEl = root.querySelector(".srs-front");
    var backEl = root.querySelector(".srs-back");
    var doneEl = root.querySelector(".srs-done");
    var flipBtn = root.querySelector(".srs-flip");
    var fWord = frontEl.querySelector(".srs-word");
    var fCat = frontEl.querySelector(".srs-cat");
    var bWord = backEl.querySelector(".srs-word");
    var bPt = backEl.querySelector(".srs-pt");
    var bSyn = backEl.querySelector(".srs-syn");
    var bEx = backEl.querySelector(".srs-ex");
    var elNew = root.querySelector(".srs-new");
    var elDue = root.querySelector(".srs-due");
    var elMastered = root.querySelector(".srs-mastered");
    var elCount = root.querySelector(".srs-count");
    var elQueued = root.querySelector(".srs-queued");
    var doneMsg = root.querySelector(".srs-done-msg");

    var queue = [], reviewed = 0;

    function updateStats(){
      var now = Date.now(), nw = 0, due = 0, mastered = 0;
      cards.forEach(function(c){
        var s = state[c.w];
        if(!s){ nw++; return; }
        if(s.box >= 4) mastered++;
        if(s.due <= now) due++;
      });
      elNew.textContent = nw;
      elDue.textContent = due;
      elMastered.textContent = mastered;
    }

    function buildQueue(all){
      var now = Date.now();
      var dueCards = [], newCards = [];
      cards.forEach(function(c){
        var s = state[c.w];
        if(!s) newCards.push(c);
        else if(all || s.due <= now) dueCards.push(c);
      });
      dueCards.sort(function(a, b){ return (state[a.w].due) - (state[b.w].due); });
      // intercala novas com revisões, começando pelas revisões
      queue = dueCards.concat(newCards);
    }

    function showFront(){ frontEl.hidden = false; backEl.hidden = true; }
    function showBack(){ frontEl.hidden = true; backEl.hidden = false; }

    function renderCard(){
      elCount.textContent = reviewed;
      elQueued.textContent = reviewed + queue.length;
      if(!queue.length){
        cardEl.hidden = true;
        doneEl.hidden = false;
        doneMsg.innerHTML = reviewed
          ? "Sessão concluída. <b>" + reviewed + "</b> cartões revisados."
          : "Nada para revisar agora. Tudo em dia!";
        return;
      }
      cardEl.hidden = false;
      doneEl.hidden = true;
      var c = queue[0];
      fWord.textContent = c.w; fCat.textContent = c.cat || "";
      bWord.textContent = c.w;
      bPt.textContent = c.pt;
      bSyn.textContent = c.syn ? "≈ " + c.syn : "";
      bEx.textContent = c.ex || "";
      showFront();
    }

    function grade(g){
      var c = queue.shift();
      var s = state[c.w] || { box: 0, due: 0 };
      if(g === 0) s.box = 0;
      else if(g === 1) s.box = Math.max(1, s.box);
      else s.box = Math.min(5, (s.box || 0) + 1);
      var days = INTERVAL_DAYS[s.box];
      s.due = Date.now() + days * DAY;
      state[c.w] = s;
      persist();
      reviewed++;
      if(g === 0) queue.push(c); // erra: volta ao fim da fila desta sessão
      updateStats();
      renderCard();
    }

    flipBtn.addEventListener("click", showBack);
    Array.prototype.forEach.call(backEl.querySelectorAll(".srs-grades button"), function(b){
      b.addEventListener("click", function(){ grade(parseInt(b.dataset.g, 10)); });
    });
    root.querySelector(".srs-restart").addEventListener("click", function(){
      reviewed = 0;
      buildQueue(true);
      renderCard();
    });

    updateStats();
    buildQueue(false);
    renderCard();
  });

  // ---------- Contas + sincronização (Supabase) ----------
  (function(){
    var box = document.getElementById("authBox");
    if(!box) return;
    var cfg = window.ITOEFL_SUPABASE;
    if(!cfg || !cfg.url || !cfg.anonKey) return; // não configurado → app segue offline
    if(!window.supabase || !window.supabase.createClient){
      // configurado, mas a biblioteca não carregou (CDN bloqueado/offline)
      box.hidden = false;
      document.getElementById("authSignIn").hidden = true;
      var m = document.getElementById("authMsg");
      m.textContent = "Biblioteca do Supabase não carregou (sem internet ou CDN bloqueado). App em modo offline.";
      m.style.color = "var(--danger)";
      m.hidden = false;
      return;
    }
    box.hidden = false;

    var signInBtn = document.getElementById("authSignIn");
    var signedIn = document.getElementById("authIn");
    var emailEl = document.getElementById("authEmail");
    var avatarEl = document.getElementById("authAvatar");
    var avatarImgEl = document.getElementById("authAvatarImg");
    var avatarLetterEl = document.getElementById("authAvatarLetter");
    var avatarFileEl = document.getElementById("authAvatarFile");
    var avatarRemoveEl = document.getElementById("authAvatarRemove");
    var signOutBtn = document.getElementById("authSignOut");
    var msgEl = document.getElementById("authMsg");

    var AVATAR_KEY = "toefl_avatar_v1";
    function renderAvatar(email){
      if(avatarLetterEl) avatarLetterEl.textContent = (email || "?").trim().charAt(0).toUpperCase();
      var data = safeGet(AVATAR_KEY);
      var hasPhoto = !!data;
      if(avatarImgEl){
        if(hasPhoto){ avatarImgEl.src = data; }
        avatarImgEl.hidden = !hasPhoto;
      }
      if(avatarLetterEl) avatarLetterEl.hidden = hasPhoto;
      if(avatarRemoveEl) avatarRemoveEl.hidden = !hasPhoto;
    }
    function resizeAvatar(file, cb){
      var reader = new FileReader();
      reader.onload = function(){
        var img = new Image();
        img.onload = function(){
          var SIZE = 160;
          var canvas = document.createElement("canvas");
          canvas.width = SIZE; canvas.height = SIZE;
          var ctx = canvas.getContext("2d");
          var side = Math.min(img.width, img.height);
          var sx = (img.width - side) / 2, sy = (img.height - side) / 2;
          ctx.drawImage(img, sx, sy, side, side, 0, 0, SIZE, SIZE);
          cb(canvas.toDataURL("image/jpeg", 0.82));
        };
        img.onerror = function(){ cb(null); };
        img.src = reader.result;
      };
      reader.onerror = function(){ cb(null); };
      reader.readAsDataURL(file);
    }
    if(avatarEl && avatarFileEl){
      avatarEl.addEventListener("click", function(){ avatarFileEl.click(); });
      avatarFileEl.addEventListener("change", function(){
        var file = avatarFileEl.files && avatarFileEl.files[0];
        avatarFileEl.value = "";
        if(!file) return;
        // não barra por file.type (alguns navegadores/SO não preenchem o MIME
        // corretamente) — deixa o próprio <img> decidir se consegue decodificar
        resizeAvatar(file, function(dataUrl){
          if(!dataUrl){ msg("Não consegui ler essa imagem. Tente um JPG ou PNG.", "err"); return; }
          safeSet(AVATAR_KEY, dataUrl);
          if(safeGet(AVATAR_KEY) !== dataUrl){
            msg("Não consegui salvar a foto (armazenamento cheio ou bloqueado).", "err");
            return;
          }
          renderAvatar(emailEl.textContent);
          msg("Foto atualizada.", "ok");
        });
      });
    }
    if(avatarRemoveEl){
      avatarRemoveEl.addEventListener("click", function(e){
        e.stopPropagation();
        safeSet(AVATAR_KEY, "");
        renderAvatar(emailEl.textContent);
      });
    }

    var client = window.supabase.createClient(cfg.url, cfg.anonKey);
    var uid = null, pushTimer = null;

    function msg(text, kind){
      msgEl.textContent = text;
      msgEl.style.color = kind === "err" ? "var(--danger)"
        : kind === "ok" ? "var(--accent)" : "var(--ink-2)";
      msgEl.hidden = false;
      if(kind === "ok"){ setTimeout(function(){ msgEl.hidden = true; }, 3500); }
    }

    function collectSynced(){
      var out = {};
      try{
        for(var i = 0; i < localStorage.length; i++){
          var k = localStorage.key(i);
          if(isSyncedKey(k)) out[k] = localStorage.getItem(k);
        }
      }catch(e){}
      return out;
    }
    function applyBundle(bundle){
      var changed = 0;
      Object.keys(bundle || {}).forEach(function(k){
        if(!isSyncedKey(k)) return;
        if(localStorage.getItem(k) !== bundle[k]){
          try { localStorage.setItem(k, bundle[k]); changed++; } catch(e){}
        }
      });
      return changed;
    }

    function push(){
      if(!uid) return;
      var bundle = collectSynced();
      var stamp = new Date().toISOString();
      client.from("user_state")
        .upsert({ user_id: uid, state: bundle, updated_at: stamp }, { onConflict: "user_id" })
        .select("updated_at").single()
        .then(function(res){
          if(res.error){ msg("Falha ao salvar na nuvem.", "err"); return; }
          try {
            localStorage.setItem("toefl_sync_at", res.data.updated_at);
            localStorage.removeItem("toefl_dirty");
          } catch(e){}
          msg("Sincronizado.", "ok");
        });
    }
    function schedulePush(){
      if(pushTimer) clearTimeout(pushTimer);
      pushTimer = setTimeout(push, 2500);
    }

    function pull(){
      client.from("user_state").select("state, updated_at").eq("user_id", uid).maybeSingle()
        .then(function(res){
          if(res.error){ msg("Erro ao sincronizar.", "err"); return; }
          var dirty = safeGet("toefl_dirty") === "1";
          if(!res.data){
            push(); // nada na nuvem ainda → envia o que há neste dispositivo
            return;
          }
          var syncAt = safeGet("toefl_sync_at");
          if(dirty){
            // edições locais não enviadas ganham; mescla o resto da nuvem
            var merged = res.data.state || {};
            var local = collectSynced();
            Object.keys(local).forEach(function(k){ merged[k] = local[k]; });
            if(applyBundle(merged)){ /* nada visual — vamos empurrar merged */ }
            push();
          }else if(!syncAt || res.data.updated_at > syncAt){
            // nuvem mais recente que este dispositivo → aplica e recarrega
            var n = applyBundle(res.data.state || {});
            try { localStorage.setItem("toefl_sync_at", res.data.updated_at); } catch(e){}
            if(n > 0) location.reload();
          }
          // senão: já está em dia
        });
    }

    function goOnline(session){
      uid = session.user.id;
      emailEl.textContent = session.user.email || "conectado";
      renderAvatar(session.user.email);
      signInBtn.hidden = true;
      signedIn.hidden = false;
      onSyncedWrite = schedulePush;
      pull();
    }
    function goOffline(){
      uid = null;
      onSyncedWrite = null;
      signInBtn.hidden = false;
      signedIn.hidden = true;
    }

    signInBtn.addEventListener("click", function(){
      var email = window.prompt("Seu e-mail. Enviaremos um link de acesso:");
      if(!email) return;
      var redirect = location.href.split("#")[0].split("?")[0];
      client.auth.signInWithOtp({ email: email.trim(), options: { emailRedirectTo: redirect } })
        .then(function(res){
          msg(res.error ? ("Erro: " + res.error.message) : "Link enviado. Confira seu e-mail.",
              res.error ? "err" : "ok");
        });
    });
    signOutBtn.addEventListener("click", function(){
      client.auth.signOut().then(goOffline);
    });

    client.auth.onAuthStateChange(function(event, session){
      if(session && session.user) goOnline(session);
      else goOffline();
    });
    client.auth.getSession().then(function(res){
      if(res.data && res.data.session) goOnline(res.data.session);
    });
  })();
})();
