// Regras do envio de redação para correção (decisões do dono, 2026-10-13).
//
// Um arquivo só para o servidor e para o site:
//   - as edge functions submit-essay e review-essay importam daqui;
//   - o app/build.py cola este arquivo no site, tirando a palavra "export".
// Por isso: JavaScript puro, sem import, sem tipo de TypeScript, e todo nome
// começa com "redacao" (no site ele vira global).
//
// Mudou uma regra aqui, mudam juntos o servidor (depois do deploy) e o site
// (depois do build). O smoke test confere que app/redacao_data.py e os
// textos das regras batem com estes números.

export var REDACAO_REGRAS = {
  intervaloDias: 4,          // 1 envio a cada 4 dias, contados do último envio
  prazoDiasUteis: 3,         // devolução em até 3 dias úteis
  minutos: { email: 7, discussion: 10 },
  minPalavras: { email: 1, discussion: 100 },
  maxPalavras: 600,
  maxCaracteres: 5000,
  // id do tema -> tarefa. Os textos dos temas estão em app/redacao_data.py
  temas: {
    E1: "email", E2: "email", E3: "email", E4: "email", E5: "email",
    D1: "discussion", D2: "discussion", D3: "discussion", D4: "discussion", D5: "discussion"
  },
  criterios: ["cumprimento", "organizacao", "gramatica", "vocabulario"],
  maxTrechos: 5,
  codigos: ["W1", "W2", "W3", "W4", "W5", "W6"],
  // quantas Partes tem cada módulo que a prioridade de estudo pode indicar
  partes: { M4: 7, M5: 10 }
};

var REDACAO_DIA_MS = 86400000;
// Horário de Brasília: UTC-3 o ano todo (o horário de verão acabou em 2019).
var REDACAO_FUSO_MS = 3 * 3600000;

// ---------- palavras ----------

export function redacaoContaPalavras(texto) {
  var t = String(texto || "").trim();
  return t ? t.split(/\s+/).length : 0;
}

// ---------- dias úteis ----------

function redacaoIso(d) {
  var m = d.getUTCMonth() + 1, dia = d.getUTCDate();
  return d.getUTCFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (dia < 10 ? "0" : "") + dia;
}

// Domingo de Páscoa (algoritmo de Meeus/Jones/Butcher), meia-noite UTC
export function redacaoPascoa(ano) {
  var a = ano % 19, b = Math.floor(ano / 100), c = ano % 100;
  var d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25);
  var g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30;
  var i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7;
  var m = Math.floor((a + 11 * h + 22 * l) / 451);
  var mes = Math.floor((h + l - 7 * m + 114) / 31), dia = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(Date.UTC(ano, mes - 1, dia));
}

// Dias sem expediente no Brasil, por ano: os feriados nacionais fixos e os
// móveis, que dependem da Páscoa. Carnaval e Corpus Christi são ponto
// facultativo na lei federal, mas quase ninguém trabalha: entram na lista,
// o que só dá mais prazo à equipe, nunca menos.
var REDACAO_FERIADOS_FIXOS = [
  ["01-01", "Confraternização Universal"],
  ["04-21", "Tiradentes"],
  ["05-01", "Dia do Trabalho"],
  ["09-07", "Independência"],
  ["10-12", "Nossa Senhora Aparecida"],
  ["11-02", "Finados"],
  ["11-15", "Proclamação da República"],
  ["11-20", "Dia Nacional de Zumbi e da Consciência Negra"],
  ["12-25", "Natal"]
];
var REDACAO_FERIADOS_MOVEIS = [  // dias contados a partir do domingo de Páscoa
  [-48, "Carnaval (segunda)"],
  [-47, "Carnaval (terça)"],
  [-2, "Sexta-feira Santa"],
  [60, "Corpus Christi"]
];

export function redacaoFeriados(ano) {
  var out = {};
  REDACAO_FERIADOS_FIXOS.forEach(function (f) { out[ano + "-" + f[0]] = f[1]; });
  var pascoa = redacaoPascoa(ano).getTime();
  REDACAO_FERIADOS_MOVEIS.forEach(function (f) {
    out[redacaoIso(new Date(pascoa + f[0] * REDACAO_DIA_MS))] = f[1];
  });
  return out;
}

function redacaoDiaUtil(d) {
  var semana = d.getUTCDay();
  if (semana === 0 || semana === 6) return false;
  return !redacaoFeriados(d.getUTCFullYear())[redacaoIso(d)];
}

// Data prevista da devolutiva ("AAAA-MM-DD"): o 3º dia útil depois do dia do
// envio, no horário de Brasília. Mandar na sexta às 23h conta igual a mandar
// na sexta de manhã: o prazo começa na segunda.
export function redacaoPrevisao(enviadaMs) {
  var local = new Date(enviadaMs - REDACAO_FUSO_MS);
  var d = new Date(Date.UTC(local.getUTCFullYear(), local.getUTCMonth(), local.getUTCDate()));
  var contados = 0;
  while (contados < REDACAO_REGRAS.prazoDiasUteis) {
    d = new Date(d.getTime() + REDACAO_DIA_MS);
    if (redacaoDiaUtil(d)) contados++;
  }
  return redacaoIso(d);
}

// "Hoje" no horário de Brasília, como "AAAA-MM-DD"
export function redacaoHoje(agoraMs) {
  return redacaoIso(new Date(agoraMs - REDACAO_FUSO_MS));
}

// ---------- 1 envio a cada 4 dias ----------

// historico: envios do aluno, cada um com submitted_at (data ISO).
// Devolve { bloqueado, liberaEm } com liberaEm em milissegundos (ou null).
export function redacaoBloqueio(historico, agoraMs) {
  var ultimo = null;
  (historico || []).forEach(function (h) {
    var t = new Date(h && h.submitted_at).getTime();
    if (!isNaN(t) && (ultimo === null || t > ultimo)) ultimo = t;
  });
  if (ultimo === null) return { bloqueado: false, liberaEm: null };
  var libera = ultimo + REDACAO_REGRAS.intervaloDias * REDACAO_DIA_MS;
  return { bloqueado: agoraMs < libera, liberaEm: libera };
}

// ---------- nota ----------

// Média dos 4 critérios arredondada para o meio ponto mais próximo (empate
// sobe: 3,25 vira 3,5). Trava: com Cumprimento da tarefa em 2 ou menos, a
// nota final não passa de 2,5.
export function redacaoNotaFinal(notas) {
  var soma = 0;
  REDACAO_REGRAS.criterios.forEach(function (c) { soma += Number(notas[c]); });
  var final = Math.round((soma / REDACAO_REGRAS.criterios.length) * 2) / 2;
  if (Number(notas.cumprimento) <= 2 && final > 2.5) final = 2.5;
  return final;
}

export function redacaoNivel(nota) {
  if (nota >= 5) return "C1/C2 (banda 5,5 a 6)";
  if (nota >= 4) return "B2 alto/C1 (banda 4,5 a 5)";
  if (nota >= 3) return "B2 (banda 4)";
  if (nota >= 2) return "B1 (banda 3 a 3,5)";
  if (nota >= 1) return "A2 (banda 2 a 2,5)";
  return "A1 ou sem resposta";
}

// ---------- formato da devolutiva ----------

var REDACAO_MAX_TEXTO = 1500;

// Confere o JSON da devolutiva (o que a IA devolve e o corretor revisa).
// Devolve { ok, erros: [frases em português] }. Campo a mais também é erro:
// o formato é exato.
export function redacaoValidaDevolutiva(d) {
  var erros = [];
  function texto(v, onde, obrigatorio) {
    if (typeof v !== "string") { erros.push(onde + ": tem de ser um texto entre aspas."); return; }
    if (obrigatorio && !v.trim()) erros.push(onde + ": está vazio.");
    if (v.length > REDACAO_MAX_TEXTO) erros.push(onde + ": passa de " + REDACAO_MAX_TEXTO + " caracteres.");
  }
  function objeto(v, onde) {
    if (!v || typeof v !== "object" || Array.isArray(v)) { erros.push(onde + ": tem de ser um objeto { }."); return false; }
    return true;
  }
  function soCampos(v, campos, onde) {
    Object.keys(v).forEach(function (k) {
      if (campos.indexOf(k) === -1) erros.push(onde + ': campo inesperado "' + k + '".');
    });
    campos.forEach(function (k) {
      if (!(k in v)) erros.push(onde + ': falta o campo "' + k + '".');
    });
  }

  if (!objeto(d, "A devolutiva")) return { ok: false, erros: erros };
  var topo = ["criterios", "trechos", "reescrita", "prioridade"];
  Object.keys(d).forEach(function (k) {
    if (topo.indexOf(k) !== -1) return;
    var dica = /final|nivel|nível|level/i.test(k) ? " A nota final e o nível são calculados pelo site." : "";
    erros.push('campo inesperado "' + k + '".' + dica);
  });
  topo.forEach(function (k) { if (!(k in d)) erros.push('falta o campo "' + k + '".'); });

  if ("criterios" in d && objeto(d.criterios, "criterios")) {
    soCampos(d.criterios, REDACAO_REGRAS.criterios, "criterios");
    REDACAO_REGRAS.criterios.forEach(function (c) {
      var onde = "criterios." + c;
      var v = d.criterios[c];
      if (!(c in d.criterios) || !objeto(v, onde)) return;
      soCampos(v, ["nota", "justificativa"], onde);
      if ("nota" in v) {
        var n = v.nota;
        if (typeof n !== "number" || !isFinite(n) || n < 0 || n > 5 || Math.round(n * 2) !== n * 2) {
          erros.push(onde + ".nota: tem de ser um número de 0 a 5, em passos de 0.5 (veio " + JSON.stringify(n) + ").");
        }
      }
      if ("justificativa" in v) texto(v.justificativa, onde + ".justificativa", true);
    });
  }

  if ("trechos" in d) {
    if (!Array.isArray(d.trechos)) {
      erros.push("trechos: tem de ser uma lista [ ].");
    } else {
      if (d.trechos.length > REDACAO_REGRAS.maxTrechos) {
        erros.push("trechos: no máximo " + REDACAO_REGRAS.maxTrechos + " (vieram " + d.trechos.length + ").");
      }
      d.trechos.forEach(function (t, i) {
        var onde = "trechos[" + (i + 1) + "]";
        if (!objeto(t, onde)) return;
        soCampos(t, ["original", "correcao", "explicacao", "codigo"], onde);
        ["original", "correcao", "explicacao"].forEach(function (k) {
          if (k in t) texto(t[k], onde + "." + k, true);
        });
        if ("codigo" in t && t.codigo !== null && REDACAO_REGRAS.codigos.indexOf(t.codigo) === -1) {
          erros.push(onde + ".codigo: use W1 a W6, ou null (veio " + JSON.stringify(t.codigo) + ").");
        }
      });
    }
  }

  if ("reescrita" in d && objeto(d.reescrita, "reescrita")) {
    soCampos(d.reescrita, ["original", "versao"], "reescrita");
    if ("original" in d.reescrita) texto(d.reescrita.original, "reescrita.original", true);
    if ("versao" in d.reescrita) texto(d.reescrita.versao, "reescrita.versao", true);
  }

  if ("prioridade" in d && objeto(d.prioridade, "prioridade")) {
    var p = d.prioridade;
    soCampos(p, ["texto", "modulo", "parte"], "prioridade");
    if ("texto" in p) texto(p.texto, "prioridade.texto", true);
    var total = REDACAO_REGRAS.partes[p.modulo];
    if ("modulo" in p && !total) erros.push('prioridade.modulo: use "M4" ou "M5" (veio ' + JSON.stringify(p.modulo) + ").");
    if ("parte" in p && total && (typeof p.parte !== "number" || Math.floor(p.parte) !== p.parte || p.parte < 1 || p.parte > total)) {
      erros.push("prioridade.parte: o " + p.modulo + " tem as Partes 1 a " + total + " (veio " + JSON.stringify(p.parte) + ").");
    }
  }

  return { ok: erros.length === 0, erros: erros };
}
