// Do resultado do diagnóstico (M0) para a banda CEFR e o cronograma indicado.
// Arquivo separado porque duas páginas usam a mesma conta: o app (app.js) e a
// tela de apresentação (landing.js), onde o diagnóstico é aberto sem conta. O
// build.py cola este arquivo antes de cada um dos dois.
//
// Mesma tabela % -> banda do Módulo 0, Parte 4.2. Mudou lá, mudar aqui.
var ToeflLevel = {
  band: function(pct){
    // meia banda com vírgula, como na calculadora e no texto do módulo
    if(pct <= 20) return {code:"1–1,5", label:"A1", desc:"fundamentos ausentes"};
    if(pct <= 40) return {code:"2–2,5", label:"A2", desc:"fundamentos parciais"};
    if(pct <= 55) return {code:"3–3,5", label:"B1", desc:"base funcional, muitos gaps de precisão"};
    if(pct <= 70) return {code:"4–4,5", label:"B2", desc:"consistência intermediária-avançada"};
    if(pct <= 85) return {code:"5–5,5", label:"C1", desc:"alta consistência, poucos erros sistemáticos"};
    return {code:"6", label:"C2", desc:"domínio quase completo"};
  },
  schedule: function(pct){
    if(pct <= 55) return "Cronograma Completo (90 dias) · Módulo 0, Parte 6.3";
    if(pct <= 70) return "Cronograma Regular (60 dias) · Módulo 0, Parte 6.2";
    return "Cronograma Intensivo (30 dias) · Módulo 0, Parte 6.1";
  }
};
