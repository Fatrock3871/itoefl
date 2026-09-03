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
})();
