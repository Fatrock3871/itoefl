(function(){
  "use strict";
  // wrap tables so wide tables scroll inside themselves, not the page
  Array.prototype.slice.call(document.querySelectorAll(".panel table")).forEach(function(t){
    var wrap = document.createElement("div");
    wrap.className = "table-wrap";
    t.parentNode.insertBefore(wrap, t);
    wrap.appendChild(t);
  });

  // botão de pronúncia (🔊) nas tabelas de palavra/termo em inglês dos
  // módulos de pronúncia e vocabulário (M3, M6, M9). Usa a Web Speech API
  // do navegador (sem arquivo de áudio, sem dependência nova): lê o cabeçalho
  // de cada tabela e, se alguma coluna bater com a lista abaixo, adiciona o
  // botão na célula daquela coluna em cada linha. Cobre listas de uma
  // palavra por linha e também células com várias palavras separadas por
  // vírgula (a API já pausa nas vírgulas ao falar).
  var SPEAK_HEADER_WHITELIST = [
    "palavra", "palavra inglesa", "inglês", "verbo de alto impacto",
    "verbo âncora", "palavras de alto risco", "termo", "expressão"
    // "verbo" sozinho de propósito NÃO entra aqui: o mesmo cabeçalho aparece
    // em tabelas de concordância (M1/M4, "Sujeito | Verbo | Exemplo") cujas
    // células dizem coisa tipo "verbo + -s", não uma palavra pra pronunciar
  ];
  // escolhe a melhor voz em inglês disponível no navegador: as vozes "remotas"
  // (Google/Microsoft Online/Natural) soam bem menos robóticas que a voz local
  // padrão do sistema. getVoices() volta vazio até o evento voiceschanged em
  // vários navegadores, por isso o cache é invalidado quando ele dispara.
  var cachedVoice = null, voiceChecked = false;
  function pickVoice(){
    if(voiceChecked) return cachedVoice;
    if(!("speechSynthesis" in window)) return null;
    var voices = window.speechSynthesis.getVoices() || [];
    if(!voices.length) return null; // ainda não carregou -- tenta de novo na próxima fala
    voiceChecked = true;
    var enVoices = voices.filter(function(v){ return /^en/i.test(v.lang); });
    if(!enVoices.length) return null;
    var preferred = /google us english|natural|online|premium|aria|guy|jenny/i;
    cachedVoice =
      enVoices.find(function(v){ return /^en-us$/i.test(v.lang) && preferred.test(v.name); }) ||
      enVoices.find(function(v){ return preferred.test(v.name); }) ||
      enVoices.find(function(v){ return /^en-us$/i.test(v.lang); }) ||
      enVoices[0];
    return cachedVoice;
  }
  if("speechSynthesis" in window){
    window.speechSynthesis.getVoices();
    window.speechSynthesis.onvoiceschanged = function(){ voiceChecked = false; };
  }
  function speakText(text){
    if(!("speechSynthesis" in window)) return;
    try {
      window.speechSynthesis.cancel(); // corta qualquer fala anterior antes de começar a nova
      var utter = new SpeechSynthesisUtterance(text);
      utter.lang = "en-US";
      utter.rate = 0.93;
      utter.pitch = 1;
      var voice = pickVoice();
      if(voice) utter.voice = voice;
      window.speechSynthesis.speak(utter);
    } catch(ex){}
  }
  if("speechSynthesis" in window){
    var speakPanelsHit = {};
    Array.prototype.slice.call(document.querySelectorAll(".panel table")).forEach(function(table){
      var headCells = Array.prototype.slice.call(table.querySelectorAll("thead th"));
      // colIndexes (plural): algumas tabelas repetem o cabeçalho duas vezes
      // na mesma linha pra economizar espaço (ex.: "Verbo | Collocations |
      // Verbo | Collocations", duas colunas lado a lado) -- pegar só a
      // primeira ocorrência deixava a segunda coluna sem botão.
      var colIndexes = [];
      headCells.forEach(function(th, i){
        if(SPEAK_HEADER_WHITELIST.indexOf(th.textContent.trim().toLowerCase()) !== -1) colIndexes.push(i);
      });
      if(!colIndexes.length) return;
      var panel = table.closest(".panel");
      if(panel) speakPanelsHit[panel.id] = true;
      Array.prototype.slice.call(table.querySelectorAll("tbody tr")).forEach(function(row){
        colIndexes.forEach(function(colIndex){
          var cell = row.children[colIndex];
          var text = cell && cell.textContent.trim();
          if(!cell || !text) return;
          var btn = document.createElement("button");
          btn.type = "button";
          btn.className = "speak-btn";
          btn.setAttribute("aria-label", "Ouvir pronúncia de " + text);
          btn.textContent = "🔊";
          btn.addEventListener("click", function(){ speakText(text); });
          cell.appendChild(btn);
        });
      });
    });
    // avisa, uma vez no topo de cada módulo que usa o recurso, o que o
    // ícone significa -- sem isso o símbolo sozinho não é óbvio pra quem
    // nunca viu (M6 ganha o aviso mesmo sem tabela batendo o cabeçalho,
    // por causa do kit de flashcards SRS, que também tem o botão)
    speakPanelsHit["panel-mod6"] = true;
    Object.keys(speakPanelsHit).forEach(function(panelId){
      var panel = document.getElementById(panelId);
      var head = panel && panel.querySelector(".panel-head");
      if(!head || head.nextElementSibling && head.nextElementSibling.classList.contains("speak-hint")) return;
      var hint = document.createElement("div");
      hint.className = "speak-hint";
      hint.innerHTML = '<span class="speak-hint-icon" aria-hidden="true">🔊</span><span>Toque nesse ícone sempre que aparecer pra ouvir a pronúncia em inglês da palavra, caso fique com dúvida.</span>';
      head.parentNode.insertBefore(hint, head.nextSibling);
    });

    // Listening (M2): os drills viravam texto pra ler em silêncio -- esses
    // dois botões tocam o item/a passagem em voz alta (Web Speech API),
    // virando prática de ouvir de verdade em vez de leitura de transcrição.
    Array.prototype.slice.call(document.querySelectorAll(".quiz-item-speak")).forEach(function(btn){
      btn.addEventListener("click", function(){
        var textEl = btn.parentNode.querySelector(".qprompt-text");
        if(!textEl) return;
        var text = textEl.textContent.replace(/^Speaker:\s*/i, "").replace(/^"|"$/g, "");
        speakText(text);
      });
    });
    Array.prototype.slice.call(document.querySelectorAll(".quiz-passage-speak")).forEach(function(btn){
      btn.addEventListener("click", function(){
        var body = btn.parentNode.querySelector(".quiz-passage-body");
        if(!body) return;
        speakText(body.textContent);
      });
    });
  }

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

  // espelha o client do Supabase e o uid logado pra fora do bloco de auth
  // (que é seu próprio IIFE) -- o certificado precisa ler/gravar
  // profiles.display_name e não tinha como chegar em `client`/`uid` de lá
  var supaClient = null, supaUid = null;

  var LS_PROGRESS = "toefl_progress_v1";
  var LS_THEME = "toefl_theme_v1";
  var LS_QUIZ = "toefl_quiz_mod0_v1";

  // chaves que sincronizam com o Supabase (progresso real do aluno).
  // ficam de fora: toefl_theme_v1, toefl_active_tab, toefl_timer_preset, toefl_sync_*
  var SYNC_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_avatar", "toefl_errlog_", "toefl_cert_", "toefl_streak", "toefl_dailygoal", "toefl_weeklydash", "toefl_h3progress", "toefl_ctw_", "toefl_spk_", "toefl_write_"];
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
      if(key !== LS_STREAK) markStreakToday();
    }
  }

  // ---------- Sequência de dias estudando (streak) ----------
  // Marca o dia de hoje sempre que qualquer chave sincronizada é escrita
  // (checkbox de progresso, quiz, SRS, registro de erro etc.) -- ou seja,
  // qualquer atividade real de estudo, não só abrir o site. O guard de
  // "já marcado hoje" evita reescrever a cada tecla e evita recursão (marcar
  // o streak também passa por safeSet, que por sua vez chamaria
  // markStreakToday de novo se não fosse por isso).
  var LS_STREAK = "toefl_streak_v1";
  function todayStr(d){ return (d || new Date()).toISOString().slice(0, 10); }
  function markStreakToday(){
    var data = {}; try { data = JSON.parse(safeGet(LS_STREAK) || "{}"); } catch(e){}
    if(!data.days) data.days = {};
    var t = todayStr();
    if(data.days[t]) return;
    data.days[t] = true;
    var keys = Object.keys(data.days);
    if(keys.length > 400){ keys.sort(); delete data.days[keys[0]]; } // não guarda histórico infinito
    safeSet(LS_STREAK, JSON.stringify(data));
  }
  function computeStreak(){
    var data = {}; try { data = JSON.parse(safeGet(LS_STREAK) || "{}"); } catch(e){}
    var days = data.days || {};
    var cursor = new Date();
    if(!days[todayStr(cursor)]) cursor.setDate(cursor.getDate() - 1); // hoje ainda vazio: conta a partir de ontem, sem "quebrar" o streak antes da meia-noite
    var n = 0;
    while(days[todayStr(cursor)]){ n++; cursor.setDate(cursor.getDate() - 1); }
    return { count: n, today: !!days[todayStr(new Date())] };
  }

  // ---------- Meta diária (1 seção concluída por dia) ----------
  // Conta só transições de não-concluída -> concluída (ver o listener de
  // checkbox mais abaixo), então marcar/desmarcar a mesma seção repetidas
  // vezes no mesmo dia não infla o contador.
  var LS_DAILY_GOAL = "toefl_dailygoal_v1";
  var DAILY_GOAL_TARGET = 1;
  function markDailyGoalProgress(){
    var data = {}; try { data = JSON.parse(safeGet(LS_DAILY_GOAL) || "{}"); } catch(e){}
    var t = todayStr();
    if(data.date !== t){ data.date = t; data.count = 0; }
    data.count = (data.count || 0) + 1;
    safeSet(LS_DAILY_GOAL, JSON.stringify(data));
    updateDailyGoalUI();
  }
  function getDailyGoal(){
    var data = {}; try { data = JSON.parse(safeGet(LS_DAILY_GOAL) || "{}"); } catch(e){}
    var count = (data.date === todayStr()) ? (data.count || 0) : 0;
    return { count: count, target: DAILY_GOAL_TARGET, done: count >= DAILY_GOAL_TARGET };
  }
  function updateDailyGoalUI(){
    var g = getDailyGoal();
    var countEl = document.getElementById("dgCount");
    var fillEl = document.getElementById("dgFill");
    if(countEl) countEl.textContent = Math.min(g.count, g.target) + "/" + g.target;
    if(fillEl) fillEl.style.width = Math.min(100, Math.round(100 * g.count / g.target)) + "%";
  }
  updateDailyGoalUI();

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
  var accountThemeTabs = document.getElementById("accountThemeTabs");
  var accountThemeLight = document.getElementById("accountThemeLight");
  var accountThemeDark = document.getElementById("accountThemeDark");

  function applyTheme(mode){
    root.setAttribute("data-theme", mode);
    if(themeIcon) themeIcon.textContent = themeIcons[mode];
    if(themeLabel) themeLabel.textContent = themeLabels[mode];
    // espelha na aba "Aparência" da tela Minha conta, se ela existir
    if(accountThemeTabs){
      accountThemeTabs.classList.toggle("is-alt", mode === "dark");
      accountThemeLight.classList.toggle("is-active", mode === "light");
      accountThemeDark.classList.toggle("is-active", mode === "dark");
    }
  }
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  var savedTheme = safeGet(LS_THEME) || (prefersDark ? "dark" : "light");
  applyTheme(savedTheme);
  if(themeBtn) themeBtn.addEventListener("click", function(){
    var cur = safeGet(LS_THEME) || savedTheme;
    var next = cur === "dark" ? "light" : "dark";
    safeSet(LS_THEME, next);
    applyTheme(next);
  });
  if(accountThemeLight){
    accountThemeLight.addEventListener("click", function(){ safeSet(LS_THEME, "light"); applyTheme("light"); });
    accountThemeDark.addEventListener("click", function(){ safeSet(LS_THEME, "dark"); applyTheme("dark"); });
  }

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

  // navegação livre entre módulos (pedido do usuário, 2026-09-20): o curso
  // não bloqueia mais a ordem de acesso, só continua marcando/medindo a
  // conclusão de cada módulo (checkbox, badge ✓, % na sidebar/jornada,
  // certificado). isUnlocked() fica só por compatibilidade com o resto do
  // código (updateBadges ainda chama ela) -- sempre true agora.
  function isUnlocked(key){
    return true;
  }

  var journeyNodes = Array.prototype.slice.call(document.querySelectorAll(".jnode"));

  // ---------- Índice lateral ("Nesta parte") ----------
  // a classe .active já tinha estilo em styles.css mas nunca era ligada em
  // lugar nenhum -- o link da parte atual nunca destacava enquanto o aluno
  // rolava a página. IntersectionObserver resolve isso: marca .active no
  // link cujo H2 está mais perto do topo visível no momento.
  var railToc = document.getElementById("railToc");
  var railObserver = null;
  function setupRailScrollSpy(links){
    if(railObserver) railObserver.disconnect();
    if(!links.length || !("IntersectionObserver" in window)) return;
    railObserver = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(!entry.isIntersecting) return;
        var match = links.filter(function(l){ return l.heading === entry.target; })[0];
        if(!match) return;
        links.forEach(function(l){ l.link.classList.toggle("active", l === match); });
      });
    }, { rootMargin: "-10% 0px -75% 0px", threshold: 0 });
    links.forEach(function(l){ railObserver.observe(l.heading); });
  }
  function populateRailToc(key){
    if(!railToc) return;
    railToc.innerHTML = "";
    var panel = document.querySelector('.panel[data-panel="' + key + '"]');
    if(!panel) return;
    var heads = Array.prototype.slice.call(panel.querySelectorAll("h2[id]"));
    var links = [];
    heads.forEach(function(h, i){
      var label = h.querySelector(".htext");
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = label ? label.textContent : h.textContent;
      if(i === 0) a.classList.add("active"); // estado inicial, antes de rolar
      a.addEventListener("click", function(e){
        e.preventDefault();
        h.scrollIntoView({behavior:"smooth", block:"start"});
      });
      railToc.appendChild(a);
      links.push({ link: a, heading: h });
    });
    setupRailScrollSpy(links);
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
    setSidebarOpen(false); // navegar fecha a gaveta, que não deve ocupar espaço
    populateRailToc(key);
    // abre a primeira subseção (h3) do módulo que acabou de aparecer -- sem
    // isso a tela troca pra um módulo novo e mostra tudo fechado até o
    // aluno clicar ou rolar (o observer de scroll só cobre rolagem, não
    // troca de aba). No load inicial, antes do accordion existir (roda
    // numa IIFE mais abaixo), isso não acha nada e não faz nada -- tudo bem,
    // essa mesma IIFE abre a primeira seção do painel ativo quando monta.
    var activeH3 = document.querySelector('.panel[data-panel="' + key + '"] .h3-toggle');
    if(activeH3 && activeH3.classList.contains("collapsed")){
      activeH3.classList.remove("collapsed");
      var activeBody = activeH3.nextElementSibling;
      if(activeBody && activeBody.classList.contains("h3-body")) activeBody.classList.remove("h3-collapsed");
    }
  }
  function navTo(key){
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
      var phPct = document.getElementById("phPct-" + mod);
      var phFill = document.getElementById("phFill-" + mod);
      if(phPct) phPct.textContent = pctMod + "%";
      if(phFill) phFill.style.width = pctMod + "%";
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
      var wasChecked = progressState[pid];
      progressState[pid] = c.checked;
      if(c.checked && !wasChecked) markDailyGoalProgress();
      var card = c.closest(".section-card");
      if(card){
        card.classList.toggle("done", c.checked);
        // marcar a Parte como concluída fecha as subseções dela de volta
        // (economiza espaço na tela) -- ainda dá pra reabrir clicando
        if(c.checked){
          Array.prototype.slice.call(card.querySelectorAll(".h3-toggle")).forEach(function(h3){
            h3.classList.add("collapsed");
            var body = h3.nextElementSibling;
            if(body && body.classList.contains("h3-body")) body.classList.add("h3-collapsed");
          });
        }
      }
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

  // melhor estimativa disponível da banda CEFR atual do aluno: prioriza o
  // diagnóstico do Módulo 0 (se completo), senão usa o agregado dos Action
  // Drills de Reading/Listening já respondidos. Movida pro escopo
  // compartilhado (era local do modal do painel) pra também alimentar a
  // recomendação de nível nos Action Drills (ver IIFE "Nível recomendado").
  function computeBandEstimate(){
    var diag = computeQuizAccuracy("mod0-diag");
    if(diag.confirmed > 0 && diag.confirmed === diag.total){
      var pct = Math.round(100 * diag.correct / diag.confirmed);
      return { pct: pct, source: "diagnóstico do Módulo 0" };
    }
    var reading = computeQuizAccuracy("mod1-"), listening = computeQuizAccuracy("mod2-");
    var confirmed = reading.confirmed + listening.confirmed, correct = reading.correct + listening.correct;
    if(confirmed > 0){
      return { pct: Math.round(100 * correct / confirmed), source: "Action Drills de Reading/Listening" };
    }
    return null;
  }

  // Action Drills de nível diferente pra cada aluno: cada drill de M1/M2 tem
  // um nível CEFR (ver "level" em drills_data.py, ex. "B2–C1"). Marca como
  // "recomendado pra você" os que incluem a banda estimada atual do aluno,
  // sem esconder os outros -- navegação livre continua valendo (ver decisão
  // em CLAUDE.md), isso só destaca por onde começar.
  function updateLevelRecommendations(){
    var est = computeBandEstimate();
    if(!est) return; // sem diagnóstico/drills respondidos ainda, não dá pra recomendar nada
    var myLevel = cefrBandFromPct(est.pct).label; // ex. "B1"
    Array.prototype.slice.call(document.querySelectorAll(".quiz-drill[data-level]")).forEach(function(drillEl){
      var levels = drillEl.dataset.level.split(/[–-]/).map(function(s){ return s.trim(); });
      var lo = levels[0], hi = levels[levels.length - 1];
      var order = ["A1", "A2", "B1", "B2", "C1", "C2"];
      var match = order.indexOf(myLevel) >= order.indexOf(lo) && order.indexOf(myLevel) <= order.indexOf(hi);
      drillEl.classList.toggle("level-recommended", match);
      var badge = document.querySelector('[data-level-badge-for="' + drillEl.dataset.drill + '"]');
      if(badge) badge.classList.toggle("is-recommended", match);
    });
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
      if(drillId === "mod0-diag" || drillId.indexOf("mod1-") === 0 || drillId.indexOf("mod2-") === 0){
        updateLevelRecommendations();
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
    var transcriptWrap = document.getElementById("mrTranscript");
    var transcriptText = document.getElementById("mrTranscriptText");

    var rec = null, chunks = [], stream = null, elapsed = 0, tick = null, url = null;

    // transcrição ao vivo (autoavaliação de Speaking): não substitui gravar o
    // áudio, roda em paralelo via SpeechRecognition -- a "irmã" da API de voz
    // já usada pros botões de pronúncia, só que no sentido contrário (fala ->
    // texto). Não pontua nada, só mostra o que o app "ouviu" pra comparar com
    // o que o aluno pretendia dizer. Sem suporte no navegador (ex.: Firefox),
    // o gravador de áudio continua funcionando normal, só sem essa parte.
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognizer = null, finalTranscript = "";
    function startTranscript(){
      if(!SpeechRec) return;
      finalTranscript = "";
      transcriptText.textContent = "";
      transcriptWrap.hidden = false;
      try {
        recognizer = new SpeechRec();
        recognizer.lang = "en-US";
        recognizer.continuous = true;
        recognizer.interimResults = true;
        recognizer.onresult = function(e){
          var interim = "";
          for(var i = e.resultIndex; i < e.results.length; i++){
            var chunk = e.results[i][0].transcript;
            if(e.results[i].isFinal) finalTranscript += chunk + " ";
            else interim += chunk;
          }
          transcriptText.textContent = (finalTranscript + interim).trim();
        };
        recognizer.onerror = function(){}; // silencioso -- audio gravado continua valendo mesmo se o reconhecimento falhar
        recognizer.start();
      } catch(ex){ recognizer = null; }
    }
    function stopTranscript(){
      if(recognizer){ try { recognizer.stop(); } catch(ex){} recognizer = null; }
    }

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
        startTranscript();
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
      stopTranscript();
      wrap.classList.remove("recording");
      recBtn.textContent = "● Gravar";
      if(rec && rec.state !== "inactive") rec.stop();
      rec = null;
    }
    function clearRec(){
      revoke();
      audioEl.hidden = true; audioEl.removeAttribute("src");
      clearBtn.hidden = true;
      transcriptWrap.hidden = true;
      transcriptText.textContent = "";
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
      var RESET_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_errlog_", "toefl_cert_", "toefl_ctw_", "toefl_spk_", "toefl_write_"];
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
  // Formato da prova: a resposta já vem com trechos fixos e espaços vazios
  // (.bsq-slot); o aluno preenche os espaços com os blocos do banco. Alguns
  // itens têm um bloco a mais, que fica de fora.
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
      var bank = card.querySelector('[data-role="bank"]');
      var slots = Array.prototype.slice.call(card.querySelectorAll(".bsq-slot"));
      var checkBtn = card.querySelector(".bsq-check");
      var fb = card.querySelector(".bsq-feedback");
      var model = card.querySelector(".bsq-model");
      var allChips = Array.prototype.slice.call(card.querySelectorAll(".bsq-chip"));

      // conteúdo de cada espaço, na ordem; null = vazio
      function placed(){
        return slots.map(function(s){
          var c = s.querySelector(".bsq-chip");
          return c ? c.dataset.frag : null;
        });
      }
      function firstEmpty(){
        for(var i = 0; i < slots.length; i++){
          if(!slots[i].querySelector(".bsq-chip")) return slots[i];
        }
        return null;
      }
      function updateCheckBtn(){ checkBtn.disabled = firstEmpty() !== null; }
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
          if(chip.parentNode === bank){
            var slot = firstEmpty();
            if(!slot) return; // tudo preenchido: devolva um bloco antes
            slot.appendChild(chip);
          } else {
            bank.appendChild(chip);
          }
          updateCheckBtn();
          state[num] = { order: placed(), checked: false };
          persist();
        });
      });

      checkBtn.addEventListener("click", function(){
        var assembled = placed();
        var ok = assembled.length === correct.length &&
          assembled.every(function(f, i){ return f === correct[i]; });
        state[num] = { order: assembled, checked: true, ok: ok };
        persist();
        reveal(ok);
        renderSummary();
      });

      // restaura estado salvo
      var s = state[num];
      shuffle(allChips);
      if(s && s.order && s.order.length){
        var pool = allChips.slice();
        s.order.forEach(function(f, i){
          if(!f || !slots[i]) return;
          for(var k = 0; k < pool.length; k++){
            if(pool[k].dataset.frag === f){ slots[i].appendChild(pool[k]); pool.splice(k, 1); break; }
          }
        });
        updateCheckBtn();
        if(s.checked) reveal(!!s.ok);
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

  // ---------- Complete the Words — formato da prova (M1) ----------
  // O aluno digita o final de cada palavra. Nada é corrigido até clicar em
  // Verificar, como na prova; depois disso o texto trava e mostra o gabarito.
  Array.prototype.forEach.call(document.querySelectorAll(".ctw"), function(root){
    var lsKey = "toefl_ctw_" + root.dataset.ctw + "_v1";
    var inputs = Array.prototype.slice.call(root.querySelectorAll(".ctw-in"));
    var checkBtn = root.querySelector(".ctw-check");
    var retryBtn = root.querySelector(".ctw-retry");
    var resultEl = root.querySelector(".ctw-result");
    var noteEl = root.querySelector(".ctw-note");
    var state = {};
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }
    if(!state || typeof state !== "object") state = {};

    function values(){ return inputs.map(function(i){ return i.value; }); }
    function persist(checked){
      state = { vals: values(), checked: !!checked };
      safeSet(lsKey, JSON.stringify(state));
    }
    function isRight(input){
      return input.value.trim().toLowerCase() === input.dataset.answer.toLowerCase();
    }
    function grade(){
      var right = 0;
      inputs.forEach(function(input){
        var ok = isRight(input);
        if(ok) right++;
        input.classList.toggle("is-ok", ok);
        input.classList.toggle("is-bad", !ok);
        input.disabled = true;
        var fix = input.parentNode.querySelector(".ctw-fix");
        if(fix && !ok){
          fix.textContent = input.parentNode.dataset.word;
          fix.hidden = false;
        }
      });
      resultEl.textContent = right + " de " + inputs.length + " corretas";
      resultEl.hidden = false;
      noteEl.hidden = false;
      checkBtn.hidden = true;
      retryBtn.hidden = false;
      root.classList.add("is-checked");
      root.dataset.right = String(right);
    }

    inputs.forEach(function(input, idx){
      input.addEventListener("input", function(){
        // só letras; ao completar a lacuna, pula para a próxima
        var clean = input.value.replace(/[^A-Za-z]/g, "");
        if(clean !== input.value) input.value = clean;
        persist(false);
        var max = parseInt(input.getAttribute("maxlength"), 10) || 0;
        if(max && input.value.length >= max && inputs[idx + 1]) inputs[idx + 1].focus();
      });
      input.addEventListener("keydown", function(e){
        if(e.key === "Backspace" && input.value === "" && inputs[idx - 1]){
          inputs[idx - 1].focus();
        } else if(e.key === "Enter"){
          e.preventDefault();
          if(inputs[idx + 1]) inputs[idx + 1].focus(); else checkBtn.focus();
        }
      });
    });

    checkBtn.addEventListener("click", function(){ persist(true); grade(); });
    retryBtn.addEventListener("click", function(){
      inputs.forEach(function(input){
        input.value = ""; input.disabled = false;
        input.classList.remove("is-ok", "is-bad");
        var fix = input.parentNode.querySelector(".ctw-fix");
        if(fix){ fix.hidden = true; fix.textContent = ""; }
      });
      resultEl.hidden = true; noteEl.hidden = true;
      retryBtn.hidden = true; checkBtn.hidden = false;
      root.classList.remove("is-checked");
      delete root.dataset.right;
      persist(false);
      if(inputs[0]) inputs[0].focus();
    });

    if(state.vals && state.vals.length === inputs.length){
      inputs.forEach(function(input, i){ input.value = state.vals[i] || ""; });
      if(state.checked) grade();
    }
  });

  // ---------- Speaking: Listen and Repeat / Take an Interview (M3) ----------
  // O aluno ouve antes de ver. Em "repeat" ele marca se repetiu igual; em
  // "interview", depois da pergunta corre a contagem do tempo de resposta.
  (function(){
    var roots = document.querySelectorAll(".spk");
    if(!roots.length) return;
    var canSpeak = "speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined";
    var activeClock = null; // só um cronômetro de resposta por vez

    function stopClock(){
      if(activeClock){ clearInterval(activeClock.timer); activeClock.el.hidden = true; activeClock = null; }
    }
    function say(text, onEnd){
      if(!canSpeak){ if(onEnd) onEnd(); return; }
      try {
        window.speechSynthesis.cancel();
        var utter = new SpeechSynthesisUtterance(text);
        utter.lang = "en-US";
        utter.rate = 0.93;
        var voice = pickVoice();
        if(voice) utter.voice = voice;
        var done = false;
        function finish(){ if(done) return; done = true; if(onEnd) onEnd(); }
        utter.onend = finish;
        utter.onerror = finish;
        window.speechSynthesis.speak(utter);
      } catch(ex){ if(onEnd) onEnd(); }
    }

    Array.prototype.forEach.call(roots, function(root){
      var lsKey = "toefl_spk_" + root.dataset.spk + "_v1";
      var mode = root.dataset.mode;
      var seconds = parseInt(root.dataset.seconds, 10) || 45;
      var items = Array.prototype.slice.call(root.querySelectorAll(".spk-item"));
      var scoreEl = root.querySelector(".spk-score");
      var retryBtn = root.querySelector(".spk-retry");
      var state = {};
      try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }
      if(!state || typeof state !== "object") state = {};

      if(!canSpeak){
        var warn = root.querySelector(".spk-nosound");
        if(warn) warn.hidden = false;
      }

      function renderScore(){
        var done = 0, ok = 0;
        items.forEach(function(it){
          var m = state[it.dataset.num];
          if(m){ done++; if(m === "ok") ok++; }
          it.classList.toggle("is-ok", m === "ok");
          it.classList.toggle("is-miss", m === "miss");
        });
        if(!done){ scoreEl.textContent = ""; }
        else if(mode === "repeat"){ scoreEl.textContent = ok + " de " + items.length + " repetidas sem erro"; }
        else { scoreEl.textContent = done + " de " + items.length + " respondidas"; }
        retryBtn.hidden = done === 0;
      }

      items.forEach(function(it){
        var playBtn = it.querySelector(".spk-play");
        var showBtn = it.querySelector(".spk-show");
        var textEl = it.querySelector(".spk-text");
        var marks = it.querySelector(".spk-marks");
        var clock = it.querySelector(".spk-clock");

        function startClock(){
          if(!clock) return;
          stopClock();
          var left = seconds;
          clock.hidden = false;
          clock.textContent = "Fale agora: " + left + " s";
          var timer = setInterval(function(){
            left--;
            if(left <= 0){
              clearInterval(timer);
              clock.textContent = "Tempo esgotado";
              activeClock = null;
              return;
            }
            clock.textContent = "Fale agora: " + left + " s";
          }, 1000);
          activeClock = { timer: timer, el: clock };
        }

        playBtn.addEventListener("click", function(){
          stopClock();
          playBtn.disabled = true;
          say(it.dataset.text, function(){
            playBtn.disabled = false;
            marks.hidden = false;
            if(mode === "interview") startClock();
          });
        });
        showBtn.addEventListener("click", function(){
          textEl.hidden = !textEl.hidden;
          showBtn.textContent = textEl.hidden ? "Mostrar texto" : "Esconder texto";
          marks.hidden = false;
        });
        Array.prototype.forEach.call(it.querySelectorAll(".spk-mark"), function(btn){
          btn.addEventListener("click", function(){
            state[it.dataset.num] = btn.dataset.mark;
            safeSet(lsKey, JSON.stringify(state));
            if(clock && activeClock && activeClock.el === clock) stopClock();
            renderScore();
          });
        });
        if(state[it.dataset.num]) marks.hidden = false;
      });

      retryBtn.addEventListener("click", function(){
        state = {};
        safeSet(lsKey, JSON.stringify(state));
        stopClock();
        items.forEach(function(it){
          it.querySelector(".spk-text").hidden = true;
          it.querySelector(".spk-show").textContent = "Mostrar texto";
          it.querySelector(".spk-marks").hidden = true;
        });
        renderScore();
      });
      renderScore();
    });
  })();

  // ---------- Caixa de escrita com cronômetro (M4) ----------
  Array.prototype.forEach.call(document.querySelectorAll(".wbox"), function(root){
    var lsKey = "toefl_write_" + root.dataset.wbox + "_v1";
    var minutes = parseInt(root.dataset.minutes, 10) || 7;
    var minWords = parseInt(root.dataset.minwords, 10) || 0;
    var area = root.querySelector(".wbox-text");
    var startBtn = root.querySelector(".wbox-start");
    var clockEl = root.querySelector(".wbox-clock");
    var countEl = root.querySelector(".wbox-count");
    var goalEl = root.querySelector(".wbox-goal");
    var statusEl = root.querySelector(".wbox-status");
    var clearBtn = root.querySelector(".wbox-clear");
    var timer = null, left = minutes * 60, saveTimer = null, clearArmed = null;

    function fmt(sec){
      var m = Math.floor(sec / 60), s = sec % 60;
      return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }
    function words(){
      var t = area.value.trim();
      return t ? t.split(/\s+/).length : 0;
    }
    function renderCount(){
      var n = words();
      countEl.textContent = n + (n === 1 ? " palavra" : " palavras");
      if(goalEl) goalEl.classList.toggle("is-met", n >= minWords);
    }
    function save(){
      safeSet(lsKey, JSON.stringify({ text: area.value }));
      statusEl.textContent = "Salvo.";
    }
    function stop(label){
      if(timer){ clearInterval(timer); timer = null; }
      startBtn.textContent = label;
      root.classList.remove("is-running");
    }

    try {
      var saved = JSON.parse(safeGet(lsKey) || "{}");
      if(saved && typeof saved.text === "string") area.value = saved.text;
    } catch(e){}
    renderCount();

    area.addEventListener("input", function(){
      renderCount();
      statusEl.textContent = "Salvando...";
      if(saveTimer) clearTimeout(saveTimer);
      saveTimer = setTimeout(save, 600);
    });

    startBtn.addEventListener("click", function(){
      if(timer){ stop("Continuar"); return; }
      if(left <= 0){ left = minutes * 60; root.classList.remove("is-over"); }
      clockEl.textContent = fmt(left);
      startBtn.textContent = "Pausar";
      root.classList.add("is-running");
      area.focus();
      timer = setInterval(function(){
        left--;
        clockEl.textContent = fmt(Math.max(left, 0));
        if(left <= 0){
          stop("Recomeçar " + minutes + " min");
          root.classList.add("is-over");
          statusEl.textContent = "Tempo esgotado. Na prova a tela trava aqui.";
        }
      }, 1000);
    });

    // apagar pede um segundo clique, porque confirm() nem sempre existe
    clearBtn.addEventListener("click", function(){
      if(!clearArmed){
        clearBtn.textContent = "Clique de novo para apagar";
        clearArmed = setTimeout(function(){ clearArmed = null; clearBtn.textContent = "Apagar texto"; }, 3500);
        return;
      }
      clearTimeout(clearArmed); clearArmed = null;
      clearBtn.textContent = "Apagar texto";
      area.value = "";
      renderCount();
      save();
      stop("Iniciar " + minutes + " min");
      left = minutes * 60;
      clockEl.textContent = fmt(left);
      root.classList.remove("is-over");
    });
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
    // texto e botão de pronúncia vivem em nós separados dentro de .srs-word
    // pra poder trocar só o texto a cada carta (textContent apagaria o botão junto)
    var fWordText = document.createTextNode("");
    var bWordText = document.createTextNode("");
    fWord.appendChild(fWordText);
    bWord.appendChild(bWordText);
    var srsSpeakWord = "";
    if("speechSynthesis" in window){
      [fWord, bWord].forEach(function(wordEl){
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "speak-btn speak-btn-inline";
        btn.setAttribute("aria-label", "Ouvir pronúncia");
        btn.textContent = "🔊";
        btn.addEventListener("click", function(){ speakText(srsSpeakWord); });
        wordEl.appendChild(btn);
      });
    }
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
      srsSpeakWord = c.w;
      fWordText.textContent = c.w; fCat.textContent = c.cat || "";
      bWordText.textContent = c.w;
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
    // formulário de e-mail+senha
    var loginForm = document.getElementById("loginForm");
    var signupForm = document.getElementById("signupForm");
    var resetPasswordForm = document.getElementById("resetPasswordForm");
    var authTabs = document.getElementById("authTabs");
    var authGateForms = [loginForm, signupForm, resetPasswordForm, document.getElementById("authLinks"),
      document.getElementById("authGateDivider"), document.getElementById("authGateGoogleWrap"),
      document.getElementById("authTabs")];
    var authGateTitle = document.getElementById("authGateTitle");
    var authGateSubtitle = document.getElementById("authGateSubtitle");
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
    supaClient = client;

    // ---- acesso pago (2026-09-17) ----
    // conta admin sempre passa direto, sem checar entitlements -- pedido
    // explícito do usuário ("eu tenho acesso ilimitado com minha conta")
    var ADMIN_EMAIL = "pietrooliveiramarquespp@gmail.com";
    var payGateEl = document.getElementById("payGate");
    var payBtn = document.getElementById("payBtn");
    var payGateMsgEl = document.getElementById("payGateMsg");
    var paySignOutBtn = document.getElementById("paySignOut");
    var couponInput = document.getElementById("couponInput");
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
          if(res.error){
            // erro de rede/consulta: mantém a tela de pagamento visível (o
            // padrão seguro pra receita continua sendo travar por padrão),
            // mas avisa que foi uma falha de conexão, não que o aluno não
            // pagou -- sem isso, quem já pagou via um erro transitório
            // lia "sem acesso" sem saber que é só tentar de novo.
            payGateEl.hidden = false;
            payGateMsg("Não deu pra confirmar seu acesso agora (erro de conexão). Atualize a página pra tentar de novo.", "err");
            console.error("Falha ao verificar pagamento:", res.error.message);
            return;
          }
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
        // functions.invoke() nem sempre anexa o token de sessão sozinho
        // (dependendo da versão da lib carregada pelo CDN) -- a edge
        // function então recebe a chamada sem Authorization e responde
        // "Não autenticado." mesmo com o aluno logado. Busca a sessão
        // atual e manda o token explicitamente pra não depender disso.
        client.auth.getSession().then(function(sessionRes){
          var token = sessionRes && sessionRes.data && sessionRes.data.session && sessionRes.data.session.access_token;
          var coupon = couponInput ? couponInput.value.trim() : "";
          var opts = { body: { origin: location.origin, coupon: coupon } };
          if(token) opts.headers = { Authorization: "Bearer " + token };
          return client.functions.invoke("create-checkout", opts);
        })
          .then(function(res){
            payBtn.disabled = false;
            if(res.error || !res.data || !res.data.url){
              // res.error.context é a Response HTTP crua quando a function
              // responde status != 2xx (ex.: cupom inválido) -- sem ler o
              // corpo, o aluno só veria "Edge Function returned a non-2xx
              // status code" em vez do motivo de verdade.
              var ctx = res.error && res.error.context;
              (ctx && typeof ctx.json === "function" ? ctx.json().catch(function(){ return null; }) : Promise.resolve(null))
                .then(function(body){
                  var reason = (body && body.error) || (res.error ? res.error.message : "resposta inválida");
                  payGateMsg("Erro ao abrir checkout: " + reason, "err");
                });
              return;
            }
            location.href = res.data.url;
          })
          .catch(function(){
            // rejeição de verdade (ex.: sem internet, DNS falhou antes de
            // chegar no Supabase) -- sem isso o botão ficava travado em
            // "Abrindo checkout..." pra sempre, sem erro e sem como tentar de novo
            payBtn.disabled = false;
            payGateMsg("Erro de conexão ao abrir checkout. Tente de novo.", "err");
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
      supaUid = uid;
      emailEl.textContent = session.user.email || "conectado";
      googleAvatarUrl = extractGoogleAvatar(session);
      renderAvatar(session.user.email);
      setGateFormsHidden(true);
      signedIn.hidden = false;
      if(gateEl) gateEl.hidden = true;
      checkEntitlement(session);
      onSyncedWrite = schedulePush;
      forceSyncPush = push;
      pull();
    }
    function goOffline(){
      uid = null;
      supaUid = null;
      googleAvatarUrl = null;
      onSyncedWrite = null;
      forceSyncPush = null;
      setGateFormsHidden(false);
      showLoginView();
      signedIn.hidden = true;
      if(gateEl) gateEl.hidden = false;
      if(payGateEl) payGateEl.hidden = true;
    }

    // ---- login por e-mail+senha ----
    var AUTH_ERROR_MAP = {
      "Invalid login credentials": "E-mail ou senha incorretos.",
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
      authGateSubtitle.textContent = "";
    }
    function showSignupView(){
      loginForm.hidden = true; signupForm.hidden = false; resetPasswordForm.hidden = true;
      authTabs.hidden = false; authTabs.classList.add("is-signup");
      authTabSignup.classList.add("is-active"); authTabLogin.classList.remove("is-active");
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = false;
      document.getElementById("authGateGoogleWrap").hidden = false;
      authGateTitle.textContent = "Criar conta";
      authGateSubtitle.textContent = "";
    }
    function showResetPasswordView(){
      loginForm.hidden = true; signupForm.hidden = true; resetPasswordForm.hidden = false;
      authTabs.hidden = true;
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = true;
      document.getElementById("authGateGoogleWrap").hidden = true;
      authGateTitle.textContent = "Escolha uma nova senha";
      authGateSubtitle.textContent = "";
      if(gateEl) gateEl.hidden = false; // aparece mesmo se o app estava "logado" na sessão de recuperação
    }

    loginForm.addEventListener("submit", function(e){
      e.preventDefault();
      var email = document.getElementById("loginEmail").value.trim();
      var password = document.getElementById("loginPassword").value;
      if(!email || !password) return;
      gateMsg("Entrando...", "ok");
      client.auth.signInWithPassword({ email: email, password: password }).then(function(r){
        if(r.error) gateMsg(friendlyError(r.error.message), "err");
      }).catch(function(){ gateMsg("Erro de conexão. Tente de novo.", "err"); });
    });

    signupForm.addEventListener("submit", function(e){
      e.preventDefault();
      var email = document.getElementById("signupEmail").value.trim();
      var password = document.getElementById("signupPassword").value;
      gateMsg("Criando conta...", "ok");
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
          gateMsg("Esse e-mail já tem conta. Use a aba Entrar, ou clique em \"Esqueci minha senha\" se não lembrar a senha.", "err");
          return;
        }
        gateMsg("Conta criada! Confira seu e-mail para confirmar antes de entrar.", "ok");
      }).catch(function(){ gateMsg("Erro de conexão. Tente de novo.", "err"); });
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

    // ---- "Minha conta": situação do acesso, troca de e-mail/senha e
    // exclusão da conta ----
    (function(){
      var accountBtn = document.getElementById("accountBtn");
      var accountModal = document.getElementById("accountModal");
      if(!accountBtn || !accountModal) return;
      var backdrop = document.getElementById("accountModalBackdrop");
      var closeBtn = document.getElementById("accountClose");
      var emailForm = document.getElementById("accountEmailForm");
      var emailInput = document.getElementById("accountEmail");
      var passwordForm = document.getElementById("accountPasswordForm");
      var accountMsgEl = document.getElementById("accountMsg");
      var accessEl = document.getElementById("accountAccess");

      function setAccess(text, cls){
        if(!accessEl) return;
        accessEl.textContent = text;
        accessEl.className = "account-access" + (cls ? " " + cls : "");
      }
      // mostra o que a tabela `entitlements` diz desta conta. É só leitura:
      // quem libera ou bloqueia o conteúdo continua sendo checkEntitlement().
      function loadAccess(user){
        if(!accessEl) return;
        if(!user){ setAccess("Não deu pra verificar agora.", ""); return; }
        if(isAdmin({ user: user })){ setAccess("Conta de administrador: acesso liberado, sem cobrança.", "is-paid"); return; }
        setAccess("Verificando...", "");
        client.from("entitlements").select("paid, paid_at").eq("user_id", user.id).maybeSingle()
          .then(function(res){
            if(res.error){ setAccess("Não deu pra verificar agora. Feche e abra esta tela pra tentar de novo.", ""); return; }
            if(res.data && res.data.paid){
              var when = "";
              if(res.data.paid_at){
                var d = new Date(res.data.paid_at);
                if(!isNaN(d.getTime())) when = " desde " + d.toLocaleDateString("pt-BR");
              }
              setAccess("Pago ✓ Acesso vitalício liberado" + when + ".", "is-paid");
            } else {
              setAccess("Sem acesso: esta conta ainda não tem compra confirmada.", "is-unpaid");
            }
          })
          .catch(function(){ setAccess("Não deu pra verificar agora (erro de conexão).", ""); });
      }

      function accountMsg(text, kind){
        accountMsgEl.textContent = text;
        if(kind === "err"){
          accountMsgEl.style.color = "var(--danger)";
          accountMsgEl.style.background = "var(--danger-wash)";
          accountMsgEl.style.borderColor = "var(--danger)";
        } else {
          accountMsgEl.style.color = "var(--ink-2)";
          accountMsgEl.style.background = "var(--bg)";
          accountMsgEl.style.borderColor = "var(--hair)";
        }
        accountMsgEl.hidden = false;
      }

      function open(){
        accountMsgEl.hidden = true;
        emailInput.value = "";
        resetDeleteForm();
        setAccess("Verificando...", "");
        client.auth.getUser().then(function(res){
          var user = res.data && res.data.user;
          emailInput.value = (user && user.email) || "";
          loadAccess(user);
        }).catch(function(){ loadAccess(null); });
        accountModal.hidden = false;
        document.body.classList.add("menu-open");
      }
      function close(){
        accountModal.hidden = true;
        document.body.classList.remove("menu-open");
      }
      accountBtn.addEventListener("click", open);
      closeBtn.addEventListener("click", close);
      backdrop.addEventListener("click", close);
      document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !accountModal.hidden) close(); });

      emailForm.addEventListener("submit", function(e){
        e.preventDefault();
        var email = emailInput.value.trim();
        if(!email) return;
        client.auth.getUser().then(function(cur){
          var current = (cur.data && cur.data.user && cur.data.user.email) || "";
          if(email.toLowerCase() === current.toLowerCase()){
            accountMsg("Esse já é o seu e-mail atual.", "ok");
            return;
          }
          accountMsg("Salvando...", "ok");
          client.auth.updateUser({ email: email }).then(function(res){
            if(res.error){ accountMsg(friendlyError(res.error.message), "err"); return; }
            // o Supabase manda link de confirmação pro endereço NOVO (e, se
            // "secure email change" estiver ligado, também pro antigo) --
            // o e-mail só troca de verdade depois de clicar nesse link
            accountMsg("Confira o e-mail enviado para " + email + " e confirme a troca por lá.", "ok");
          }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
        }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
      });

      passwordForm.addEventListener("submit", function(e){
        e.preventDefault();
        var newPassword = document.getElementById("accountNewPassword").value;
        if(!newPassword || newPassword.length < 6) return;
        accountMsg("Salvando...", "ok");
        client.auth.updateUser({ password: newPassword }).then(function(res){
          if(res.error){ accountMsg("Erro ao salvar: " + res.error.message, "err"); return; }
          passwordForm.reset();
          accountMsg("Senha atualizada.", "ok");
        }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
      });

      // ---- excluir conta ----
      // quem apaga de verdade é a edge function delete-account (precisa da
      // service_role, que não pode vir pro navegador). Aqui é só a
      // confirmação e a limpeza do que ficou neste aparelho.
      var deleteOpenBtn = document.getElementById("accountDeleteOpen");
      var deleteForm = document.getElementById("accountDeleteForm");
      var deleteConfirm = document.getElementById("accountDeleteConfirm");
      var deleteCancel = document.getElementById("accountDeleteCancel");
      var deleteSubmit = document.getElementById("accountDeleteSubmit");
      var deleteMsgEl = document.getElementById("accountDeleteMsg");
      var DELETE_WORD = "EXCLUIR";

      function deleteMsg(text, kind){
        if(!deleteMsgEl) return;
        deleteMsgEl.textContent = text;
        if(kind === "err"){
          deleteMsgEl.style.color = "var(--danger)";
          deleteMsgEl.style.background = "var(--danger-wash)";
          deleteMsgEl.style.borderColor = "var(--danger)";
        } else {
          deleteMsgEl.style.color = "var(--ink-2)";
          deleteMsgEl.style.background = "var(--bg)";
          deleteMsgEl.style.borderColor = "var(--hair)";
        }
        deleteMsgEl.hidden = false;
      }
      function deleteWordOk(){
        return !!deleteConfirm && deleteConfirm.value.trim().toUpperCase() === DELETE_WORD;
      }
      function resetDeleteForm(){
        if(!deleteForm) return;
        deleteForm.hidden = true;
        deleteOpenBtn.hidden = false;
        deleteConfirm.value = "";
        deleteConfirm.disabled = false;
        deleteCancel.disabled = false;
        deleteSubmit.disabled = true;
        deleteMsgEl.hidden = true;
      }
      // apaga tudo que é do aluno neste aparelho. Tema fica: é preferência
      // do aparelho, não dado da conta.
      function wipeLocalData(){
        var keys = [];
        try{
          for(var i = 0; i < localStorage.length; i++){
            var k = localStorage.key(i);
            if(k && k.indexOf("toefl_") === 0 && k !== LS_THEME) keys.push(k);
          }
        }catch(e){}
        keys.forEach(function(k){ try{ localStorage.removeItem(k); }catch(e){} });
      }
      if(deleteForm && deleteOpenBtn){
        deleteOpenBtn.addEventListener("click", function(){
          deleteOpenBtn.hidden = true;
          deleteForm.hidden = false;
          deleteMsgEl.hidden = true;
          deleteConfirm.focus();
        });
        deleteCancel.addEventListener("click", resetDeleteForm);
        deleteConfirm.addEventListener("input", function(){ deleteSubmit.disabled = !deleteWordOk(); });
        deleteForm.addEventListener("submit", function(e){
          e.preventDefault();
          if(!deleteWordOk()) return;
          deleteSubmit.disabled = true;
          deleteCancel.disabled = true;
          deleteConfirm.disabled = true;
          deleteMsg("Excluindo sua conta...", "ok");
          function fail(text){
            deleteConfirm.disabled = false;
            deleteCancel.disabled = false;
            deleteSubmit.disabled = !deleteWordOk();
            deleteMsg(text, "err");
          }
          // mesmo cuidado do checkout: manda o token de sessão explicitamente
          client.auth.getSession().then(function(sessionRes){
            var token = sessionRes && sessionRes.data && sessionRes.data.session && sessionRes.data.session.access_token;
            var opts = { body: { confirm: DELETE_WORD } };
            if(token) opts.headers = { Authorization: "Bearer " + token };
            return client.functions.invoke("delete-account", opts);
          })
            .then(function(res){
              if(res.error || !res.data || !res.data.deleted){
                var ctx = res.error && res.error.context;
                (ctx && typeof ctx.json === "function" ? ctx.json().catch(function(){ return null; }) : Promise.resolve(null))
                  .then(function(body){
                    fail((body && body.error) || "Não foi possível excluir a conta agora. Tente de novo em alguns minutos.");
                  });
                return;
              }
              // conta apagada no servidor. Para a sincronização antes de
              // limpar o aparelho, senão um push pendente tentaria regravar.
              if(pushTimer){ clearTimeout(pushTimer); pushTimer = null; }
              onSyncedWrite = null;
              forceSyncPush = null;
              wipeLocalData();
              deleteMsg("Conta excluída. Até mais.", "ok");
              function done(){ location.href = location.pathname; }
              // a sessão já não vale no servidor: encerra só a cópia local
              client.auth.signOut({ scope: "local" }).then(done, done);
            })
            .catch(function(){ fail("Erro de conexão. Sua conta não foi excluída. Tente de novo."); });
        });
      }
    })();

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
    var bandEl = document.getElementById("certBand");
    var nameStep = document.getElementById("certNameStep");
    var certView = document.getElementById("certView");
    var nameForm = document.getElementById("certNameForm");
    var nameInput = document.getElementById("certNameInput");
    var editNameBtn = document.getElementById("certEditName");

    function fmtDate(iso){
      try{
        var d = new Date(iso);
        return d.toLocaleDateString("pt-BR", { day:"2-digit", month:"long", year:"numeric" });
      }catch(e){ return ""; }
    }
    function fillCert(name){
      nameEl.textContent = name;
      var iso = safeGet("toefl_cert_date_v1");
      dateEl.textContent = iso ? fmtDate(iso) : "—";
      var diag = computeQuizAccuracy("mod0-diag");
      if(diag.confirmed > 0 && diag.confirmed === diag.total){
        var band = cefrBandFromPct(Math.round(100 * diag.correct / diag.confirmed));
        bandEl.textContent = "Banda " + band.code + " (" + band.label + ")";
      } else {
        bandEl.textContent = "—";
      }
      nameStep.hidden = true;
      certView.hidden = false;
    }
    function showNameStep(current){
      nameInput.value = current || "";
      certView.hidden = true;
      nameStep.hidden = false;
      nameInput.focus();
    }
    function open(){
      modal.hidden = false;
      document.body.classList.add("menu-open"); // reaproveita o travamento de scroll do drawer
      if(!supaClient || !supaUid){
        // sem sessão (raro, já que o gate exige login): usa o usuário/e-mail como fallback
        var email = document.getElementById("authEmail");
        var fallback = (email && email.textContent.trim()) ? email.textContent.trim().split("@")[0] : "Aluno(a) iTOEFL";
        fillCert(fallback);
        return;
      }
      supaClient.from("profiles").select("display_name").eq("id", supaUid).maybeSingle().then(function(res){
        var saved = res.data && res.data.display_name;
        if(saved) fillCert(saved); else showNameStep("");
      });
    }
    function close(){
      modal.hidden = true;
      document.body.classList.remove("menu-open");
    }
    nameForm.addEventListener("submit", function(e){
      e.preventDefault();
      var name = nameInput.value.trim();
      if(!name) return;
      if(supaClient && supaUid){
        supaClient.from("profiles").update({ display_name: name }).eq("id", supaUid).then(function(){
          fillCert(name);
        });
      } else {
        fillCert(name);
      }
    });
    editNameBtn.addEventListener("click", function(){ showNameStep(nameEl.textContent); });
    btn.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !modal.hidden) close(); });
    printBtn.addEventListener("click", function(){ window.print(); });
  })();

  // ---------- Painel (dashboard): sequência, banda estimada, progresso, pontos fracos ----------
  // Tudo aqui só lê dados que já existem em outros widgets (progresso,
  // diagnóstico do M0, live score de Reading/Listening, registro de erros)
  // -- nenhum estado novo além do streak em si.
  (function(){
    var btn = document.getElementById("dashboardBtn");
    var modal = document.getElementById("dashboardModal");
    if(!btn || !modal) return;
    var backdrop = document.getElementById("dashboardModalBackdrop");
    var closeBtn = document.getElementById("dashboardClose");
    var streakEl = document.getElementById("dashStreak");
    var goalFillEl = document.getElementById("dashGoalFill");
    var goalTextEl = document.getElementById("dashGoalText");
    var bandEl = document.getElementById("dashBand");
    var progressFillEl = document.getElementById("dashProgressFill");
    var progressTextEl = document.getElementById("dashProgressText");
    var weakListEl = document.getElementById("dashWeakSpots");
    var planTextEl = document.getElementById("dashPlanText");
    var planBtnEl = document.getElementById("dashPlanBtn");

    // pra onde mandar o aluno a partir do código de erro mais frequente --
    // mesmo agrupamento do mapa reverso do Módulo 9, Parte 8 (RG antes de R,
    // senão "RG1" bateria como se fosse Reading por causa do prefixo "R")
    var ERROR_MODULE_MAP = [
      { re: /^RG/, mod: "mod5", title: "Registro & Retórica" },
      { re: /^R/, mod: "mod1", title: "Reading" },
      { re: /^L/, mod: "mod2", title: "Listening" },
      { re: /^S/, mod: "mod3", title: "Speaking" },
      { re: /^W/, mod: "mod4", title: "Writing" },
      { re: /^V/, mod: "mod6", title: "Vocabulário" }
    ];
    function moduleForErrorCode(code){
      for(var i = 0; i < ERROR_MODULE_MAP.length; i++){
        if(ERROR_MODULE_MAP[i].re.test(code)) return ERROR_MODULE_MAP[i];
      }
      return null;
    }

    // mesmos rótulos de app/build_pipeline.py (ERRLOG_CODES) -- duplicado
    // aqui de propósito: são só 36 pares fixos, não vale a pena gerar isso
    // no build só pra não repetir uma lista curta.
    var ERRLOG_LABELS = {
      R1:"Não entendi a pergunta", R2:"Caí num distrator", R3:"Lacuna de gramática (CTW)",
      R4:"Lacuna de vocabulário / collocation", R5:"Tempo", R6:"Desatenção / releitura",
      L1:"Não decodifiquei o áudio", L2:"Não entendi a pergunta", L3:"Caí num distrator",
      L4:"Anotação errada", L5:"Vocabulário", L6:"Atenção / fim do áudio",
      S1:"Fonema / segmento", S2:"Acento de palavra", S3:"Ritmo / acento de frase",
      S4:"Fluência", S5:"Gramática sob pressão", S6:"Estrutura da resposta",
      W1:"Estrutura de frase", W2:"Gramática de verbo", W3:"Artigo / preposição / word form",
      W4:"Registro", W5:"Conteúdo / prompt", W6:"Léxico",
      RG1:"Over-formality / cerimônia", RG2:"Register clash", RG3:"Sofisticação sem controle",
      RG4:"Repetição lexical", RG5:"Conector impreciso ou ausente", RG6:"Densidade plana",
      V1:"Forma errada da palavra", V2:"Colocação errada", V3:"Falso cognato",
      V4:"Registro trocado", V5:"Overreach (usou palavra que não controla)", V6:"Sinônimo impreciso"
    };
    function computeWeakSpots(){
      var freq = {};
      ["mod1","mod2","mod3","mod4","mod5","mod6"].forEach(function(mod){
        var entries = []; try { entries = JSON.parse(safeGet("toefl_errlog_" + mod + "_v1") || "[]"); } catch(e){}
        entries.forEach(function(entry){
          (entry.codes || []).forEach(function(c){ freq[c] = (freq[c] || 0) + 1; });
        });
      });
      return Object.keys(freq)
        .map(function(c){ return { code: c, label: ERRLOG_LABELS[c] || c, count: freq[c] }; })
        .sort(function(a, b){ return b.count - a.count; })
        .slice(0, 3);
    }
    function computeOverallProgress(){
      var totalAll = 0, doneAll = 0, modsDone = 0;
      allChecks.forEach(function(c){
        totalAll++;
        if(progressState[c.dataset.pid]) doneAll++;
      });
      modOrder.forEach(function(k){ if((modPct[k] || 0) >= 100) modsDone++; });
      return { pct: totalAll ? Math.round(100 * doneAll / totalAll) : 0, modsDone: modsDone, totalMods: modOrder.length };
    }
    function render(){
      var streak = computeStreak();
      streakEl.textContent = streak.count === 0
        ? "Comece hoje pra iniciar sua sequência."
        : streak.count + (streak.count === 1 ? " dia seguido estudando" : " dias seguidos estudando") +
          (streak.today ? "" : " (continue hoje pra manter)");

      var goal = getDailyGoal();
      goalFillEl.style.width = Math.min(100, Math.round(100 * goal.count / goal.target)) + "%";
      goalTextEl.textContent = goal.done
        ? "Meta batida hoje! (" + goal.count + "/" + goal.target + ")"
        : Math.min(goal.count, goal.target) + " de " + goal.target + " seção concluída hoje.";

      var band = computeBandEstimate();
      bandEl.textContent = band
        ? "Banda " + cefrBandFromPct(band.pct).code + " (" + cefrBandFromPct(band.pct).label + ") · com base em " + band.source
        : "Complete o diagnóstico do Módulo 0 pra ver sua estimativa.";

      var prog = computeOverallProgress();
      progressFillEl.style.width = prog.pct + "%";
      progressTextEl.textContent = prog.pct + "% · " + prog.modsDone + " de " + prog.totalMods + " módulos concluídos";

      var weak = computeWeakSpots();
      weakListEl.innerHTML = weak.length ? "" : '<p class="dash-empty">Nenhum erro registrado ainda. Use o "Registre esta sessão" no fim dos módulos M1–M6.</p>';
      weak.forEach(function(w){
        var row = document.createElement("div");
        row.className = "dash-weak-row";
        row.innerHTML = '<span class="dash-weak-code">' + w.code + '</span>' +
          '<span class="dash-weak-label">' + w.label + '</span>' +
          '<span class="dash-weak-count">' + w.count + 'x</span>';
        weakListEl.appendChild(row);
      });

      if(weak.length){
        var top = weak[0];
        var target = moduleForErrorCode(top.code);
        if(target){
          planTextEl.textContent = "Seu erro mais frequente é \"" + top.label + "\" (" + top.code + ", " + top.count +
            "x). Revise no Módulo: " + target.title + ".";
          planBtnEl.hidden = false;
          planBtnEl.onclick = function(){
            close();
            navTo(target.mod);
          };
        } else {
          planTextEl.textContent = "Continue registrando sessões pra receber uma sugestão personalizada.";
          planBtnEl.hidden = true;
        }
      } else {
        planTextEl.textContent = "Continue estudando e registrando sessões (M1–M6) pra receber uma sugestão personalizada aqui.";
        planBtnEl.hidden = true;
      }
    }
    function open(){
      render();
      modal.hidden = false;
      document.body.classList.add("menu-open");
    }
    function close(){
      modal.hidden = true;
      document.body.classList.remove("menu-open");
    }
    btn.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !modal.hidden) close(); });
  })();

  // ---------- Weekly Performance Dashboard (M0, Parte 5.1) ----------
  // toefl_weeklydash_v1 guarda { <metrica>: { w1..w4: "valor digitado" } },
  // salvo a cada tecla (o safeSet já cuida do dirty flag/push debounced pra
  // quem está logado, igual ao resto do progresso).
  (function(){
    var root = document.getElementById("weeklyDash");
    if(!root) return;
    var LS_KEY = "toefl_weeklydash_v1";
    var state = {};
    try { state = JSON.parse(safeGet(LS_KEY) || "{}"); } catch(e){ state = {}; }
    Array.prototype.slice.call(root.querySelectorAll(".wd-input")).forEach(function(inp){
      var metric = inp.dataset.metric, week = inp.dataset.week;
      if(state[metric] && state[metric][week] !== undefined) inp.value = state[metric][week];
      inp.addEventListener("input", function(){
        if(!state[metric]) state[metric] = {};
        state[metric][week] = inp.value;
        safeSet(LS_KEY, JSON.stringify(state));
      });
    });
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
  // Pedido do usuário: cada h3 de conteúdo (não os títulos dos próprios
  // drills/widgets interativos, que ficam sempre visíveis) começa FECHADA,
  // e abre sozinha quando o aluno rola até ela (IntersectionObserver) --
  // "anda" pelo módulo abrindo uma subseção de cada vez, em vez de mostrar
  // tudo de uma vez. Continua dando pra abrir/fechar clicando no título a
  // qualquer momento. Marcar a Parte (h2) inteira como concluída fecha as
  // subseções dela de volta (ver o listener de .pchk mais acima) -- depois
  // disso elas não reabrem sozinhas de novo, só se o aluno clicar. Roda por
  // último de propósito: outros passes (botão de cronômetro por drill,
  // índice "Nesta parte") contam com a posição original dos elementos em
  // relação aos h3/h2.
  // marcação de concluído por subseção (h3), separada da marcação por Parte
  // (h2) que já existia -- pedido do usuário: só dava pra marcar a Parte
  // inteira de uma vez, sem visão de quais subseções específicas já tinham
  // sido lidas.
  function readH3Progress(){
    var raw = safeGet("toefl_h3progress_v1");
    try{ return JSON.parse(raw) || {}; }catch(e){ return {}; }
  }
  function setH3Progress(id, done){
    var obj = readH3Progress();
    if(done) obj[id] = true; else delete obj[id];
    safeSet("toefl_h3progress_v1", JSON.stringify(obj));
  }

  (function(){
    var cards = Array.prototype.slice.call(document.querySelectorAll(".section-card"));
    var allH3 = [];
    var h3Seq = {}; // contador por módulo, pra dar um id estável a cada h3
    var h3Done = readH3Progress();
    cards.forEach(function(card){
      var panelEl = card.closest(".panel");
      var modKey = panelEl ? panelEl.dataset.panel : "mod";
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
        body.className = "h3-body h3-collapsed";
        nodes.forEach(function(n){ body.appendChild(n); });
        h3.parentNode.insertBefore(body, node);
        h3.classList.add("h3-toggle", "collapsed");
        h3Seq[modKey] = (h3Seq[modKey] || 0) + 1;
        h3.id = "h3-" + modKey + "-" + h3Seq[modKey];
        h3.dataset.mod = modKey;
        h3.addEventListener("click", function(){
          h3.classList.toggle("collapsed");
          body.classList.toggle("h3-collapsed");
        });
        allH3.push(h3);

        var dot = document.createElement("span");
        dot.className = "h3-done-dot";
        dot.textContent = "✓";
        h3.insertBefore(dot, h3.firstChild);

        var doneWrap = document.createElement("label");
        doneWrap.className = "prog-check h3-done-check";
        var chk = document.createElement("input");
        chk.type = "checkbox";
        chk.className = "h3chk";
        var box = document.createElement("span");
        box.className = "box";
        var lbl = document.createElement("span");
        lbl.className = "h3-done-label";
        lbl.textContent = "Marcar esta subseção como concluída";
        doneWrap.appendChild(chk);
        doneWrap.appendChild(box);
        doneWrap.appendChild(lbl);
        body.appendChild(doneWrap);

        if(h3Done[h3.id]){ chk.checked = true; h3.classList.add("h3-done"); }
        chk.addEventListener("change", function(){
          setH3Progress(h3.id, chk.checked);
          h3.classList.toggle("h3-done", chk.checked);
          if(chk.checked && !h3.classList.contains("collapsed")){
            h3.classList.add("collapsed");
            body.classList.add("h3-collapsed");
          }
        });
      });
    });

    // "continuar de onde parei": guarda a última subseção que o aluno leu
    // (a que entrou na faixa de leitura no meio da tela), pra sidebar
    // oferecer um atalho direto pra lá na próxima visita -- ver resumeBtn
    // mais abaixo. Separado do observer de auto-abrir porque precisa
    // disparar mesmo pra seções que já estavam abertas.
    // o IntersectionObserver dispara um callback inicial assim que começa a
    // observar, refletindo o que já está na tela nesse instante (a seção
    // 1.1 do módulo que acabou de carregar) -- isso não é "o aluno rolou até
    // aqui", é só o estado de largada, e não pode sobrescrever a posição
    // salva de uma visita anterior. Só passa a gravar depois desse atraso.
    var trackingLastPos = false;
    setTimeout(function(){ trackingLastPos = true; }, 900);
    function saveLastPos(h3){
      if(!trackingLastPos) return;
      safeSet("toefl_lastpos_v1", JSON.stringify({ mod: h3.dataset.mod, id: h3.id, title: h3.textContent.trim() }));
      updateResumeBtn();
    }

    if(allH3.length && "IntersectionObserver" in window){
      var h3Observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(!entry.isIntersecting) return;
          var h3 = entry.target;
          saveLastPos(h3);
          if(!h3.classList.contains("collapsed")) return;
          h3.classList.remove("collapsed");
          var body = h3.nextElementSibling;
          if(body && body.classList.contains("h3-body")) body.classList.remove("h3-collapsed");
        });
      }, { rootMargin: "0px 0px -35% 0px", threshold: 0 });
      allH3.forEach(function(h3){ h3Observer.observe(h3); });
    }

    // abre direto a primeira subseção do painel ativo no momento em que essa
    // IIFE roda (o painel que o showTab() inicial já deixou visível) -- não
    // depende do primeiro callback do IntersectionObserver, que na prática
    // nem sempre dispara a tempo pra quem já está com a seção na tela sem
    // ter rolado nada ainda.
    var firstActiveH3 = document.querySelector(".panel:not([hidden]) .h3-toggle");
    if(firstActiveH3 && firstActiveH3.classList.contains("collapsed")){
      firstActiveH3.classList.remove("collapsed");
      var firstActiveBody = firstActiveH3.nextElementSibling;
      if(firstActiveBody && firstActiveBody.classList.contains("h3-body")) firstActiveBody.classList.remove("h3-collapsed");
    }

    var resumeBtn = document.getElementById("resumeBtn");
    var resumeLabel = document.getElementById("resumeLabel");
    function readLastPos(){
      var raw = safeGet("toefl_lastpos_v1");
      if(!raw) return null;
      try{ return JSON.parse(raw); }catch(e){ return null; }
    }
    function updateResumeBtn(){
      if(!resumeBtn) return;
      var pos = readLastPos();
      if(!pos || !document.getElementById(pos.id)){ resumeBtn.hidden = true; return; }
      resumeLabel.textContent = pos.title;
      resumeBtn.hidden = false;
    }
    if(resumeBtn){
      resumeBtn.addEventListener("click", function(){
        var pos = readLastPos();
        if(!pos) return;
        navTo(pos.mod);
        setTimeout(function(){
          var target = document.getElementById(pos.id);
          if(!target) return;
          // se o módulo estiver paginado por parte (ver IIFE de paginação
          // logo abaixo), pula primeiro pra parte que contém essa subseção,
          // senão ela fica escondida e o scroll não acha nada
          var showPart = window.__toeflShowPart && window.__toeflShowPart[pos.mod];
          var card = target.closest(".section-card");
          if(showPart && card){ showPart(card, { noScroll: true }); }
          if(target.classList.contains("collapsed")){
            target.classList.remove("collapsed");
            var body = target.nextElementSibling;
            if(body && body.classList.contains("h3-body")) body.classList.remove("h3-collapsed");
          }
          target.scrollIntoView({ behavior: "smooth", block: "center" });
          target.classList.add("resume-highlight");
          setTimeout(function(){ target.classList.remove("resume-highlight"); }, 2200);
        }, 60);
      });
    }
    updateResumeBtn();
  })();

  // ---------- Paginação por Parte, tipo flashcard ----------
  // Pedido do usuário: em vez de rolar por todas as Partes de um módulo de
  // uma vez, mostrar uma Parte inteira por vez com um botão pra passar pra
  // próxima (e voltar pra anterior). Roda depois do accordion de h3 (que já
  // preparou os data-mod/ids); só mexe em visibilidade (hidden), não na
  // ordem/estrutura dos elementos, então o resto do app (observer de scroll,
  // "continuar de onde parei" etc.) continua funcionando normalmente dentro
  // da Parte visível.
  window.__toeflShowPart = window.__toeflShowPart || {};
  (function(){
    function readPartPos(){
      var raw = safeGet("toefl_partpos_v1");
      try{ return JSON.parse(raw) || {}; }catch(e){ return {}; }
    }
    function savePartPos(modKey, idx){
      var obj = readPartPos();
      obj[modKey] = idx;
      safeSet("toefl_partpos_v1", JSON.stringify(obj));
    }
    Array.prototype.slice.call(document.querySelectorAll(".panel")).forEach(function(panel){
      var modKey = panel.dataset.panel;
      var cards = Array.prototype.slice.call(panel.querySelectorAll(".section-card"));
      if(cards.length < 2) return; // um módulo com 1 parte só não precisa de paginação
      var head = panel.querySelector(".panel-head");
      var inner = panel.querySelector(".panel-inner");
      var titles = cards.map(function(c){
        var h2 = c.querySelector("h2");
        return h2 ? h2.textContent.trim() : "";
      });

      var pager = document.createElement("div");
      pager.className = "part-pager";
      pager.innerHTML =
        '<button type="button" class="part-nav-btn part-prev" aria-label="Parte anterior">‹ Anterior</button>' +
        '<span class="part-pager-label"><span class="part-pager-count"></span><b class="part-pager-title"></b></span>' +
        '<button type="button" class="part-nav-btn part-next" aria-label="Próxima parte">Próxima ›</button>';
      if(head && head.parentNode === inner){ head.parentNode.insertBefore(pager, head.nextSibling); }
      else if(inner){ inner.insertBefore(pager, inner.firstChild); }

      // no fim da última Parte, em vez de só esconder o botão, oferece a
      // transição pro próximo módulo -- pedido do usuário: terminar um
      // módulo não tinha nenhum convite claro pra seguir pro seguinte.
      var modIdx = modOrder.indexOf(modKey);
      var nextModKey = modIdx >= 0 ? modOrder[modIdx + 1] : null;
      var nextModBtn = nextModKey ? tabBtns[modOrder.indexOf(nextModKey)] : null;
      var nextModTitle = nextModBtn ? nextModBtn.dataset.title : "";

      var bottomBtns = cards.map(function(card, i){
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "part-next-bottom";
        card.appendChild(btn);
        btn.addEventListener("click", function(){
          var idx = indexOf(card);
          if(idx === cards.length - 1){ if(nextModKey) navTo(nextModKey); }
          else { showPartIdx(idx + 1); }
        });
        return btn;
      });
      var modDoneNote = nextModKey ? null : (function(){
        var el = document.createElement("p");
        el.className = "part-next-bottom part-next-bottom-done";
        el.textContent = "🎉 Última parte do curso!";
        return el;
      })();
      if(modDoneNote){ cards[cards.length - 1].appendChild(modDoneNote); }

      function indexOf(card){ return cards.indexOf(card); }

      function showPart(card, opts){ showPartIdx(indexOf(card), opts); }

      function showPartIdx(idx, opts){
        opts = opts || {};
        idx = Math.max(0, Math.min(cards.length - 1, idx));
        cards.forEach(function(c, i){ c.hidden = i !== idx; });
        pager.querySelector(".part-pager-count").textContent = "Parte " + (idx + 1) + " de " + cards.length + " · ";
        pager.querySelector(".part-pager-title").textContent = titles[idx];
        pager.querySelector(".part-prev").disabled = idx === 0;
        var topNextBtn = pager.querySelector(".part-next");
        topNextBtn.disabled = idx === cards.length - 1 && !nextModKey;
        topNextBtn.textContent = (idx === cards.length - 1 && nextModKey) ? "Próximo módulo ›" : "Próxima ›";
        bottomBtns.forEach(function(btn, i){
          if(i !== idx) return;
          if(idx === cards.length - 1){
            if(nextModKey){ btn.hidden = false; btn.textContent = "Módulo concluído! Próximo: " + nextModTitle + " →"; }
            else { btn.hidden = true; }
          } else { btn.hidden = false; btn.textContent = "Próxima parte: " + titles[idx + 1] + " →"; }
        });
        savePartPos(modKey, idx);
        if(!opts.noScroll){
          window.scrollTo(0, 0);
          var ma = document.getElementById("mainArea"); if(ma) ma.scrollTop = 0;
        }
        // mesma rede de segurança do accordion de h3: abre a primeira
        // subseção da parte que acabou de aparecer
        var firstH3 = cards[idx].querySelector(".h3-toggle");
        if(firstH3 && firstH3.classList.contains("collapsed")){
          firstH3.classList.remove("collapsed");
          var body = firstH3.nextElementSibling;
          if(body && body.classList.contains("h3-body")) body.classList.remove("h3-collapsed");
        }
      }

      pager.querySelector(".part-prev").addEventListener("click", function(){
        var cur = cards.findIndex(function(c){ return !c.hidden; });
        showPartIdx(cur - 1);
      });
      pager.querySelector(".part-next").addEventListener("click", function(){
        var cur = cards.findIndex(function(c){ return !c.hidden; });
        if(cur === cards.length - 1){ if(nextModKey) navTo(nextModKey); return; }
        showPartIdx(cur + 1);
      });

      window.__toeflShowPart[modKey] = showPart;
      var saved = readPartPos()[modKey];
      showPartIdx(typeof saved === "number" ? saved : 0, { noScroll: true });
    });
  })();
})();
