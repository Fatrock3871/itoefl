// ---------- Redação para correção (Etapa 3, versão assistida) ----------
// Tela do aluno: escolha do tema, regras antes de começar, escrita com
// cronômetro sem pausa, confirmação do envio, histórico com devolutiva e
// gráfico. O build cola este arquivo depois do app.js; as regras (prazo,
// intervalo, nota, validação) vêm de supabase/functions/_shared/redacao.js,
// colado antes, e são as mesmas que o servidor usa. O que se confere aqui é
// só para avisar mais cedo: quem decide é a edge function submit-essay.
(function(){
  "use strict";
  var APP = window.__toeflApp;
  var modal = document.getElementById("essayModal");
  var dataEl = document.getElementById("essayData");
  if(!modal || !APP || !dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);
  var R = REDACAO_REGRAS;
  var TOPICS = {};
  DATA.topics.forEach(function(t){ TOPICS[t.id] = t; });
  var CRIT_NAME = {};
  DATA.rubrica.forEach(function(c){ CRIT_NAME[c.id] = c.nome; });
  var MOD_KEY = { M4: "mod4", M5: "mod5" };

  // rascunho em andamento: só neste aparelho (não sincroniza). Guarda a hora
  // em que o cronômetro começou, então fechar a janela não pausa nada.
  var LS_DRAFT = "toefl_essaydraft_v1";
  // ids das devolutivas que o aluno já abriu (sincroniza com a conta)
  var LS_SEEN = "toefl_essay_seen_v1";
  var DAY = 86400000, BRT = 3 * 3600000;

  var state = { online: false, history: null, reviewer: false };
  var draft = null, timer = null, discardArmed = null;

  function $(id){ return document.getElementById(id); }
  function el(tag, cls, text){
    var n = document.createElement(tag);
    if(cls) n.className = cls;
    if(text != null) n.textContent = text;
    return n;
  }
  // datas no horário de Brasília
  function brt(ms){ return new Date(ms - BRT); }
  function two(n){ return (n < 10 ? "0" : "") + n; }
  function fmtDM(ms){ var d = brt(ms); return two(d.getUTCDate()) + "/" + two(d.getUTCMonth() + 1); }
  function fmtDMH(ms){ var d = brt(ms); return fmtDM(ms) + ", às " + two(d.getUTCHours()) + ":" + two(d.getUTCMinutes()); }
  function fmtIso(iso){ var p = String(iso || "").split("-"); return p.length === 3 ? p[2] + "/" + p[1] : ""; }
  function fmtScore(n){ return String(Number(n)).replace(".", ","); }
  function topicLabel(id){ var t = TOPICS[id]; return id + " · " + (t ? t.titulo : ""); }
  function limitMs(task){ return R.minutos[task] * 60000; }

  var VIEWS = ["essayHome", "essayBrief", "essayWrite", "essayConfirm", "essayDone", "essayFeedback"];
  function show(view){
    VIEWS.forEach(function(id){ $(id).hidden = id !== view; });
    var card = modal.querySelector(".essay-card");
    if(card) card.scrollTop = 0;
  }

  // ---------- bloqueio de 4 dias ----------
  function block(){ return redacaoBloqueio(state.history || [], Date.now()); }
  function blockText(b){ return "Próximo envio liberado em " + fmtDMH(b.liberaEm) + "."; }

  // ---------- rascunho ----------
  function loadDraft(){
    try { var d = JSON.parse(APP.safeGet(LS_DRAFT) || "null"); return d && TOPICS[d.topic] ? d : null; }
    catch(e){ return null; }
  }
  function saveDraft(){ APP.safeSet(LS_DRAFT, draft ? JSON.stringify(draft) : ""); }
  function clearDraft(){
    draft = null;
    saveDraft();
    if(timer){ clearInterval(timer); timer = null; }
  }

  // ---------- início ----------
  function renderHome(){
    var status = $("essayStatus"), b = block();
    if(!state.online){
      status.textContent = "O envio de redações exige estar conectado à sua conta com o plano em dia. Você já pode ler os temas e as regras.";
    } else if(state.history === null){
      status.textContent = "Carregando as suas redações...";
    } else if(b.bloqueado){
      status.textContent = blockText(b) + " Enquanto isso, leia as devolutivas e os temas.";
    } else {
      status.textContent = "Você pode enviar uma redação agora. Escolha um tema.";
    }
    renderHistory();
    renderChart();
  }

  function seenIds(){
    try { return JSON.parse(APP.safeGet(LS_SEEN) || "[]") || []; } catch(e){ return []; }
  }
  function unseen(){
    var seen = seenIds();
    return (state.history || []).filter(function(r){ return r.status === "devolvida" && seen.indexOf(r.id) === -1; });
  }
  function markSeen(id){
    var seen = seenIds();
    if(seen.indexOf(id) === -1){ seen.push(id); APP.safeSet(LS_SEEN, JSON.stringify(seen)); }
    updateBadge();
  }
  // selo em Minha conta (e um ponto na engrenagem) quando há devolutiva nova
  function updateBadge(){
    var n = unseen().length;
    var badge = $("accountEssayBadge");
    if(badge){
      badge.hidden = n === 0;
      badge.textContent = n === 1 ? "1 devolutiva nova" : n + " devolutivas novas";
    }
    var gear = $("accountBtn");
    if(gear){
      var dot = $("essayDot");
      if(!dot){
        dot = el("span", "essay-dot");
        dot.id = "essayDot";
        dot.setAttribute("aria-hidden", "true");
        gear.appendChild(dot);
      }
      dot.hidden = n === 0;
      gear.setAttribute("aria-label", n ? "Minha conta (" + badge.textContent + ")" : "Minha conta");
    }
  }

  var STATUS_NAME = { na_fila: "Na fila", em_correcao: "Em correção", devolvida: "Devolvida" };
  function renderHistory(){
    var box = $("essayHistory");
    box.textContent = "";
    var rows = state.history || [];
    if(!rows.length){
      box.appendChild(el("p", "essay-empty", state.history === null && state.online ? "Carregando..." : "Nenhuma redação enviada ainda."));
      return;
    }
    var seen = seenIds();
    rows.forEach(function(r){
      var item = el("div", "essay-item");
      var head = el("p", "essay-item-head");
      head.appendChild(el("b", null, topicLabel(r.topic_id)));
      var chip = el("span", "essay-chip is-" + r.status, STATUS_NAME[r.status] || r.status);
      head.appendChild(chip);
      if(r.status === "devolvida" && seen.indexOf(r.id) === -1) head.appendChild(el("span", "essay-chip is-new", "nova"));
      item.appendChild(head);
      var when = "Enviada em " + fmtDM(new Date(r.submitted_at).getTime());
      when += r.status === "devolvida" && r.returned_at ? " · devolvida em " + fmtDM(new Date(r.returned_at).getTime())
                                                        : " · devolutiva prevista para " + fmtIso(r.due_on);
      item.appendChild(el("p", "essay-item-meta", when));
      if(r.status === "devolvida"){
        item.appendChild(el("p", "essay-item-score", "Nota " + fmtScore(r.final_score) + " de 5 · " + r.level));
        var btn = el("button", "essay-secondary essay-see", "Ver devolutiva");
        btn.type = "button";
        btn.addEventListener("click", function(){ openFeedback(r); });
        item.appendChild(btn);
      }
      box.appendChild(item);
    });
  }

  // gráfico de evolução: uma série (nota final de cada devolutiva, na ordem
  // do envio), linha de 2 px, pontos com dica, grade discreta. A lista acima
  // é a versão em tabela dos mesmos números.
  var SVG = "http://www.w3.org/2000/svg";
  function svg(tag, attrs){
    var n = document.createElementNS(SVG, tag);
    Object.keys(attrs).forEach(function(k){ n.setAttribute(k, attrs[k]); });
    return n;
  }
  function renderChart(){
    var box = $("essayChart");
    box.textContent = "";
    var pts = (state.history || []).filter(function(r){ return r.status === "devolvida"; })
      .sort(function(a, b){ return new Date(a.submitted_at) - new Date(b.submitted_at); });
    box.hidden = pts.length === 0;
    if(!pts.length) return;
    box.appendChild(el("p", "essay-chart-title", "Evolução da nota final (0 a 5)"));
    var W = 320, H = 150, L = 26, Rt = 12, T = 10, B = 26;
    var g = svg("svg", { viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Nota final das redações devolvidas, da mais antiga para a mais nova" });
    function y(v){ return T + (5 - v) * (H - T - B) / 5; }
    function x(i){ return pts.length === 1 ? (L + W - Rt) / 2 : L + i * (W - L - Rt) / (pts.length - 1); }
    for(var v = 0; v <= 5; v++){
      g.appendChild(svg("line", { x1: L, x2: W - Rt, y1: y(v), y2: y(v), "class": "essay-grid" }));
      var lab = svg("text", { x: L - 8, y: y(v) + 3.5, "text-anchor": "end", "class": "essay-axis" });
      lab.textContent = v;
      g.appendChild(lab);
    }
    if(pts.length > 1){
      g.appendChild(svg("polyline", { points: pts.map(function(r, i){ return x(i) + "," + y(Number(r.final_score)); }).join(" "), "class": "essay-line" }));
    }
    pts.forEach(function(r, i){
      var when = fmtDM(new Date(r.submitted_at).getTime());
      var hit = svg("circle", { cx: x(i), cy: y(Number(r.final_score)), r: 11, "class": "essay-hit" });
      var dot = svg("circle", { cx: x(i), cy: y(Number(r.final_score)), r: 4, "class": "essay-point" });
      var tip = svg("title", {});
      tip.textContent = when + " · " + r.topic_id + " · nota " + fmtScore(r.final_score);
      hit.appendChild(tip);
      g.appendChild(dot);
      g.appendChild(hit);
      if(i === 0 || i === pts.length - 1){
        var d = svg("text", { x: x(i), y: H - 8, "text-anchor": "middle", "class": "essay-axis" });
        d.textContent = when;
        g.appendChild(d);
      }
    });
    box.appendChild(g);
    if(pts.length === 1) box.appendChild(el("p", "essay-chart-note", "A linha aparece a partir da segunda devolutiva."));
  }

  // ---------- antes de começar ----------
  var briefTopic = null;
  function openBrief(id){
    var t = TOPICS[id];
    briefTopic = id;
    $("essayBriefKicker").textContent = id + " · " + (t.task === "email" ? "Write an Email" : "Write for an Academic Discussion") +
      " · " + R.minutos[t.task] + " minutos";
    $("essayBriefTitle").textContent = t.titulo;
    $("essayBriefGoal").textContent = t.objetivo;
    var b = block();
    $("essayBriefBlock").hidden = !b.bloqueado;
    $("essayBriefBlock").textContent = b.bloqueado ? blockText(b) + " Você pode ler o tema, mas só começa a escrever quando o envio liberar." : "";
    $("essayStart").disabled = b.bloqueado;
    show("essayBrief");
  }

  // ---------- escrita ----------
  function words(){ return redacaoContaPalavras($("essayText").value); }
  function renderCount(){
    var n = words(), task = TOPICS[draft.topic].task, min = R.minPalavras[task];
    $("essayCount").textContent = n + (n === 1 ? " palavra" : " palavras");
    var goal = $("essayGoal");
    goal.hidden = task !== "discussion";
    goal.textContent = "mínimo " + min + " palavras";
    goal.classList.toggle("is-met", n >= min);
  }
  function fmtClock(sec){ return two(Math.floor(sec / 60)) + ":" + two(sec % 60); }
  function deadline(){ return draft.startedAt + limitMs(TOPICS[draft.topic].task); }
  function isLocked(){ return !!draft && !!draft.lockedAt; }

  function lock(byTime){
    if(!draft) return;
    if(!draft.lockedAt) draft.lockedAt = Math.min(Date.now(), deadline());
    if(byTime) draft.timeUp = true;
    saveDraft();
    $("essayText").readOnly = true;
    $("essayBox").classList.remove("is-running");
    $("essayBox").classList.toggle("is-over", !!draft.timeUp);
    $("essayLocked").hidden = !draft.timeUp;
  }
  function tick(){
    if(!draft) return;
    var left = Math.max(0, Math.ceil((deadline() - Date.now()) / 1000));
    $("essayClock").textContent = fmtClock(left);
    if(left <= 0){
      if(timer){ clearInterval(timer); timer = null; }
      lock(true);
    }
  }
  function enterWrite(){
    var id = draft.topic;
    Array.prototype.forEach.call(modal.querySelectorAll(".essay-prompt"), function(p){ p.hidden = p.dataset.topic !== id; });
    var area = $("essayText");
    area.value = draft.text || "";
    if(timer){ clearInterval(timer); timer = null; }
    if(!draft.timeUp){
      // voltar ao texto destrava; o prazo continua o mesmo (startedAt)
      draft.lockedAt = null;
      saveDraft();
      area.readOnly = false;
      $("essayLocked").hidden = true;
      $("essayBox").classList.remove("is-over");
      $("essayBox").classList.add("is-running");
      timer = setInterval(tick, 500);
    }
    renderCount();
    show("essayWrite");
    tick();
    if(draft.timeUp) lock(true);
    else { try { area.focus(); } catch(e){} }
  }
  function start(){
    if(!briefTopic || block().bloqueado) return;
    draft = { topic: briefTopic, startedAt: Date.now(), text: "", lockedAt: null, timeUp: false };
    saveDraft();
    enterWrite();
  }

  // ---------- confirmação ----------
  function secondsUsed(){
    var end = draft.lockedAt || Math.min(Date.now(), deadline());
    return Math.max(0, Math.min(Math.round((end - draft.startedAt) / 1000), R.minutos[TOPICS[draft.topic].task] * 60));
  }
  function needsConsent(){ return !state.history || state.history.length === 0; }
  // motivos que seguram o botão Enviar (vazio = pode enviar)
  function sendBlockers(){
    var out = [], task = TOPICS[draft.topic].task, n = redacaoContaPalavras(draft.text);
    if(n < Math.max(1, R.minPalavras[task])) out.push("min");
    if(n > R.maxPalavras || (draft.text || "").length > R.maxCaracteres) out.push("max");
    if(block().bloqueado) out.push("intervalo");
    if(!state.online) out.push("conta");
    if(needsConsent() && !$("essayConsent").checked) out.push("consentimento");
    return out;
  }
  function renderConfirm(){
    var t = TOPICS[draft.topic], n = redacaoContaPalavras(draft.text), s = secondsUsed();
    $("essaySumTopic").textContent = topicLabel(t.id);
    $("essaySumWords").textContent = n + (n === 1 ? " palavra" : " palavras");
    $("essaySumTime").textContent = Math.floor(s / 60) + " min " + two(s % 60) + " s de " + R.minutos[t.task] + " min";
    $("essaySumDue").textContent = fmtIso(redacaoPrevisao(Date.now())) + " (até " + R.prazoDiasUteis + " dias úteis)";
    $("essaySumNext").textContent = "liberado em " + fmtDMH(Date.now() + R.intervaloDias * DAY);
    $("essayConsentWrap").hidden = !needsConsent();
    $("essayConfirmBack").hidden = !!draft.timeUp;
    var reasons = sendBlockers(), msg = $("essayMinMsg"), texts = [];
    if(reasons.indexOf("min") !== -1){
      var min = Math.max(1, R.minPalavras[t.task]);
      texts.push(t.task === "discussion"
        ? "Faltam " + (min - n) + " palavras para liberar o envio: a discussão pede no mínimo " + min + "."
        : "A redação está vazia.");
    }
    if(reasons.indexOf("max") !== -1) texts.push("A redação passa do tamanho máximo (" + R.maxPalavras + " palavras).");
    if(reasons.indexOf("intervalo") !== -1) texts.push(blockText(block()));
    if(reasons.indexOf("conta") !== -1) texts.push("Para enviar, entre na sua conta com o plano em dia.");
    msg.hidden = !texts.length;
    msg.textContent = texts.join(" ");
    $("essaySend").disabled = reasons.length > 0;
  }
  function openConfirm(){
    lock(false);
    if(timer){ clearInterval(timer); timer = null; }
    $("essaySendMsg").hidden = true;
    renderConfirm();
    show("essayConfirm");
  }

  function sendMsg(text, isErr){
    var m = $("essaySendMsg");
    m.textContent = text;
    m.classList.toggle("is-err", !!isErr);
    m.hidden = false;
  }
  function send(){
    var client = APP.client();
    if(!client || sendBlockers().length) return;
    var btn = $("essaySend");
    btn.disabled = true;
    sendMsg("Enviando...", false);
    var body = { topic: draft.topic, text: draft.text, seconds: secondsUsed(), consent: needsConsent() ? $("essayConsent").checked : false };
    // mesmo cuidado do checkout: manda o token de sessão explicitamente
    client.auth.getSession().then(function(res){
      var token = res && res.data && res.data.session && res.data.session.access_token;
      var opts = { body: body };
      if(token) opts.headers = { Authorization: "Bearer " + token };
      return client.functions.invoke("submit-essay", opts);
    }).then(function(res){
      if(res.error || !res.data || !res.data.id){
        var ctx = res.error && res.error.context;
        (ctx && typeof ctx.json === "function" ? ctx.json().catch(function(){ return null; }) : Promise.resolve(null))
          .then(function(b){
            sendMsg((b && b.error) || "Não deu para enviar agora. Tente de novo em alguns minutos.", true);
            renderConfirm();
          });
        return;
      }
      var row = res.data, label = topicLabel(row.topic_id);
      clearDraft();
      state.history = [row].concat(state.history || []);
      $("essayDoneText").textContent = "Recebemos a sua redação (" + label + "). A devolutiva está prevista para " +
        fmtIso(row.due_on) + " (até " + R.prazoDiasUteis + " dias úteis). Próximo envio liberado em " +
        fmtDMH(new Date(row.next_at).getTime()) + ".";
      show("essayDone");
      loadHistory();
    }).catch(function(){
      sendMsg("Erro de conexão. A redação não foi enviada e continua guardada aqui. Tente de novo.", true);
      renderConfirm();
    });
  }

  // descartar pede um segundo clique, como o "Apagar texto" das caixas do M4
  function armDiscard(btn){
    if(discardArmed !== btn){
      if(discardArmed) discardArmed.textContent = discardArmed.dataset.label;
      btn.dataset.label = btn.dataset.label || btn.textContent;
      btn.textContent = "Clique de novo para descartar";
      discardArmed = btn;
      setTimeout(function(){ if(discardArmed === btn){ btn.textContent = btn.dataset.label; discardArmed = null; } }, 3500);
      return;
    }
    btn.textContent = btn.dataset.label;
    discardArmed = null;
    clearDraft();
    renderHome();
    show("essayHome");
  }

  // ---------- devolutiva ----------
  function section(title){
    var s = el("section", "essay-fb-part");
    s.appendChild(el("h4", "essay-h4", title));
    return s;
  }
  function en(tag, cls, text){ var n = el(tag, cls, text); n.lang = "en"; return n; }
  function openFeedback(r){
    var body = $("essayFeedbackBody"), fb = r.feedback || {};
    body.textContent = "";
    body.appendChild(el("p", "essay-kicker", topicLabel(r.topic_id) + " · enviada em " + fmtDM(new Date(r.submitted_at).getTime())));

    // 1. nota final e nível
    var p1 = section("Nota e nível estimado");
    p1.appendChild(el("p", "essay-fb-score", fmtScore(r.final_score) + " de 5"));
    p1.appendChild(el("p", "essay-fb-level", "Nível estimado: " + r.level));
    p1.appendChild(el("p", "essay-fb-note", "Estimativa de treino, não é a nota oficial da ETS."));
    body.appendChild(p1);

    // 2. critérios
    var p2 = section("Nota de cada critério");
    var list = el("dl", "essay-fb-crit");
    R.criterios.forEach(function(c){
      var item = fb.criterios && fb.criterios[c];
      if(!item) return;
      list.appendChild(el("dt", null, CRIT_NAME[c] + ": " + fmtScore(item.nota) + " de 5"));
      list.appendChild(el("dd", null, item.justificativa));
    });
    p2.appendChild(list);
    body.appendChild(p2);

    // 3. trechos
    var p3 = section("Trechos para corrigir");
    var trechos = fb.trechos || [];
    if(!trechos.length) p3.appendChild(el("p", null, "Nenhum trecho destacado nesta redação."));
    trechos.forEach(function(t){
      var item = el("div", "essay-fb-fix");
      if(t.codigo) item.appendChild(el("span", "essay-chip", t.codigo + " · " + (DATA.codigos[t.codigo] || "")));
      var o = el("p", "essay-fb-was");
      o.appendChild(el("span", "essay-fb-label", "Você escreveu: "));
      o.appendChild(en("s", null, t.original));
      item.appendChild(o);
      var c = el("p", "essay-fb-fixed");
      c.appendChild(el("span", "essay-fb-label", "Correção: "));
      c.appendChild(en("span", null, t.correcao));
      item.appendChild(c);
      item.appendChild(el("p", "essay-fb-why", t.explicacao));
      p3.appendChild(item);
    });
    body.appendChild(p3);

    // 4. reescrita um nível acima
    var p4 = section("Um nível acima");
    if(fb.reescrita){
      var a = el("p");
      a.appendChild(el("span", "essay-fb-label", "Você escreveu: "));
      a.appendChild(en("span", null, fb.reescrita.original));
      p4.appendChild(a);
      var b = el("p");
      b.appendChild(el("span", "essay-fb-label", "Versão um nível acima: "));
      b.appendChild(en("span", null, fb.reescrita.versao));
      p4.appendChild(b);
    }
    body.appendChild(p4);

    // 5. prioridade de estudo, com link para a Parte
    var p5 = section("Prioridade de estudo");
    if(fb.prioridade){
      p5.appendChild(el("p", null, fb.prioridade.texto));
      var parts = DATA.partes[fb.prioridade.modulo] || [];
      var n = fb.prioridade.parte, title = parts[n - 1];
      if(MOD_KEY[fb.prioridade.modulo] && title){
        var go = el("button", "essay-primary", "Abrir " + fb.prioridade.modulo + ", Parte " + n + ": " + title);
        go.type = "button";
        go.addEventListener("click", function(){
          close();
          APP.openPart(MOD_KEY[fb.prioridade.modulo], n);
        });
        p5.appendChild(go);
      }
    }
    body.appendChild(p5);

    if(r.text){
      var mine = el("details", "essay-fb-text");
      mine.appendChild(el("summary", null, "O texto que você enviou"));
      mine.appendChild(en("p", "essay-fb-own", r.text));
      body.appendChild(mine);
    }
    markSeen(r.id);
    show("essayFeedback");
  }

  // ---------- dados da conta ----------
  var HISTORY_COLS = "id, topic_id, task, text, word_count, seconds_used, submitted_at, due_on, status, final_score, level, feedback, returned_at";
  function setHistory(rows){
    state.history = rows || [];
    updateBadge();
    if(!$("essayHome").hidden) renderHome();
    if(!$("essayConfirm").hidden && draft) renderConfirm();
  }
  function loadHistory(){
    var client = APP.client(), uid = APP.uid();
    if(!client || !uid) return;
    client.from("essay_submissions").select(HISTORY_COLS).eq("user_id", uid).order("submitted_at", { ascending: false })
      .then(function(res){
        // banco sem a migração de redações: segue sem histórico, sem quebrar
        if(res.error){ console.error("Redações:", res.error.message); setHistory([]); return; }
        setHistory(res.data);
      });
  }
  window.__toeflEssayOnline = function(){
    state.online = true;
    loadHistory();
    if(window.__toeflReviewerCheck) window.__toeflReviewerCheck();
  };
  window.__toeflEssayOffline = function(){
    state.online = false;
    state.history = null;
    updateBadge();
    if(window.__toeflReviewerReset) window.__toeflReviewerReset();
  };

  // ---------- abrir e fechar ----------
  function open(){
    modal.hidden = false;
    document.body.classList.add("menu-open");
    draft = loadDraft();
    if(draft){
      // redação em andamento: volta direto para ela, com o tempo que sobrou.
      // Quem já tinha terminado volta para a confirmação.
      if(draft.lockedAt && !draft.timeUp) openConfirm();
      else enterWrite();
      return;
    }
    renderHome();
    show("essayHome");
  }
  function close(){
    modal.hidden = true;
    document.body.classList.remove("menu-open");
  }

  Array.prototype.forEach.call(document.querySelectorAll(".essay-open"), function(b){ b.addEventListener("click", open); });
  var accBtn = $("accountEssay");
  if(accBtn) accBtn.addEventListener("click", function(){ var c = $("accountClose"); if(c) c.click(); open(); });
  $("essayClose").addEventListener("click", close);
  $("essayBackdrop").addEventListener("click", close);
  document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !modal.hidden) close(); });
  Array.prototype.forEach.call(modal.querySelectorAll(".essay-topic"), function(b){
    b.addEventListener("click", function(){ openBrief(b.dataset.topic); });
  });
  $("essayBriefBack").addEventListener("click", function(){ renderHome(); show("essayHome"); });
  $("essayStart").addEventListener("click", start);
  $("essayText").addEventListener("input", function(){
    if(!draft || isLocked()) return;
    draft.text = $("essayText").value;
    saveDraft();
    renderCount();
  });
  $("essayFinish").addEventListener("click", openConfirm);
  $("essayConfirmBack").addEventListener("click", function(){
    if(!draft || draft.timeUp) return;
    enterWrite();
  });
  $("essayDiscard").addEventListener("click", function(){ armDiscard($("essayDiscard")); });
  $("essayConfirmDiscard").addEventListener("click", function(){ armDiscard($("essayConfirmDiscard")); });
  $("essayConsent").addEventListener("change", renderConfirm);
  $("essaySend").addEventListener("click", send);
  $("essayDoneBack").addEventListener("click", function(){ renderHome(); show("essayHome"); });
  $("essayFeedbackBack").addEventListener("click", function(){ renderHome(); show("essayHome"); });

  // ganchos do smoke test
  window.__toeflEssay = {
    open: open, close: close, tick: tick, setHistory: setHistory, sendBlockers: sendBlockers,
    draft: function(){ return draft; }, state: function(){ return state; }
  };
})();
