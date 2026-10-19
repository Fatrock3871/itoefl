// Lógica do Stripe que não depende de rede nem de banco (2026-10-18).
//
// A edge function stripe-webhook importa daqui e passa as dependências de
// verdade (API do Stripe, funções do banco). O smoke test carrega este mesmo
// arquivo num navegador, sem a palavra "export", e passa dependências de
// mentira: é assim que a verificação de assinatura e o fluxo de cada evento
// são testados sem conta no Stripe. Por isso: JavaScript puro, sem import,
// sem tipo de TypeScript, e todo nome começa com "stripe".
//
// Regra de segurança: o corpo do evento só serve para saber QUAL objeto
// mudou. O estado (pago? de quem? até quando?) é sempre lido de novo da API
// do Stripe, com a versão de API fixa abaixo. Assim o código não depende da
// versão escolhida no painel para o endpoint, e um aviso antigo ou repetido
// sempre grava o estado atual.

// Versão da API pedida em toda chamada (cabeçalho Stripe-Version). Nela a
// fatura ainda traz `subscription` e `payment_intent`, a cobrança traz
// `invoice` e a assinatura traz `current_period_end`.
export var STRIPE_API_VERSION = "2024-06-20";

// Diferença máxima, em segundos, entre o carimbo da assinatura e o relógio
// do servidor. É o padrão das bibliotecas do Stripe.
export var STRIPE_SIG_TOLERANCE = 300;

// Os eventos tratados. Os mesmos que o dono marca no painel do Stripe.
export var STRIPE_EVENTS = [
  "checkout.session.completed",
  "invoice.paid",
  "invoice.payment_failed",
  "customer.subscription.updated",
  "customer.subscription.deleted",
  "charge.refunded"
];

// situações da assinatura em que ela ainda cobra ou vai cobrar
export var STRIPE_LIVE_STATUSES = ["active", "trialing", "past_due", "unpaid", "incomplete"];

var STRIPE_UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function stripeHex(buf) {
  return Array.prototype.map.call(new Uint8Array(buf), function (b) {
    return ("0" + b.toString(16)).slice(-2);
  }).join("");
}

// comparação que não para no primeiro caractere diferente
function stripeSameText(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// Confere o cabeçalho Stripe-Signature ("t=<segundos>,v1=<hmac>[,v1=...]"):
// HMAC-SHA256 de "<t>.<corpo cru>" com o segredo do endpoint (whsec_...).
// Devolve true ou false; nunca lança erro por entrada ruim.
export async function stripeVerifySignature(payload, header, secret, nowSec) {
  if (typeof payload !== "string" || typeof header !== "string" || typeof secret !== "string" || !secret) return false;
  var t = null, v1 = [];
  header.split(",").forEach(function (part) {
    var i = part.indexOf("=");
    if (i < 0) return;
    var k = part.slice(0, i).trim(), v = part.slice(i + 1).trim();
    if (k === "t") t = v;
    else if (k === "v1") v1.push(v);
  });
  if (!t || !/^\d+$/.test(t) || !v1.length) return false;
  var now = typeof nowSec === "number" ? nowSec : Math.floor(Date.now() / 1000);
  if (Math.abs(now - Number(t)) > STRIPE_SIG_TOLERANCE) return false;
  var enc = new TextEncoder();
  var key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  var expected = stripeHex(await crypto.subtle.sign("HMAC", key, enc.encode(t + "." + payload)));
  return v1.some(function (s) { return stripeSameText(s, expected); });
}

// campo que o Stripe devolve como id ("cus_...") ou como objeto expandido
function stripeId(v) {
  if (typeof v === "string") return v;
  return v && typeof v.id === "string" ? v.id : null;
}

function stripeUser(v) {
  return typeof v === "string" && STRIPE_UUID_RE.test(v) ? v.toLowerCase() : null;
}

function stripeIso(sec) {
  return typeof sec === "number" && sec > 0 ? new Date(sec * 1000).toISOString() : null;
}

function stripeMoney(cents) {
  return typeof cents === "number" ? cents / 100 : null;
}

// deps (o que a edge function, ou o teste, fornece):
//   get(path)                 objeto da API do Stripe (GET com a versão fixa)
//   cancelSubscription(id)    cancela já (sem reembolso automático)
//   applyPayment(args)        rpc apply_payment: { id, user, plan, days, amount, status, approvedAt, periodEnd }
//   applyBilling(args)        rpc apply_billing: { user, customer, subscription, status, cancelAtPeriodEnd, periodEnd, at }
//   findBilling(user)         linha de billing da conta, ou null
//   plan(id)                  plano de ./plans.ts ({ id, interval, days }), ou null
//   now()                     data ISO de agora
// Devolve a lista do que foi feito, em texto (vai para o log da function).
export async function stripeHandleEvent(event, deps) {
  var obj = event && event.data && event.data.object;
  var id = obj && typeof obj.id === "string" ? encodeURIComponent(obj.id) : null;
  if (!id) return ["evento sem objeto: ignorado"];
  var at = stripeIso(event.created) || deps.now();
  switch (event.type) {
    case "checkout.session.completed":
      return stripeOnCheckout(await deps.get("/v1/checkout/sessions/" + id), at, deps);
    case "invoice.paid":
      return stripeOnInvoice(await deps.get("/v1/invoices/" + id), at, deps, null, null);
    case "invoice.payment_failed": {
      var inv = await deps.get("/v1/invoices/" + id);
      var subId = stripeId(inv.subscription);
      if (!subId) return ["fatura avulsa recusada: ignorada"];
      return stripeOnSubscription(await deps.get("/v1/subscriptions/" + encodeURIComponent(subId)), deps, null);
    }
    case "customer.subscription.updated":
    case "customer.subscription.deleted":
      return stripeOnSubscription(await deps.get("/v1/subscriptions/" + id), deps, null);
    case "charge.refunded":
      return stripeOnRefund(await deps.get("/v1/charges/" + id), deps);
    default:
      return ["evento não tratado: " + event.type];
  }
}

// Checkout concluído. Plano de dias (mode=payment): o pagamento está
// confirmado aqui mesmo e os dias somam ao fim do acesso atual. Mensal
// (mode=subscription): grava a assinatura e a 1ª fatura, sem esperar o
// invoice.paid (que também chega e não muda nada).
async function stripeOnCheckout(session, at, deps) {
  var user = stripeUser(session.client_reference_id) || stripeUser(session.metadata && session.metadata.user_id);
  if (!user) return ["checkout " + session.id + " sem id de usuário válido: nada gravado"];
  var customer = stripeId(session.customer);
  var done = [];

  if (session.mode === "payment") {
    if (session.payment_status !== "paid") return ["checkout " + session.id + " ainda sem pagamento confirmado"];
    var plan = deps.plan(session.metadata && session.metadata.plan_id);
    if (!plan || plan.interval || !(plan.days > 0)) return ["checkout " + session.id + " de pagamento único sem plano de dias: nada gravado"];
    var pi = stripeId(session.payment_intent);
    if (!pi) return ["checkout " + session.id + " sem payment_intent: nada gravado"];
    if (customer) {
      await deps.applyBilling({ user: user, customer: customer, subscription: null, status: null,
                                cancelAtPeriodEnd: null, periodEnd: null, at: deps.now() });
    }
    await deps.applyPayment({ id: "stripe:" + pi, user: user, plan: plan.id, days: plan.days,
                              amount: stripeMoney(session.amount_total), status: "approved",
                              approvedAt: at, periodEnd: null });
    return ["plano " + plan.id + " gravado: stripe:" + pi + " (" + plan.days + " dias)"];
  }

  if (session.mode === "subscription") {
    var subId = stripeId(session.subscription);
    if (!subId) return ["checkout " + session.id + " de assinatura sem assinatura: nada gravado"];
    var sub = await deps.get("/v1/subscriptions/" + encodeURIComponent(subId));
    done = done.concat(await stripeOnSubscription(sub, deps, user));
    var invId = stripeId(sub.latest_invoice);
    if (invId) {
      var inv = await deps.get("/v1/invoices/" + encodeURIComponent(invId));
      done = done.concat(await stripeOnInvoice(inv, at, deps, sub, user));
    }
    return done;
  }
  return ["checkout " + session.id + " em modo " + session.mode + ": ignorado"];
}

// Fatura paga da assinatura: os dias do período pago (28 a 31), somados ao
// fim do acesso que a conta ainda tem (regra 7 da migração do Stripe).
async function stripeOnInvoice(inv, at, deps, sub, fallbackUser) {
  if (inv.status !== "paid") return ["fatura " + inv.id + " em " + inv.status + ": nada gravado"];
  var subId = stripeId(inv.subscription);
  if (!subId) return ["fatura " + inv.id + " sem assinatura: ignorada"];
  if (!sub) sub = await deps.get("/v1/subscriptions/" + encodeURIComponent(subId));
  var meta = sub.metadata || {};
  var user = stripeUser(meta.user_id) || fallbackUser;
  if (!user) return ["fatura " + inv.id + ": assinatura " + subId + " sem id de usuário: nada gravado"];
  var plan = deps.plan(meta.plan_id);
  if (!plan || plan.interval !== "month") return ["fatura " + inv.id + ": assinatura sem plano mensal: nada gravado"];

  // período pago: a linha da fatura que termina mais tarde; se a fatura não
  // trouxer, o período atual da assinatura
  var periodStart = 0, periodEnd = 0;
  ((inv.lines && inv.lines.data) || []).forEach(function (line) {
    var p = (line && line.period) || {};
    if (typeof p.end === "number" && typeof p.start === "number" && p.end > periodEnd) {
      periodEnd = p.end;
      periodStart = p.start;
    }
  });
  if (!periodEnd) {
    periodStart = sub.current_period_start;
    periodEnd = sub.current_period_end;
  }
  var periodIso = stripeIso(periodEnd);
  if (!periodIso || !(periodStart > 0) || periodEnd <= periodStart) {
    return ["fatura " + inv.id + " sem período válido: nada gravado"];
  }
  var days = Math.max(1, Math.round((periodEnd - periodStart) / 86400));

  var paidAt = stripeIso(inv.status_transitions && inv.status_transitions.paid_at) || at;
  await deps.applyPayment({ id: "stripe:" + inv.id, user: user, plan: plan.id, days: days,
                            amount: stripeMoney(inv.amount_paid), status: "approved",
                            approvedAt: paidAt, periodEnd: periodIso });
  return ["mês gravado: stripe:" + inv.id + " (" + days + " dias, período até " + periodIso + ")"];
}

// Situação da assinatura (ativa, atrasada, cancelada, cancelamento marcado
// para o fim do mês). Não mexe no acesso: só na linha de billing.
async function stripeOnSubscription(sub, deps, fallbackUser) {
  var user = stripeUser(sub.metadata && sub.metadata.user_id) || fallbackUser;
  if (!user) return ["assinatura " + sub.id + " sem id de usuário: nada gravado"];
  // aviso atrasado de uma assinatura velha, já encerrada, não apaga a nova
  var current = await deps.findBilling(user);
  if (current && current.subscription_id && current.subscription_id !== sub.id &&
      STRIPE_LIVE_STATUSES.indexOf(current.subscription_status) !== -1 &&
      STRIPE_LIVE_STATUSES.indexOf(sub.status) === -1) {
    return ["assinatura antiga " + sub.id + " (" + sub.status + "): a atual " + current.subscription_id + " foi mantida"];
  }
  await deps.applyBilling({ user: user, customer: stripeId(sub.customer), subscription: sub.id, status: sub.status,
                            cancelAtPeriodEnd: !!sub.cancel_at_period_end,
                            periodEnd: stripeIso(sub.current_period_end), at: deps.now() });
  return ["assinatura " + sub.id + ": " + sub.status + (sub.cancel_at_period_end ? " (cancela no fim do período)" : "")];
}

// Reembolso. Só o total tira o acesso (o parcial é um acerto de valor). Se a
// cobrança era de uma fatura da assinatura, a assinatura também é cancelada:
// quem pede o dinheiro de volta não quer ser cobrado no mês seguinte.
async function stripeOnRefund(charge, deps) {
  if (!charge.refunded) return ["reembolso parcial de " + charge.id + ": acesso mantido"];
  var invId = stripeId(charge.invoice), pi = stripeId(charge.payment_intent);
  var done = [];
  var ids = [];
  if (invId) ids.push("stripe:" + invId);
  if (pi) ids.push("stripe:" + pi);
  for (var i = 0; i < ids.length; i++) {
    // reembolso de pagamento que não está no extrato não faz nada (apply_payment)
    await deps.applyPayment({ id: ids[i], user: null, plan: null, days: null, amount: null,
                              status: "refunded", approvedAt: null, periodEnd: null });
    done.push("reembolso gravado: " + ids[i]);
  }
  if (invId) {
    var inv = await deps.get("/v1/invoices/" + encodeURIComponent(invId));
    var subId = stripeId(inv.subscription);
    if (subId) {
      var sub = await deps.get("/v1/subscriptions/" + encodeURIComponent(subId));
      if (STRIPE_LIVE_STATUSES.indexOf(sub.status) !== -1) {
        await deps.cancelSubscription(subId);
        done.push("assinatura " + subId + " cancelada (mês reembolsado)");
      }
    }
  }
  return done.length ? done : ["reembolso de " + charge.id + " sem pagamento ligado: nada a desfazer"];
}
