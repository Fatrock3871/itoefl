// Abre o pagamento do plano escolhido pelo aluno autenticado e devolve a URL
// da página de pagamento. Quem libera o acesso de verdade é o webhook
// (stripe-webhook ou mp-webhook), depois que o pagamento é confirmado.
//
//   cartão (padrão)  Stripe Checkout. Mensal: mode=subscription, cobrança
//                    todo mês até cancelar. 60 dias, 90 dias e Anual:
//                    mode=payment, pagamento único sem renovação.
//   pix              Mercado Pago (Checkout Pro só com Pix), só nos planos de
//                    pagamento único, enquanto pix_mercado_pago for true em
//                    ../_shared/plans.json.
//
// O navegador manda só o id do plano, o meio (card ou pix) e o cupom. O preço
// sai de ../_shared/plans.json: valor que chegue no corpo é ignorado. O id do
// aluno vai em client_reference_id e nos metadados da sessão, da assinatura e
// do pagamento, que é de onde o stripe-webhook o lê de volta.
//
// Segredos (configurar com `supabase secrets set`, nunca aqui):
//   STRIPE_SECRET_KEY  chave secreta do Stripe (sk_test_... no modo de teste)
//   MP_ACCESS_TOKEN    Access Token do Mercado Pago (só para o Pix)
//   SITE_URL           endereço do site; a volta do pagamento vai sempre para ele
// (SUPABASE_URL e a chave pública já existem no ambiente; ver ../_shared/keys.ts.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { buildReference, findPlan, PIX_VIA_MERCADO_PAGO, type Plan } from "../_shared/plans.ts";
import { PUBLISHABLE_KEY } from "../_shared/keys.ts";
import { BRAND } from "../_shared/brand.ts";
import { STRIPE_LIVE_STATUSES } from "../_shared/stripe.js";
import { StripeError, stripeConfigured, stripeRequest } from "../_shared/stripe_api.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

function productName(plan: Plan) {
  return plan.interval ? `${BRAND}: plano ${plan.name} (assinatura mensal)` : `${BRAND}: plano ${plan.name} (${plan.days} dias de acesso)`;
}

// Cupom do site (tabela coupons, um percentual) como cupom do Stripe de uso
// único: no Mensal o desconto vale só para o primeiro mês. O id é fixo por
// percentual, então o mesmo cupom do Stripe é reaproveitado.
async function stripeCouponFor(percent: number): Promise<string> {
  const id = `itoefl-${percent}-primeira-cobranca`;
  try {
    await stripeRequest("GET", `/v1/coupons/${id}`);
    return id;
  } catch (e) {
    if (!(e instanceof StripeError) || e.status !== 404) throw e;
  }
  await stripeRequest("POST", "/v1/coupons", {
    id,
    percent_off: percent,
    duration: "once",
    name: `Cupom de ${percent}% na primeira cobrança`,
  }, id);
  return id;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: CORS_HEADERS });
  }

  try {
    const authHeader = req.headers.get("Authorization") || "";
    const supabase = createClient(SUPABASE_URL, PUBLISHABLE_KEY, {
      global: { headers: { Authorization: authHeader } },
    });
    const { data: { user }, error: userErr } = await supabase.auth.getUser();
    if (userErr || !user) {
      return json({ error: "Não autenticado." }, 401);
    }

    let origin = "";
    let couponCode = "";
    let planId: unknown = "";
    let method = "card";
    try {
      const body = await req.json();
      if (typeof body?.origin === "string" && /^https?:\/\/[^/\s?#]+$/.test(body.origin)) origin = body.origin;
      if (typeof body?.coupon === "string") couponCode = body.coupon.trim();
      if (body?.method === "pix") method = "pix";
      planId = body?.plan;
    } catch { /* corpo vazio cai na recusa de plano abaixo */ }
    // Com SITE_URL definido (secret do Supabase), a volta do pagamento vai
    // sempre para o site oficial e ignora o que o navegador mandou.
    const siteUrl = (Deno.env.get("SITE_URL") || "").trim().replace(/\/+$/, "");
    if (siteUrl) origin = siteUrl;

    const plan = findPlan(planId);
    if (!plan) {
      return json({ error: "Escolha um dos planos para continuar." }, 400);
    }
    if (method === "pix" && (plan.interval || !PIX_VIA_MERCADO_PAGO)) {
      return json({ error: "O Pix é aceito só nos planos de 60 dias, 90 dias e Anual. O Mensal é cobrado no cartão." }, 400);
    }

    // conta com acesso sem prazo (compra antiga, Premium ou legado) não tem
    // o que ganhar com outra compra: recusa antes de cobrar. A leitura usa o
    // token do próprio aluno (a RLS só deixa ver a própria linha). Se a
    // consulta falhar, segue a compra. Quem tem prazo correndo pode comprar:
    // os dias somam ao fim do acesso atual.
    const { data: ent, error: entErr } = await supabase
      .from("entitlements")
      .select("paid, expires_at")
      .eq("user_id", user.id)
      .maybeSingle();
    if (!entErr && ent && ent.paid && !ent.expires_at) {
      return json({ error: "Esta conta já tem acesso sem prazo. Não é preciso comprar de novo." }, 409);
    }

    let percent = 0;
    if (couponCode) {
      const { data: coupon, error: couponErr } = await supabase
        .from("coupons")
        .select("percent, active")
        .ilike("code", couponCode)
        .maybeSingle();
      if (couponErr || !coupon || !coupon.active) {
        return json({ error: "Cupom inválido ou expirado." }, 400);
      }
      percent = coupon.percent;
    }

    if (method === "pix") return await mercadoPagoPix(user, plan, percent, origin);

    // ---------- cartão: Stripe Checkout ----------
    if (!stripeConfigured()) {
      console.error("create-checkout: STRIPE_SECRET_KEY ausente");
      return json({ error: "O pagamento com cartão ainda não está disponível. Tente de novo mais tarde." }, 503);
    }
    if (!origin) {
      return json({ error: "Endereço do site ausente para a volta do pagamento." }, 400);
    }

    const { data: bill } = await supabase
      .from("billing")
      .select("stripe_customer_id, subscription_status")
      .eq("user_id", user.id)
      .maybeSingle();
    if (plan.interval && bill && STRIPE_LIVE_STATUSES.includes(bill.subscription_status)) {
      return json({
        error: "Esta conta já tem a assinatura Mensal. Para trocar o cartão ou cancelar, use Gerenciar ou cancelar a assinatura, em Minha conta.",
      }, 409);
    }

    const meta = { user_id: user.id, plan_id: plan.id };
    const params: Record<string, string | number | boolean | undefined> = {
      mode: plan.interval ? "subscription" : "payment",
      client_reference_id: user.id,
      "metadata[user_id]": meta.user_id,
      "metadata[plan_id]": meta.plan_id,
      locale: "pt-BR",
      "payment_method_types[0]": "card",
      "line_items[0][quantity]": 1,
      "line_items[0][price_data][currency]": "brl",
      "line_items[0][price_data][unit_amount]": plan.priceCents,
      "line_items[0][price_data][product_data][name]": productName(plan),
      success_url: `${origin}/?pay=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/?pay=cancel`,
    };
    if (plan.interval) {
      params["line_items[0][price_data][recurring][interval]"] = plan.interval;
      params["subscription_data[metadata][user_id]"] = meta.user_id;
      params["subscription_data[metadata][plan_id]"] = meta.plan_id;
    } else {
      params["payment_intent_data[metadata][user_id]"] = meta.user_id;
      params["payment_intent_data[metadata][plan_id]"] = meta.plan_id;
    }
    if (bill?.stripe_customer_id) {
      params.customer = bill.stripe_customer_id;
    } else {
      if (user.email) params.customer_email = user.email;
      if (!plan.interval) params.customer_creation = "always";
    }
    if (percent > 0) params["discounts[0][coupon]"] = await stripeCouponFor(percent);

    const session = await stripeRequest("POST", "/v1/checkout/sessions", params);
    return json({ url: session.url, plan: plan.id });
  } catch (e) {
    // o motivo real fica só no log da function; o aluno vê mensagem genérica
    console.error("create-checkout falhou:", String(e));
    return json({ error: "Não foi possível abrir o pagamento agora. Tente de novo em alguns minutos." }, 502);
  }
});

// ---------- Pix: Mercado Pago, só planos de pagamento único ----------
async function mercadoPagoPix(user: { id: string; email?: string }, plan: Plan, percent: number, origin: string) {
  const token = (Deno.env.get("MP_ACCESS_TOKEN") || "").trim();
  if (!token) {
    console.error("create-checkout: MP_ACCESS_TOKEN ausente");
    return json({ error: "O Pix ainda não está disponível. Use o cartão ou tente mais tarde." }, 503);
  }
  const priceCents = Math.round(plan.priceCents * (100 - percent) / 100);
  const title = `${BRAND}: plano ${plan.name} (${plan.days} dias de acesso)` + (percent ? `, cupom de ${percent}%` : "");
  const preferenceBody: Record<string, unknown> = {
    items: [{ id: plan.id, title, quantity: 1, unit_price: priceCents / 100, currency_id: "BRL" }],
    // o mp-webhook lê isto de volta para saber de quem é o pagamento
    external_reference: buildReference(user.id, plan.id),
    metadata: { user_id: user.id, plan_id: plan.id },
    notification_url: `${SUPABASE_URL}/functions/v1/mp-webhook`,
    // só Pix: cartão é pelo Stripe
    payment_methods: {
      excluded_payment_types: [{ id: "credit_card" }, { id: "debit_card" }, { id: "ticket" }, { id: "prepaid_card" }],
    },
  };
  if (user.email) preferenceBody.payer = { email: user.email };
  if (origin) {
    preferenceBody.back_urls = {
      success: `${origin}/?mp=success`,
      failure: `${origin}/?mp=failure`,
      pending: `${origin}/?mp=pending`,
    };
    // auto_return exige URL https de verdade (não localhost)
    if (origin.startsWith("https://")) preferenceBody.auto_return = "approved";
  }
  const prefRes = await fetch("https://api.mercadopago.com/checkout/preferences", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(preferenceBody),
  });
  const pref = await prefRes.json();
  if (!prefRes.ok) {
    console.error("Mercado Pago recusou a preferência:", prefRes.status, JSON.stringify(pref));
    return json({ error: "Não foi possível abrir o Pix agora. Tente de novo em alguns minutos." }, 502);
  }
  return json({ url: pref.init_point, plan: plan.id });
}
