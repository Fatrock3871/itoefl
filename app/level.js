// Do resultado do diagnóstico (M0) para a banda CEFR e o cronograma indicado.
// Arquivo separado porque duas páginas usam a mesma conta: o app (app.js) e a
// tela de apresentação (landing.js), onde o diagnóstico é aberto sem conta. O
// build.py cola este arquivo antes de cada um dos dois.
//
// Mesma tabela % -> banda do Módulo 0, Parte 4.2. Mudou lá, mudar aqui.
var ToeflLevel = {
  band: function(pct){
    // meia banda com vírgula, como na calculadora e no texto do módulo
    if(pct <= 20) return {code:"1–1,5", label:"A1", low:1, desc:"fundamentos ausentes"};
    if(pct <= 40) return {code:"2–2,5", label:"A2", low:2, desc:"fundamentos parciais"};
    if(pct <= 55) return {code:"3–3,5", label:"B1", low:3, desc:"base funcional, muitos gaps de precisão"};
    if(pct <= 70) return {code:"4–4,5", label:"B2", low:4, desc:"consistência intermediária-avançada"};
    if(pct <= 85) return {code:"5–5,5", label:"C1", low:5, desc:"alta consistência, poucos erros sistemáticos"};
    return {code:"6", label:"C2", low:6, desc:"domínio quase completo"};
  },
  schedule: function(pct){
    if(pct <= 55) return "Cronograma Completo (90 dias) · Módulo 0, Parte 6.3";
    if(pct <= 70) return "Cronograma Regular (60 dias) · Módulo 0, Parte 6.2";
    return "Cronograma Intensivo (30 dias) · Módulo 0, Parte 6.1";
  },

  // Concordância oficial da ETS entre as bandas e a escala 0 a 120 (M0, Parte
  // 2.3): o menor valor de cada banda. O maior é o menor da banda seguinte - 1.
  SCALE: [
    {band:1, cefr:"A1", min:0}, {band:1.5, cefr:"A1", min:12}, {band:2, cefr:"A2", min:24},
    {band:2.5, cefr:"A2", min:34}, {band:3, cefr:"B1", min:44}, {band:3.5, cefr:"B1", min:58},
    {band:4, cefr:"B2", min:72}, {band:4.5, cefr:"B2", min:86}, {band:5, cefr:"C1", min:95},
    {band:5.5, cefr:"C1", min:107}, {band:6, cefr:"C2", min:114}
  ],
  fmt: function(n){ return String(n).replace(".", ","); },
  // "4,5 (B2): 86 a 94 na escala de 0 a 120"
  scaleLabel: function(i){
    var s = ToeflLevel.SCALE[i], next = ToeflLevel.SCALE[i + 1];
    return ToeflLevel.fmt(s.band) + " (" + s.cefr + "): " + s.min + " a " + (next ? next.min - 1 : 120) + " na escala de 0 a 120";
  },
  cefrOf: function(band){
    var hit = ToeflLevel.SCALE.filter(function(s){ return s.band === band; })[0];
    return hit ? hit.cefr : "";
  },

  // Os três cronogramas do M0, Parte 6
  PLANS: {
    30: {days:30, name:"Intensivo", part:"6.1"},
    60: {days:60, name:"Regular", part:"6.2"},
    90: {days:90, name:"Completo", part:"6.3"}
  },
  // Cronograma indicado, pelas regras da Parte 6: Completo para quem parte
  // de B1 ou abaixo; Intensivo para quem já está perto da meta (até 1 banda,
  // como B2 alto para C1); Regular para os outros. Sem meta informada, vale a
  // régua do schedule() acima. Se a prova chega antes do fim do cronograma,
  // fica o maior que cabe; com menos de 30 dias, o Intensivo com o Plano de
  // Emergência (Parte 7).
  // Devolve {days, name, part, gap, reason, squeezed, emergency}.
  recommend: function(pct, target, daysLeft){
    var lvl = ToeflLevel.band(pct), gap = target ? target - lvl.low : null, days;
    if(pct <= 55) days = 90;
    else if(gap === null) days = pct <= 70 ? 60 : 30;
    else days = gap <= 1 ? 30 : 60;
    var reason = pct <= 55 ? "você parte de " + lvl.label + ", e a base vem antes da estratégia"
      : gap === null ? "é o indicado para o seu nível de partida"
      : gap <= 0 ? "você já está na faixa da meta: o trabalho é afiar e manter"
      : gap <= 1 ? "você já está perto da meta"
      : "a distância até a meta pede um ritmo constante";
    var squeezed = false, emergency = false;
    if(typeof daysLeft === "number" && daysLeft < days){
      squeezed = true;
      days = daysLeft >= 90 ? 90 : daysLeft >= 60 ? 60 : 30;
      emergency = daysLeft < 30;
    }
    var p = ToeflLevel.PLANS[days];
    return {days:days, name:p.name, part:p.part, gap:gap, reason:reason, squeezed:squeezed, emergency:emergency};
  }
};
