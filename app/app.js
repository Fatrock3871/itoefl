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
  var SYNC_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_avatar", "toefl_errlog_", "toefl_cert_"];
  function isSyncedKey(key){
    if(!key || key.indexOf("toefl_") !== 0) return false;
    for(var i = 0; i < SYNC_PREFIXES.length; i++){
      if(key.indexOf(SYNC_PREFIXES[i]) === 0) return true;
    }
    return false;
  }
  var onSyncedWrite = null; // atribuído pelo módulo de sync quando logado
  var forceSyncPush = null; // idem, mas sem debounce e devolvendo a Promise -- usado pelo reset de progresso, que precisa confirmar que a nuvem já ficou vazia antes de recarregar (senão o pull() do próximo load reidrata o estado antigo)

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
  // Só dois termos: claro/escuro — sem estado "sistema". Na primeira visita
  // (nada salvo ainda), usa a preferência do SO uma vez só como ponto de
  // partida; dali em diante é um alternador simples entre os dois.
  var themeIcons = {light:"☀️", dark:"🌙"};
  var themeLabels = {light:"Claro", dark:"Escuro"};

  function applyTheme(mode){
    root.setAttribute("data-theme", mode);
    themeIcon.textContent = themeIcons[mode];
    themeLabel.textContent = themeLabels[mode];
  }
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  var savedTheme = safeGet(LS_THEME) || (prefersDark ? "dark" : "light");
  applyTheme(savedTheme);
  themeBtn.addEventListener("click", function(){
    var cur = safeGet(LS_THEME) || savedTheme;
    var next = cur === "dark" ? "light" : "dark";
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

  // gravador e cronômetro só fazem sentido nos módulos de prática cronometrada
  // (Reading/Listening/Speaking/Writing/Simulados) — em módulos de referência
  // (registro, vocabulário, exam day, traps) e no diagnóstico eles só distraem
  var PRACTICE_MODULES = {mod1:1, mod2:1, mod3:1, mod4:1, mod7:1};
  var floatTools = document.querySelector(".float-tools");

  function showTab(key){
    tabBtns.forEach(function(b){ b.classList.toggle("active", b.dataset.tab === key); });
    if(floatTools) floatTools.hidden = !PRACTICE_MODULES[key];
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
    });
    var pct = totalAll ? Math.round(100*doneAll/totalAll) : 0;
    document.getElementById("opPct").textContent = pct + "%";
    document.getElementById("opFill").style.width = pct + "%";
    var opCount = document.getElementById("opCount");
    if(opCount) opCount.innerHTML = "<b>" + modsDone + "</b> de " + modOrder.length + " módulos concluídos";

    // curso inteiro concluído (todos os módulos + o quiz do último, já que o
    // gate de avanço só valida o módulo ANTERIOR ao entrar no próximo — o
    // último nunca passa por essa checagem sozinho)
    var lastMod = modOrder[modOrder.length - 1];
    var courseDone = modsDone === modOrder.length && moduleQuizPct(lastMod) >= 100;
    var certBtn = document.getElementById("certBtn");
    if(certBtn) certBtn.hidden = !courseDone;
    if(courseDone && !safeGet("toefl_cert_date_v1")){
      safeSet("toefl_cert_date_v1", new Date().toISOString());
    }

    // reflete no estado visual da sidebar: concluído (✓), atual, ou bloqueado (🔒).
    // o número do módulo fica sempre visível (mesmo bloqueado — o texto dos
    // módulos referencia "Módulo N" e precisa bater com o que aparece aqui);
    // só o "%" de progresso é escondido quando bloqueado, pra não parecer que
    // dá pra entrar só porque já tem progresso ali.
    tabBtns.forEach(function(b){
      var key = b.dataset.tab;
      var badgeEl = b.querySelector(".num-badge");
      var pbadgeEl = document.getElementById("badge-"+key);
      var done = (modPct[key] || 0) >= 100;
      var unlocked = isUnlocked(key);
      b.classList.toggle("done", done);
      b.classList.toggle("locked", !unlocked);
      if(badgeEl){
        badgeEl.textContent = done ? "✓" : badgeEl.dataset.n;
      }
      if(pbadgeEl){
        pbadgeEl.textContent = (unlocked && byMod[key] && byMod[key].total) ? modPct[key] + "%" : "";
      }
    });
    // mapa da jornada: done (✓) / reached (linha preenchida) / locked (🔒, mas
    // com o número sempre visível — mesma lógica da sidebar acima)
    journeyNodes.forEach(function(j){
      var key = j.dataset.tab;
      var done = (modPct[key] || 0) >= 100;
      var unlocked = isUnlocked(key);
      j.classList.toggle("done", done);
      j.classList.toggle("reached", unlocked);
      j.classList.toggle("locked", !unlocked);
      var dot = j.querySelector(".jdot");
      if(dot) dot.textContent = done ? "✓" : dot.dataset.n;
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

  // itens de múltipla seleção (data-multi="N" no .qcard): picked vira um
  // array de letras em vez de uma letra só; acerta se o CONJUNTO bate,
  // independente da ordem em que foram marcadas. Compartilhado entre os
  // widgets individuais e o painel de desempenho agregado (M0, Parte 4).
  function isMultiCard(card){ return !!card.dataset.multi; }
  function isCardCorrect(card, picked){
    if(isMultiCard(card)){
      var want = card.dataset.correct.split(",").map(function(s){ return s.trim(); }).sort();
      var got = (picked || []).slice().sort();
      return want.length === got.length && want.every(function(L, i){ return L === got[i]; });
    }
    return picked === card.dataset.correct;
  }

  // painel "Seu desempenho real até agora" (M0, Parte 4) — soma acertos
  // confirmados em todos os .quiz-drill cujo id começa com um prefixo
  // (mod1- = Reading, mod2- = Listening), sem depender de estar na aba certa
  function computeQuizAccuracy(prefix){
    var drills = Array.prototype.slice.call(document.querySelectorAll('.quiz-drill[data-drill^="' + prefix + '"]'));
    var total = 0, confirmed = 0, correct = 0;
    drills.forEach(function(drillEl){
      var st = {};
      try { st = JSON.parse(safeGet("toefl_quiz_" + drillEl.dataset.drill + "_v1") || "{}"); } catch(e){}
      Array.prototype.forEach.call(drillEl.querySelectorAll(".qcard"), function(card){
        total++;
        var s = st[card.dataset.num];
        if(s && s.confirmed){
          confirmed++;
          if(isCardCorrect(card, s.picked)) correct++;
        }
      });
    });
    return { total: total, confirmed: confirmed, correct: correct };
  }
  function renderLiveScoreSection(prefix, pctId, bandId, emptyText){
    var pctEl = document.getElementById(pctId);
    var bandEl = document.getElementById(bandId);
    if(!pctEl || !bandEl) return;
    var a = computeQuizAccuracy(prefix);
    if(a.confirmed === 0){
      pctEl.textContent = "—";
      bandEl.textContent = emptyText;
      return;
    }
    var pct = Math.round(100 * a.correct / a.confirmed);
    var band = cefrBandFromPct(pct);
    pctEl.textContent = pct + "%";
    bandEl.textContent = "Banda " + band.code + " (" + band.label + ") · " + a.correct + "/" + a.confirmed + " confirmadas" +
      (a.confirmed < a.total ? " de " + a.total + " no total" : "");
  }
  function updateLiveScorePanel(){
    renderLiveScoreSection("mod1-", "liveScoreReadingPct", "liveScoreReadingBand", "Responda os Action Drills do Módulo 1 para calcular");
    renderLiveScoreSection("mod2-", "liveScoreListeningPct", "liveScoreListeningBand", "Responda os Action Drills do Módulo 2 para calcular");
  }

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
          if(isCardCorrect(card, s.picked)) correct++;
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
      if(drillId.indexOf("mod1-") === 0 || drillId.indexOf("mod2-") === 0){
        updateLiveScorePanel();
      }
    }

    function applyCardState(card){
      var num = card.dataset.num;
      var s = state[num];
      var multi = isMultiCard(card);
      var need = multi ? parseInt(card.dataset.multi, 10) : 1;
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
        var pickedList = multi ? (s.picked || []) : (s.picked ? [s.picked] : []);
        opts.forEach(function(o){
          o.disabled = false;
          o.classList.toggle("picked", pickedList.indexOf(o.dataset.letter) !== -1);
        });
        if(confirmBtn){ confirmBtn.hidden = false; confirmBtn.disabled = pickedList.length !== need; }
        if(fb) fb.hidden = true;
      } else {
        var wantSet = multi ? card.dataset.correct.split(",").map(function(x){ return x.trim(); }) : [card.dataset.correct];
        var gotSet = multi ? (s.picked || []) : [s.picked];
        opts.forEach(function(o){
          o.disabled = true;
          o.classList.remove("picked");
          var L = o.dataset.letter;
          if(wantSet.indexOf(L) !== -1) o.classList.add("correct");
          else if(gotSet.indexOf(L) !== -1) o.classList.add("wrong");
        });
        if(confirmBtn){ confirmBtn.hidden = true; }
        if(fb) fb.hidden = false;
      }
    }

    qcards.forEach(function(card){
      var num = card.dataset.num;
      var multi = isMultiCard(card);
      var need = multi ? parseInt(card.dataset.multi, 10) : 1;
      var opts = Array.prototype.slice.call(card.querySelectorAll(".opt"));
      var confirmBtn = card.querySelector(".qconfirm");

      opts.forEach(function(o){
        o.addEventListener("click", function(){
          var s = state[num];
          if(s && s.confirmed) return; // already revealed, locked
          if(multi){
            var cur = (state[num] && state[num].picked) || [];
            var L = o.dataset.letter;
            var idx = cur.indexOf(L);
            if(idx !== -1){ cur = cur.slice(0, idx).concat(cur.slice(idx + 1)); }
            else if(cur.length < need){ cur = cur.concat([L]); }
            state[num] = { picked: cur, confirmed: false };
          } else {
            state[num] = { picked: o.dataset.letter, confirmed: false };
          }
          saveState();
          applyCardState(card);
        });
      });

      if(confirmBtn){
        confirmBtn.addEventListener("click", function(){
          var s = state[num];
          var pickedCount = s ? (multi ? (s.picked || []).length : (s.picked ? 1 : 0)) : 0;
          if(pickedCount !== need) return;
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
  // setDrillTimerMinutes fica exposta fora da IIFE pro botão "iniciar
  // cronômetro" de cada Action Drill (mais abaixo) poder carregar o alvo
  // específico daquele drill, sem duplicar a lógica do widget.
  var setDrillTimerMinutes = null;
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

    setDrillTimerMinutes = function(mins){
      minutes = mins;
      safeSet(LS_PRESET, String(mins));
      markPreset(); // nenhum preset padrão bate com o alvo do drill — fica sem destaque, esperado
      reset();
      wrap.classList.remove("collapsed");
      if(wrap.scrollIntoView) wrap.scrollIntoView({behavior:"smooth", block:"nearest"});
    };

    markPreset();
    render();
  })();

  // ---------- Botão "iniciar cronômetro" em cada Action Drill ----------
  // Lê o "alvo: N min" que já existe no título do drill (mesmo texto que o
  // conteúdo sempre teve) e carrega esse valor no cronômetro flutuante —
  // sem duplicar o alvo em nenhum lugar novo.
  (function(){
    if(!setDrillTimerMinutes) return;
    Array.prototype.forEach.call(document.querySelectorAll(".quiz-drill"), function(drillEl){
      var node = drillEl.previousElementSibling;
      while(node && node.tagName !== "H3"){ node = node.previousElementSibling; }
      if(!node) return;
      var m = node.textContent.match(/alvo:\s*(\d+)\s*min/i);
      if(!m) return;
      var mins = parseInt(m[1], 10);
      if(!mins) return;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "drill-timer-btn";
      btn.textContent = "⏱ Iniciar cronômetro (" + mins + " min)";
      btn.addEventListener("click", function(){ setDrillTimerMinutes(mins); });
      node.parentNode.insertBefore(btn, node.nextSibling);
    });
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

    // ---- Reiniciar todo o progresso ----
    // não usa onSyncedWrite (debounced, 2.5s) porque recarregamos a página
    // logo em seguida -- se o push ainda não tivesse terminado, o pull() do
    // próximo load acharia a nuvem "mais nova" (com o progresso antigo) e
    // reidrataria tudo de volta. forceSyncPush() é a versão sem debounce,
    // e só recarrega depois que ela resolve (ou imediatamente se offline).
    var resetBtn = document.getElementById("resetBtn");
    if(resetBtn){
      var RESET_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_errlog_", "toefl_cert_"];
      resetBtn.addEventListener("click", function(){
        var ok = window.confirm(
          "Isso apaga TODO o seu progresso no curso (checkboxes, questões respondidas, " +
          "flashcards, frases escritas, registro de erros) e não pode ser desfeito. Continuar?"
        );
        if(!ok) return;
        var keys = [];
        try{
          for(var i = 0; i < localStorage.length; i++){
            var k = localStorage.key(i);
            if(k && RESET_PREFIXES.some(function(p){ return k.indexOf(p) === 0; })) keys.push(k);
          }
        }catch(e){}
        keys.forEach(function(k){ try{ localStorage.removeItem(k); }catch(e){} });
        try{ localStorage.setItem("toefl_dirty", "1"); }catch(e){}

        function finishReset(){
          flash("Progresso reiniciado. Recarregando…");
          setTimeout(function(){ location.reload(); }, 600);
        }
        if(typeof forceSyncPush === "function"){
          try{
            var p = forceSyncPush();
            if(p && typeof p.then === "function") p.then(finishReset, finishReset);
            else finishReset();
          }catch(e){ finishReset(); }
        } else {
          finishReset();
        }
      });
    }
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
    var gateEl = document.getElementById("authGate");
    if(!box) return;
    var cfg = window.ITOEFL_SUPABASE;
    if(!cfg || !cfg.url || !cfg.anonKey) return; // não configurado → app segue offline (gate já vem hidden do build)
    if(!window.supabase || !window.supabase.createClient){
      // configurado, mas a biblioteca não carregou (CDN bloqueado/offline) —
      // uma falha de rede não pode trancar o aluno fora do próprio conteúdo
      if(gateEl) gateEl.hidden = true;
      box.hidden = false;
      var m = document.getElementById("authMsg");
      m.textContent = "Biblioteca do Supabase não carregou (sem internet ou CDN bloqueado). App em modo offline.";
      m.style.color = "var(--danger)";
      m.hidden = false;
      return;
    }
    box.hidden = false;

    var gateMsgEl = document.getElementById("authGateMsg");
    function gateMsg(text, kind){
      if(!gateMsgEl) return;
      gateMsgEl.textContent = text;
      if(kind === "err"){
        gateMsgEl.style.color = "var(--danger)";
        gateMsgEl.style.background = "var(--danger-wash)";
        gateMsgEl.style.borderColor = "var(--danger)";
      } else {
        gateMsgEl.style.color = "var(--ink-2)";
        gateMsgEl.style.background = "var(--bg)";
        gateMsgEl.style.borderColor = "var(--hair)";
      }
      gateMsgEl.hidden = false;
    }

    var googleBtn = document.getElementById("authSignInGoogle");
    var signedIn = document.getElementById("authIn");
    var emailEl = document.getElementById("authEmail");
    // formulário de usuário+senha (substitui o antigo link mágico por e-mail)
    var loginForm = document.getElementById("loginForm");
    var signupForm = document.getElementById("signupForm");
    var resetPasswordForm = document.getElementById("resetPasswordForm");
    var authTabs = document.getElementById("authTabs");
    var authGateForms = [loginForm, signupForm, resetPasswordForm, document.getElementById("authLinks"),
      document.getElementById("authGateDivider"), document.getElementById("authGateGoogleWrap"),
      document.getElementById("authTabs")];
    var authGateTitle = document.getElementById("authGateTitle");
    var authGateSubtitle = document.getElementById("authGateSubtitle");
    var authGateKicker = document.getElementById("authGateKicker");
    var PENDING_USERNAME_KEY = "toefl_pending_username";
    var avatarEl = document.getElementById("authAvatar");
    var avatarImgEl = document.getElementById("authAvatarImg");
    var avatarLetterEl = document.getElementById("authAvatarLetter");
    var avatarFileEl = document.getElementById("authAvatarFile");
    var avatarRemoveEl = document.getElementById("authAvatarRemove");
    var signOutBtn = document.getElementById("authSignOut");
    var msgEl = document.getElementById("authMsg");

    var AVATAR_KEY = "toefl_avatar_v1";
    var googleAvatarUrl = null; // foto da conta Google logada (se veio por esse provedor)
    function extractGoogleAvatar(session){
      var meta = (session && session.user && session.user.user_metadata) || {};
      var url = meta.avatar_url || meta.picture || null;
      if(!url) return null;
      // o Google costuma devolver uma miniatura pequena (ex.: "=s96-c" no
      // fim da URL) — pede uma versão maior pra não borrar/encolher dentro
      // do avatar do site, que é bem maior que 96px
      if(/googleusercontent\.com/.test(url)){
        url = /=s\d+-c$/.test(url) ? url.replace(/=s\d+-c$/, "=s256-c") : url + "=s256-c";
      }
      return url;
    }
    function renderAvatar(email){
      if(avatarLetterEl) avatarLetterEl.textContent = (email || "?").trim().charAt(0).toUpperCase();
      var custom = safeGet(AVATAR_KEY);
      var src = custom || googleAvatarUrl || null;
      var hasPhoto = !!src;
      if(avatarImgEl){
        if(hasPhoto){ avatarImgEl.src = src; }
        avatarImgEl.hidden = !hasPhoto;
      }
      if(avatarLetterEl) avatarLetterEl.hidden = hasPhoto;
      // o "x" só remove a foto enviada manualmente — a do Google volta a
      // aparecer sozinha (não tem o que "remover" nela por aqui)
      if(avatarRemoveEl) avatarRemoveEl.hidden = !custom;
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

    // ---- acesso pago (2026-09-17) ----
    // conta admin sempre passa direto, sem checar entitlements -- pedido
    // explícito do usuário ("eu tenho acesso ilimitado com minha conta")
    var ADMIN_EMAIL = "pietrooliveiramarquespp@gmail.com";
    var payGateEl = document.getElementById("payGate");
    var payBtn = document.getElementById("payBtn");
    var payGateMsgEl = document.getElementById("payGateMsg");
    var paySignOutBtn = document.getElementById("paySignOut");
    function payGateMsg(text, kind){
      if(!payGateMsgEl) return;
      payGateMsgEl.textContent = text;
      if(kind === "err"){
        payGateMsgEl.style.color = "var(--danger)";
        payGateMsgEl.style.background = "var(--danger-wash)";
        payGateMsgEl.style.borderColor = "var(--danger)";
      } else {
        payGateMsgEl.style.color = "var(--ink-2)";
        payGateMsgEl.style.background = "var(--bg)";
        payGateMsgEl.style.borderColor = "var(--hair)";
      }
      payGateMsgEl.hidden = false;
    }
    function isAdmin(session){
      return !!(session && session.user && session.user.email &&
        session.user.email.toLowerCase() === ADMIN_EMAIL.toLowerCase());
    }
    function checkEntitlement(session, attempt){
      if(!payGateEl) return;
      if(isAdmin(session)){ payGateEl.hidden = true; return; }
      client.from("entitlements").select("paid").eq("user_id", session.user.id).maybeSingle()
        .then(function(res){
          var paid = !!(res.data && res.data.paid);
          payGateEl.hidden = paid;
          if(paid) return;
          // volta de um checkout recém-aprovado: o webhook do Mercado Pago é
          // assíncrono e pode demorar alguns segundos a mais que o redirect
          // -- tenta de novo umas poucas vezes antes de deixar o aluno preso
          // olhando "não pago" logo depois de pagar de verdade
          var params = new URLSearchParams(location.search);
          if(params.get("mp") === "success" && (attempt || 0) < 6){
            payGateMsg("Pagamento recebido, confirmando acesso...", "ok");
            setTimeout(function(){ checkEntitlement(session, (attempt || 0) + 1); }, 2500);
          } else if(params.get("mp") === "success"){
            payGateMsg("O pagamento foi recebido mas a liberação está demorando. Atualize a página em alguns minutos.", "err");
          } else if(params.get("mp") === "pending"){
            payGateMsg("Pagamento pendente de confirmação.", "err");
          } else if(params.get("mp") === "failure"){
            payGateMsg("Pagamento não concluído. Tente novamente.", "err");
          }
        });
    }
    if(payBtn){
      payBtn.addEventListener("click", function(){
        payBtn.disabled = true;
        payGateMsg("Abrindo checkout...", "ok");
        client.functions.invoke("create-checkout", { body: { origin: location.origin } })
          .then(function(res){
            payBtn.disabled = false;
            if(res.error || !res.data || !res.data.url){
              payGateMsg("Erro ao abrir checkout: " + (res.error ? res.error.message : "resposta inválida"), "err");
              return;
            }
            location.href = res.data.url;
          });
      });
    }
    if(paySignOutBtn){
      paySignOutBtn.addEventListener("click", function(){ client.auth.signOut().then(goOffline); });
    }

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
      return client.from("user_state")
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

    function setGateFormsHidden(hidden){
      authGateForms.forEach(function(el){ if(el) el.hidden = hidden; });
    }
    function goOnline(session){
      uid = session.user.id;
      emailEl.textContent = session.user.email || "conectado";
      googleAvatarUrl = extractGoogleAvatar(session);
      renderAvatar(session.user.email);
      setGateFormsHidden(true);
      signedIn.hidden = false;
      if(gateEl) gateEl.hidden = true;
      checkEntitlement(session);
      checkUsername(session);
      onSyncedWrite = schedulePush;
      forceSyncPush = push;
      pull();
    }
    function goOffline(){
      uid = null;
      googleAvatarUrl = null;
      onSyncedWrite = null;
      forceSyncPush = null;
      setGateFormsHidden(false);
      showLoginView();
      signedIn.hidden = true;
      if(gateEl) gateEl.hidden = false;
      if(payGateEl) payGateEl.hidden = true;
    }

    // ---- login por usuário+senha (substitui o antigo link mágico) ----
    var AUTH_ERROR_MAP = {
      "Invalid login credentials": "Usuário ou senha incorretos.",
      "User already registered": "Já existe uma conta com esse e-mail.",
      "Password should be at least 6 characters": "A senha precisa ter pelo menos 6 caracteres.",
    };
    function friendlyError(message){ return AUTH_ERROR_MAP[message] || ("Erro: " + message); }

    var authTabLogin = document.getElementById("authTabLogin");
    var authTabSignup = document.getElementById("authTabSignup");

    function showLoginView(){
      loginForm.hidden = false; signupForm.hidden = true; resetPasswordForm.hidden = true;
      authTabs.hidden = false; authTabs.classList.remove("is-signup");
      authTabLogin.classList.add("is-active"); authTabSignup.classList.remove("is-active");
      document.getElementById("authLinks").hidden = false;
      document.getElementById("authGateDivider").hidden = false;
      document.getElementById("authGateGoogleWrap").hidden = false;
      authGateTitle.textContent = "Entre para continuar";
      authGateSubtitle.textContent = "Seu progresso fica salvo na sua conta e sincroniza entre dispositivos.";
      authGateKicker.textContent = "Acesso à plataforma";
    }
    function showSignupView(){
      loginForm.hidden = true; signupForm.hidden = false; resetPasswordForm.hidden = true;
      authTabs.hidden = false; authTabs.classList.add("is-signup");
      authTabSignup.classList.add("is-active"); authTabLogin.classList.remove("is-active");
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = false;
      document.getElementById("authGateGoogleWrap").hidden = false;
      authGateTitle.textContent = "Criar conta";
      authGateSubtitle.textContent = "O e-mail confirma que a conta é sua e serve pra recuperar usuário/senha depois.";
      authGateKicker.textContent = "Novo por aqui?";
    }
    function showResetPasswordView(){
      loginForm.hidden = true; signupForm.hidden = true; resetPasswordForm.hidden = false;
      authTabs.hidden = true;
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = true;
      document.getElementById("authGateGoogleWrap").hidden = true;
      authGateTitle.textContent = "Escolha uma nova senha";
      authGateSubtitle.textContent = "";
      authGateKicker.textContent = "Recuperação de senha";
      if(gateEl) gateEl.hidden = false; // aparece mesmo se o app estava "logado" na sessão de recuperação
    }

    loginForm.addEventListener("submit", function(e){
      e.preventDefault();
      var username = document.getElementById("loginUsername").value.trim();
      var password = document.getElementById("loginPassword").value;
      if(!username || !password) return;
      gateMsg("Entrando...", "ok");
      client.rpc("email_for_username", { uname: username }).then(function(res){
        if(res.error || !res.data){
          gateMsg("Usuário ou senha incorretos.", "err");
          return;
        }
        client.auth.signInWithPassword({ email: res.data, password: password }).then(function(r){
          if(r.error) gateMsg(friendlyError(r.error.message), "err");
        });
      });
    });

    signupForm.addEventListener("submit", function(e){
      e.preventDefault();
      var email = document.getElementById("signupEmail").value.trim();
      var username = document.getElementById("signupUsername").value.trim().toLowerCase();
      var password = document.getElementById("signupPassword").value;
      if(!/^[a-z0-9_]{3,20}$/.test(username)){
        gateMsg("Usuário: só letras minúsculas, números e _ (3 a 20 caracteres).", "err");
        return;
      }
      gateMsg("Criando conta...", "ok");
      client.rpc("email_for_username", { uname: username }).then(function(checkRes){
        if(checkRes.data){ gateMsg("Esse nome de usuário já está em uso.", "err"); return; }
        try { sessionStorage.setItem(PENDING_USERNAME_KEY, username); } catch(ex){}
        client.auth.signUp({ email: email, password: password }).then(function(res){
          if(res.error){ gateMsg(friendlyError(res.error.message), "err"); return; }
          if(res.data && res.data.session){
            gateMsg("Conta criada!", "ok"); // goOnline() cuida do resto via onAuthStateChange
            return;
          }
          // e-mail já cadastrado e confirmado: o Supabase responde como se tivesse
          // dado certo (pra não revelar quais e-mails já existem) mas não manda
          // nada e não cria identidade nova -- sem checar isso, o aviso de
          // "confira seu e-mail" mente pra quem já tem conta.
          var identities = res.data && res.data.user && res.data.user.identities;
          if(identities && identities.length === 0){
            try { sessionStorage.removeItem(PENDING_USERNAME_KEY); } catch(ex){}
            gateMsg("Esse e-mail já tem conta. Use a aba Entrar, ou clique em \"Esqueci minha senha\" se não lembrar a senha.", "err");
            return;
          }
          gateMsg("Conta criada! Confira seu e-mail para confirmar antes de entrar.", "ok");
        });
      });
    });

    // mostrar/ocultar senha em qualquer campo do gate
    document.querySelectorAll(".auth-eye").forEach(function(btn){
      btn.addEventListener("click", function(){
        var target = document.getElementById(btn.dataset.target);
        if(!target) return;
        var shown = target.type === "text";
        target.type = shown ? "password" : "text";
        btn.classList.toggle("is-shown", !shown);
        btn.textContent = shown ? "👁" : "🙈";
        btn.setAttribute("aria-label", shown ? "Mostrar senha" : "Ocultar senha");
      });
    });

    // checagem ao vivo do usuário de cadastro: formato primeiro, depois
    // disponibilidade (mesma RPC usada no submit, só que sem esperar o envio)
    var signupUsernameEl = document.getElementById("signupUsername");
    var signupUsernameHint = document.getElementById("signupUsernameHint");
    var usernameCheckSeq = 0;
    if(signupUsernameEl){
      signupUsernameEl.addEventListener("input", function(){
        var raw = signupUsernameEl.value.trim().toLowerCase();
        var seq = ++usernameCheckSeq;
        if(!raw){
          signupUsernameHint.textContent = "Letras, números e _, de 3 a 20 caracteres";
          signupUsernameHint.className = "auth-hint";
          return;
        }
        if(!/^[a-z0-9_]{3,20}$/.test(raw)){
          signupUsernameHint.textContent = "Só letras, números e _ (3 a 20 caracteres)";
          signupUsernameHint.className = "auth-hint is-bad";
          return;
        }
        signupUsernameHint.textContent = "Verificando disponibilidade...";
        signupUsernameHint.className = "auth-hint";
        setTimeout(function(){
          if(seq !== usernameCheckSeq) return; // usuário já digitou de novo, descarta
          client.rpc("email_for_username", { uname: raw }).then(function(res){
            if(seq !== usernameCheckSeq) return;
            if(res.data){
              signupUsernameHint.textContent = "Esse nome de usuário já está em uso";
              signupUsernameHint.className = "auth-hint is-bad";
            } else {
              signupUsernameHint.textContent = "Disponível";
              signupUsernameHint.className = "auth-hint is-ok";
            }
          });
        }, 450);
      });
    }

    // medidor de força da senha de cadastro (só feedback visual, não bloqueia envio)
    var signupPasswordEl = document.getElementById("signupPassword");
    var signupStrengthEl = document.getElementById("signupStrength");
    var signupStrengthFill = document.getElementById("signupStrengthFill");
    var signupStrengthLabel = document.getElementById("signupStrengthLabel");
    if(signupPasswordEl){
      signupPasswordEl.addEventListener("input", function(){
        var val = signupPasswordEl.value;
        if(!val){ signupStrengthEl.hidden = true; return; }
        signupStrengthEl.hidden = false;
        var variety = (/[a-z]/.test(val) ? 1 : 0) + (/[A-Z]/.test(val) ? 1 : 0) +
          (/[0-9]/.test(val) ? 1 : 0) + (/[^a-zA-Z0-9]/.test(val) ? 1 : 0);
        var score = (val.length >= 6 ? 1 : 0) + (val.length >= 10 ? 1 : 0) + (variety >= 2 ? 1 : 0) + (variety >= 3 ? 1 : 0);
        var levels = [
          { pct: "20%", color: "var(--danger)", label: "Fraca" },
          { pct: "45%", color: "var(--danger)", label: "Fraca" },
          { pct: "65%", color: "var(--accent-2)", label: "Ok" },
          { pct: "85%", color: "var(--accent)", label: "Boa" },
          { pct: "100%", color: "var(--accent-strong)", label: "Forte" }
        ];
        var lvl = levels[Math.min(score, 4)];
        signupStrengthFill.style.width = lvl.pct;
        signupStrengthFill.style.background = lvl.color;
        signupStrengthLabel.textContent = lvl.label;
      });
    }

    resetPasswordForm.addEventListener("submit", function(e){
      e.preventDefault();
      var newPassword = document.getElementById("newPassword").value;
      if(!newPassword || newPassword.length < 6) return;
      gateMsg("Salvando...", "ok");
      client.auth.updateUser({ password: newPassword }).then(function(res){
        if(res.error){ gateMsg(friendlyError(res.error.message), "err"); return; }
        gateMsg("Senha atualizada! Entrando...", "ok");
        showLoginView();
      });
    });

    document.getElementById("forgotPasswordLink").addEventListener("click", function(){
      var email = window.prompt("Seu e-mail. Enviaremos um link pra você escolher uma nova senha:");
      if(!email) return;
      var redirect = location.href.split("#")[0].split("?")[0];
      client.auth.resetPasswordForEmail(email.trim(), { redirectTo: redirect }).then(function(res){
        gateMsg(res.error ? friendlyError(res.error.message) : "Link enviado. Confira seu e-mail.",
          res.error ? "err" : "ok");
      });
    });
    document.getElementById("forgotUsernameLink").addEventListener("click", function(){
      var email = window.prompt("Seu e-mail. Enviaremos um link de acesso — ao entrar, seu usuário aparece na barra do topo:");
      if(!email) return;
      var redirect = location.href.split("#")[0].split("?")[0];
      client.auth.signInWithOtp({ email: email.trim(), options: { emailRedirectTo: redirect } }).then(function(res){
        gateMsg(res.error ? friendlyError(res.error.message) : "Link enviado. Confira seu e-mail.",
          res.error ? "err" : "ok");
      });
    });
    authTabLogin.addEventListener("click", showLoginView);
    authTabSignup.addEventListener("click", showSignupView);

    if(googleBtn){
      googleBtn.addEventListener("click", function(){
        var redirect = location.href.split("#")[0].split("?")[0];
        client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: redirect } })
          .then(function(res){
            // sucesso: o navegador é redirecionado pro Google, não sobra nada pra fazer aqui
            if(res.error) gateMsg("Erro: " + res.error.message, "err");
          });
      });
    }
    signOutBtn.addEventListener("click", function(){
      client.auth.signOut().then(goOffline);
    });

    // ---- nome de usuário: aplica o escolhido no cadastro assim que a conta
    // tem sessão ativa (pode não ter tido sessão no momento do signUp, se a
    // confirmação por e-mail estiver ligada) e mostra o usuário (em vez do
    // e-mail cru) na barra do topo assim que ele existir -- é também como
    // "esqueci meu usuário" se resolve: a pessoa entra por qualquer método
    // e o nome aparece aqui, sem precisar de um e-mail separado pra isso.
    function checkUsername(session){
      client.from("profiles").select("username").eq("id", session.user.id).maybeSingle().then(function(res){
        var current = res.data && res.data.username;
        if(current){ emailEl.textContent = current; return; }
        var pending = null;
        try { pending = sessionStorage.getItem(PENDING_USERNAME_KEY); } catch(ex){}
        if(!pending) return;
        client.from("profiles").update({ username: pending }).eq("id", session.user.id).then(function(upd){
          if(upd.error) return;
          try { sessionStorage.removeItem(PENDING_USERNAME_KEY); } catch(ex){}
          emailEl.textContent = pending;
        });
      });
    }

    client.auth.onAuthStateChange(function(event, session){
      if(event === "PASSWORD_RECOVERY"){ showResetPasswordView(); return; }
      if(session && session.user) goOnline(session);
      else goOffline();
    });
    client.auth.getSession().then(function(res){
      if(res.data && res.data.session) goOnline(res.data.session);
    });
  })();

  // ---------- Certificado de conclusão (nada oficial) ----------
  (function(){
    var btn = document.getElementById("certBtn");
    var modal = document.getElementById("certModal");
    if(!btn || !modal) return;
    var backdrop = document.getElementById("certModalBackdrop");
    var closeBtn = document.getElementById("certClose");
    var printBtn = document.getElementById("certPrint");
    var nameEl = document.getElementById("certName");
    var dateEl = document.getElementById("certDate");

    function fmtDate(iso){
      try{
        var d = new Date(iso);
        return d.toLocaleDateString("pt-BR", { day:"2-digit", month:"long", year:"numeric" });
      }catch(e){ return ""; }
    }
    function open(){
      var email = document.getElementById("authEmail");
      var name = (email && email.textContent.trim()) ? email.textContent.trim().split("@")[0] : "Aluno(a) iTOEFL";
      nameEl.textContent = name;
      var iso = safeGet("toefl_cert_date_v1");
      dateEl.textContent = iso ? "Concluído em " + fmtDate(iso) : "";
      modal.hidden = false;
      document.body.classList.add("menu-open"); // reaproveita o travamento de scroll do drawer
    }
    function close(){
      modal.hidden = true;
      document.body.classList.remove("menu-open");
    }
    btn.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !modal.hidden) close(); });
    printBtn.addEventListener("click", function(){ window.print(); });
  })();

  // ---------- Registro de erros (formulário por módulo) ----------
  // Cada .errlog guarda um histórico em toefl_errlog_<mod>_v1 (sincroniza
  // como o resto do progresso). Substitui o template de texto antigo
  // ("preencha à mão em outro lugar") por um formulário que já soma
  // frequência por código — o mesmo aviso que o conteúdo já dava ("código
  // que aparece 3+ vezes é prioridade") passa a ser calculado, não lido.
  (function(){
    var panels = Array.prototype.slice.call(document.querySelectorAll(".errlog"));
    panels.forEach(function(panel){
      var modKey = panel.dataset.errlog;
      var lsKey = "toefl_errlog_" + modKey + "_v1";
      var form = panel.querySelector(".errlog-form");
      var dateEl = panel.querySelector(".errlog-date");
      var drillEl = panel.querySelector(".errlog-drill");
      var resultEl = panel.querySelector(".errlog-result");
      var historyEl = panel.querySelector(".errlog-history");
      var listEl = panel.querySelector(".errlog-list");
      var freqEl = panel.querySelector(".errlog-freq");

      function load(){
        try { return JSON.parse(safeGet(lsKey) || "[]"); } catch(e){ return []; }
      }
      function save(entries){ safeSet(lsKey, JSON.stringify(entries)); }

      function render(){
        var entries = load();
        historyEl.hidden = entries.length === 0;
        if(!entries.length) return;

        var freq = {};
        entries.forEach(function(e){
          (e.codes || []).forEach(function(c){ freq[c] = (freq[c] || 0) + 1; });
        });
        var hot = Object.keys(freq).filter(function(c){ return freq[c] >= 3; }).sort(function(a,b){ return freq[b]-freq[a]; });
        freqEl.textContent = hot.length ? "· prioridade: " + hot.map(function(c){ return c + " (" + freq[c] + "×)"; }).join(", ") : "";

        listEl.innerHTML = "";
        entries.forEach(function(entry, idx){
          var row = document.createElement("div");
          row.className = "errlog-entry";
          var codesTxt = (entry.codes || []).join(", ");
          row.innerHTML =
            '<span class="errlog-entry-date">' + (entry.date || "—") + '</span>' +
            '<span class="errlog-entry-drill">' + (entry.drill || "—") + '</span>' +
            '<span class="errlog-entry-result">' + (entry.result || "—") + '</span>' +
            '<span class="errlog-entry-codes">' + (codesTxt || "sem código") + '</span>' +
            '<button type="button" class="errlog-entry-del" aria-label="Remover registro">✕</button>';
          row.querySelector(".errlog-entry-del").addEventListener("click", function(){
            var cur = load();
            cur.splice(idx, 1);
            save(cur);
            render();
          });
          listEl.appendChild(row);
        });
      }

      if(form){
        form.addEventListener("submit", function(e){
          e.preventDefault();
          var codes = Array.prototype.slice.call(panel.querySelectorAll(".errlog-code input:checked")).map(function(i){ return i.value; });
          var entries = load();
          entries.unshift({
            date: dateEl.value || new Date().toISOString().slice(0, 10),
            drill: drillEl.value.trim(),
            result: resultEl.value.trim(),
            codes: codes,
          });
          save(entries);
          form.reset();
          render();
        });
      }

      render();
    });
  })();

  // ---------- Accordion por subseção (h3) dentro de cada parte ----------
  // Cada h3 de conteúdo (não os títulos dos próprios drills/widgets
  // interativos, que ficam sempre visíveis) vira clicável pra esconder/
  // mostrar o que vem depois dele, até o próximo h3. Nada fica escondido
  // por padrão — só dá a opção de recolher o que já foi lido; ajuda em
  // partes longas (Laboratório de Língua, Gabaritos extensos) e em telas
  // pequenas. Roda por último de propósito: outros passes (botão de
  // cronômetro por drill, índice "Nesta parte") contam com a posição
  // original dos elementos em relação aos h3/h2.
  (function(){
    var cards = Array.prototype.slice.call(document.querySelectorAll(".section-card"));
    cards.forEach(function(card){
      var h3s = Array.prototype.slice.call(card.children).filter(function(n){ return n.tagName === "H3"; });
      h3s.forEach(function(h3){
        var nodes = [];
        var node = h3.nextSibling;
        while(node && !(node.nodeType === 1 && node.tagName === "H3")){
          nodes.push(node);
          node = node.nextSibling;
        }
        var hasWidget = nodes.some(function(n){
          return n.nodeType === 1 && (n.classList.contains("quiz-drill") || n.classList.contains("bsq") || n.querySelector(".quiz-drill, .bsq"));
        });
        if(hasWidget || !nodes.length) return;
        var body = document.createElement("div");
        body.className = "h3-body";
        nodes.forEach(function(n){ body.appendChild(n); });
        h3.parentNode.insertBefore(body, node);
        h3.classList.add("h3-toggle");
        h3.addEventListener("click", function(){
          h3.classList.toggle("collapsed");
          body.classList.toggle("h3-collapsed");
        });
      });
    });
  })();
})();
