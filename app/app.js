(function(){
  "use strict";
  // ícone de interface: o mesmo <use> do sprite que o build põe no <body>
  // (app/icons.py). Devolve o HTML, para innerHTML.
  function toeflIcon(name, cls){
    return '<svg class="' + (cls || "ico") + '" aria-hidden="true" focusable="false"><use href="#i-' + name + '"/></svg>';
  }
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
    // células dizem coisa tipo "verbo + -s", não uma palavra para pronunciar
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
      // na mesma linha para economizar espaço (ex.: "Verbo | Collocations |
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
          btn.innerHTML = toeflIcon("volume");
          btn.addEventListener("click", function(){ speakText(text); });
          cell.appendChild(btn);
        });
      });
    });
    // avisa, uma vez no topo de cada módulo que usa o recurso, o que o
    // ícone significa -- sem isso o símbolo sozinho não é óbvio para quem
    // nunca viu (M6 ganha o aviso mesmo sem tabela batendo o cabeçalho,
    // por causa do kit de flashcards SRS, que também tem o botão)
    speakPanelsHit["panel-mod6"] = true;
    Object.keys(speakPanelsHit).forEach(function(panelId){
      var panel = document.getElementById(panelId);
      var head = panel && panel.querySelector(".panel-head");
      if(!head || head.nextElementSibling && head.nextElementSibling.classList.contains("speak-hint")) return;
      var hint = document.createElement("div");
      hint.className = "speak-hint";
      hint.innerHTML = '<span class="speak-hint-icon" aria-hidden="true">' + toeflIcon("volume") + '</span><span>Toque neste ícone para ouvir a pronúncia da palavra em inglês sempre que tiver dúvida.</span>';
      head.parentNode.insertBefore(hint, head.nextSibling);
    });

    // Listening (M2): os drills viravam texto para ler em silêncio -- esses
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
        // o texto vai DENTRO do <label> da caixa: assim clicar na frase
        // também marca (antes só a caixinha de 19 px respondia) e o leitor
        // de tela anuncia a caixa com nome
        pendingCheck.appendChild(labelSpan);
        wrap.appendChild(pendingCheck);
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

  // ---------- Conta grátis: o que é amostra (app/free_sample.json) ----------
  // Marca uma vez, na carga, o que fica trancado para a conta logada sem
  // acesso pago: as Partes fora da lista ganham um cartão de cadeado, e o
  // conteúdo delas ganha data-locked. Quem esconde é o CSS, só com
  // body.acc-free; sem essa classe (conta paga, admin, modo offline) o site
  // fica igual a antes. Numa Parte trancada, o exercício da amostra fica à
  // vista com o título e a instrução logo acima dele.
  // O conteúdo continua dentro da página: é um bloqueio de interface, como o
  // da tela de compra (docs/versao-gratuita.md, seção 5).
  var FREE = (function(){
    var el = document.getElementById("freeSample");
    try { return el ? JSON.parse(el.textContent) : null; } catch(e){ return null; }
  })();
  var accessFree = false;
  function isFree(){ return accessFree; }
  function isLockedNow(el){ return accessFree && !!el.closest("[data-locked]"); }
  var FREE_REASON = {
    part: "Esta Parte é do curso completo.",
    partial: "O texto desta Parte é do curso completo.",
    exam: "Os simulados são do curso completo.",
    essay: "A correção de redação é do curso completo."
  };
  var WIDGET_ATTRS = ["data-ctw", "data-drill", "data-spk", "data-bsq", "data-exam", "data-wbox", "data-srs"];
  function isWidget(el){
    return WIDGET_ATTRS.some(function(a){ return el.hasAttribute(a) || !!el.querySelector("[" + a + "]"); });
  }
  function widgetSel(id){
    return WIDGET_ATTRS.map(function(a){ return "[" + a + '="' + id + '"]'; }).join(",");
  }
  function lockCard(reason, extra){
    var box = document.createElement("div");
    box.className = "fs-lock";
    var kicker = document.createElement("p");
    kicker.className = "fs-lock-kicker";
    kicker.innerHTML = toeflIcon("lock") + " Curso completo";
    var text = document.createElement("p");
    text.textContent = reason + (extra ? " " + extra : "") + " Com um plano, você libera os 10 módulos inteiros, todos os exercícios, os simulados e a correção de redação.";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "fs-lock-btn";
    btn.textContent = "Ver os planos";
    btn.addEventListener("click", function(){ openPlans(reason); });
    box.appendChild(kicker); box.appendChild(text); box.appendChild(btn);
    return box;
  }
  if(FREE){
    Array.prototype.forEach.call(document.querySelectorAll(".panel"), function(panel){
      var open = FREE.partes[panel.dataset.panel] || [];
      Array.prototype.forEach.call(panel.querySelectorAll(".section-card"), function(card, i){
        if(open === "todas" || open.indexOf(i + 1) !== -1) return;
        card.classList.add("fs-part-locked");
        var keep = [], labels = [];
        FREE.exercicios.forEach(function(ex){
          var w = card.querySelector(widgetSel(ex.id));
          if(!w) return;
          labels.push(ex.rotulo);
          var top = w;
          while(top.parentNode !== card) top = top.parentNode;
          keep.push(top);
          // leva junto o título e a instrução logo acima, até o h3 anterior
          for(var prev = top.previousElementSibling; prev && prev.tagName !== "H2" && !isWidget(prev); prev = prev.previousElementSibling){
            keep.push(prev);
            if(prev.tagName === "H3") break;
          }
        });
        Array.prototype.forEach.call(card.children, function(ch){
          if(ch.tagName !== "H2" && keep.indexOf(ch) === -1) ch.setAttribute("data-locked", "");
        });
        var reason = card.querySelector("[data-exam]") ? FREE_REASON.exam : labels.length ? FREE_REASON.partial : FREE_REASON.part;
        var extra = labels.length ? "Na conta grátis, fica aberto aqui: " + labels.join(", ") + "." : "";
        var h2 = card.querySelector("h2");
        card.insertBefore(lockCard(reason, extra), h2 ? h2.nextSibling : card.firstChild);
      });
    });
    // exercício aberto só em parte (Build a Sentence): os primeiros itens
    FREE.exercicios.forEach(function(ex){
      if(!ex.itens) return;
      var w = document.querySelector(widgetSel(ex.id));
      var items = w ? w.querySelectorAll(".bsq-card") : [];
      if(items.length <= ex.itens) return;
      Array.prototype.forEach.call(items, function(it, i){ if(i >= ex.itens) it.setAttribute("data-locked", ""); });
      var more = items.length - ex.itens;
      items[ex.itens - 1].parentNode.insertBefore(
        lockCard("Os outros " + more + " itens deste exercício são do curso completo."), items[ex.itens]);
    });
  }

  // ---------- Tipo e tempo de cada Parte (app/partes.json, embutido) ----------
  // { mod0: [{ tipo: "pratica", min: 15 }, ...], ... }, na ordem das Partes.
  var PART_KINDS = (function(){
    var el = document.getElementById("partKinds");
    try { return el ? JSON.parse(el.textContent) : {}; } catch(e){ return {}; }
  })();
  var KIND_NAME = { teoria: "Teoria", pratica: "Prática", simulado: "Simulado", referencia: "Referência" };
  function partInfo(mod, n){ var l = PART_KINDS[mod]; return (l && l[n - 1]) || null; }
  function kindText(p){ return p ? KIND_NAME[p.tipo] + " · " + p.min + " min" : ""; }
  function partCards(mod){ return Array.prototype.slice.call(document.querySelectorAll('.panel[data-panel="' + mod + '"] .section-card')); }
  function partShortTitle(card){
    var h = card && card.querySelector("h2 .htext");
    return h ? h.textContent.trim().replace(/^PARTE\s+\d+\s*[:·]\s*/i, "") : "";
  }

  // ---------- Caixas explicativas: 7 tipos (item 7 de 2026-10-25) ----------
  // Os blocos de citação dos .md viram caixas com tipo: dica, atenção,
  // exemplo, erro comum, resumo, regra da ETS e resposta-modelo. O tipo sai
  // do que já está no texto: o rótulo em negrito do começo ("Erro comum:",
  // "Dica de execução:"), o emoji do começo (💡 ⚠️ 📌 🎯 ⚡ ⏱️ ✅) e, para
  // inglês entre aspas, o parágrafo de cima ("Resposta-modelo", "B1:").
  // Caixa sem marcador fica neutra. O emoji do começo dá lugar ao ícone.
  // Blocos dentro de exercício (texto de prova) não mudam.
  var CALLOUT_TYPES = {
    dica: ["Dica", "bulb"], atencao: ["Atenção", "alert"], exemplo: ["Exemplo", "book"], erro: ["Erro comum", "x-circle"],
    resumo: ["Resumo", "list"], ets: ["Regra da ETS", "shield"], modelo: ["Resposta-modelo", "quote"]
  };
  var CALLOUT_SKIP = ".quiz-drill, .exam, .ctw, .bsq, .spk, .wbox, .srs, .diag-result";
  // palavras de ligação do português (acento não serve: nomes como Tomás)
  var PT_STOP = /\s(não|que|para|uma|você|de|do|os|da|com|em|é|um)\s/i;
  function calloutType(bq, simulado){
    var first = bq.firstElementChild, text = bq.textContent.trim();
    var lead = (text.match(/^[^\p{L}\p{N}"“'(\[*]+/u) || [""])[0].trim();
    var bare = text.slice(lead.length).trim();
    var strong = first && first.firstElementChild && first.firstElementChild.tagName === "STRONG" &&
      first.textContent.trim().slice(lead.length).trim().indexOf(first.firstElementChild.textContent.trim()) === 0
      ? first.firstElementChild.textContent.trim().toLowerCase() : "";
    if(/\berro\b|armadilha|\bnunca\b/.test(strong)) return "erro";
    if(/exemplo|passo \d|minuto \d|segundos \d|plano \(|planejamento/.test(strong)) return "exemplo";
    if(/^(a ets|fonte oficial)/i.test(bare) || /\bets\b/.test(strong)) return "ets";
    if(/resumo|em dois minutos|padrão geral|princípio|regra de ouro|três números|checklist|^regra:/.test(strong)) return "resumo";
    if(/atenção|cuidado|disclaimer|exceção|impacto|importa|confusão|fadiga|o que é fixo|regra de ativação|detectado/.test(strong)) return "atencao";
    if(/dica|foco|como usar|como se autoavaliar|prioridade|objetivo|tempo sugerido|regra prática|meta|grave-se|drill|diagnóstico/.test(strong)) return "dica";
    if(/⚠/.test(lead)) return "atencao";
    if(/💡|🎯|⚡|⏱/.test(lead)) return "dica";
    if(/📌|✅/.test(lead)) return "resumo";
    // texto em inglês (fala, e-mail, parágrafo): exemplo curto ou
    // resposta-modelo. Caixa com rótulo em negrito em inglês é texto de
    // prova (aviso, cardápio, e-mail do exercício) e fica neutra; enunciado
    // de exercício ("Reescreva", "Complete") também.
    if(!strong && /^(["“]|[A-Z][a-z])/.test(bare) && !PT_STOP.test(" " + bare + " ") && !/\(\d\)/.test(bare)){
      var prev = bq.previousElementSibling, label = prev ? prev.textContent.trim() : "";
      if(/reescreva|complete|transforme/i.test(label)) return "";
      if(bq.closest("details.reveal") || /modelo|resposta|banda/i.test(label)) return "modelo";
      if(simulado) return "";
      if(/^(A1|A2|B1|B2|C1|C2)\b/.test(label)) return "exemplo";
      return bare.split(/\s+/).length >= 45 ? "modelo" : "exemplo";
    }
    return "";
  }
  function stripLead(bq){
    var w = document.createTreeWalker(bq, NodeFilter.SHOW_TEXT, null), n;
    while((n = w.nextNode())){
      if(!n.nodeValue.trim()) continue;
      n.nodeValue = n.nodeValue.replace(/^[^\p{L}\p{N}"“'(\[*]+/u, function(m){ return /\S/.test(m) ? "" : m; });
      return;
    }
  }
  Array.prototype.forEach.call(document.querySelectorAll(".panel blockquote"), function(bq){
    if(bq.closest(CALLOUT_SKIP)) return;
    var card = bq.closest(".section-card"), panel = bq.closest(".panel"), simulado = false;
    if(card && panel){
      var cards = Array.prototype.slice.call(panel.querySelectorAll(".section-card"));
      var kinds = (function(){ try { return JSON.parse(document.getElementById("partKinds").textContent); } catch(e){ return {}; } })();
      var p = (kinds[panel.dataset.panel] || [])[cards.indexOf(card)];
      simulado = !!p && p.tipo === "simulado";
    }
    var type = calloutType(bq, simulado);
    bq.classList.add("callout", "callout-" + (type || "neutro"));
    if(!type) return;
    bq.dataset.callout = type;
    stripLead(bq);
    var head = document.createElement("p");
    head.className = "callout-head";
    head.innerHTML = toeflIcon(CALLOUT_TYPES[type][1], "ico callout-ico") + "<span></span>";
    head.lastChild.textContent = CALLOUT_TYPES[type][0];
    bq.insertBefore(head, bq.firstChild);
  });

  // ---------- Tabelas: no celular, as largas viram cartões (item 14) ----------
  // Cada célula leva o nome da sua coluna (data-label), que o CSS mostra
  // dentro do cartão quando a tela é estreita. Tabela de 2 colunas cabe e
  // continua tabela.
  Array.prototype.forEach.call(document.querySelectorAll(".panel table"), function(t){
    var heads = Array.prototype.map.call(t.querySelectorAll("thead th"), function(th){ return th.textContent.trim(); });
    if(heads.length < 3 || t.closest(CALLOUT_SKIP)) return;
    t.classList.add("t-cards");
    Array.prototype.forEach.call(t.querySelectorAll("tbody tr"), function(tr){
      Array.prototype.forEach.call(tr.children, function(td, i){ if(heads[i]) td.setAttribute("data-label", heads[i]); });
    });
  });

  // espelha o client do Supabase e o uid logado para fora do bloco de auth
  // (que é seu próprio IIFE) -- o certificado precisa ler/gravar
  // profiles.display_name e não tinha como chegar em `client`/`uid` de lá
  var supaClient = null, supaUid = null;

  var LS_PROGRESS = "toefl_progress_v1";
  var LS_THEME = "toefl_theme_v1";
  var LS_QUIZ = "toefl_quiz_mod0_v1";

  // chaves que sincronizam com o Supabase (progresso real do aluno).
  // ficam de fora: toefl_theme_v1, toefl_active_tab, toefl_timer_preset, toefl_sync_*
  var SYNC_PREFIXES = ["toefl_progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_avatar", "toefl_errlog_", "toefl_cert_", "toefl_streak", "toefl_dailygoal", "toefl_weeklydash", "toefl_h3progress", "toefl_ctw_", "toefl_spk_", "toefl_write_", "toefl_exam_", "toefl_scorecalc", "toefl_essay_seen", "toefl_goal"];
  function isSyncedKey(key){
    if(!key || key.indexOf("toefl_") !== 0) return false;
    for(var i = 0; i < SYNC_PREFIXES.length; i++){
      if(key.indexOf(SYNC_PREFIXES[i]) === 0) return true;
    }
    return false;
  }
  // texto do rodapé do menu: logado, o progresso vai para a conta (item 25)
  function setSyncNote(online){
    var el = document.getElementById("syncNote");
    if(el) el.textContent = online ? "Sincronizado na sua conta: seu progresso aparece em qualquer aparelho em que você entrar."
                                   : "Seu progresso é salvo neste navegador.";
  }
  window.__toeflSyncNote = setSyncNote;   // ganchos do smoke test
  window.__toeflIsSynced = isSyncedKey;
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

  // ---------- Migração: o diagnóstico virou a Parte 1 do M0 (2026-10-25) ----------
  // Até 2026-10-25 a ordem era 1 O que está em jogo, 2 Radiografia, 3
  // Diagnóstico. Agora é 1 Diagnóstico, 2 O que está em jogo, 3 Radiografia.
  // O progresso das Partes (pid "mod0-N", por posição) e a Parte aberta
  // (índice) foram gravados na ordem antiga. Os objetos gravados daqui em
  // diante levam a marca M0_ORDER_KEY; objeto sem a marca (deste aparelho,
  // de backup importado ou vindo da nuvem) é da ordem antiga e é remapeado
  // uma vez. As subseções (h3-mod0-N) não mudam: a do diagnóstico nunca teve id.
  var M0_ORDER_KEY = "_ordem_m0", M0_ORDER = 2;
  var M0_PID_MAP = { "mod0-1": "mod0-2", "mod0-2": "mod0-3", "mod0-3": "mod0-1" };
  var M0_IDX_MAP = { 0: 1, 1: 2, 2: 0 };
  function migrateM0Order(){
    function fix(key, remap){
      var raw = null, obj;
      try { raw = localStorage.getItem(key); } catch(e){}
      if(!raw) return;
      try { obj = JSON.parse(raw); } catch(e){ return; }
      if(!obj || typeof obj !== "object" || obj[M0_ORDER_KEY] === M0_ORDER) return;
      remap(obj);
      obj[M0_ORDER_KEY] = M0_ORDER;
      try { localStorage.setItem(key, JSON.stringify(obj)); } catch(e){}
      return true;
    }
    var progressMoved = fix("toefl_progress_v1", function(o){
      var old = {};
      Object.keys(M0_PID_MAP).forEach(function(k){ if(k in o){ old[k] = o[k]; delete o[k]; } });
      Object.keys(old).forEach(function(k){ o[M0_PID_MAP[k]] = old[k]; });
    });
    fix("toefl_partpos_v1", function(o){
      if(typeof o.mod0 === "number" && o.mod0 in M0_IDX_MAP) o.mod0 = M0_IDX_MAP[o.mod0];
    });
    // a nuvem ainda tem a ordem antiga: marca para subir a versão nova (sem
    // passar pelo safeSet, que contaria a carga da página como dia de estudo)
    if(progressMoved){ try { localStorage.setItem("toefl_dirty", "1"); } catch(e){} }
  }
  migrateM0Order();
  window.__toeflMigrateM0 = migrateM0Order; // gancho do smoke test

  // ---------- Sequência de dias estudando (streak) ----------
  // Marca o dia de hoje sempre que qualquer chave sincronizada é escrita
  // (checkbox de progresso, quiz, SRS, registro de erro etc.) -- ou seja,
  // qualquer atividade real de estudo, não só abrir o site. O guard de
  // "já marcado hoje" evita reescrever a cada tecla e evita recursão (marcar
  // o streak também passa por safeSet, que por sua vez chamaria
  // markStreakToday de novo se não fosse por isso).
  var LS_STREAK = "toefl_streak_v1";
  // data LOCAL do aparelho (aaaa-mm-dd). Não usar toISOString(): ele devolve
  // a data em UTC, e no Brasil (UTC-3) o "hoje" virava amanhã às 21h, o que
  // zerava a meta do dia e furava a sequência de quem estuda à noite.
  function todayStr(d){
    d = d || new Date();
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }
  // "aaaa-mm-dd" -> Date local à meia-noite (ou null), e dias de hoje até lá
  function parseDay(s){
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
  }
  function daysUntil(s){
    var d = parseDay(s);
    return d ? Math.round((d - parseDay(todayStr())) / 86400000) : null;
  }
  // meta do aluno, gravada na tela de resultado do diagnóstico:
  // { target: banda 1 a 6, exam: "aaaa-mm-dd", sched: 30|60|90, start: "aaaa-mm-dd" }
  var LS_GOAL = "toefl_goal_v1";
  function readGoal(){
    var g = null;
    try { g = JSON.parse(safeGet(LS_GOAL) || "null"); } catch(e){}
    return g && typeof g === "object" && g.target && g.exam ? g : null;
  }
  function markStreakToday(){
    var data = {}; try { data = JSON.parse(safeGet(LS_STREAK) || "{}"); } catch(e){}
    if(!data.days) data.days = {};
    var t = todayStr();
    if(data.days[t]) return;
    data.days[t] = true;
    var keys = Object.keys(data.days);
    if(keys.length > 400){ keys.sort(); delete data.days[keys[0]]; } // não guarda histórico infinito
    safeSet(LS_STREAK, JSON.stringify(data));
    updateDailyGoalUI(); // a linha da sequência na gaveta muda junto
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

  // ---------- Registro do dia: atividades concluídas ----------
  // count: Partes e exercícios concluídos hoje (só a transição para
  // concluído conta, então marcar e desmarcar não infla). ex: data do último
  // exercício feito, que a meta de hoje usa. plan: a lista da meta de hoje,
  // congelada no primeiro cálculo do dia (ver "Plano de estudo" mais abaixo).
  var LS_DAILY_GOAL = "toefl_dailygoal_v1";
  function readDay(){
    var data = {};
    try { data = JSON.parse(safeGet(LS_DAILY_GOAL) || "{}") || {}; } catch(e){}
    if(data.date !== todayStr()) data = { date: todayStr(), count: 0 };
    return data;
  }
  function markDailyGoalProgress(isExercise){
    var data = readDay();
    data.count = (data.count || 0) + 1;
    if(isExercise) data.ex = data.date;
    safeSet(LS_DAILY_GOAL, JSON.stringify(data));
    updateDailyGoalUI();
  }
  function updateDailyGoalUI(){
    if(typeof window.__toeflRefreshPlan === "function") window.__toeflRefreshPlan();
    // sequência de dias à vista na gaveta (antes só dentro do Painel, que
    // só abre com login)
    var streakEl = document.getElementById("streakLine");
    var topStreak = document.getElementById("topStreak");
    if(topStreak) topStreak.textContent = computeStreak().count;
    if(streakEl){
      var s = computeStreak();
      streakEl.innerHTML = "";
      if(s.count === 0){
        streakEl.textContent = "Que tal 20 minutos hoje? Um pouco por dia rende mais do que muito de vez em quando.";
      } else {
        var b = document.createElement("b");
        b.textContent = s.count + (s.count === 1 ? " dia" : " dias");
        streakEl.appendChild(b);
        streakEl.appendChild(document.createTextNode(s.count === 1 ? " de estudo seguido" : " de estudo seguidos"));
        if(!s.today) streakEl.appendChild(document.createTextNode(". Estude hoje para manter."));
      }
    }
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
  var topChip = document.getElementById("topChip");
  if(topChip) topChip.addEventListener("click", function(){ setSidebarOpen(true); });
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
    // a coluna "Nesta Parte" (montada mais abaixo) acompanha a troca de módulo
    if(window.__toeflRenderRail) window.__toeflRenderRail();
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

  // barra do topo: módulo e Parte atuais. A Parte vem da paginação, que é
  // montada mais abaixo e avisa por setBarPart().
  var jtMod = document.getElementById("jtMod"), jtPart = document.getElementById("jtPart");
  var journeyTitle = document.getElementById("journeyTitle");
  var barParts = {}, currentTab = null;
  function renderBar(){
    var btn = tabBtns.filter(function(b){ return b.dataset.tab === currentTab; })[0];
    if(!btn || !jtMod) return;
    var badge = btn.querySelector(".num-badge");
    jtMod.textContent = (badge ? badge.dataset.n + " · " : "") + btn.dataset.title;
    jtPart.textContent = barParts[currentTab] || "";
  }
  function setBarPart(modKey, text){ barParts[modKey] = text; if(modKey === currentTab) renderBar(); }
  if(journeyTitle) journeyTitle.addEventListener("click", function(){ setSidebarOpen(true); });

  function showTab(key){
    currentTab = key;
    renderBar();
    tabBtns.forEach(function(b){
      var on = b.dataset.tab === key;
      b.classList.toggle("active", on);
      if(on) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
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
    // isso a tela troca para um módulo novo e mostra tudo fechado até o
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
    // na conta grátis, a porcentagem mede a amostra: Parte trancada não conta
    // (docs/versao-gratuita.md, seção 4). O certificado continua exigindo o
    // curso inteiro, e por isso não aparece na conta grátis.
    allChecks.filter(function(c){ return !isLockedNow(c); }).forEach(function(c){
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
    if(opCount) opCount.innerHTML = "<b>" + modsDone + "</b> de " + modOrder.length + (accessFree ? " módulos com a amostra concluída" : " módulos concluídos");
    Array.prototype.forEach.call(document.querySelectorAll(".ph-progress-label span:first-child"), function(s){
      s.textContent = accessFree ? "Seu progresso na amostra deste módulo" : "Seu progresso neste módulo";
    });

    // curso inteiro concluído (todos os módulos + o quiz do último, já que o
    // gate de avanço só valida o módulo ANTERIOR ao entrar no próximo — o
    // último nunca passa por essa checagem sozinho)
    var lastMod = modOrder[modOrder.length - 1];
    var courseDone = !accessFree && modsDone === modOrder.length && moduleQuizPct(lastMod) >= 100;
    var certBtn = document.getElementById("certBtn");
    if(certBtn) certBtn.hidden = !courseDone;
    if(courseDone && !safeGet("toefl_cert_date_v1")){
      safeSet("toefl_cert_date_v1", new Date().toISOString());
    }

    // reflete no estado visual da sidebar: concluído (✓), atual, ou bloqueado (🔒).
    // o número do módulo fica sempre visível (mesmo bloqueado — o texto dos
    // módulos referencia "Módulo N" e precisa bater com o que aparece aqui);
    // só o "%" de progresso é escondido quando bloqueado, para não parecer que
    // dá para entrar só porque já tem progresso ali.
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
      var tabFill = document.getElementById("tabFill-" + key);
      if(tabFill) tabFill.style.width = (modPct[key] || 0) + "%";
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
    // "aula assistida" de uma videoaula também é um .pchk (conta no
    // progresso do módulo), mas não conclui nem fecha a Parte onde está
    var isVideo = c.classList.contains("vid-chk");
    if(progressState[pid]){
      c.checked = true;
      var doneCard = isVideo ? null : c.closest(".section-card");
      if(doneCard) doneCard.classList.add("done");
    }
    c.addEventListener("change", function(){
      var wasChecked = progressState[pid];
      progressState[pid] = c.checked;
      if(c.checked && !wasChecked) markDailyGoalProgress();
      var card = isVideo ? null : c.closest(".section-card");
      if(card){
        card.classList.toggle("done", c.checked);
        // marcar a Parte como concluída fecha as subseções dela de volta
        // (economiza espaço na tela) -- ainda dá para reabrir clicando
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
      progressState[M0_ORDER_KEY] = M0_ORDER; // já na ordem nova do M0 (ver migrateM0Order)
      safeSet(LS_PROGRESS, JSON.stringify(progressState));
      updateBadges();
      if(!c.checked) updateDailyGoalUI(); // desmarcar também mexe na meta de hoje
    });
  });
  updateBadges();

  // ---------- Nivelamento: o diagnóstico (M0) calibra o resto do curso ----------
  // Mesma tabela % -> banda CEFR do Módulo 0, Parte 4.2. O gate de avanço do
  // diagnóstico exige só responder as 10 (ver isUnlocked/moduleQuizPct) --
  // nunca um mínimo de acertos. O que os acertos FAZEM é isto aqui: estimar
  // a banda de entrada e recomendar um dos 3 cronogramas do Módulo 0, Parte 6.
  // A tabela mora em app/level.js (ToeflLevel), que o build cola antes deste
  // arquivo: a tela de apresentação usa a mesma no diagnóstico sem conta.
  function cefrBandFromPct(pct){ return ToeflLevel.band(pct); }
  // cronograma do aluno: o da meta salva (nota e data da prova) quando há
  // meta; sem ela, o indicado só pelo nível do diagnóstico
  function scheduleFromPct(pct){
    var g = readGoal(), p = g && ToeflLevel.PLANS[g.sched];
    return p ? "Cronograma " + p.name + " (" + p.days + " dias) · Módulo 0, Parte " + p.part : ToeflLevel.schedule(pct);
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
    // na conta grátis, só o que está aberto (isLockedNow)
    var drills = Array.prototype.filter.call(document.querySelectorAll('.quiz-drill[data-drill^="' + prefix + '"]'), function(d){ return !isLockedNow(d); });
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
    // Reading inclui o Complete the Words de digitar: cada texto verificado
    // entra com as suas 10 lacunas
    if(prefix === "mod1-"){
      var ctw = extraAccuracy("ctw");
      total += ctw.total; confirmed += ctw.confirmed; correct += ctw.correct;
    }
    return { total: total, confirmed: confirmed, correct: correct };
  }
  // acertos dos exercícios que não são .quiz-drill, lidos do estado salvo
  // (o mesmo que cada widget grava): "ctw", "bsq" ou "exam"
  function extraAccuracy(kind){
    var total = 0, confirmed = 0, correct = 0;
    function read(key){ try { return JSON.parse(safeGet(key) || "{}") || {}; } catch(e){ return {}; } }
    if(kind === "ctw"){
      Array.prototype.forEach.call(document.querySelectorAll(".ctw"), function(root){
        if(isLockedNow(root)) return;
        var inputs = root.querySelectorAll(".ctw-in");
        var st = read("toefl_ctw_" + root.dataset.ctw + "_v1");
        total += inputs.length;
        if(!st.checked || !st.vals) return;
        confirmed += inputs.length;
        Array.prototype.forEach.call(inputs, function(input, i){
          if(String(st.vals[i] || "").trim().toLowerCase() === input.dataset.answer.toLowerCase()) correct++;
        });
      });
    } else if(kind === "bsq"){
      Array.prototype.forEach.call(document.querySelectorAll(".bsq"), function(root){
        var st = read("toefl_bsq_" + root.dataset.bsq + "_v1");
        Array.prototype.forEach.call(root.querySelectorAll(".bsq-card"), function(card){
          if(isLockedNow(card)) return;
          total++;
          var s = st[card.dataset.num];
          if(s && s.checked){ confirmed++; if(s.ok) correct++; }
        });
      });
    } else if(kind === "exam"){
      Array.prototype.forEach.call(document.querySelectorAll(".exam"), function(root){
        if(isLockedNow(root)) return;
        var st = read("toefl_exam_" + root.dataset.exam + "_v1");
        Array.prototype.forEach.call(root.querySelectorAll(".exam-item"), function(it){
          total++;
          if(!st.done || !st.answers) return;
          confirmed++;
          if(st.answers[it.dataset.num] === it.dataset.correct) correct++;
        });
      });
    }
    return { total: total, confirmed: confirmed, correct: correct };
  }
  var LIVE_SCORE_MIN = 10;
  function renderLiveScoreSection(prefix, pctId, bandId, emptyText){
    var pctEl = document.getElementById(pctId);
    var bandEl = document.getElementById(bandId);
    if(!pctEl || !bandEl) return;
    // prefixo "extra:<tipo>" = exercício que não é .quiz-drill
    var a = prefix.indexOf("extra:") === 0 ? extraAccuracy(prefix.slice(6)) : computeQuizAccuracy(prefix);
    if(a.confirmed === 0){
      pctEl.textContent = "—";
      bandEl.textContent = emptyText;
      return;
    }
    var pct = Math.round(100 * a.correct / a.confirmed);
    var band = cefrBandFromPct(pct);
    pctEl.textContent = pct + "%";
    // com poucas respostas o percentual não diz nada (1 de 1 daria "banda
    // 6"): a banda só aparece a partir de LIVE_SCORE_MIN respostas
    var tail = a.correct + "/" + a.confirmed + " confirmadas" + (a.confirmed < a.total ? " de " + a.total + " no total" : "");
    bandEl.textContent = (a.confirmed < LIVE_SCORE_MIN
      ? "Amostra pequena: a banda aparece a partir de " + LIVE_SCORE_MIN + " respostas"
      : "Banda " + band.code + " (" + band.label + ")") + " · " + tail;
  }
  function updateLiveScorePanel(){
    renderLiveScoreSection("mod1-", "liveScoreReadingPct", "liveScoreReadingBand", "Responda aos exercícios do Módulo 1 para calcular");
    renderLiveScoreSection("mod2-", "liveScoreListeningPct", "liveScoreListeningBand", "Responda aos exercícios do Módulo 2 para calcular");
    renderLiveScoreSection("extra:bsq", "liveScoreWritingPct", "liveScoreWritingBand", "Faça o exercício interativo do Módulo 4 para calcular");
    renderLiveScoreSection("extra:exam", "liveScoreExamPct", "liveScoreExamBand",
      accessFree ? FREE_REASON.exam : "Entregue um bloco de simulado do Módulo 7 para calcular");
  }

  // diagnóstico do M0 lido do estado salvo: acertos no total e por área
  // (data-area de cada questão, ver quiz_mod0.json). done: as 10 respondidas.
  function diagStats(){
    var drill = document.querySelector('.quiz-drill[data-drill="mod0-diag"]');
    if(!drill) return null;
    var st = {};
    try { st = JSON.parse(safeGet("toefl_quiz_mod0-diag_v1") || "{}") || {}; } catch(e){}
    var out = { total: 0, confirmed: 0, correct: 0, areas: {} };
    Array.prototype.forEach.call(drill.querySelectorAll(".qcard"), function(c){
      var a = c.dataset.area || "outros", s = st[c.dataset.num];
      out.total++;
      out.areas[a] = out.areas[a] || { ok: 0, n: 0 };
      out.areas[a].n++;
      if(s && s.confirmed){
        out.confirmed++;
        if(isCardCorrect(c, s.picked)){ out.correct++; out.areas[a].ok++; }
      }
    });
    out.done = out.total > 0 && out.confirmed === out.total;
    out.pct = out.total ? Math.round(100 * out.correct / out.total) : 0;
    return out;
  }

  // melhor estimativa disponível da banda CEFR atual do aluno: prioriza o
  // diagnóstico do Módulo 0 (se completo), senão usa o agregado dos Action
  // Drills de Reading/Listening já respondidos. Movida para o escopo
  // compartilhado (era local do modal do painel) para também alimentar a
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
      return { pct: Math.round(100 * correct / confirmed), source: "exercícios de Reading e Listening" };
    }
    return null;
  }

  // Action Drills de nível diferente para cada aluno: cada drill de M1/M2 tem
  // um nível CEFR (ver "level" em drills_data.py, ex. "B2–C1"). Marca como
  // "recomendado para você" os que incluem a banda estimada atual do aluno,
  // sem esconder os outros -- navegação livre continua valendo (ver decisão
  // em CLAUDE.md), isso só destaca por onde começar.
  function updateLevelRecommendations(){
    var est = computeBandEstimate();
    if(!est) return; // sem diagnóstico/drills respondidos ainda, não dá para recomendar nada
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
    if(typeof window.__toeflRefreshLevelPractice === "function") window.__toeflRefreshLevelPractice();
  }

  // Embaralha a ordem das alternativas de uma questão NA TELA. Roda a cada
  // carregamento da página e a cada "Refazer", para o aluno não decorar a
  // posição da resposta. A letra que identifica a alternativa para correção
  // e para o progresso salvo é a de origem (data-letter) e não muda; o que
  // muda é a ordem e a letra mostrada (.oletter). As explicações citam
  // alternativas em <span class="optref" data-ref="X">, atualizadas aqui.
  var CHOICE_LETTERS = ["A", "B", "C", "D", "E", "F"];
  function shuffleChoices(card, optSelector){
    if(!card || card.hasAttribute("data-noshuffle")) return;
    var opts = Array.prototype.slice.call(card.querySelectorAll(optSelector));
    if(opts.length < 2) return;
    var parent = opts[0].parentNode;
    for(var i = opts.length - 1; i > 0; i--){
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = opts[i]; opts[i] = opts[j]; opts[j] = tmp;
    }
    var shown = {};
    opts.forEach(function(o, idx){
      parent.appendChild(o);
      shown[o.dataset.letter] = CHOICE_LETTERS[idx];
      var label = o.querySelector(".oletter");
      if(label) label.textContent = CHOICE_LETTERS[idx];
    });
    Array.prototype.forEach.call(card.querySelectorAll(".optref"), function(ref){
      var L = shown[ref.dataset.ref];
      if(L) ref.textContent = "(" + L + ")";
    });
  }

  // Devolutiva em palavras, usada pelos quizzes e pelos simulados. Antes a
  // correção era só cor (errada em vermelho, certa em laranja): quem não
  // distingue as duas não sabia se tinha acertado. Agora cada alternativa
  // ganha uma etiqueta ("sua resposta", "correta") e a questão ganha uma
  // frase de veredito, anunciada por leitor de tela (role="status").
  function shownLetter(opt){
    var l = opt.querySelector(".oletter");
    return l ? l.textContent.trim() : opt.dataset.letter;
  }
  function setOptTag(opt, text, kind){
    var tag = opt.querySelector(".otag");
    if(!text){ if(tag) tag.parentNode.removeChild(tag); return; }
    if(!tag){ tag = document.createElement("span"); opt.appendChild(tag); }
    tag.className = "otag otag-" + kind;
    tag.textContent = text;
  }
  function verdictText(ok, pickedOpts, keyOpts){
    function list(opts){
      var L = opts.map(function(o){ return "(" + shownLetter(o) + ")"; });
      return L.length > 1 ? L.slice(0, -1).join(", ") + " e " + L[L.length - 1] : (L[0] || "");
    }
    if(ok) return "Você acertou.";
    return "Quase. Você marcou " + list(pickedOpts) + ", mas " + (keyOpts.length > 1 ? "as respostas são " : "a resposta é ") + list(keyOpts) + ".";
  }
  // marca as alternativas de uma questão corrigida e devolve a frase
  function tagOptions(opts, pickedLetters, keyLetters){
    var picked = [], key = [];
    opts.forEach(function(o){
      var L = o.dataset.letter, isKey = keyLetters.indexOf(L) !== -1, isPicked = pickedLetters.indexOf(L) !== -1;
      if(isKey) key.push(o);
      if(isPicked) picked.push(o);
      if(isKey && isPicked) setOptTag(o, "sua resposta, correta", "ok");
      else if(isKey) setOptTag(o, "correta", "ok");
      else if(isPicked) setOptTag(o, "sua resposta", "bad");
      else setOptTag(o, "");
    });
    var ok = key.length === picked.length && key.every(function(o){ return picked.indexOf(o) !== -1; });
    return { ok: ok, text: verdictText(ok, picked, key) };
  }
  function setVerdict(holder, beforeNode, result){
    var v = holder.querySelector(".verdict");
    if(!result){ if(v) v.parentNode.removeChild(v); return; }
    if(!v){
      v = document.createElement("p");
      v.setAttribute("role", "status");
      holder.insertBefore(v, beforeNode || null);
    }
    v.className = "verdict " + (result.ok ? "verdict-ok" : "verdict-bad");
    v.textContent = (result.ok ? "✓ " : "✗ ") + result.text;
  }

  var quizDrills = Array.prototype.slice.call(document.querySelectorAll(".quiz-drill"));

  quizDrills.forEach(function(drillEl){
    var drillId = drillEl.dataset.drill;
    var lsKey = "toefl_quiz_" + drillId + "_v1";
    var state = {}; // { num: { picked: "A", confirmed: true/false } }
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }

    var qcards = Array.prototype.slice.call(drillEl.querySelectorAll(".qcard"));
    // data-reveal="end" (diagnóstico do M0): a resposta confirmada fica
    // guardada sem correção, e o gabarito com as explicações aparece em todas
    // as questões de uma vez, depois da última (item 2 de 2026-10-25)
    var revealAtEnd = drillEl.dataset.reveal === "end";
    function allConfirmed(){
      return qcards.every(function(c){ return state[c.dataset.num] && state[c.dataset.num].confirmed; });
    }
    function setPending(card, on){
      var note = card.querySelector(".qpending");
      if(!on){ if(note) note.parentNode.removeChild(note); return; }
      if(!note){
        note = document.createElement("p");
        note.className = "qpending";
        note.setAttribute("role", "status");
        note.textContent = "Resposta guardada. O gabarito aparece no fim, depois da última questão.";
        card.appendChild(note);
      }
    }

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
      if(drillId === "mod0-diag" && typeof window.__toeflRefreshStart === "function") window.__toeflRefreshStart();
      if(drillId === "mod0-diag" && typeof window.__toeflRefreshDiag === "function") window.__toeflRefreshDiag();
      if(drillId === "mod0-diag" && typeof window.__toeflRefreshPlan === "function") window.__toeflRefreshPlan();
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
      if(!s || !s.confirmed){
        opts.forEach(function(o){ setOptTag(o, ""); });
        if(fb) setVerdict(fb, null, null);
      }
      var pending = revealAtEnd && !!s && s.confirmed && !allConfirmed();
      setPending(card, pending);
      if(pending){
        var mine = multi ? (s.picked || []) : [s.picked];
        opts.forEach(function(o){
          var on = mine.indexOf(o.dataset.letter) !== -1;
          o.disabled = true;
          o.classList.remove("correct", "wrong");
          o.classList.toggle("picked", on);
          o.setAttribute("aria-pressed", on ? "true" : "false");
          setOptTag(o, on ? "sua resposta" : "", "pending");
        });
        if(confirmBtn) confirmBtn.hidden = true;
        if(fb){ setVerdict(fb, null, null); fb.hidden = true; }
        return;
      }
      if(!s){
        opts.forEach(function(o){ o.disabled = false; o.classList.remove("correct","wrong","picked"); o.setAttribute("aria-pressed", "false"); });
        if(confirmBtn){ confirmBtn.hidden = true; confirmBtn.disabled = true; }
        if(fb) fb.hidden = true;
        return;
      }
      if(!s.confirmed){
        var pickedList = multi ? (s.picked || []) : (s.picked ? [s.picked] : []);
        opts.forEach(function(o){
          o.disabled = false;
          var on = pickedList.indexOf(o.dataset.letter) !== -1;
          o.classList.toggle("picked", on);
          o.setAttribute("aria-pressed", on ? "true" : "false");
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
        if(fb){
          setVerdict(fb, fb.firstChild, tagOptions(opts, gotSet, wantSet));
          fb.hidden = false;
        }
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
          var wasDone = allConfirmed();
          s.confirmed = true;
          saveState();
          // exercício inteiro respondido conta na meta de hoje
          if(!wasDone && allConfirmed()) markDailyGoalProgress(true);
          if(revealAtEnd && !wasDone && allConfirmed()){
            // a última: corrige todas de uma vez e mostra o resultado
            qcards.forEach(applyCardState);
            renderSummary();
            drillEl.dispatchEvent(new CustomEvent("toefl-reveal", { bubbles: true }));
            return;
          }
          applyCardState(card);
          renderSummary();
        });
      }

      // questão ainda não respondida nesta conta: ordem nova a cada sessão.
      // A já confirmada fica como está, com a correção já à mostra.
      if(!(state[num] && state[num].confirmed)) shuffleChoices(card, ".opt");
      applyCardState(card);
    });

    var retryBtn = drillEl.querySelector(".quiz-retry");
    if(retryBtn){
      retryBtn.addEventListener("click", function(){
        state = {};
        saveState();
        qcards.forEach(function(card){ shuffleChoices(card, ".opt"); });
        qcards.forEach(applyCardState);
        renderSummary();
      });
    }

    renderSummary();
  });

  // ---------- Cronômetro de seção ----------
  // setDrillTimerMinutes fica exposta fora da IIFE para o botão "iniciar
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
    // presets antigos (antes da conferência com a ETS de 2026-10-07) viram os
    // novos: tempo-base de cada seção e duração máxima da prova
    var OLD_PRESETS = { 28: 30, 18: 29, 85: 89 };
    if(OLD_PRESETS[minutes]){ minutes = OLD_PRESETS[minutes]; safeSet(LS_PRESET, String(minutes)); }
    if(!minutes || minutes < 1) minutes = 30;
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
      btn.innerHTML = toeflIcon("timer") + " Iniciar cronômetro (" + mins + " min)";
      btn.addEventListener("click", function(){ setDrillTimerMinutes(mins); });
      if(node.hasAttribute("data-locked")) btn.setAttribute("data-locked", ""); // drill fora da amostra grátis
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
    // texto). Não pontua nada, só mostra o que o app "ouviu" para comparar com
    // o que o aluno pretendia dizer. Sem suporte no navegador (ex.: Firefox),
    // o gravador de áudio continua funcionando normal, só sem essa parte.
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognizer = null, finalTranscript = "";

    // Plano B do iPhone/iPad. No iOS o Safari até expõe o reconhecimento de
    // fala, mas rodar ele junto com o MediaRecorder disputa o microfone: um
    // dos dois para ou volta vazio. Então no iOS o padrão é só gravar o áudio,
    // e uma opção "Só transcrever" usa só o reconhecimento. Sem reconhecimento
    // nenhum (Firefox, alguns navegadores dentro de app), aparece um aviso
    // fixo e o gravador segue funcionando. Transcrição no servidor fica para a
    // Etapa 5 do ROADMAP.
    var isIOS = /iP(hone|ad|od)/.test(navigator.userAgent) ||
                (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    // splitMode: neste aparelho é gravar OU transcrever, nunca os dois juntos
    var splitMode = isIOS, transcribing = false;
    var modeWrap = document.getElementById("mrModeWrap");
    var modeChk = document.getElementById("mrMode");
    var noteEl = document.getElementById("mrNote");
    function setNote(txt){ if(!noteEl) return; noteEl.textContent = txt || ""; noteEl.hidden = !txt; }
    function transcribeOnly(){ return !!(splitMode && SpeechRec && modeChk && modeChk.checked); }
    function concurrentTranscript(){ return !!SpeechRec && !splitMode; }
    if(!SpeechRec){
      setNote("Transcrição automática indisponível neste navegador. A gravação funciona normalmente: ouça e compare com o texto do exercício.");
    } else if(isIOS){
      if(modeWrap) modeWrap.hidden = false;
      setNote("No iPhone e no iPad, gravar e transcrever ao mesmo tempo não funciona bem. Grave para ouvir sua voz, ou marque \"Só transcrever\" para ver o texto que o aparelho entendeu.");
    }

    function startTranscript(onError, onEnd){
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
        recognizer.onerror = function(e){ if(onError) onError(e); }; // no modo normal fica silencioso: o áudio gravado continua valendo
        // o iOS encerra o reconhecimento sozinho depois de um silêncio
        recognizer.onend = function(){ if(onEnd) onEnd(); };
        recognizer.start();
      } catch(ex){ recognizer = null; if(onError) onError(ex); }
    }
    function stopTranscript(){
      // zera antes de parar: o stop() dispara o onend, que pode voltar aqui
      var r = recognizer;
      recognizer = null;
      if(r){ try { r.stop(); } catch(ex){} }
    }

    if((!navigator.mediaDevices || !window.MediaRecorder) && !SpeechRec){
      recBtn.disabled = true;
      statusEl.textContent = "Gravação não suportada neste navegador.";
    } else if(!navigator.mediaDevices || !window.MediaRecorder){
      // sem gravador mas com reconhecimento: o modo "só transcrever" é o que sobra
      if(modeWrap) modeWrap.hidden = false;
      if(modeChk){ modeChk.checked = true; modeChk.disabled = true; }
      splitMode = true;
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
      if(transcribeOnly()){
        // plano B: só o reconhecimento de fala, sem MediaRecorder
        revoke();
        audioEl.hidden = true;
        clearBtn.hidden = true;
        transcribing = true;
        var failed = "";
        startTranscript(function(e){
          var err = e && e.error;
          if(err === "no-speech" || err === "aborted") return; // silêncio ou parada normal: o onend cuida
          failed = err === "not-allowed" || err === "service-not-allowed"
            ? "Permissão de microfone ou de reconhecimento de fala negada."
            : (err === "network" ? "A transcrição precisa de internet." : "Não foi possível transcrever agora.");
          if(transcribing) stopRec(failed);
        }, function(){
          if(transcribing) stopRec(failed);
        });
        if(!transcribing) return; // falhou já na partida
        elapsed = 0; display.textContent = "00:00";
        wrap.classList.add("recording");
        recBtn.textContent = "■ Parar";
        if(modeChk) modeChk.disabled = true;
        statusEl.textContent = "Transcrevendo… fale em inglês.";
        tick = setInterval(function(){ elapsed++; display.textContent = fmt(elapsed); }, 1000);
        return;
      }
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
        if(concurrentTranscript()) startTranscript();
        elapsed = 0; display.textContent = "00:00";
        wrap.classList.add("recording");
        recBtn.textContent = "■ Parar";
        statusEl.textContent = "Gravando…";
        tick = setInterval(function(){ elapsed++; display.textContent = fmt(elapsed); }, 1000);
      }).catch(function(){
        statusEl.textContent = "Permissão de microfone negada.";
      });
    }
    function stopRec(failMsg){
      stopClock();
      stopTranscript();
      wrap.classList.remove("recording");
      recBtn.textContent = "● Gravar";
      if(transcribing){
        // modo só transcrever: não há áudio para ouvir (rec é null), sobra o texto
        transcribing = false;
        if(modeChk && (navigator.mediaDevices && window.MediaRecorder)) modeChk.disabled = false;
        clearBtn.hidden = false;
        statusEl.textContent = typeof failMsg === "string" && failMsg ? failMsg : "Compare o texto com o que você quis dizer.";
        return;
      }
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
    if(modeChk) modeChk.addEventListener("change", function(){
      clearRec();
      if(modeChk.checked) statusEl.textContent = "Fale e veja o texto que o aparelho entendeu.";
    });
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
          function(){ flash("Arquivo baixado e copiado para a área de transferência."); },
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
            // os dois marcadores internos da sincronização são do aparelho
            // que exportou, não entram
            if(k === "toefl_sync_at" || k === "toefl_dirty") return;
            if(k.indexOf(PREFIX) === 0 && typeof data[k] === "string"){ localStorage.setItem(k, data[k]); n++; }
          });
          if(!n){ flash("Nenhum dado do iTOEFL neste arquivo.", false); return; }
          // marca como alteração local pendente: com conta logada, o que foi
          // importado sobe para a nuvem em vez de ser trocado pelo que está lá
          localStorage.setItem("toefl_dirty", "1");
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
      // tudo que é progresso de estudo. Ficam de fora, de propósito: a
      // sequência de dias e a meta de hoje (histórico de constância), a foto
      // e as preferências do aparelho (tema, cronômetro, trilha).
      var RESET_PREFIXES = ["toefl_progress", "toefl_h3progress", "toefl_srs_", "toefl_bsq_", "toefl_quiz_", "toefl_errlog_", "toefl_cert_", "toefl_ctw_", "toefl_spk_", "toefl_write_", "toefl_exam_", "toefl_scorecalc", "toefl_weeklydash", "toefl_partpos", "toefl_lastpos", "toefl_goal"];
      // confirmação dupla (item 28 de 2026-10-25): o botão abre um aviso, o
      // aviso pede uma segunda confirmação, e só ela apaga
      var confirmBox = document.getElementById("resetConfirm");
      var confirmText = document.getElementById("resetConfirmText");
      var yesBtn = document.getElementById("resetYes");
      var step = 0;
      function setStep(n){
        step = n;
        confirmBox.hidden = n === 0;
        resetBtn.hidden = n !== 0;
        if(n === 1){
          confirmText.textContent = "Isso apaga todo o seu progresso no curso: Partes e subseções marcadas, questões respondidas, " +
            "flashcards, textos escritos, a sua meta e o registro de erros.";
          yesBtn.textContent = "Quero apagar";
          yesBtn.className = "side-action";
        } else if(n === 2){
          confirmText.textContent = "Tem certeza? Depois de apagar, não dá para desfazer. Se quiser guardar uma cópia, use Exportar progresso antes.";
          yesBtn.textContent = "Apagar tudo agora";
          yesBtn.className = "side-action is-danger";
        }
        if(n) yesBtn.focus();
      }
      resetBtn.addEventListener("click", function(){ setStep(1); });
      document.getElementById("resetCancel").addEventListener("click", function(){ setStep(0); resetBtn.focus(); });
      yesBtn.addEventListener("click", function(){
        if(step === 1){ setStep(2); return; }
        if(step !== 2) return;
        setStep(0);
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

    // na conta grátis só contam os itens abertos (app/free_sample.json)
    function liveCards(){ return cards.filter(function(c){ return !isLockedNow(c); }); }
    function renderSummary(){
      var live = liveCards(), total = live.length, checked = 0, right = 0;
      live.forEach(function(card){
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
        updateLiveScorePanel();
        // o conjunto inteiro verificado conta como uma atividade do dia
        if(liveCards().every(function(c){ return state[c.dataset.num] && state[c.dataset.num].checked; })) markDailyGoalProgress(true);
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
    document.addEventListener("toefl-access", renderSummary);
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

    checkBtn.addEventListener("click", function(){
      persist(true); grade();
      markDailyGoalProgress(true);
      updateLiveScorePanel();
      updateLevelRecommendations();
    });
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
      updateLiveScorePanel();
      updateLevelRecommendations();
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

  // ---------- Calculadora de score (M0, Parte 4) ----------
  // Percentual de acerto por seção -> banda, pela tabela 4.2 do módulo. Cada
  // faixa da tabela cobre duas meias bandas: a metade de baixo da faixa dá a
  // banda cheia, a de cima dá a meia banda seguinte.
  (function(){
    var root = document.getElementById("scoreCalc");
    if(!root) return;
    var LS = "toefl_scorecalc_v1";
    var RANGES = [[0, 20, 1], [21, 40, 2], [41, 55, 3], [56, 70, 4], [71, 85, 5]];
    var LABELS = { 1: "A1", 2: "A2", 3: "B1", 4: "B2", 5: "C1", 6: "C2" };
    var inputs = Array.prototype.slice.call(root.querySelectorAll(".scalc-in"));
    var totalEl = document.getElementById("scalcTotal");
    var saved = {};
    try { saved = JSON.parse(safeGet(LS) || "{}") || {}; } catch(e){ saved = {}; }

    function bandFromPct(pct){
      if(pct >= 86) return 6;
      for(var i = 0; i < RANGES.length; i++){
        var lo = RANGES[i][0], hi = RANGES[i][1];
        if(pct <= hi) return RANGES[i][2] + (pct > (lo + hi) / 2 ? 0.5 : 0);
      }
      return 6;
    }
    function fmt(band){ return String(band).replace(".", ","); }
    // save só quando o aluno digita. Gravar também na carga da página
    // marcava a sequência de dias e a sincronização só por abrir o site.
    function render(save){
      var bands = [], store = {};
      inputs.forEach(function(input){
        var out = root.querySelector('[data-band-for="' + input.dataset.section + '"]');
        var raw = input.value.trim();
        var pct = raw === "" ? NaN : Number(raw);
        if(isNaN(pct) || pct < 0 || pct > 100){
          out.textContent = raw === "" ? "sem dado" : "use de 0 a 100";
          out.classList.remove("is-set");
          return;
        }
        var band = bandFromPct(pct);
        bands.push(band);
        store[input.dataset.section] = raw;
        out.textContent = "banda " + fmt(band) + " (" + LABELS[Math.floor(band)] + ")";
        out.classList.add("is-set");
      });
      if(save === true) safeSet(LS, JSON.stringify(store));
      if(bands.length < inputs.length){
        totalEl.textContent = "preencha as quatro seções";
        return;
      }
      var mean = bands.reduce(function(a, b){ return a + b; }, 0) / bands.length;
      var overall = Math.round(mean * 2) / 2;
      totalEl.textContent = fmt(overall) + " (" + LABELS[Math.floor(overall)] + ")";
    }
    inputs.forEach(function(input){
      if(saved[input.dataset.section] != null) input.value = saved[input.dataset.section];
      input.addEventListener("input", function(){ render(true); });
    });
    render(false);
  })();

  // ---------- Blocos de simulado (M7) ----------
  // Sem correção item a item: o aluno responde o bloco e só vê acertos,
  // gabarito e explicações depois de entregar, como numa prova.
  Array.prototype.forEach.call(document.querySelectorAll(".exam"), function(root){
    var lsKey = "toefl_exam_" + root.dataset.exam + "_v1";
    var items = Array.prototype.slice.call(root.querySelectorAll(".exam-item"));
    var submitBtn = root.querySelector(".exam-submit");
    var retryBtn = root.querySelector(".exam-retry");
    var resultEl = root.querySelector(".exam-result");
    var leftEl = document.createElement("span");
    leftEl.className = "exam-left";
    resultEl.parentNode.insertBefore(leftEl, resultEl);
    var state = {};
    try { state = JSON.parse(safeGet(lsKey) || "{}"); } catch(e){ state = {}; }
    if(!state || typeof state !== "object" || !state.answers) state = { answers: {}, done: false };

    function persist(){ safeSet(lsKey, JSON.stringify(state)); }
    function paintSelection(){
      items.forEach(function(it){
        var chosen = state.answers[it.dataset.num];
        Array.prototype.forEach.call(it.querySelectorAll(".exam-opt"), function(o){
          o.classList.toggle("is-chosen", o.dataset.letter === chosen);
          o.setAttribute("aria-pressed", o.dataset.letter === chosen ? "true" : "false");
        });
      });
      var missing = items.filter(function(it){ return !state.answers[it.dataset.num]; }).length;
      submitBtn.disabled = missing > 0;
      // o botão apagado não dizia por quê: mostra quantas faltam
      if(leftEl){
        leftEl.hidden = missing === 0 || state.done;
        leftEl.textContent = missing === 1 ? "Falta 1 questão para entregar." : "Faltam " + missing + " questões para entregar.";
      }
    }
    function grade(){
      var right = 0;
      items.forEach(function(it){
        var chosen = state.answers[it.dataset.num], key = it.dataset.correct;
        var ok = chosen === key;
        if(ok) right++;
        it.classList.add(ok ? "is-right" : "is-wrong");
        var opts = Array.prototype.slice.call(it.querySelectorAll(".exam-opt"));
        opts.forEach(function(o){
          o.disabled = true;
          o.classList.toggle("is-key", o.dataset.letter === key);
        });
        var expl = it.querySelector(".exam-expl");
        if(expl) expl.hidden = false;
        setVerdict(it, expl, tagOptions(opts, [chosen], [key]));
      });
      resultEl.textContent = right + " de " + items.length + " corretas";
      resultEl.hidden = false;
      submitBtn.hidden = true;
      retryBtn.hidden = false;
      root.classList.add("is-done");
    }

    items.forEach(function(it){
      Array.prototype.forEach.call(it.querySelectorAll(".exam-opt"), function(o){
        o.addEventListener("click", function(){
          if(state.done) return;
          state.answers[it.dataset.num] = o.dataset.letter;
          persist();
          paintSelection();
        });
      });
    });
    submitBtn.addEventListener("click", function(){
      state.done = true; persist(); grade();
      markDailyGoalProgress(true);
      updateLiveScorePanel();
    });
    retryBtn.addEventListener("click", function(){
      state = { answers: {}, done: false }; persist();
      items.forEach(function(it){
        it.classList.remove("is-right", "is-wrong");
        Array.prototype.forEach.call(it.querySelectorAll(".exam-opt"), function(o){
          o.disabled = false; o.classList.remove("is-key", "is-chosen");
          setOptTag(o, "");
        });
        setVerdict(it, null, null);
        var expl = it.querySelector(".exam-expl");
        if(expl) expl.hidden = true;
      });
      root.classList.remove("is-done");
      resultEl.hidden = true; retryBtn.hidden = true; submitBtn.hidden = false;
      items.forEach(function(it){ shuffleChoices(it, ".exam-opt"); });
      paintSelection();
      updateLiveScorePanel();
    });

    // bloco ainda não entregue: ordem nova das alternativas a cada sessão
    if(!state.done) items.forEach(function(it){ shuffleChoices(it, ".exam-opt"); });
    paintSelection();
    if(state.done) grade();
  });

  // ---------- Caixa de escrita com cronômetro (M4) ----------
  // só as caixas de treino: a caixa da redação para correção (sem data-wbox)
  // é do app/redacao.js, que não deixa pausar
  Array.prototype.forEach.call(document.querySelectorAll(".wbox[data-wbox]"), function(root){
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
      statusEl.textContent = "Salvando…";
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
    // para poder trocar só o texto a cada carta (textContent apagaria o botão junto)
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
        btn.innerHTML = toeflIcon("volume");
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

  // ---- erros de login em português ----
  // Fica fora do bloco de contas (que nem roda sem Supabase configurado)
  // para o smoke test conseguir conferir. Mensagens que o servidor manda em
  // inglês: as fixas casam inteiras, as que variam casam por trecho. O que
  // não for reconhecido sai com uma frase em português e o original entre
  // parênteses, para o aluno ter o que dizer ao suporte.
  var AUTH_ERROR_MAP = {
    "Invalid login credentials": "E-mail ou senha incorretos.",
    "User already registered": "Já existe uma conta com esse e-mail.",
    "Password should be at least 6 characters": "A senha precisa ter pelo menos 6 caracteres."
  };
  var AUTH_ERROR_PATTERNS = [
    [/email not confirmed/i, "Confirme o seu e-mail pelo link que enviamos antes de entrar."],
    [/rate limit|too many requests|security purposes/i, "Muitas tentativas em pouco tempo. Espere alguns minutos e tente de novo."],
    [/failed to fetch|network|load failed/i, "Sem conexão com o servidor. Confira a internet e tente de novo."],
    [/invalid.*email|unable to validate email/i, "Esse e-mail não parece válido."],
    [/weak|password should/i, "Senha fraca demais. Use pelo menos 6 caracteres."],
    [/same.*password/i, "A nova senha precisa ser diferente da atual."],
    [/expired|invalid.*token|otp/i, "Esse link expirou ou já foi usado. Peça um novo."]
  ];
  function friendlyError(message){
    if(AUTH_ERROR_MAP[message]) return AUTH_ERROR_MAP[message];
    for(var i = 0; i < AUTH_ERROR_PATTERNS.length; i++){
      if(AUTH_ERROR_PATTERNS[i][0].test(message || "")) return AUTH_ERROR_PATTERNS[i][1];
    }
    return "Não deu certo agora. Tente de novo em instantes. (" + message + ")";
  }
  window.__toeflFriendlyError = friendlyError; // gancho do smoke test

  // ---------- Planos e validade do acesso ----------
  // Fica fora do bloco do Supabase porque não depende dele: são contas puras
  // sobre a linha de `entitlements` e os textos da tela de compra, e o smoke
  // test roda sem login. Quem grava o prazo é o servidor (mp-webhook); aqui
  // só se lê e se explica.
  var DAY_MS = 86400000;
  // volta do checkout: quantas vezes e de quanto em quanto tempo a conta é
  // consultada até o webhook liberar o acesso (20 x 3 s: cerca de 60 s)
  var PAY_RETRY_MS = 3000, PAY_RETRY_TRIES = 20;
  // row: a linha de `entitlements` da conta (ou null). Banco que ainda não
  // tem a coluna expires_at devolve só `paid`: vale como acesso sem prazo,
  // que é o que toda compra anterior aos planos era.
  function accessState(row, nowMs){
    var st = { active:false, expired:false, lifetime:false, plan:(row && row.plan) || null, until:null, daysLeft:null };
    if(!row || !row.paid) return st;
    if(!row.expires_at){ st.active = true; st.lifetime = true; return st; }
    var t = new Date(row.expires_at).getTime();
    if(isNaN(t)) return st; // data ilegível: trava, que é o padrão seguro
    st.until = new Date(t);
    st.active = t > nowMs;
    st.expired = !st.active;
    st.daysLeft = st.active ? Math.ceil((t - nowMs) / DAY_MS) : 0;
    return st;
  }
  function planName(id){
    var input = id ? document.querySelector('#planPick input[value="' + String(id).replace(/[^a-z0-9_-]/gi, "") + '"]') : null;
    return input ? input.dataset.name : "";
  }
  function fmtDate(d){ return d.toLocaleDateString("pt-BR"); }
  function daysLeftText(n){ return n === 1 ? "falta 1 dia" : "faltam " + n + " dias"; }
  // frase de "Minha conta"
  function accessText(st, paidAt){
    var name = planName(st.plan);
    var label = name ? "Plano " + name : "Acesso";
    if(st.lifetime){
      var when = "";
      var d = paidAt ? new Date(paidAt) : null;
      if(d && !isNaN(d.getTime())) when = " desde " + fmtDate(d);
      return { text: (name ? "Plano " + name + ": acesso" : "Acesso") + " vitalício liberado" + when + ".", cls: "is-paid" };
    }
    if(st.active){
      return { text: label + (name ? ": acesso" : "") + " liberado até " + fmtDate(st.until) + " (" + daysLeftText(st.daysLeft) + ").",
               cls: st.daysLeft <= 7 ? "is-ending" : "is-paid" };
    }
    var free = FREE ? " A conta segue grátis, com " + FREE.resumo + "." : "";
    if(st.expired){
      return { text: (name ? "O plano " + name : "O seu acesso") + " venceu em " + fmtDate(st.until) + ". Seu progresso continua salvo." + free, cls: "is-unpaid" };
    }
    return { text: FREE ? "Conta grátis: você tem " + FREE.resumo + ". Os simulados, a correção de redação e o resto do curso são liberados por um plano."
                        : "Sem acesso: esta conta ainda não tem compra confirmada.", cls: "is-free" };
  }
  // título e parágrafo da tela de compra, conforme a situação da conta
  function gateCopy(st){
    if(st.expired){
      return { kicker: "Acesso vencido", title: "Seu acesso venceu",
        text: (planName(st.plan) ? "O plano " + planName(st.plan) : "O seu acesso") + " terminou em " + fmtDate(st.until) +
          ". O seu progresso continua salvo: escolha um plano para voltar a estudar de onde parou." };
    }
    if(st.active && !st.lifetime){
      return { kicker: "Seu plano", title: "Comprar mais dias",
        text: "Seu acesso vai até " + fmtDate(st.until) + ". Um plano novo soma os dias ao fim desse prazo: nenhum dia se perde." };
    }
    return { kicker: "Acesso pago", title: "Libere seu acesso",
      text: "Sua conta está conectada. O conteúdo completo fica disponível depois da compra." };
  }
  function selectedPlan(){
    return document.querySelector("#planPick input:checked");
  }
  // meio de pagamento: Pix (Mercado Pago) só nos planos de pagamento único;
  // sem o bloco #payMethod no HTML (Pix desligado no plans.json), é cartão
  function selectedMethod(){
    var box = document.getElementById("payMethod");
    var m = box && !box.hidden ? box.querySelector("input:checked") : null;
    return m ? m.value : "card";
  }
  // Situação da assinatura Mensal (linha de `billing`) em texto, para Minha
  // conta. null quando não há assinatura para mostrar.
  function subscriptionText(row){
    if(!row || !row.subscription_id || !row.subscription_status) return null;
    var end = row.current_period_end ? new Date(row.current_period_end) : null;
    var when = end && !isNaN(end.getTime()) ? fmtDate(end) : "";
    var s = row.subscription_status;
    if(s === "active" || s === "trialing"){
      if(row.cancel_at_period_end){
        return { text: "Assinatura Mensal cancelada: não haverá nova cobrança" + (when ? ", e o mês pago vai até " + when : "") + ".", cls: "is-ending" };
      }
      return { text: "Assinatura Mensal ativa" + (when ? ": renova em " + when : "") + ". Cancele quando quiser.", cls: "is-paid" };
    }
    if(s === "past_due" || s === "unpaid" || s === "incomplete"){
      return { text: "A última cobrança da assinatura Mensal não passou. Atualize o cartão em Gerenciar ou cancelar a assinatura.", cls: "is-unpaid" };
    }
    if(s === "canceled" || s === "incomplete_expired"){
      return { text: "Assinatura Mensal encerrada. Nada mais é cobrado.", cls: "" };
    }
    return null;
  }
  (function(){
    var pick = document.getElementById("planPick");
    var btn = document.getElementById("payBtn");
    if(!pick || !btn) return;
    var methodBox = document.getElementById("payMethod");
    function sync(){
      var p = selectedPlan();
      if(!p) return;
      var oneTime = !p.dataset.interval;
      if(methodBox) methodBox.hidden = !oneTime;
      btn.textContent = oneTime && selectedMethod() === "pix"
        ? "Pagar o plano " + p.dataset.name + " com Pix: " + p.dataset.price
        : p.dataset.cta;
    }
    pick.addEventListener("change", sync);
    if(methodBox) methodBox.addEventListener("change", sync);
    sync();
    // plano clicado na tela de apresentação (landing.js): já vem marcado
    var wanted = safeGet("toefl_plan_pick_v1");
    var input = wanted ? pick.querySelector('input[value="' + wanted.replace(/[^a-z0-9_-]/gi, "") + '"]') : null;
    if(input){ input.checked = true; sync(); }
  })();
  // Tela de compra aberta por quem está na conta grátis (cadeado, faixa do
  // topo, Minha conta, redação): diz o motivo e tem "Voltar", porque a
  // amostra continua aberta por baixo.
  function openPlans(reason){
    var gate = document.getElementById("payGate");
    if(!gate) return;
    var set = function(id, t){ var el = document.getElementById(id); if(el) el.textContent = t; };
    set("payGateKicker", "Curso completo");
    set("payGateTitle", "Libere o curso completo");
    set("payGateText", (reason ? reason + " " : "") +
      "Um plano libera os 10 módulos inteiros, todos os exercícios, os simulados e a correção de redação. A sua conta grátis e o seu progresso continuam como estão.");
    var back = document.getElementById("payGateBack"), out = document.getElementById("paySignOut");
    var m = document.getElementById("payGateMsg");
    if(back) back.hidden = false;
    if(out) out.hidden = true;
    if(m) m.hidden = true;
    gate.hidden = false;
  }
  (function(){
    var back = document.getElementById("payGateBack");
    if(back) back.addEventListener("click", function(){ document.getElementById("payGate").hidden = true; });
    var barBtn = document.getElementById("freeBarBtn");
    if(barBtn) barBtn.addEventListener("click", function(){ openPlans(""); });
  })();
  // Nível de acesso: "full" (pago, admin, ou site sem Supabase) ou "free"
  // (logado, sem plano em dia). st: o accessState() da conta, para a faixa
  // dizer quando o plano venceu.
  function setAccessLevel(level, st){
    accessFree = level === "free";
    document.body.classList.toggle("acc-free", accessFree);
    var barText = document.getElementById("freeBarText"), barBtn = document.getElementById("freeBarBtn");
    if(accessFree && barText && FREE){
      if(st && st.expired){
        barText.textContent = (planName(st.plan) ? "O plano " + planName(st.plan) : "O seu acesso") + " venceu em " + fmtDate(st.until) +
          ". O seu progresso continua salvo, e a conta segue com a amostra grátis: " + FREE.resumo + ".";
        if(barBtn) barBtn.textContent = "Renovar";
      } else {
        barText.textContent = "Conta grátis: você tem " + FREE.resumo + ". O resto do curso aparece trancado.";
        if(barBtn) barBtn.textContent = "Ver os planos";
      }
    }
    updateBadges();
    updateLiveScorePanel();
    document.dispatchEvent(new Event("toefl-access"));
    if(window.__toeflRefreshLevelPractice) window.__toeflRefreshLevelPractice(true);
  }
  window.__toeflAccess = { state: accessState, text: accessText, gateCopy: gateCopy, setLevel: setAccessLevel, openPlans: openPlans,
    subText: subscriptionText, payRetryMs: PAY_RETRY_MS * PAY_RETRY_TRIES }; // gancho do smoke test

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
      m.textContent = "Não foi possível conectar ao servidor (sem internet ou rede bloqueada). O app segue funcionando offline.";
      m.style.color = "var(--danger)";
      m.hidden = false;
      return;
    }
    box.hidden = false;

    var gateMsgEl = document.getElementById("authGateMsg");
    function gateMsg(text, kind){
      if(!gateMsgEl) return;
      gateMsgEl.textContent = text;
      gateMsgEl.dataset.kind = kind || "";
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
    // a caixa só mostra a resposta da última ação. Ela começa vazia, esvazia
    // ao trocar de aba, ao digitar de novo e quando o navegador devolve a
    // página da memória (botão Voltar), para um aviso antigo, como o de
    // confirmar o e-mail, não ficar na tela sem o aluno ter feito nada.
    function gateMsgClear(){
      if(!gateMsgEl) return;
      gateMsgEl.textContent = "";
      gateMsgEl.hidden = true;
    }
    gateMsgClear();
    window.addEventListener("pageshow", function(e){ if(e.persisted) gateMsgClear(); });
    ["loginEmail", "loginPassword", "signupEmail", "signupPassword"].forEach(function(id){
      var el = document.getElementById(id);
      if(el) el.addEventListener("input", function(){ if(gateMsgEl && gateMsgEl.dataset.kind === "err") gateMsgClear(); });
    });

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
      // fim da URL) — pede uma versão maior para não borrar/encolher dentro
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
          if(!dataUrl){ msg("Não foi possível ler essa imagem. Tente um JPG ou PNG.", "err"); return; }
          safeSet(AVATAR_KEY, dataUrl);
          if(safeGet(AVATAR_KEY) !== dataUrl){
            msg("Não foi possível salvar a foto (armazenamento cheio ou bloqueado).", "err");
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
    // Lê a linha de entitlements da conta. Se o banco ainda não tiver as
    // colunas dos planos (migração de 2026-10-08 não rodada), a consulta
    // completa falha: repete só com `paid`, que accessState() lê como acesso
    // sem prazo. Assim o site novo funciona com o banco antigo.
    function fetchEntitlement(userId){
      return client.from("entitlements").select("paid, paid_at, plan, expires_at").eq("user_id", userId).maybeSingle()
        .then(function(res){
          if(!res.error) return res;
          return client.from("entitlements").select("paid, paid_at").eq("user_id", userId).maybeSingle();
        });
    }
    var payGateBack = document.getElementById("payGateBack");
    // o clique do "Voltar" fica junto do openPlans(), fora deste bloco
    function setGateCopy(st, canGoBack){
      var copy = gateCopy(st);
      var kicker = document.getElementById("payGateKicker");
      var title = document.getElementById("payGateTitle");
      var text = document.getElementById("payGateText");
      if(kicker) kicker.textContent = copy.kicker;
      if(title) title.textContent = copy.title;
      if(text) text.textContent = copy.text;
      // "Voltar" só existe para quem abriu a tela por Minha conta com o
      // acesso em dia; quem está bloqueado só pode comprar ou sair
      if(payGateBack) payGateBack.hidden = !canGoBack;
      if(paySignOutBtn) paySignOutBtn.hidden = !!canGoBack;
    }
    function checkEntitlement(session, attempt){
      if(!payGateEl) return;
      if(isAdmin(session)){ payGateEl.hidden = true; setAccessLevel("full"); return; }
      fetchEntitlement(session.user.id)
        .then(function(res){
          if(res.error){
            // erro de rede/consulta: mantém a tela de pagamento visível (o
            // padrão seguro para receita continua sendo travar por padrão),
            // mas avisa que foi uma falha de conexão, não que o aluno não
            // pagou -- sem isso, quem já pagou via um erro transitório
            // lia "sem acesso" sem saber que é só tentar de novo.
            payGateEl.hidden = false;
            payGateMsg("Não consegui confirmar seu acesso agora, parece ser a conexão. Atualize a página que eu tento de novo.", "err");
            console.error("Falha ao verificar pagamento:", res.error.message);
            return;
          }
          var st = accessState(res.data, Date.now());
          // sem plano em dia (nunca comprou, ou venceu): conta grátis, com a
          // amostra aberta e o resto trancado. A tela de compra só cobre o
          // site na volta do checkout, para dizer como ficou o pagamento.
          setAccessLevel(st.active ? "full" : "free", st);
          // volta do pagamento: ?pay= (Stripe: success ou cancel) ou ?mp=
          // (Mercado Pago, Pix: success, pending ou failure)
          var params = new URLSearchParams(location.search);
          var ret = params.get("pay") || params.get("mp");
          payGateEl.hidden = st.active || !ret;
          if(payGateEl.hidden) return;
          setGateCopy(st, true);
          // volta de um checkout recém-aprovado: o webhook é assíncrono e
          // pode chegar bem depois do redirect (o do Stripe às vezes leva
          // dezenas de segundos). Tenta de novo durante cerca de 1 minuto
          // (PAY_RETRY_TRIES x PAY_RETRY_MS) antes de dizer que demorou.
          if(ret === "success" && (attempt || 0) < PAY_RETRY_TRIES){
            payGateMsg("Pagamento recebido. Estou liberando o seu acesso, isso pode levar até um minuto.", "ok");
            setTimeout(function(){ checkEntitlement(session, (attempt || 0) + 1); }, PAY_RETRY_MS);
          } else if(ret === "success"){
            payGateMsg("Recebemos o pagamento, mas a liberação está demorando mais que o normal. Atualize a página daqui a alguns minutos.", "err");
          } else if(ret === "pending"){
            payGateMsg("Pagamento pendente de confirmação.", "err");
          } else if(ret === "failure" || ret === "cancel"){
            payGateMsg("Pagamento não concluído. Nada foi cobrado. Tente novamente quando quiser.", "err");
          }
        });
    }
    if(payBtn){
      payBtn.addEventListener("click", function(){
        payBtn.disabled = true;
        payGateMsg("Abrindo a página de pagamento…", "ok");
        // functions.invoke() nem sempre anexa o token de sessão sozinho
        // (dependendo da versão da lib carregada pelo CDN) -- a edge
        // function então recebe a chamada sem Authorization e responde
        // "Não autenticado." mesmo com o aluno logado. Busca a sessão
        // atual e manda o token explicitamente para não depender disso.
        client.auth.getSession().then(function(sessionRes){
          var token = sessionRes && sessionRes.data && sessionRes.data.session && sessionRes.data.session.access_token;
          var coupon = couponInput ? couponInput.value.trim() : "";
          var chosen = selectedPlan();
          // vai só o id do plano e o meio: o preço é decidido no servidor
          var opts = { body: { origin: location.origin, coupon: coupon, plan: chosen ? chosen.value : "", method: selectedMethod() } };
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
                  payGateMsg("Erro ao abrir a página de pagamento: " + reason, "err");
                });
              return;
            }
            location.href = res.data.url;
          })
          .catch(function(){
            // rejeição de verdade (ex.: sem internet, DNS falhou antes de
            // chegar no Supabase) -- sem isso o botão ficava travado em
            // "Abrindo a página de pagamento…" para sempre, sem erro e sem como tentar de novo
            payBtn.disabled = false;
            payGateMsg("Erro de conexão ao abrir a página de pagamento. Tente de novo.", "err");
          });
      });
    }
    if(paySignOutBtn){
      paySignOutBtn.addEventListener("click", function(){ client.auth.signOut().then(signedOut); });
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
          if(res.error){ msg("Não consegui salvar na nuvem agora. Seu progresso continua guardado neste aparelho.", "err"); return; }
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
      setSyncNote(true);
      pull();
      // redações (app/redacao.js): histórico, selo de devolutiva nova e,
      // para conta corretora, o painel
      if(window.__toeflEssayOnline) window.__toeflEssayOnline(session);
    }
    // "Sair": a pessoa volta para a tela de apresentação, a mesma que vê
    // quem abre o site sem login (item 23 de 2026-10-25)
    function signedOut(){
      goOffline();
      if(location.protocol !== "file:") location.replace("apresentacao.html");
    }
    function goOffline(){
      uid = null;
      supaUid = null;
      googleAvatarUrl = null;
      onSyncedWrite = null;
      forceSyncPush = null;
      setSyncNote(false);
      setGateFormsHidden(false);
      showLoginView();
      signedIn.hidden = true;
      if(gateEl) gateEl.hidden = false;
      if(payGateEl) payGateEl.hidden = true;
      if(accessFree) setAccessLevel("full"); // a tela de login cobre tudo; a amostra volta a valer no próximo login sem plano
      if(window.__toeflEssayOffline) window.__toeflEssayOffline();
    }

    // ---- login por e-mail+senha ----
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
      setFreeNote(true);
    }
    // convite da conta grátis: na tela de entrar é um parágrafo com botão; na
    // de criar conta vira o subtítulo
    function setFreeNote(on){
      var note = document.getElementById("authFreeNote");
      if(note) note.hidden = !on;
    }
    var freeSignupBtn = document.getElementById("authFreeSignup");
    if(freeSignupBtn) freeSignupBtn.addEventListener("click", function(){ showSignupView(); });
    function showSignupView(){
      loginForm.hidden = true; signupForm.hidden = false; resetPasswordForm.hidden = true;
      authTabs.hidden = false; authTabs.classList.add("is-signup");
      authTabSignup.classList.add("is-active"); authTabLogin.classList.remove("is-active");
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = false;
      document.getElementById("authGateGoogleWrap").hidden = false;
      authGateTitle.textContent = "Criar conta grátis";
      authGateSubtitle.textContent = "A conta grátis não pede cartão e abre o Módulo 0 inteiro.";
      setFreeNote(false);
    }
    function showResetPasswordView(){
      loginForm.hidden = true; signupForm.hidden = true; resetPasswordForm.hidden = false;
      authTabs.hidden = true;
      document.getElementById("authLinks").hidden = true;
      document.getElementById("authGateDivider").hidden = true;
      document.getElementById("authGateGoogleWrap").hidden = true;
      authGateTitle.textContent = "Escolha uma nova senha";
      authGateSubtitle.textContent = "";
      setFreeNote(false);
      if(gateEl) gateEl.hidden = false; // aparece mesmo se o app estava "logado" na sessão de recuperação
    }

    loginForm.addEventListener("submit", function(e){
      e.preventDefault();
      var email = document.getElementById("loginEmail").value.trim();
      var password = document.getElementById("loginPassword").value;
      if(!email || !password) return;
      gateMsg("Entrando…", "ok");
      client.auth.signInWithPassword({ email: email, password: password }).then(function(r){
        if(r.error) gateMsg(friendlyError(r.error.message), "err");
      }).catch(function(){ gateMsg("Erro de conexão. Tente de novo.", "err"); });
    });

    signupForm.addEventListener("submit", function(e){
      e.preventDefault();
      var email = document.getElementById("signupEmail").value.trim();
      var password = document.getElementById("signupPassword").value;
      gateMsg("Criando conta…", "ok");
      client.auth.signUp({ email: email, password: password }).then(function(res){
        if(res.error){ gateMsg(friendlyError(res.error.message), "err"); return; }
        if(res.data && res.data.session){
          gateMsg("Conta criada!", "ok"); // goOnline() cuida do resto via onAuthStateChange
          return;
        }
        // e-mail já cadastrado e confirmado: o Supabase responde como se tivesse
        // dado certo (para não revelar quais e-mails já existem) mas não manda
        // nada e não cria identidade nova -- sem checar isso, o aviso de
        // "confira seu e-mail" mente para quem já tem conta.
        var identities = res.data && res.data.user && res.data.user.identities;
        if(identities && identities.length === 0){
          gateMsg("Esse e-mail já tem conta. Use a aba Entrar ou, se não lembrar a senha, clique em \"Esqueci minha senha\".", "err");
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
        btn.innerHTML = toeflIcon(shown ? "eye" : "eye-off");
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
      gateMsg("Salvando…", "ok");
      client.auth.updateUser({ password: newPassword }).then(function(res){
        if(res.error){ gateMsg(friendlyError(res.error.message), "err"); return; }
        gateMsg("Senha atualizada! Entrando…", "ok");
        showLoginView();
      });
    });

    document.getElementById("forgotPasswordLink").addEventListener("click", function(){
      var email = window.prompt("Seu e-mail. Enviaremos um link para você escolher uma nova senha:");
      if(!email) return;
      var redirect = location.href.split("#")[0].split("?")[0];
      client.auth.resetPasswordForEmail(email.trim(), { redirectTo: redirect }).then(function(res){
        gateMsg(res.error ? friendlyError(res.error.message) : "Link enviado. Confira seu e-mail.",
          res.error ? "err" : "ok");
      });
    });
    authTabLogin.addEventListener("click", function(){ gateMsgClear(); showLoginView(); });
    authTabSignup.addEventListener("click", function(){ gateMsgClear(); showSignupView(); });
    // "Criar conta" da tela de apresentação chega com #criar-conta
    if(location.hash === "#criar-conta") showSignupView();
    // cartões de plano do painel da direita: mesmo destino dos botões da
    // apresentação. Guarda o plano (a tela de compra abre com ele marcado) e
    // abre "Criar conta", sem recarregar a página.
    Array.prototype.forEach.call(document.querySelectorAll("#authGate [data-plan-pick]"), function(a){
      a.addEventListener("click", function(e){
        e.preventDefault();
        safeSet("toefl_plan_pick_v1", a.getAttribute("data-plan-pick"));
        showSignupView();
        var email = document.getElementById("signupEmail");
        if(email){ email.scrollIntoView({ block: "center", behavior: "smooth" }); email.focus({ preventScroll: true }); }
      });
    });

    if(googleBtn){
      googleBtn.addEventListener("click", function(){
        var redirect = location.href.split("#")[0].split("?")[0];
        client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: redirect } })
          .then(function(res){
            // sucesso: o navegador é redirecionado para o Google, não sobra nada para fazer aqui
            if(res.error) gateMsg("Algo deu errado: " + res.error.message, "err");
          });
      });
    }
    signOutBtn.addEventListener("click", function(){
      client.auth.signOut().then(signedOut);
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
      var renewBtn = document.getElementById("accountRenew");
      var subEl = document.getElementById("accountSub");
      var manageBtn = document.getElementById("accountManage");

      function setAccess(text, cls){
        if(!accessEl) return;
        accessEl.textContent = text;
        accessEl.className = "account-access" + (cls ? " " + cls : "");
      }
      // assinatura Mensal: a linha de `billing` (só leitura, RLS da própria
      // conta). Banco sem a tabela (migração do Stripe não rodada) só não
      // mostra nada. O botão abre o Customer Portal do Stripe (stripe-portal).
      function loadSubscription(user){
        if(subEl) subEl.hidden = true;
        if(manageBtn) manageBtn.hidden = true;
        if(!subEl || !manageBtn) return;
        client.from("billing").select("stripe_customer_id, subscription_id, subscription_status, cancel_at_period_end, current_period_end")
          .eq("user_id", user.id).maybeSingle()
          .then(function(res){
            if(res.error || !res.data) return;
            var line = subscriptionText(res.data);
            if(line){
              subEl.textContent = line.text;
              subEl.className = "account-access" + (line.cls ? " " + line.cls : "");
              subEl.hidden = false;
            }
            manageBtn.hidden = !res.data.stripe_customer_id || !res.data.subscription_id;
          }).catch(function(){});
      }
      if(manageBtn){
        manageBtn.addEventListener("click", function(){
          manageBtn.disabled = true;
          accountMsg("Abrindo o gerenciamento da assinatura…", "ok");
          client.auth.getSession().then(function(sessionRes){
            var token = sessionRes && sessionRes.data && sessionRes.data.session && sessionRes.data.session.access_token;
            var opts = { body: { origin: location.origin } };
            if(token) opts.headers = { Authorization: "Bearer " + token };
            return client.functions.invoke("stripe-portal", opts);
          }).then(function(res){
            manageBtn.disabled = false;
            if(res.error || !res.data || !res.data.url){
              var ctx = res.error && res.error.context;
              (ctx && typeof ctx.json === "function" ? ctx.json().catch(function(){ return null; }) : Promise.resolve(null))
                .then(function(body){ accountMsg((body && body.error) || "Não deu para abrir agora. Tente de novo em instantes.", "err"); });
              return;
            }
            location.href = res.data.url;
          }).catch(function(){
            manageBtn.disabled = false;
            accountMsg("Erro de conexão. Tente de novo.", "err");
          });
        });
      }
      // mostra o que a tabela `entitlements` diz desta conta. É só leitura:
      // quem libera ou bloqueia o conteúdo continua sendo checkEntitlement().
      function loadAccess(user){
        if(!accessEl) return;
        if(renewBtn) renewBtn.hidden = true;
        if(!user){ setAccess("Não consegui verificar agora.", ""); return; }
        if(isAdmin({ user: user })){ setAccess("Conta de administrador: acesso liberado, sem cobrança.", "is-paid"); return; }
        setAccess("Verificando…", "");
        fetchEntitlement(user.id)
          .then(function(res){
            if(res.error){ setAccess("Não consegui verificar agora. Feche e abra esta tela que eu tento de novo.", ""); return; }
            var st = accessState(res.data, Date.now());
            var line = accessText(st, res.data && res.data.paid_at);
            setAccess(line.text, line.cls);
            loadSubscription(user);
            // comprar mais dias para quem tem prazo correndo (somam ao fim);
            // ver os planos para a conta grátis (nunca comprou ou venceu).
            // Compra antiga sem prazo não tem o que comprar.
            if(renewBtn){
              renewBtn.hidden = st.lifetime;
              renewBtn.textContent = st.active ? "Comprar mais dias" : "Ver os planos";
              renewBtn.onclick = function(){
                close();
                if(!st.active){ openPlans(""); return; }
                setGateCopy(st, true);
                if(payGateMsgEl) payGateMsgEl.hidden = true;
                payGateEl.hidden = false;
              };
            }
          })
          .catch(function(){ setAccess("Não consegui verificar agora, parece ser a conexão.", ""); });
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
        setAccess("Verificando…", "");
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
          accountMsg("Salvando…", "ok");
          client.auth.updateUser({ email: email }).then(function(res){
            if(res.error){ accountMsg(friendlyError(res.error.message), "err"); return; }
            // o Supabase manda link de confirmação para o endereço NOVO (e, se
            // "secure email change" estiver ligado, também para o antigo) --
            // o e-mail só troca de verdade depois de clicar nesse link
            accountMsg("Confira o e-mail enviado para " + email + " e confirme a troca por lá.", "ok");
          }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
        }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
      });

      passwordForm.addEventListener("submit", function(e){
        e.preventDefault();
        var newPassword = document.getElementById("accountNewPassword").value;
        if(!newPassword || newPassword.length < 6) return;
        accountMsg("Salvando…", "ok");
        client.auth.updateUser({ password: newPassword }).then(function(res){
          if(res.error){ accountMsg(friendlyError(res.error.message), "err"); return; }
          passwordForm.reset();
          accountMsg("Senha atualizada.", "ok");
        }).catch(function(){ accountMsg("Erro de conexão. Tente de novo.", "err"); });
      });

      // ---- excluir conta ----
      // quem apaga de verdade é a edge function delete-account (precisa da
      // service_role, que não pode vir para o navegador). Aqui é só a
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
          deleteMsg("Excluindo sua conta…", "ok");
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
  // diagnóstico do M0, exercícios, meta) -- nenhum estado novo além do
  // streak em si. Pontos fracos e prioridade: weakAreas() e computePriority(),
  // no bloco "Pontos fracos e Sua prioridade hoje".
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
    var planWhyEl = document.getElementById("dashPlanWhy");
    var planBtnEl = document.getElementById("dashPlanBtn");

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
        ? "Que tal 20 minutos hoje? Um pouco por dia rende mais do que muito de vez em quando."
        : streak.count + (streak.count === 1 ? " dia seguido estudando" : " dias seguidos estudando") +
          (streak.today ? "" : " (continue hoje para manter)");

      // a mesma meta de hoje da gaveta e da faixa do topo (plano de estudo)
      var today = window.__toeflToday ? window.__toeflToday() : null;
      goalFillEl.style.width = today ? Math.round(100 * Math.min(today.doneCount, today.total) / today.total) + "%" : "0%";
      goalTextEl.textContent = !today ? "" : today.done
        ? "Meta batida hoje! " + today.doneCount + " de " + today.total + " feitos."
        : today.text + ". Feito até agora: " + today.doneCount + " de " + today.total + ".";

      var band = computeBandEstimate();
      bandEl.textContent = band
        ? "Banda " + cefrBandFromPct(band.pct).code + " (" + cefrBandFromPct(band.pct).label + ") · fonte: " + band.source
        : "Complete o diagnóstico do Módulo 0 para ver sua estimativa.";

      var prog = computeOverallProgress();
      progressFillEl.style.width = prog.pct + "%";
      progressTextEl.textContent = prog.pct + "% · " + prog.modsDone + " de " + prog.totalMods + " módulos concluídos";

      renderWeak();
      var pr = window.__toeflPriority ? window.__toeflPriority() : null;
      planTextEl.textContent = pr ? pr.text : "";
      planWhyEl.textContent = pr ? pr.why : "";
      planBtnEl.hidden = !pr;
      planBtnEl.textContent = pr && pr.kind === "diag" ? "Começar" : pr && pr.kind === "goal" ? "Montar meu plano" : "Continuar";
      planBtnEl.onclick = function(){ close(); if(pr) pr.go(); };
    }
    // as áreas com dado suficiente e abaixo de 70%, da mais fraca para a
    // menos fraca (no máximo 3), cada uma com o atalho para a Parte que ensina
    function renderWeak(){
      var all = window.__toeflWeak ? window.__toeflWeak() : [];
      var enough = all.filter(function(a){ return a.enough; });
      var weak = enough.filter(function(a){ return a.pct < WEAK_SHOW; }).slice(0, 3);
      var few = all.filter(function(a){ return !a.enough; }).map(function(a){ return a.nome; });
      weakListEl.innerHTML = "";
      function note(text){
        var p = document.createElement("p"); p.className = "dash-empty"; p.textContent = text;
        weakListEl.appendChild(p);
      }
      if(!enough.length) note("Ainda não há respostas suficientes para apontar pontos fracos com honestidade. " +
        "Faça o diagnóstico e alguns exercícios: a partir de " + WEAK_MIN + " respostas numa área, ela aparece aqui com a taxa de acerto.");
      else if(!weak.length) note("Nenhuma área abaixo de " + WEAK_SHOW + "% de acerto até agora. Bom sinal: siga o cronograma.");
      weak.forEach(function(a){
        var row = document.createElement("div");
        row.className = "dash-weak-row";
        row.dataset.area = a.key;
        var pct = document.createElement("span"); pct.className = "dash-weak-code"; pct.textContent = a.pct + "%";
        var label = document.createElement("span"); label.className = "dash-weak-label";
        label.textContent = a.nome + " (" + a.ok + " de " + a.n + ")";
        var go = document.createElement("button"); go.type = "button"; go.className = "diag-link dash-weak-go";
        go.textContent = "Abrir M" + a.mod.slice(3) + ", Parte " + a.parte;
        go.setAttribute("aria-label", "Abrir " + partTitle(a.mod, a.parte));
        go.addEventListener("click", function(){ close(); openPart(a.mod, a.parte); });
        row.appendChild(pct); row.appendChild(label); row.appendChild(go);
        weakListEl.appendChild(row);
      });
      if(enough.length && few.length) note("Ainda com poucos dados: " + joinPt(few) + ".");
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
  // salvo a cada tecla (o safeSet já cuida do dirty flag/push debounced para
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
          // textContent, nunca innerHTML: drill e resultado são texto livre
          // do aluno (e chegam também por sincronização e por importação)
          [["date", entry.date || "—"], ["drill", entry.drill || "—"],
           ["result", entry.result || "—"], ["codes", codesTxt || "sem código"]].forEach(function(cell){
            var span = document.createElement("span");
            span.className = "errlog-entry-" + cell[0];
            span.textContent = cell[1];
            row.appendChild(span);
          });
          var del = document.createElement("button");
          del.type = "button";
          del.className = "errlog-entry-del";
          del.setAttribute("aria-label", "Remover registro");
          del.textContent = "✕";
          row.appendChild(del);
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
            date: dateEl.value || todayStr(),
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
  // tudo de uma vez. Continua dando para abrir/fechar clicando no título a
  // qualquer momento. Marcar a Parte (h2) inteira como concluída fecha as
  // subseções dela de volta (ver o listener de .pchk mais acima) -- depois
  // disso elas não reabrem sozinhas de novo, só se o aluno clicar. Roda por
  // último de propósito: outros passes (botão de cronômetro por drill,
  // índice "Nesta parte") contam com a posição original dos elementos em
  // relação aos h3/h2.
  // marcação de concluído por subseção (h3), separada da marcação por Parte
  // (h2) que já existia -- pedido do usuário: só dava para marcar a Parte
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
  // marca a subseção como lida (ou não), no título e no armazenamento, e
  // avisa a coluna "Nesta Parte"
  function setH3Done(h3, done){
    if(h3.classList.contains("h3-done") === !!done) return;
    setH3Progress(h3.id, done);
    h3.classList.toggle("h3-done", !!done);
    document.dispatchEvent(new CustomEvent("toefl-h3", { detail: { id: h3.id } }));
  }
  window.__toeflSetH3Done = setH3Done; // gancho do smoke test

  (function(){
    var cards = Array.prototype.slice.call(document.querySelectorAll(".section-card"));
    var allH3 = [];
    var h3Ends = []; // o fim de cada subseção: chegar nele marca como lida
    var h3Seq = {}; // contador por módulo, para dar um id estável a cada h3
    var h3Done = readH3Progress();
    cards.forEach(function(card){
      var panelEl = card.closest(".panel");
      var modKey = panelEl ? panelEl.dataset.panel : "mod";
      var h3s = Array.prototype.slice.call(card.children).filter(function(n){ return n.tagName === "H3"; });
      h3s.forEach(function(h3){
        var nodes = [];
        var node = h3.nextSibling;
        // o "concluída" da Parte fica fora da última subseção: visível mesmo
        // com ela fechada
        while(node && !(node.nodeType === 1 && (node.tagName === "H3" || node.classList.contains("mark-done")))){
          nodes.push(node);
          node = node.nextSibling;
        }
        var hasWidget = nodes.some(function(n){
          return n.nodeType === 1 && (n.classList.contains("quiz-drill") || n.classList.contains("bsq") || n.querySelector(".quiz-drill, .bsq"));
        });
        if(hasWidget || !nodes.length) return;
        var body = document.createElement("div");
        body.className = "h3-body h3-collapsed";
        // subseção trancada na conta grátis: o corpo (e a caixa de concluída
        // que entra nele) some junto com o título
        if(h3.hasAttribute("data-locked")) body.setAttribute("data-locked", "");
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
        dot.setAttribute("aria-label", "lida");
        h3.insertBefore(dot, h3.firstChild);

        // o título inteiro vira um <button> dentro do <h3>: continua sendo
        // título para leitor de tela, mas ganha foco de teclado, Enter e
        // Espaço, e anuncia aberto ou fechado. O clique sobe para o h3, que
        // é quem abre e fecha. A seta vai colada ao texto (item 15), e a
        // linha toda é clicável.
        var hbtn = document.createElement("button");
        hbtn.type = "button";
        hbtn.className = "h3-btn";
        var htxt = document.createElement("span");
        htxt.className = "h3-text";
        while(h3.firstChild) htxt.appendChild(h3.firstChild);
        hbtn.appendChild(htxt);
        hbtn.insertAdjacentHTML("beforeend", toeflIcon("chevron", "ico h3-chevron"));
        hbtn.setAttribute("aria-expanded", "false");
        h3.appendChild(hbtn);

        // lida: o aluno chegou ao fim da subseção aberta (item 26). Sem
        // caixa de marcar em cada uma; o ✓ fica no título, mesmo fechada.
        var end = document.createElement("span");
        end.className = "h3-end";
        end.setAttribute("aria-hidden", "true");
        body.appendChild(end);
        h3Ends.push({ end: end, h3: h3, body: body });
        if(h3Done[h3.id]) h3.classList.add("h3-done");
      });
    });

    // só conta quando o aluno rola a página: abrir o site (ou uma subseção
    // curta que cabe inteira na tela) não é ler, e não pode marcar nada nem
    // contar como dia de estudo
    if(h3Ends.length && "IntersectionObserver" in window){
      var inView = [];
      var endObserver = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          var it = h3Ends.filter(function(x){ return x.end === entry.target; })[0];
          if(!it) return;
          var at = inView.indexOf(it);
          if(entry.isIntersecting && at === -1) inView.push(it);
          if(!entry.isIntersecting && at !== -1) inView.splice(at, 1);
        });
      }, { threshold: 0 });
      h3Ends.forEach(function(x){ endObserver.observe(x.end); });
      // rolagem do próprio navegador (ao recarregar, ao trocar de Parte) não
      // conta: só depois de o aluno mexer (roda, toque, teclado, clique)
      var engaged = false;
      ["wheel", "touchmove", "keydown", "pointerdown"].forEach(function(ev){
        window.addEventListener(ev, function(){ engaged = true; }, { passive: true });
      });
      var pending = false;
      window.addEventListener("scroll", function(){
        if(pending || !engaged) return;
        pending = true;
        setTimeout(function(){
          pending = false;
          inView.forEach(function(it){
            if(it.body.classList.contains("h3-collapsed") || it.h3.classList.contains("h3-done")) return;
            if(it.h3.closest("[hidden]")) return;
            setH3Done(it.h3, true);
          });
        }, 250);
      }, { passive: true });
    }

    // "continuar de onde parei": guarda a última subseção que o aluno leu
    // (a que entrou na faixa de leitura no meio da tela), para sidebar
    // oferecer um atalho direto para lá na próxima visita -- ver resumeBtn
    // mais abaixo. Separado do observer de auto-abrir porque precisa
    // disparar mesmo para seções que já estavam abertas.
    // o IntersectionObserver dispara um callback inicial assim que começa a
    // observar, refletindo o que já está na tela nesse instante (a seção
    // 1.1 do módulo que acabou de carregar) -- isso não é "o aluno rolou até
    // aqui", é só o estado de largada, e não pode sobrescrever a posição
    // salva de uma visita anterior. Só passa a gravar depois desse atraso.
    var trackingLastPos = false;
    setTimeout(function(){ trackingLastPos = true; }, 900);
    // título da subseção sem a marquinha "✓" (.h3-done-dot), que mora dentro
    // do próprio h3 e saía grudada no rótulo do "Continuar de onde parei"
    function h3Title(h3){
      var dot = h3.querySelector(".h3-done-dot");
      var text = h3.textContent;
      if(dot && text.indexOf(dot.textContent) === 0) text = text.slice(dot.textContent.length);
      return text.trim();
    }
    function saveLastPos(h3){
      if(!trackingLastPos) return;
      safeSet("toefl_lastpos_v1", JSON.stringify({ mod: h3.dataset.mod, id: h3.id, title: h3Title(h3) }));
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
    // nem sempre dispara a tempo para quem já está com a seção na tela sem
    // ter rolado nada ainda.
    var firstActiveH3 = document.querySelector(".panel:not([hidden]) .h3-toggle");
    if(firstActiveH3 && firstActiveH3.classList.contains("collapsed")){
      firstActiveH3.classList.remove("collapsed");
      var firstActiveBody = firstActiveH3.nextElementSibling;
      if(firstActiveBody && firstActiveBody.classList.contains("h3-body")) firstActiveBody.classList.remove("h3-collapsed");
    }

    // aberto ou fechado muda em vários pontos do código (clique, rolagem,
    // troca de aba, paginação, concluir Parte). Em vez de avisar o botão em
    // cada um, um observador só acompanha a classe do h3.
    if("MutationObserver" in window){
      var syncExpanded = function(h3){
        var b = h3.querySelector(".h3-btn");
        if(b) b.setAttribute("aria-expanded", h3.classList.contains("collapsed") ? "false" : "true");
      };
      var h3Sync = new MutationObserver(function(muts){ muts.forEach(function(m){ syncExpanded(m.target); }); });
      allH3.forEach(function(h3){
        syncExpanded(h3);
        h3Sync.observe(h3, { attributes: true, attributeFilter: ["class"] });
      });
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
      var posEl = pos && document.getElementById(pos.id);
      if(!posEl){ resumeBtn.hidden = true; return; }
      // relê o título da página: posição salva antes desta correção ainda
      // traz o "✓" no texto
      resumeLabel.textContent = h3Title(posEl);
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
          // logo abaixo), pula primeiro para parte que contém essa subseção,
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

  // ---------- Treino no seu nível (M0) ----------
  // Monta uma sessão de exercícios compatíveis com o nível estimado do aluno
  // (diagnóstico do M0 ou, na falta dele, os drills de M1/M2). A sessão é
  // sorteada de novo a cada carregamento da página e no botão "Sortear outra
  // sessão". Não cria questões: escolhe entre os exercícios do site que têm
  // faixa CEFR declarada (data-level), dando prioridade aos ainda não feitos.
  (function(){
    var box = document.getElementById("levelPractice");
    if(!box) return;
    var statusEl = document.getElementById("lvlpStatus");
    var listEl = document.getElementById("lvlpList");
    var shuffleBtn = document.getElementById("lvlpShuffle");
    var ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"];
    var MOD_NAMES = { mod1: "Reading", mod2: "Listening", mod3: "Speaking", mod4: "Writing" };
    var SESSION_SIZE = 5;
    var lastLevel = null;

    function range(el){
      var parts = el.dataset.level.split(/[–-]/).map(function(x){ return x.trim(); });
      return [ORDER.indexOf(parts[0]), ORDER.indexOf(parts[parts.length - 1])];
    }
    // distância entre o nível do aluno e a faixa do exercício (0 = dentro)
    function distance(el, lvl){
      var r = range(el);
      if(r[0] < 0 || r[1] < 0) return 99;
      if(lvl < r[0]) return r[0] - lvl;
      if(lvl > r[1]) return lvl - r[1];
      return 0;
    }
    function isDone(el){
      if(el.classList.contains("ctw")) return el.classList.contains("is-checked");
      var summary = el.querySelector(".quiz-summary");
      return !!summary && !summary.hidden;
    }
    function shuffled(arr){
      var a = arr.slice();
      for(var i = a.length - 1; i > 0; i--){
        var j = Math.floor(Math.random() * (i + 1));
        var t = a[i]; a[i] = a[j]; a[j] = t;
      }
      return a;
    }
    function pool(){
      return Array.prototype.filter.call(document.querySelectorAll("[data-level][data-lp-title]"), function(el){
        var panel = el.closest(".panel");
        return panel && MOD_NAMES[panel.dataset.panel] && !isLockedNow(el);
      });
    }
    function pick(lvl){
      var all = pool();
      var best = Math.min.apply(null, all.map(function(el){ return distance(el, lvl); }));
      var fit = all.filter(function(el){ return distance(el, lvl) === best; });
      // por módulo, os não feitos primeiro; depois um de cada módulo por vez,
      // para a sessão misturar habilidades em vez de sair toda de Reading
      var byMod = {};
      shuffled(fit).forEach(function(el){
        var mod = el.closest(".panel").dataset.panel;
        (byMod[mod] = byMod[mod] || []).push(el);
      });
      Object.keys(byMod).forEach(function(mod){
        byMod[mod].sort(function(a, b){ return (isDone(a) ? 1 : 0) - (isDone(b) ? 1 : 0); });
      });
      var mods = shuffled(Object.keys(byMod)), out = [];
      while(out.length < SESSION_SIZE){
        var took = false;
        for(var i = 0; i < mods.length && out.length < SESSION_SIZE; i++){
          var next = byMod[mods[i]].shift();
          if(next){ out.push(next); took = true; }
        }
        if(!took) break;
      }
      return out;
    }
    function goTo(el){
      var mod = el.closest(".panel").dataset.panel;
      navTo(mod);
      setTimeout(function(){
        var showPart = window.__toeflShowPart && window.__toeflShowPart[mod];
        var card = el.closest(".section-card");
        if(showPart && card) showPart(card, { noScroll: true });
        var body = el.closest(".h3-body");
        if(body && body.classList.contains("h3-collapsed")){
          body.classList.remove("h3-collapsed");
          var head = body.previousElementSibling;
          if(head) head.classList.remove("collapsed");
        }
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        el.classList.add("resume-highlight");
        setTimeout(function(){ el.classList.remove("resume-highlight"); }, 2200);
      }, 60);
    }
    function render(force){
      var est = computeBandEstimate();
      if(!est){ listEl.innerHTML = ""; shuffleBtn.hidden = true; lastLevel = null; return; }
      var label = cefrBandFromPct(est.pct).label;
      if(!force && label === lastLevel && listEl.children.length) return; // não troca a sessão no meio do estudo
      lastLevel = label;
      var session = pick(ORDER.indexOf(label));
      statusEl.textContent = "Nível estimado: " + label + " (fonte: " + est.source + "). Sessão sorteada para esse nível:";
      listEl.innerHTML = "";
      session.forEach(function(el){
        var li = document.createElement("li");
        var name = document.createElement("span");
        name.className = "lvlp-name";
        name.textContent = MOD_NAMES[el.closest(".panel").dataset.panel] + " · " + el.dataset.lpTitle;
        var meta = document.createElement("span");
        meta.className = "lvlp-meta";
        meta.textContent = el.dataset.level + (isDone(el) ? " · já feito" : "");
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "lvlp-go";
        btn.textContent = "Abrir";
        btn.addEventListener("click", function(){ goTo(el); });
        li.appendChild(name); li.appendChild(meta); li.appendChild(btn);
        listEl.appendChild(li);
      });
      shuffleBtn.hidden = session.length === 0;
    }
    shuffleBtn.addEventListener("click", function(){ render(true); });
    // force: sorteia de novo (a conta grátis muda o que pode entrar na sessão)
    window.__toeflRefreshLevelPractice = function(force){ render(!!force); };
    render(true);
  })();

  // ---------- Paginação por Parte, tipo flashcard ----------
  // Pedido do usuário: em vez de rolar por todas as Partes de um módulo de
  // uma vez, mostrar uma Parte inteira por vez com um botão para passar para
  // próxima (e voltar para anterior). Roda depois do accordion de h3 (que já
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
      obj[M0_ORDER_KEY] = M0_ORDER; // já na ordem nova do M0 (ver migrateM0Order)
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
      var shortTitles = titles.map(function(t){ return t.replace(/^PARTE\s+\d+\s*[:·]\s*/i, ""); });

      var pager = document.createElement("div");
      pager.className = "part-pager";
      pager.innerHTML =
        '<button type="button" class="part-nav-btn part-prev">‹ Parte anterior</button>' +
        '<span class="part-pager-label"><span class="part-pager-count"></span><b class="part-pager-title"></b></span>' +
        '<button type="button" class="part-nav-btn part-next">Próxima Parte ›</button>';
      if(head && head.parentNode === inner){ head.parentNode.insertBefore(pager, head.nextSibling); }
      else if(inner){ inner.insertBefore(pager, inner.firstChild); }

      // no fim da última Parte, em vez de só esconder o botão, oferece a
      // transição para o próximo módulo -- pedido do usuário: terminar um
      // módulo não tinha nenhum convite claro para seguir para o seguinte.
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
        el.textContent = "Esta é a última Parte do curso. Você chegou ao fim do caminho.";
        return el;
      })();
      if(modDoneNote){ cards[cards.length - 1].appendChild(modDoneNote); }

      function indexOf(card){ return cards.indexOf(card); }

      function showPart(card, opts){ showPartIdx(indexOf(card), opts); }

      function showPartIdx(idx, opts){
        opts = opts || {};
        idx = Math.max(0, Math.min(cards.length - 1, idx));
        cards.forEach(function(c, i){ c.hidden = i !== idx; });
        // "Parte 1 de 9" já diz o número: o título entra sem o "PARTE 1:"
        pager.querySelector(".part-pager-count").textContent = "Parte " + (idx + 1) + " de " + cards.length;
        pager.querySelector(".part-pager-title").textContent = shortTitles[idx];
        // o CSS põe o cadeado no título só na conta grátis
        pager.classList.toggle("is-locked", cards[idx].classList.contains("fs-part-locked"));
        setBarPart(modKey, "Parte " + (idx + 1) + " de " + cards.length);
        pager.querySelector(".part-prev").disabled = idx === 0;
        var topNextBtn = pager.querySelector(".part-next");
        topNextBtn.disabled = idx === cards.length - 1 && !nextModKey;
        // deixa claro que vai para outra Parte, não para a próxima subseção (item 30)
        topNextBtn.textContent = idx === cards.length - 1 ? (nextModKey ? "Próximo módulo: " + nextModTitle + " ›" : "Última Parte")
                                                         : "Próxima Parte: " + shortTitles[idx + 1] + " ›";
        topNextBtn.title = topNextBtn.textContent;
        bottomBtns.forEach(function(btn, i){
          if(i !== idx) return;
          if(idx === cards.length - 1){
            if(nextModKey){ btn.hidden = false; btn.textContent = "Módulo concluído! Próximo: " + nextModTitle + " →"; }
            else { btn.hidden = true; }
          } else { btn.hidden = false; btn.textContent = "Próxima Parte: " + shortTitles[idx + 1] + " →"; }
        });
        savePartPos(modKey, idx);
        // quem depende da Parte visível (cartão "Comece aqui", selos) escuta isto
        document.dispatchEvent(new CustomEvent("toefl-part", { detail: { mod: modKey, idx: idx } }));
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

  // ---------- Selo de tipo: paginação, mapa do módulo, "Agora pratique" ----------
  // O selo no topo de cada Parte já vem do build (p.part-kind). Aqui: o tipo
  // ao lado do título na paginação, o "Mapa do módulo" (todas as Partes com
  // tipo, tempo e ✓) e, no fim de cada Parte, o atalho entre teoria e
  // prática do mesmo módulo (item 13 de 2026-10-25).
  (function(){
    function jumpTarget(mod, i){
      var p = partInfo(mod, i + 1), list = PART_KINDS[mod] || [];
      if(!p) return null;
      if(p.tipo === "teoria"){
        if(p.pratica) return { n: p.pratica, label: "Agora pratique" };
        for(var j = i + 1; j < list.length; j++) if(list[j].tipo === "pratica" || list[j].tipo === "simulado") return { n: j + 1, label: "Agora pratique" };
      } else if(p.tipo === "pratica" || p.tipo === "simulado"){
        if(p.teoria) return { n: p.teoria, label: "Rever a teoria" };
        for(var k = i - 1; k >= 0; k--) if(list[k].tipo === "teoria") return { n: k + 1, label: "Rever a teoria" };
      }
      return null;
    }
    Array.prototype.forEach.call(document.querySelectorAll(".panel"), function(panel){
      var mod = panel.dataset.panel, cards = partCards(mod);
      var show = window.__toeflShowPart && window.__toeflShowPart[mod];
      if(cards.length < 2 || !show || !PART_KINDS[mod]) return;
      var pager = panel.querySelector(".part-pager");

      // tipo na paginação
      var kindEl = document.createElement("span");
      kindEl.className = "part-pager-kind";
      pager.querySelector(".part-pager-label").appendChild(kindEl);
      function syncPager(){
        var idx = cards.findIndex(function(c){ return !c.hidden; }), p = partInfo(mod, idx + 1);
        kindEl.textContent = kindText(p);
        kindEl.className = "part-pager-kind" + (p ? " kind-" + p.tipo : "");
      }

      // mapa do módulo
      var map = document.createElement("details");
      map.className = "part-map";
      var sum = document.createElement("summary");
      sum.textContent = "Mapa do módulo: " + cards.length + " Partes";
      var ol = document.createElement("ol");
      map.appendChild(sum); map.appendChild(ol);
      pager.parentNode.insertBefore(map, pager.nextSibling);
      var rows = cards.map(function(card, i){
        var p = partInfo(mod, i + 1);
        var li = document.createElement("li");
        var b = document.createElement("button");
        b.type = "button"; b.className = "part-map-item";
        var t = document.createElement("span"); t.className = "part-map-title"; t.textContent = "Parte " + (i + 1) + ": " + partShortTitle(card);
        var k = document.createElement("span"); k.className = "part-kind-tag kind-" + (p ? p.tipo : ""); k.textContent = kindText(p);
        b.appendChild(t); b.appendChild(k);
        b.addEventListener("click", function(){ show(card); map.open = false; });
        li.appendChild(b); ol.appendChild(li);
        return li;
      });
      function syncMap(){
        var cur = cards.findIndex(function(c){ return !c.hidden; });
        rows.forEach(function(li, i){
          li.classList.toggle("is-done", cards[i].classList.contains("done"));
          li.classList.toggle("is-current", i === cur);
        });
      }

      // atalho no fim de cada Parte
      cards.forEach(function(card, i){
        var to = jumpTarget(mod, i), target = to && cards[to.n - 1];
        if(!target) return;
        var box = document.createElement("div");
        box.className = "part-jump part-jump-" + (to.label === "Agora pratique" ? "practice" : "theory");
        if(card.classList.contains("fs-part-locked")) box.setAttribute("data-locked", "");
        var lbl = document.createElement("span"); lbl.className = "part-jump-label"; lbl.textContent = to.label;
        var btn = document.createElement("button");
        btn.type = "button"; btn.className = "part-jump-btn";
        btn.textContent = "Parte " + to.n + ": " + partShortTitle(target) + " (" + kindText(partInfo(mod, to.n)) + ")";
        btn.addEventListener("click", function(){ show(target); });
        box.appendChild(lbl); box.appendChild(btn);
        // fim da Parte, logo antes do botão "Próxima parte" (filho direto do
        // cartão; o "concluída" pode estar dentro da última subseção)
        var next = Array.prototype.filter.call(card.children, function(c){ return c.classList.contains("part-next-bottom"); })[0];
        card.insertBefore(box, next || null);
      });

      document.addEventListener("toefl-part", function(e){ if(e.detail.mod === mod){ syncPager(); syncMap(); } });
      panel.addEventListener("change", function(e){ if(e.target.classList.contains("pchk")) syncMap(); });
      syncPager(); syncMap();
    });
  })();

  // ---------- "Nesta Parte": coluna lateral (computador) e barra (celular) ----------
  // Itens 15, 26 e 30 de 2026-10-25. Mostra a Parte aberta: número, tipo,
  // título, subseções com ✓ (cada uma leva até ela), quantas foram lidas, o
  // tempo e um único botão "Marcar Parte como concluída", que mexe na mesma
  // caixa .pchk do fim da Parte. No celular a coluna vira uma barra fina no
  // topo, que abre o sumário.
  (function(){
    var rail = document.getElementById("partRail");
    if(!rail) return;
    var $ = function(id){ return document.getElementById(id); };
    var toggle = $("railToggle"), toc = $("railToc"), doneBtn = $("railDone");
    var current = null;
    function isBar(){ return !(window.matchMedia && window.matchMedia("(min-width: 1100px)").matches); }
    function setOpen(open){
      rail.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    function openH3(h3){
      if(h3.classList.contains("collapsed")){
        h3.classList.remove("collapsed");
        var body = h3.nextElementSibling;
        if(body && body.classList.contains("h3-body")) body.classList.remove("h3-collapsed");
      }
      if(isBar()) setOpen(false);
      h3.scrollIntoView({ behavior: "smooth", block: "start" });
      var b = h3.querySelector(".h3-btn"); if(b) b.focus({ preventScroll: true });
    }
    function render(){
      var panel = document.querySelector(".panel:not([hidden])");
      var mod = panel && panel.dataset.panel, cards = mod ? partCards(mod) : [];
      var idx = cards.findIndex(function(c){ return !c.hidden; });
      var card = cards[idx];
      if(!card){ rail.hidden = true; current = null; return; }
      current = card;
      var p = partInfo(mod, idx + 1), chk = partDoneBox(card), partDone = !!(chk && chk.checked);
      var h3s = Array.prototype.filter.call(card.querySelectorAll("h3.h3-toggle"), function(h){ return !isLockedNow(h); });
      var read = h3s.filter(function(h){ return h.classList.contains("h3-done"); }).length;
      $("railKicker").textContent = "Parte " + (idx + 1) + " de " + cards.length + (p ? " · " + KIND_NAME[p.tipo] : "");
      $("railTitle").textContent = partShortTitle(card) || (card.querySelector("h2") || {}).textContent || "";
      $("railCount").textContent = partDone ? "Parte concluída" : h3s.length ? read + " de " + h3s.length + " subseções lidas" : (p ? p.min + " min" : "");
      $("railFill").style.width = (partDone ? 100 : h3s.length ? Math.round(100 * read / h3s.length) : 0) + "%";
      var left = p && h3s.length && read ? Math.max(1, Math.round(p.min * (h3s.length - read) / h3s.length)) : null;
      $("railTime").textContent = !p ? "" : partDone ? "Tempo previsto: " + p.min + " min. Feito." :
        "Tempo previsto: " + p.min + " min" + (left !== null && read < h3s.length ? ". Faltam cerca de " + left + " min." : ".");
      toc.innerHTML = "";
      h3s.forEach(function(h){
        var li = document.createElement("li");
        var b = document.createElement("button");
        b.type = "button";
        b.className = "rail-sub" + (h.classList.contains("h3-done") ? " is-done" : "");
        var mark = document.createElement("span");
        mark.className = "rail-sub-mark";
        mark.textContent = h.classList.contains("h3-done") ? "✓" : "";
        var t = document.createElement("span");
        t.textContent = (h.querySelector(".h3-text") || h).textContent.replace(/^✓/, "").trim();
        b.appendChild(mark); b.appendChild(t);
        if(h.classList.contains("h3-done")) b.setAttribute("aria-label", t.textContent + " (lida)");
        b.addEventListener("click", function(){ openH3(h); });
        li.appendChild(b); toc.appendChild(li);
      });
      toc.previousElementSibling.hidden = !h3s.length;
      doneBtn.hidden = !chk || card.classList.contains("fs-part-locked") && accessFree;
      doneBtn.textContent = partDone ? "✓ Parte concluída" : "Marcar Parte como concluída";
      doneBtn.setAttribute("aria-pressed", partDone ? "true" : "false");
      doneBtn.classList.toggle("is-done", partDone);
      rail.hidden = false;
    }
    doneBtn.addEventListener("click", function(){
      var chk = current && partDoneBox(current);
      if(!chk) return;
      chk.checked = !chk.checked;
      chk.dispatchEvent(new Event("change", { bubbles: true }));
    });
    toggle.addEventListener("click", function(){ if(isBar()) setOpen(!rail.classList.contains("is-open")); });
    // Parte concluída: as subseções dela contam como lidas
    document.addEventListener("change", function(e){
      var c = e.target;
      if(!c.classList || !c.classList.contains("pchk") || c.classList.contains("vid-chk")) return;
      var card = c.closest(".section-card");
      if(c.checked && card) Array.prototype.forEach.call(card.querySelectorAll("h3.h3-toggle"), function(h){ window.__toeflSetH3Done(h, true); });
      render();
    });
    document.addEventListener("toefl-part", render);
    document.addEventListener("toefl-h3", render);
    document.addEventListener("toefl-access", render);
    document.addEventListener("keydown", function(e){ if(e.key === "Escape" && rail.classList.contains("is-open")){ setOpen(false); toggle.focus(); } });
    window.__toeflRenderRail = render;
    render();
  })();

  // ---------- Balão de tradução (item 18 de 2026-10-25) ----------
  // O build transforma [[inglês::tradução]] dos .md em <span class="tr">. A
  // tradução aparece num balão: mouse por cima (computador), toque (celular;
  // tocar de novo ou fora fecha) ou foco pelo teclado (Esc fecha). Dentro de
  // exercício, diagnóstico e simulado fica desligada até o aluno responder
  // aquele item. O interruptor "Traduções" das Configurações vale para o
  // site todo e fica no aparelho (toefl_tr_v1), como o tema.
  (function(){
    var tip = document.getElementById("trTip"), toggle = document.getElementById("trToggle");
    if(!tip) return;
    var LS_TR = "toefl_tr_v1", on = safeGet(LS_TR) !== "off", cur = null;
    if(toggle) toggle.checked = on;
    var EXERCISE = ".qcard, .exam, .ctw, .bsq-card, .spk-item, .wbox, .srs";
    function answered(el){
      var w = el.closest(EXERCISE);
      if(!w) return true;
      if(w.classList.contains("ctw")) return w.classList.contains("is-checked");
      if(w.classList.contains("exam")) return w.classList.contains("is-submitted") || !!w.querySelector(".verdict");
      return !!w.querySelector(".verdict") || w.classList.contains("is-checked") || w.classList.contains("checked");
    }
    function allowed(el){ return on && answered(el); }
    function refresh(){
      Array.prototype.forEach.call(document.querySelectorAll(".tr[data-tr]"), function(t){
        var ok = allowed(t);
        t.classList.toggle("tr-off", !ok);
        if(ok) t.setAttribute("tabindex", "0"); else t.removeAttribute("tabindex");
      });
      if(cur && !allowed(cur)) hide();
    }
    function place(t){
      var r = t.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
      var top = r.bottom + 8;
      if(top + h > window.innerHeight - 8) top = Math.max(8, r.top - h - 8);
      tip.style.top = Math.round(top) + "px";
      tip.style.left = Math.round(Math.max(8, Math.min(r.left, window.innerWidth - w - 8))) + "px";
    }
    function show(t){
      if(!allowed(t)) return;
      if(cur && cur !== t) hide();
      cur = t;
      tip.textContent = t.dataset.tr;
      tip.hidden = false;
      place(t);
      t.setAttribute("aria-describedby", "trTip");
      t.classList.add("tr-open");
    }
    function hide(){
      if(!cur) return;
      cur.removeAttribute("aria-describedby");
      cur.classList.remove("tr-open");
      cur = null;
      tip.hidden = true;
    }
    document.addEventListener("pointerover", function(e){
      if(e.pointerType !== "mouse") return;
      var t = e.target.closest && e.target.closest(".tr[data-tr]");
      if(t) show(t);
    });
    document.addEventListener("pointerout", function(e){
      if(e.pointerType !== "mouse" || !cur) return;
      var t = e.target.closest && e.target.closest(".tr[data-tr]");
      if(t === cur && !cur.contains(e.relatedTarget) && document.activeElement !== cur) hide();
    });
    document.addEventListener("focusin", function(e){ var t = e.target.closest && e.target.closest(".tr[data-tr]"); if(t) show(t); });
    document.addEventListener("focusout", function(e){ if(cur && e.target === cur) hide(); });
    var lastPointer = "";
    document.addEventListener("pointerdown", function(e){ lastPointer = e.pointerType; }, true);
    document.addEventListener("click", function(e){
      var t = e.target.closest && e.target.closest(".tr[data-tr]");
      // mouse: o balão já abriu ao passar por cima e fica; toque: alterna
      if(t){ if(cur === t && lastPointer !== "mouse") hide(); else show(t); }
      else if(cur) hide();
      setTimeout(refresh, 0); // uma resposta pode ter liberado as traduções do item
    });
    document.addEventListener("keydown", function(e){
      if(e.key === "Escape" && cur){ hide(); return; }
      var t = e.target.closest && e.target.closest(".tr[data-tr]");
      if(t && (e.key === "Enter" || e.key === " ")){ e.preventDefault(); if(cur === t) hide(); else show(t); }
    });
    window.addEventListener("scroll", hide, { passive: true });
    if(toggle) toggle.addEventListener("change", function(){
      on = toggle.checked;
      safeSet(LS_TR, on ? "on" : "off");
      refresh();
    });
    window.__toeflTr = { show: show, hide: hide, refresh: refresh }; // gancho do smoke test
    refresh();
  })();

  // ---------- Janelas (painel, conta, certificado): foco e teclado ----------
  // Ao abrir, o foco entra na janela; Tab fica preso nela; Esc fecha; ao
  // fechar, o foco volta para o botão que abriu. Quem abre e fecha cada
  // janela é o código dela: aqui só se observa o atributo hidden.
  (function(){
    if(!("MutationObserver" in window)) return;
    function focusables(m){
      return Array.prototype.filter.call(
        m.querySelectorAll('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])'),
        function(el){ return !el.disabled && el.offsetParent !== null; });
    }
    ["certModal", "accountModal", "dashboardModal"].forEach(function(id){
      var m = document.getElementById(id);
      if(!m) return;
      var opener = null;
      new MutationObserver(function(){
        if(!m.hidden){
          if(!m.contains(document.activeElement)){
            opener = document.activeElement;
            var first = focusables(m)[0];
            if(first) first.focus();
          }
        } else if(opener && opener.focus){
          opener.focus();
          opener = null;
        }
      }).observe(m, { attributes: true, attributeFilter: ["hidden"] });
      m.addEventListener("keydown", function(e){
        if(e.key === "Escape"){
          var closeBtn = m.querySelector('[aria-label="Fechar"]');
          if(closeBtn && !m.hidden) closeBtn.click();
          return;
        }
        if(e.key !== "Tab") return;
        var f = focusables(m);
        if(!f.length) return;
        if(e.shiftKey && document.activeElement === f[0]){ e.preventDefault(); f[f.length - 1].focus(); }
        else if(!e.shiftKey && document.activeElement === f[f.length - 1]){ e.preventDefault(); f[0].focus(); }
      });
    });
  })();

  // ---------- Inglês marcado como inglês ----------
  // A página é pt-BR, e sem lang="en" o leitor de tela lê as alternativas e
  // os textos dos exercícios com pronúncia de português. Marca só o que é
  // conteúdo-alvo dos widgets; alternativa escrita em português (há algumas)
  // fica de fora pelo teste abaixo. O texto corrido dos módulos mistura as
  // duas línguas na mesma frase e não é marcado.
  (function(){
    var PT = /[ãõçáéíóúâêôà]|\s(não|que|para|uma|você|de|os|da|com|em)\s/i;
    Array.prototype.forEach.call(
      document.querySelectorAll(".opt .otext, .exam-opt .otext, .quiz-passage-body, .ctw-text, .bsq-chip, .bsq-context, .spk-text"),
      function(el){
        var t = " " + el.textContent + " ";
        if(t.trim() && !PT.test(t)) el.setAttribute("lang", "en");
      });
    Array.prototype.forEach.call(document.querySelectorAll(".srs-word, .srs-ex, .srs-syn"), function(el){ el.setAttribute("lang", "en"); });
  })();

  // ---------- "Comece aqui": o primeiro passo, no topo do Módulo 0 ----------
  // Sem isto o aluno novo caía na Parte 1 (teoria sobre a prova) sem ninguém
  // dizer o que fazer primeiro nem onde fica o menu. O cartão tem dois
  // estados: antes do diagnóstico (leva até ele) e depois (leva ao
  // cronograma). Some quando o aluno dispensa; a escolha fica em
  // toefl_welcome_v1, local do aparelho como o tema.
  (function(){
    var panel = document.getElementById("panel-mod0");
    var diag = document.querySelector('.quiz-drill[data-drill="mod0-diag"]');
    var head = panel && panel.querySelector(".panel-head");
    if(!panel || !diag || !head) return;
    var LS_WELCOME = "toefl_welcome_v1";
    var card = document.createElement("section");
    card.className = "start-card";
    card.id = "startCard";
    card.setAttribute("aria-label", "Comece aqui");
    card.innerHTML =
      '<p class="start-kicker">Comece aqui</p>' +
      '<h2 class="start-title"></h2>' +
      '<p class="start-text"></p>' +
      '<div class="start-actions">' +
      '<button type="button" class="start-go"></button>' +
      '<button type="button" class="start-skip">Dispensar este aviso</button>' +
      '</div>';
    head.parentNode.insertBefore(card, head.nextSibling);
    var titleEl = card.querySelector(".start-title"), textEl = card.querySelector(".start-text");
    var goBtn = card.querySelector(".start-go");

    function partCard(n){ return panel.querySelectorAll(".section-card")[n - 1]; }
    function goToPart(n, target){
      navTo("mod0");
      var showPart = window.__toeflShowPart && window.__toeflShowPart.mod0;
      if(showPart && partCard(n)) showPart(partCard(n), { noScroll: true });
      setTimeout(function(){ (target || partCard(n)).scrollIntoView({ behavior: "smooth", block: "start" }); }, 60);
    }
    // o diagnóstico é a Parte 1: com ela aberta, o cartão não aparece por
    // cima dele (item 4 de 2026-10-25). Nas outras Partes do M0 ele volta.
    var diagCard = diag.closest(".section-card");
    function render(){
      card.hidden = safeGet(LS_WELCOME) === "1" || (!!diagCard && !diagCard.hidden);
      var a = computeQuizAccuracy("mod0-diag");
      if(a.confirmed < a.total){
        titleEl.textContent = "Faça o diagnóstico antes de ler qualquer coisa";
        textEl.textContent = "São 10 questões, cerca de 12 minutos. O resultado mostra o seu nível de partida e o cronograma que mais combina com você.";
        goBtn.textContent = a.confirmed ? "Continuar o diagnóstico (" + a.confirmed + " de " + a.total + ")" : "Fazer o diagnóstico agora";
        goBtn.onclick = function(){ goToPart(1, diag); };
      } else {
        var band = cefrBandFromPct(Math.round(100 * a.correct / a.total));
        titleEl.textContent = "Diagnóstico feito: nível estimado " + band.label;
        textEl.textContent = "Você acertou " + a.correct + " de " + a.total + ". " +
          scheduleFromPct(Math.round(100 * a.correct / a.total)).split(" · ")[0] + ". O próximo passo é abrir esse cronograma.";
        goBtn.textContent = "Ver o meu cronograma";
        goBtn.onclick = function(){ goToPart(6); };
      }
    }
    card.querySelector(".start-skip").addEventListener("click", function(){
      safeSet(LS_WELCOME, "1");
      render();
    });
    window.__toeflRefreshStart = render;
    document.addEventListener("toefl-part", function(e){ if(e.detail.mod === "mod0") render(); });
    render();
  })();

  // abre uma Parte de um módulo e, se pedido, a subseção cujo título começa
  // com `h3code` (ex. "6.2"), rolando até ela
  function openPart(mod, n, h3code){
    navTo(mod);
    var panel = document.getElementById("panel-" + mod);
    var card = panel && panel.querySelectorAll(".section-card")[n - 1];
    if(!card) return;
    var showPart = window.__toeflShowPart && window.__toeflShowPart[mod];
    if(showPart) showPart(card, { noScroll: true });
    var target = card;
    if(h3code){
      var h3 = Array.prototype.filter.call(card.querySelectorAll("h3.h3-toggle"), function(h){
        return h.textContent.replace("✓", "").trim().indexOf(h3code + " ") === 0;
      })[0];
      if(h3){
        h3.classList.remove("collapsed");
        var body = h3.nextElementSibling;
        if(body && body.classList.contains("h3-body")) body.classList.remove("h3-collapsed");
        target = h3;
      }
    }
    setTimeout(function(){ target.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60);
  }

  // áreas dos pontos fracos (itens 42 e 43): nome, módulo e Parte do atalho.
  // Ficam aqui em cima porque o resultado do diagnóstico, logo abaixo, usa o
  // mesmo atalho. O cálculo está no bloco "Pontos fracos e Sua prioridade hoje".
  var WEAK_AREAS = {
    reading: { nome: "Reading", mod: "mod1", parte: 2 },
    listening: { nome: "Listening", mod: "mod2", parte: 3 },
    speaking: { nome: "Speaking", mod: "mod3", parte: 3 },
    writing: { nome: "Writing (Build a Sentence)", mod: "mod4", parte: 3 },
    gramatica: { nome: "Gramática e ordem das palavras", mod: "mod4", parte: 3 },
    vocabulario: { nome: "Vocabulário", mod: "mod6", parte: 2 },
    registro: { nome: "Registro e conectivos", mod: "mod5", parte: 3 }
  };
  var WEAK_MIN = 4, WEAK_SHOW = 70, WEAK_STRONG = 50, EXAM_NEAR = 14;
  // o registro de erros de cada módulo entra na área dele
  var ERRLOG_AREA = { mod1: "reading", mod2: "listening", mod3: "speaking", mod4: "writing", mod5: "registro", mod6: "vocabulario" };

  // ---------- Resultado do diagnóstico e a meta (M0, Parte 1) ----------
  // Aparece logo abaixo da décima questão quando ela é confirmada: nível
  // estimado, acertos por área, pontos fortes e a melhorar, e o formulário da
  // meta (nota que o aluno precisa e data da prova). Com a meta, mostra a
  // distância e o cronograma indicado (ToeflLevel.recommend, regras do M0,
  // Parte 6) e grava em toefl_goal_v1, que a meta de hoje usa.
  (function(){
    var box = document.getElementById("diagResult");
    if(!box) return;
    var $ = function(id){ return document.getElementById(id); };
    var AREAS = {};
    try { AREAS = JSON.parse($("diagAreas").textContent); } catch(e){}
    var sel = $("goalTarget"), dateIn = $("goalDate"), msg = $("goalMsg");
    var blank = document.createElement("option");
    blank.value = ""; blank.textContent = "Escolha a banda";
    sel.appendChild(blank);
    ToeflLevel.SCALE.forEach(function(s, i){
      var o = document.createElement("option");
      o.value = String(s.band); o.textContent = ToeflLevel.scaleLabel(i);
      sel.appendChild(o);
    });
    dateIn.min = todayStr();

    function bandText(b){ return "banda " + b.code.replace("–", " a "); }
    function say(text, err){ msg.textContent = text; msg.classList.toggle("is-err", !!err); msg.hidden = !text; }
    // o atalho abre a Parte que ensina a área: a mesma dos pontos fracos do Painel
    function item(list, text, painel){
      var li = document.createElement("li");
      li.appendChild(document.createTextNode(text));
      var w = painel && WEAK_AREAS[painel];
      if(w){
        var b = document.createElement("button");
        b.type = "button"; b.className = "diag-link"; b.textContent = "Abrir a Parte " + w.parte + " do Módulo " + w.mod.slice(3);
        b.addEventListener("click", function(){ openPart(w.mod, w.parte); });
        li.appendChild(document.createTextNode(" "));
        li.appendChild(b);
      }
      list.appendChild(li);
    }
    function daysText(n){
      if(n === null) return "";
      if(n < 0) return " A data da prova já passou: atualize a data.";
      if(n === 0) return " A prova é hoje.";
      if(n === 1) return " A prova é amanhã.";
      return " Faltam " + n + " dias para a prova.";
    }

    function renderPlan(d){
      var g = readGoal(), plan = $("diagPlan");
      if(g){ sel.value = String(g.target); dateIn.value = g.exam; }
      if(!g){ plan.hidden = true; return; }
      var lvl = cefrBandFromPct(d.pct), left = daysUntil(g.exam);
      var rec = ToeflLevel.recommend(d.pct, g.target, left);
      var want = ToeflLevel.cefrOf(g.target) + " (banda " + ToeflLevel.fmt(g.target) + ")";
      $("diagPlanGap").textContent = (rec.gap <= 0
        ? "Você está em " + lvl.label + " (" + bandText(lvl) + ") e a sua meta é " + want + ": você já está na faixa."
        : "Você está em " + lvl.label + " (" + bandText(lvl) + ") e precisa de " + want + ".") + daysText(left);
      $("diagPlanSched").textContent = "Cronograma indicado: " + rec.name + ", de " + rec.days + " dias (Parte " + rec.part +
        "), porque " + rec.reason + "." +
        (rec.emergency ? " Com menos de 30 dias até a prova, siga o Intensivo junto com o Plano de Emergência da Parte 7."
          : rec.squeezed ? " A prova chega antes do fim de um cronograma mais longo, então fica o que cabe no prazo." : "");
      $("diagPlanGo").onclick = function(){ openPart("mod0", 6, rec.part); };
      plan.hidden = false;
    }

    function render(){
      var d = diagStats();
      if(!d || !d.done){ box.hidden = true; return; }
      box.hidden = false;
      var lvl = cefrBandFromPct(d.pct);
      $("diagResultTitle").textContent = "Nível estimado: " + lvl.label + ", " + bandText(lvl);
      $("diagScore").textContent = "Você acertou " + d.correct + " de " + d.total +
        ". Isso não é uma nota, é um mapa: agora dá para saber por onde começar.";
      var list = $("diagAreaList"), strong = $("diagStrong"), weak = $("diagWeak");
      list.innerHTML = ""; strong.innerHTML = ""; weak.innerHTML = "";
      Object.keys(AREAS).forEach(function(k){
        var a = d.areas[k];
        if(!a) return;
        var li = document.createElement("li");
        li.className = "diag-area " + (a.ok === a.n ? "is-ok" : a.ok === 0 ? "is-bad" : "is-mid");
        var name = document.createElement("span"); name.className = "diag-area-name"; name.textContent = AREAS[k].nome;
        var n = document.createElement("span"); n.className = "diag-area-n"; n.textContent = a.ok + " de " + a.n;
        var bar = document.createElement("span"); bar.className = "diag-area-bar";
        var fill = document.createElement("span"); fill.style.width = Math.round(100 * a.ok / a.n) + "%";
        bar.appendChild(fill);
        li.appendChild(name); li.appendChild(n); li.appendChild(bar);
        list.appendChild(li);
        if(a.ok === a.n) item(strong, AREAS[k].nome + ": " + a.ok + " de " + a.n + ".");
        else item(weak, AREAS[k].nome + ": " + a.ok + " de " + a.n + ". Onde treinar: " + AREAS[k].onde + ".", AREAS[k].painel);
      });
      if(!strong.children.length) item(strong, "Ainda nenhuma área completa. Tudo bem: é exatamente isso que o curso vai construir.");
      if(!weak.children.length) item(weak, "Você acertou todas as áreas. O foco agora é estratégia e tempo de prova.");
      renderPlan(d);
    }

    $("goalSave").addEventListener("click", function(){
      var d = diagStats();
      var target = parseFloat(sel.value), exam = dateIn.value, left = daysUntil(exam);
      if(!target){ say("Escolha a nota que você precisa.", true); sel.focus(); return; }
      if(left === null){ say("Informe a data da prova.", true); dateIn.focus(); return; }
      if(left < 0){ say("Essa data já passou. Confira a data da prova.", true); dateIn.focus(); return; }
      var rec = ToeflLevel.recommend(d.pct, target, left), old = readGoal();
      safeSet(LS_GOAL, JSON.stringify({ target: target, exam: exam, sched: rec.days,
        start: old && old.sched === rec.days && old.start ? old.start : todayStr() }));
      say("Plano salvo. A meta de hoje já segue este cronograma.");
      renderPlan(d);
      updateLevelBadge(d.correct, d.total); // o selo da gaveta passa a citar o cronograma da meta
      if(typeof window.__toeflRefreshStart === "function") window.__toeflRefreshStart();
      if(typeof window.__toeflRefreshPlan === "function") window.__toeflRefreshPlan();
    });

    document.addEventListener("toefl-reveal", function(e){
      if(!e.target.matches || !e.target.matches('[data-drill="mod0-diag"]')) return;
      render();
      if(!box.hidden){
        box.focus({ preventScroll: true });
        box.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
    window.__toeflRefreshDiag = render;
    render();
  })();

  // ---------- Plano de estudo e meta de hoje (item 5 de 2026-10-25) ----------
  // A meta deixa de ser "1 Parte por dia". Ela sai do cronograma da meta do
  // aluno (toefl_goal_v1: nota, data da prova, 30/60/90 dias e início):
  // 1. PLAN_PHASES segue as tabelas do M0, Parte 6 (semanas -> módulos), com
  //    M5, M6, M8 e M9 encaixados onde o cronograma fala de registro,
  //    vocabulário, armadilhas e véspera. Módulo que aparece em duas fases
  //    divide as Partes entre elas.
  // 2. Cada Parte de teoria, prática ou simulado (referência fica de fora:
  //    é para consultar) ganha um dia, pelo tempo estimado de app/partes.json.
  //    Se a prova vem antes do fim do cronograma, os dias encolhem.
  // 3. A meta de hoje são as Partes previstas até hoje e ainda não
  //    concluídas (no máximo 3, ou 120 min), mais 1 exercício quando nenhuma
  //    delas é de prática. Quem atrasou recebe as atrasadas primeiro; quem
  //    está em dia recebe a próxima. A lista fica congelada no dia.
  // Sem diagnóstico, a meta é fazer o diagnóstico; sem a meta, é montá-la.
  var PLAN_PHASES = {
    30: [[7, ["mod0", "mod1"]], [7, ["mod2", "mod4"]], [7, ["mod4", "mod3"]], [9, ["mod3", "mod7", "mod8"]]],
    60: [[14, ["mod0", "mod1"]], [14, ["mod2"]], [14, ["mod4", "mod5"]], [7, ["mod3", "mod6", "mod9"]], [11, ["mod7", "mod8"]]],
    90: [[21, ["mod0", "mod6", "mod9"]], [21, ["mod1"]], [21, ["mod2"]], [14, ["mod4", "mod5"]], [7, ["mod3"]], [6, ["mod7", "mod8"]]]
  };
  var PLAN_MAX_PARTS = 3, PLAN_MAX_MIN = 120, PLAN_EXERCISE_MIN = 10;
  function partDoneBox(card){ return card.querySelector(".mark-done .pchk"); }
  function planParts(goal){
    var phases = PLAN_PHASES[goal.sched] || PLAN_PHASES[60], occ = {}, seen = {}, out = [], start = 0;
    phases.forEach(function(ph){ ph[1].forEach(function(m){ occ[m] = (occ[m] || 0) + 1; }); });
    phases.forEach(function(ph){
      var items = [];
      ph[1].forEach(function(m){
        var list = [];
        partCards(m).forEach(function(card, i){
          var p = partInfo(m, i + 1), chk = partDoneBox(card);
          if(!p || p.tipo === "referencia" || !chk) return;
          if(card.querySelector('[data-drill="mod0-diag"]')) return; // o diagnóstico já foi feito para chegar aqui
          if(accessFree && card.classList.contains("fs-part-locked")) return; // conta grátis: só a amostra
          list.push({ mod: m, n: i + 1, pid: chk.dataset.pid, min: p.min, tipo: p.tipo });
        });
        var j = seen[m] = (seen[m] || 0) + 1;
        items = items.concat(list.slice(Math.floor(list.length * (j - 1) / occ[m]), Math.floor(list.length * j / occ[m])));
      });
      var total = items.reduce(function(s, x){ return s + x.min; }, 0) || 1, acc = 0;
      items.forEach(function(x){ x.day = start + Math.floor(acc / total * ph[0]); acc += x.min; out.push(x); });
      start += ph[0];
    });
    return { parts: out, length: start };
  }
  function partLabel(x){ return "M" + x.mod.slice(3) + " Parte " + x.n; }
  function joinPt(list){ return list.length > 1 ? list.slice(0, -1).join(", ") + " e " + list[list.length - 1] : (list[0] || ""); }

  // a meta de hoje: { kind: "diag" | "goal" | "plan" | "done", text, items,
  // needEx, exDone, done, total, doneCount, min, meta, next, go }
  function computeToday(){
    var d = diagStats();
    if(!d) return null;
    if(!d.done){
      return { kind: "diag", text: "Hoje: fazer o diagnóstico (15 min)", total: 1, doneCount: 0, done: false,
        next: "Depois: dizer a nota que você precisa e a data da prova, para eu montar o seu plano.",
        go: function(){ openPart("mod0", 1); } };
    }
    var g = readGoal(), lvl = cefrBandFromPct(d.pct);
    if(!g){
      return { kind: "goal", text: "Hoje: montar o seu plano, com a nota que você precisa e a data da prova (2 min)",
        total: 1, doneCount: 0, done: false, meta: "Seu nível estimado: " + lvl.label + ".",
        next: "Depois: seguir a meta de cada dia, tirada do cronograma.",
        go: function(){
          openPart("mod0", 1);
          setTimeout(function(){ var el = document.getElementById("diagGoal"); if(el) el.scrollIntoView({ behavior: "smooth", block: "center" }); }, 120);
        } };
    }
    var plan = planParts(g), startDay = parseDay(g.start) || parseDay(todayStr());
    var toExam = Math.round((parseDay(g.exam) - startDay) / 86400000);
    var span = Math.max(1, Math.min(plan.length, toExam > 0 ? toExam : plan.length));
    var t = Math.max(0, Math.round((parseDay(todayStr()) - startDay) / 86400000));
    plan.parts.forEach(function(x){ x.due = Math.floor(x.day * span / plan.length); });
    var pending = plan.parts.filter(function(x){ return !progressState[x.pid]; });
    var late = pending.filter(function(x){ return x.due < t; }).length;
    var left = daysUntil(g.exam);
    var meta = (left > 1 ? "Prova em " + left + " dias" : left === 1 ? "Prova amanhã" : left === 0 ? "Prova hoje" : "A data da prova já passou") +
      ". Você: " + lvl.label + ". Meta: " + ToeflLevel.cefrOf(g.target) + " (banda " + ToeflLevel.fmt(g.target) + ").";

    // a lista do dia, congelada no primeiro cálculo de hoje
    var key = [g.start, g.sched, g.exam, accessFree ? "free" : "full"].join("|");
    var day = readDay(), pids;
    if(day.plan && day.plan.key === key) pids = day.plan.pids;
    else {
      var pick = [], mins = 0;
      pending.filter(function(x){ return x.due <= t; }).some(function(x){
        if(pick.length && (pick.length >= PLAN_MAX_PARTS || mins + x.min > PLAN_MAX_MIN)) return true;
        pick.push(x); mins += x.min; return false;
      });
      if(!pick.length && pending.length) pick.push(pending[0]); // em dia: adianta a próxima
      pids = pick.map(function(x){ return x.pid; });
      day.plan = { key: key, pids: pids };
      try { localStorage.setItem(LS_DAILY_GOAL, JSON.stringify(day)); } catch(e){} // sem safeSet: calcular não é estudar
    }
    var byPid = {};
    plan.parts.forEach(function(x){ byPid[x.pid] = x; });
    var items = pids.map(function(p){ return byPid[p]; }).filter(Boolean);
    if(!items.length){
      return { kind: "done", text: "Hoje: o cronograma está cumprido. Faça um bloco de simulado do Módulo 7 para manter o ritmo.",
        total: 1, doneCount: 0, done: false, meta: meta, next: "", go: function(){ openPart("mod7", 3); } };
    }
    var needEx = !items.some(function(x){ return x.tipo === "pratica" || x.tipo === "simulado"; });
    var exDone = day.ex === day.date;
    var doneParts = items.filter(function(x){ return progressState[x.pid]; }).length;
    var min = items.reduce(function(s, x){ return s + x.min; }, 0) + (needEx ? PLAN_EXERCISE_MIN : 0);
    var names = items.map(partLabel);
    if(needEx) names.push("1 exercício");
    var nextPart = pending.filter(function(x){ return pids.indexOf(x.pid) === -1; })[0];
    var next = late > items.length
      ? "Você está " + late + " Partes atrás do cronograma. A meta de hoje já começa pelas atrasadas; se o atraso crescer, use o Plano de Emergência (M0, Parte 7)."
      : nextPart ? "Depois: " + partLabel(nextPart) + " (" + kindText(partInfo(nextPart.mod, nextPart.n)) + ")." : "Depois disso, o cronograma está cumprido.";
    var firstOpen = items.filter(function(x){ return !progressState[x.pid]; })[0];
    return {
      kind: "plan", items: items, needEx: needEx, exDone: exDone, late: late,
      text: "Hoje: " + joinPt(names) + " (" + min + " min)",
      total: items.length + (needEx ? 1 : 0), doneCount: doneParts + (needEx && exDone ? 1 : 0),
      done: doneParts === items.length && (!needEx || exDone), meta: meta, next: next,
      go: function(){
        if(firstOpen) openPart(firstOpen.mod, firstOpen.n);
        else { navTo("mod0"); var lp = document.getElementById("levelPractice"); if(lp){ var c = lp.closest(".section-card"); if(c && window.__toeflShowPart.mod0) window.__toeflShowPart.mod0(c, { noScroll: true }); setTimeout(function(){ lp.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60); } }
      }
    };
  }

  // ---------- Pontos fracos e "Sua prioridade hoje" (itens 42 e 43) ----------
  // Pontos fracos: os acertos de tudo que já guarda certo e errado no
  // progresso, somados por área. Diagnóstico (cada questão pela área dela,
  // campo "painel" de DIAG_AREAS no build_pipeline.py), exercícios de Reading
  // e Complete the Words, Listening, Build a Sentence, os blocos do simulado
  // pela seção, e o Listen and Repeat (o aluno marca se repetiu sem erro).
  // Área com menos de WEAK_MIN respostas não ganha taxa: aparece como "poucos
  // dados". Não há estado novo: tudo sai de chaves que já sincronizam.
  function weakAreas(){
    var acc = {};
    Object.keys(WEAK_AREAS).forEach(function(k){ acc[k] = { ok: 0, n: 0 }; });
    function add(k, ok, n){ acc[k].ok += ok; acc[k].n += n; }
    function read(key){ try { return JSON.parse(safeGet(key) || "{}") || {}; } catch(e){ return {}; } }
    var diagMap = {};
    try { diagMap = JSON.parse(document.getElementById("diagAreas").textContent); } catch(e){}
    var diag = document.querySelector('.quiz-drill[data-drill="mod0-diag"]');
    if(diag){
      var st = read("toefl_quiz_mod0-diag_v1");
      Array.prototype.forEach.call(diag.querySelectorAll(".qcard"), function(c){
        var s = st[c.dataset.num], a = diagMap[c.dataset.area];
        if(s && s.confirmed && a && acc[a.painel]) add(a.painel, isCardCorrect(c, s.picked) ? 1 : 0, 1);
      });
    }
    var r = computeQuizAccuracy("mod1-"), l = computeQuizAccuracy("mod2-"), b = extraAccuracy("bsq");
    add("reading", r.correct, r.confirmed);
    add("listening", l.correct, l.confirmed);
    add("writing", b.correct, b.confirmed);
    // simulado: cada bloco conta na seção do título de cima ("Listen to..." é Listening)
    var section = "reading";
    Array.prototype.forEach.call(document.querySelectorAll("#panel-mod7 h3, #panel-mod7 h4, #panel-mod7 .exam"), function(el){
      if(!el.classList.contains("exam")){
        if(/\bListen/i.test(el.textContent)) section = "listening";
        else if(/\bRead|Complete the Words/i.test(el.textContent)) section = "reading";
        return;
      }
      if(isLockedNow(el)) return;
      var es = read("toefl_exam_" + el.dataset.exam + "_v1");
      if(!es.done || !es.answers) return;
      Array.prototype.forEach.call(el.querySelectorAll(".exam-item"), function(it){
        add(section, es.answers[it.dataset.num] === it.dataset.correct ? 1 : 0, 1);
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll('.spk[data-mode="repeat"]'), function(root){
      if(isLockedNow(root)) return;
      var ss = read("toefl_spk_" + root.dataset.spk + "_v1");
      Object.keys(ss).forEach(function(num){
        if(ss[num] === "ok") add("speaking", 1, 1);
        else if(ss[num] === "miss") add("speaking", 0, 1);
      });
    });
    // registro de erros (quadro "Registre esta sessão", M1 a M6): cada código
    // marcado conta como 1 erro na área do módulo. Sessão sem código não conta
    // acerto, porque o aluno não disse quantas acertou.
    Object.keys(ERRLOG_AREA).forEach(function(mod){
      var entries;
      try { entries = JSON.parse(safeGet("toefl_errlog_" + mod + "_v1") || "[]"); } catch(e){ entries = []; }
      if(!Array.isArray(entries)) return;
      entries.forEach(function(en){
        var n = en && Array.isArray(en.codes) ? en.codes.length : 0;
        if(n) add(ERRLOG_AREA[mod], 0, n);
      });
    });
    return Object.keys(WEAK_AREAS).map(function(k){
      var a = acc[k], w = WEAK_AREAS[k];
      return { key: k, nome: w.nome, mod: w.mod, parte: w.parte, ok: a.ok, n: a.n,
        pct: a.n ? Math.round(100 * a.ok / a.n) : null, enough: a.n >= WEAK_MIN };
    }).sort(function(x, y){
      if(x.enough !== y.enough) return x.enough ? -1 : 1;
      return x.enough ? x.pct - y.pct : y.n - x.n;
    });
  }

  function partOpenable(mod, n){
    var card = partCards(mod)[n - 1];
    return !!card && !(accessFree && card.classList.contains("fs-part-locked"));
  }
  function partIsDone(mod, n){
    var card = partCards(mod)[n - 1], chk = card && partDoneBox(card);
    return !!chk && !!progressState[chk.dataset.pid];
  }
  function partTitle(mod, n){
    var t = partShortTitle(partCards(mod)[n - 1]);
    return "Módulo " + mod.slice(3) + ", Parte " + n + (t ? ": " + t : "");
  }
  // primeira Parte do módulo, de um tipo, aberta e ainda não concluída
  function firstPending(mod, tipo){
    var cards = partCards(mod);
    for(var i = 0; i < cards.length; i++){
      var p = partInfo(mod, i + 1);
      if(p && p.tipo === tipo && partOpenable(mod, i + 1) && !partIsDone(mod, i + 1)) return i + 1;
    }
    return 0;
  }

  // "Sua prioridade hoje": UMA Parte, pela primeira regra que vale, nesta
  // ordem (a mesma regra está no CLAUDE.md).
  // 1. Sem o diagnóstico completo: o diagnóstico (M0, Parte 1).
  // 2. Prova em até 14 dias: reta final. No dia, M8 Parte 9; na véspera, M8
  //    Parte 2; até 7 dias, M8 Parte 1 (se não feita); senão o próximo
  //    simulado do M7 em aberto; com todos feitos, M8 Parte 1.
  // 3. Ponto fraco forte (WEAK_MIN respostas ou mais e menos de 50% de
  //    acerto): a Parte que ensina a área e, se já foi feita, a de prática.
  // 4. Sem meta (nota e data da prova): montar o plano.
  // 5. Senão, a meta de hoje do cronograma: a primeira Parte dela em aberto.
  //    Cronograma cumprido: um bloco de simulado (M7, Parte 3).
  // { kind: "diag" | "exam" | "weak" | "goal" | "plan" | "done", mod, n, text, why, go }
  function computePriority(){
    var d = diagStats();
    if(!d) return null;
    function pick(kind, mod, n, why){
      return { kind: kind, mod: mod, n: n, text: partTitle(mod, n), why: why, go: function(){ openPart(mod, n); } };
    }
    if(!d.done) return pick("diag", "mod0", 1, "Sem ele eu não sei por onde você deve começar. São cerca de 15 minutos.");
    var g = readGoal(), left = g ? daysUntil(g.exam) : null;
    if(left !== null && left >= 0 && left <= EXAM_NEAR){
      var when = left === 0 ? "A prova é hoje" : left === 1 ? "A prova é amanhã" : "Faltam " + left + " dias para a prova";
      if(left === 0 && partOpenable("mod8", 9)) return pick("exam", "mod8", 9, when + ". Revise a sua cola mental e confie no que você treinou.");
      if(left === 1 && partOpenable("mod8", 2)) return pick("exam", "mod8", 2, when + ". Hoje o foco é chegar descansado, com tudo pronto.");
      if(left <= 7 && !partIsDone("mod8", 1) && partOpenable("mod8", 1)) return pick("exam", "mod8", 1, when + ". Na última semana, o que mais rende é ajustar a rotina de prova.");
      var sim = firstPending("mod7", "simulado");
      if(sim) return pick("exam", "mod7", sim, when + ". Agora o treino que mais rende é a prova inteira, no tempo dela.");
      if(!partIsDone("mod8", 1) && partOpenable("mod8", 1)) return pick("exam", "mod8", 1, when + ". Os simulados estão feitos, então é hora de preparar a semana da prova.");
    }
    var weak = weakAreas().filter(function(a){ return a.enough && a.pct < WEAK_STRONG; })[0];
    if(weak){
      var why = "Seu ponto mais fraco agora é " + weak.nome + ", com " + weak.pct + "% de acerto (" + weak.ok + " de " + weak.n + "). ";
      if(partOpenable(weak.mod, weak.parte) && !partIsDone(weak.mod, weak.parte)) return pick("weak", weak.mod, weak.parte, why + "Esta Parte ensina exatamente isso.");
      var pr = firstPending(weak.mod, "pratica");
      if(pr) return pick("weak", weak.mod, pr, why + "Você já leu a teoria. Agora é praticar.");
    }
    var td = computeToday();
    if(!g) return { kind: "goal", mod: "mod0", n: 1, text: "Montar o seu plano (Módulo 0, Parte 1)",
      why: "Com a nota que você precisa e a data da prova, eu monto o cronograma e passo a indicar a Parte de cada dia.", go: td.go };
    if(td.kind === "plan"){
      var first = td.items.filter(function(x){ return !progressState[x.pid]; })[0];
      if(first) return pick("plan", first.mod, first.n, "É a próxima Parte do seu cronograma.");
      var ahead = planParts(g).parts.filter(function(x){ return !progressState[x.pid]; })[0];
      if(ahead) return pick("plan", ahead.mod, ahead.n, "A meta de hoje está cumprida. Se quiser adiantar, esta é a próxima do cronograma.");
    }
    return pick("done", "mod7", 3, "O cronograma está cumprido. Um bloco de simulado mantém o ritmo até a prova.");
  }
  window.__toeflWeak = weakAreas; // ganchos do smoke test e do Painel
  window.__toeflPriority = computePriority;

  (function(){
    var $ = function(id){ return document.getElementById(id); };
    var current = null;
    function setText(id, text){ var el = $(id); if(!el) return; el.textContent = text || ""; el.hidden = !text; }
    function render(){
      var td = computeToday();
      current = td;
      var bar = $("todayBar");
      if(!td){ if(bar) bar.hidden = true; return; }
      var doneText = "Meta de hoje cumprida. Mais um passo dado, e ele conta.";
      setText("dgText", td.done ? doneText : td.text);
      setText("dgMeta", td.meta);
      setText("dgNext", td.next);
      $("dgCount").textContent = Math.min(td.doneCount, td.total) + "/" + td.total;
      // o selo do topo repete a conta, ao lado do perfil (item 29)
      if($("topGoal")) $("topGoal").textContent = $("dgCount").textContent;
      var chip = $("topChip");
      if(chip){
        chip.classList.toggle("is-done", !!td.done);
        chip.setAttribute("aria-label", "Meta de hoje: " + $("dgCount").textContent + ". Sequência: " +
          computeStreak().count + " dias. Abrir o menu");
      }
      $("dgFill").style.width = Math.round(100 * Math.min(td.doneCount, td.total) / td.total) + "%";
      $("dgGo").textContent = td.done ? "Continuar estudando" : td.kind === "goal" ? "Montar meu plano" : "Começar";
      // a faixa do topo mostra "Sua prioridade hoje" (item 43); a meta do
      // cronograma continua na gaveta e aqui, na linha de baixo, com a conta
      var pr = computePriority();
      priority = pr;
      if(bar && pr){
        bar.hidden = false;
        bar.classList.toggle("is-done", !!td.done);
        setText("todayText", "Sua prioridade hoje: " + pr.text);
        setText("todayMeta", (td.done ? doneText + " " : "") + pr.why + (td.meta ? " " + td.meta : "") +
          (td.kind === "plan" && !td.done ? " Meta do cronograma: " + td.text.replace(/^Hoje: /, "") + ", " + td.doneCount + " de " + td.total + " feitos." : ""));
        $("todayGo").textContent = pr.kind === "diag" ? "Começar" : pr.kind === "goal" ? "Montar meu plano" : "Continuar";
      }
    }
    var priority = null;
    function go(){ if(current && current.go){ setSidebarOpen(false); current.go(); } }
    $("dgGo").addEventListener("click", go);
    $("todayGo").addEventListener("click", function(){ if(priority && priority.go) priority.go(); });
    window.__toeflRefreshPlan = render;
    window.__toeflToday = computeToday; // gancho do smoke test e do Painel
    document.addEventListener("toefl-access", render);
    render();
  })();

  // ---------- Videoaulas (app/videos.json) ----------
  // O build só põe a capa. O player (iframe do YouTube ou <video>) nasce no
  // clique, para a página não buscar nada de fora antes disso. A caixa "aula
  // assistida" é um .pchk comum: quem salva e conta no progresso é o bloco de
  // Progress checkboxes lá em cima.
  Array.prototype.slice.call(document.querySelectorAll(".vid")).forEach(function(box){
    var cover = box.querySelector(".vid-cover");
    var frame = box.querySelector(".vid-frame");
    var chk = box.querySelector(".vid-chk");
    var doneLabel = box.querySelector(".vid-done-label");
    function syncLabel(){
      box.classList.toggle("watched", chk.checked);
      doneLabel.textContent = chk.checked ? "Aula assistida" : "Marcar aula como assistida";
    }
    chk.addEventListener("change", syncLabel);
    syncLabel();

    cover.addEventListener("click", function(){
      var player;
      if(box.dataset.provider === "youtube"){
        player = document.createElement("iframe");
        // nocookie: o YouTube não grava cookie antes do aluno dar play.
        // cc_load_policy liga a legenda, em português quando o vídeo tiver.
        player.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(box.dataset.src) +
          "?autoplay=1&rel=0&cc_load_policy=1&cc_lang_pref=pt-BR&hl=pt-BR";
        player.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen";
        player.allowFullscreen = true;
        player.referrerPolicy = "strict-origin-when-cross-origin";
      } else {
        player = document.createElement("video");
        player.controls = true;
        player.autoplay = true;
        player.playsInline = true;
        player.preload = "metadata";
        player.src = box.dataset.src;
        if(box.dataset.captions){
          var track = document.createElement("track");
          track.kind = "captions";
          track.srclang = "pt-BR";
          track.label = "Português";
          track.src = box.dataset.captions;
          track.default = true;
          player.appendChild(track);
        }
        // arquivo próprio avisa quando termina, então a marcação é automática
        player.addEventListener("ended", function(){
          if(!chk.checked){ chk.checked = true; chk.dispatchEvent(new Event("change", { bubbles: true })); }
        });
      }
      player.className = "vid-player";
      player.title = cover.querySelector(".vid-title").textContent;
      frame.appendChild(player);
      frame.hidden = false;
      cover.hidden = true;
    });
  });

  // ---------- Trilha rápida ou completa (blocos de aprofundamento) ----------
  // Os blocos <details class="deep"> vêm do build (marcação :::aprofundamento
  // nos .md). Na trilha rápida ficam fechados e o aluno abre o que quiser; na
  // completa já vêm abertos. A escolha é preferência do aparelho, como o
  // tema: fica em toefl_trilha_v1 e não sincroniza. Sem nenhum bloco no site,
  // o seletor nem aparece.
  (function(){
    var box = document.getElementById("trailBox");
    var deep = Array.prototype.slice.call(document.querySelectorAll("details.deep"));
    if(!box || !deep.length) return;
    var btns = Array.prototype.slice.call(box.querySelectorAll(".trail-btn"));
    var hint = document.getElementById("trailHint");
    var LS_TRAIL = "toefl_trilha_v1";
    var HINTS = {
      rapida: "O essencial primeiro. Os blocos de aprofundamento ficam fechados: abra só os que quiser.",
      completa: "Tudo aberto: o essencial e os blocos de aprofundamento."
    };
    function apply(trail, save){
      if(!HINTS[trail]) trail = "rapida";
      deep.forEach(function(d){ d.open = trail === "completa"; });
      btns.forEach(function(b){
        var on = b.dataset.trail === trail;
        b.classList.toggle("active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      hint.textContent = HINTS[trail];
      document.documentElement.setAttribute("data-trail", trail);
      if(save) safeSet(LS_TRAIL, trail);
    }
    btns.forEach(function(b){
      b.addEventListener("click", function(){ apply(b.dataset.trail, true); });
    });
    box.hidden = false;
    apply(safeGet(LS_TRAIL) || "rapida", false);
  })();

  // ---------- PWA: instalar app, service worker e aviso de nova versão ----------
  // O service worker (app/sw.js, carimbado pelo build) só é registrado em
  // https ou em localhost. Aberto direto do disco (file://) nada disto roda e
  // o site segue como sempre foi. A versão nova fica em espera até o aluno
  // clicar em "Recarregar", para não trocar o site no meio de um exercício.
  (function(){
    var tools = document.getElementById("pwaTools");
    var installBtn = document.getElementById("pwaInstall");
    var iosHint = document.getElementById("pwaIosHint");
    var updateBar = document.getElementById("pwaUpdate");
    var updateBtn = document.getElementById("pwaUpdateBtn");
    var laterBtn = document.getElementById("pwaUpdateLater");
    if(!tools || !updateBar) return;

    var host = location.hostname;
    var canRegister = "serviceWorker" in navigator &&
      (location.protocol === "https:" || host === "localhost" || host === "127.0.0.1");
    var standalone = navigator.standalone === true ||
      (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches);
    var isIOS = /iP(hone|ad|od)/.test(navigator.userAgent) ||
                (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

    // Android, Windows e macOS (Chrome e Edge): o navegador avisa quando o
    // site pode ser instalado e a gente guarda o evento para o botão usar
    var deferredPrompt = null;
    window.addEventListener("beforeinstallprompt", function(e){
      e.preventDefault();
      deferredPrompt = e;
      tools.hidden = false;
      installBtn.hidden = false;
    });
    installBtn.addEventListener("click", function(){
      if(!deferredPrompt) return;
      var p = deferredPrompt;
      deferredPrompt = null;
      installBtn.hidden = true;
      tools.hidden = iosHint.hidden;
      if(p.prompt) p.prompt();
    });
    window.addEventListener("appinstalled", function(){
      deferredPrompt = null;
      installBtn.hidden = true;
      tools.hidden = true;
    });

    // iPhone e iPad não têm botão de instalar: só o caminho pelo Compartilhar
    if(isIOS && !standalone && location.protocol !== "file:"){
      tools.hidden = false;
      iosHint.hidden = false;
    }

    var waiting = null, reloading = false;
    function showUpdate(worker){
      waiting = worker || null;
      updateBar.hidden = false;
    }
    updateBtn.addEventListener("click", function(){
      updateBtn.disabled = true;
      reloading = true;
      if(waiting) waiting.postMessage("SKIP_WAITING");
      else location.reload();
    });
    laterBtn.addEventListener("click", function(){ updateBar.hidden = true; });

    // gancho usado pelo smoke test, que roda em file:// e não tem service worker
    window.__toeflPwa = { canRegister: canRegister, showUpdate: showUpdate };

    if(!canRegister) return;
    // só recarrega quando foi o aluno que pediu: na primeira instalação o
    // service worker também assume o controle, e ali não há o que recarregar
    navigator.serviceWorker.addEventListener("controllerchange", function(){
      if(reloading) location.reload();
    });
    window.addEventListener("load", function(){
      navigator.serviceWorker.register("sw.js").then(function(reg){
        // já havia versão nova esperando de uma visita anterior
        if(reg.waiting && navigator.serviceWorker.controller) showUpdate(reg.waiting);
        reg.addEventListener("updatefound", function(){
          var fresh = reg.installing;
          if(!fresh) return;
          fresh.addEventListener("statechange", function(){
            if(fresh.state === "installed" && navigator.serviceWorker.controller) showUpdate(fresh);
          });
        });
        // o navegador só procura versão nova ao abrir a página. App instalado
        // fica aberto por dias: confere de novo quando a janela volta ao
        // primeiro plano, no máximo uma vez por hora.
        var lastCheck = Date.now();
        document.addEventListener("visibilitychange", function(){
          if(document.visibilityState !== "visible" || Date.now() - lastCheck < 3600000) return;
          lastCheck = Date.now();
          reg.update().catch(function(){});
        });
      }).catch(function(){}); // sem service worker o site funciona igual, só não fica offline
    });
  })();

  // ponte para o app/redacao.js, que o build cola depois deste arquivo e
  // precisa do armazenamento, da conta e da navegação daqui
  window.__toeflApp = {
    safeGet: safeGet,
    safeSet: safeSet,
    client: function(){ return supaClient; },
    uid: function(){ return supaUid; },
    // conta grátis: a redação abre a tela de planos em vez do envio
    isFree: isFree,
    openPlans: function(){ openPlans(FREE_REASON.essay); },
    // abre o módulo na Parte n (prioridade de estudo da devolutiva)
    openPart: function(mod, n){
      navTo(mod);
      var panel = document.querySelector('.panel[data-panel="' + mod + '"]');
      var card = panel && panel.querySelectorAll(".section-card")[n - 1];
      var showPart = window.__toeflShowPart && window.__toeflShowPart[mod];
      if(card && showPart) showPart(card, { noScroll: true });
      if(card) setTimeout(function(){ card.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60);
    }
  };
})();
