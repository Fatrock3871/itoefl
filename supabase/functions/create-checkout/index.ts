// Cria uma preferência de checkout no Mercado Pago (Checkout Pro) para o
// aluno autenticado que escolheu um plano na tela de compra do site. Devolve
// a URL de pagamento; quem libera o acesso de verdade é o mp-webhook, depois
// que o Mercado Pago confirma o pagamento.
//
// O navegador manda só o ID do plano (e o cupom, se houver). O preço sai de
// ../_shared/plans.ts, aqui no servidor: valor que chegue no corpo da
// requisição é ignorado.
//
// Segredos necessários (configurar com `supabase secrets set`, nunca aqui):
//   MP_ACCESS_TOKEN — Access Token de produção da sua conta Mercado Pago
// (SUPABASE_URL e a chave pública já existem automaticamente no ambiente de
// toda edge function do projeto; ver ../_shared/keys.ts.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { buildReference, findPlan } from "../_shared/plans.ts";
import { PUBLISHABLE_KEY } from "../_shared/keys.ts";

const MP_ACCESS_TOKEN = Deno.env.get("MP_ACCESS_TOKEN")!;
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
    try {
      const body = await req.json();
      if (typeof body?.origin === "string" && body.origin.startsWith("http")) origin = body.origin;
      if (typeof body?.coupon === "string") couponCode = body.coupon.trim();
      planId = body?.plan;
    } catch { /* corpo vazio cai na recusa de plano abaixo */ }
    // Com SITE_URL definido (secret do Supabase), o retorno do pagamento vai
    // sempre para o site oficial e ignora o que o navegador mandou.
    const siteUrl = (Deno.env.get("SITE_URL") || "").trim().replace(/\/+$/, "");
    if (siteUrl) origin = siteUrl;

    const plan = findPlan(planId);
    if (!plan) {
      return json({ error: "Escolha um dos planos para continuar." }, 400);
    }

    // quem já tem acesso sem prazo não tem o que ganhar com outra compra:
    // recusa antes de cobrar. A leitura usa o token do próprio aluno (a RLS
    // de entitlements só deixa ver a própria linha). Se a consulta falhar
    // (por exemplo, coluna expires_at ainda não criada), segue a compra.
    const { data: ent, error: entErr } = await supabase
      .from("entitlements")
      .select("paid, expires_at")
      .eq("user_id", user.id)
      .maybeSingle();
    if (!entErr && ent && ent.paid && !ent.expires_at) {
      return json({ error: "Esta conta já tem acesso vitalício. Não é preciso comprar de novo." }, 409);
    }

    let priceCents = plan.priceCents;
    const access = plan.days ? `${plan.days} dias de acesso` : "acesso vitalício";
    let itemTitle = `iTOEFL: plano ${plan.name} (${access})`;
    if (couponCode) {
      const { data: coupon, error: couponErr } = await supabase
        .from("coupons")
        .select("percent, active")
        .ilike("code", couponCode)
        .maybeSingle();
      if (couponErr || !coupon || !coupon.active) {
        return json({ error: "Cupom inválido ou expirado." }, 400);
      }
      // o cupom é um percentual sobre o preço do plano escolhido
      priceCents = Math.round(plan.priceCents * (100 - coupon.percent) / 100);
      itemTitle = `${itemTitle}, cupom de ${coupon.percent}%`;
    }

    const preferenceBody: Record<string, unknown> = {
      items: [{ id: plan.id, title: itemTitle, quantity: 1, unit_price: priceCents / 100, currency_id: "BRL" }],
      // o mp-webhook lê isto de volta para saber de quem é o pagamento e
      // qual plano foi comprado
      external_reference: buildReference(user.id, plan.id),
      metadata: { user_id: user.id, plan_id: plan.id },
      notification_url: `${SUPABASE_URL}/functions/v1/mp-webhook`,
    };
    if (user.email) preferenceBody.payer = { email: user.email };
    if (origin) {
      preferenceBody.back_urls = {
        success: `${origin}?mp=success`,
        failure: `${origin}?mp=failure`,
        pending: `${origin}?mp=pending`,
      };
      // auto_return exige que success/failure/pending sejam URLs https
      // "de verdade" (não localhost) -- em produção, com o site publicado
      // num domínio https, dá pra religar isso pra voltar sozinho depois
      // do pagamento em vez de precisar clicar num botão na tela do MP.
      if (origin.startsWith("https://")) preferenceBody.auto_return = "approved";
    }

    const prefRes = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${MP_ACCESS_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(preferenceBody),
    });
    const pref = await prefRes.json();
    if (!prefRes.ok) {
      // o motivo real fica só no log da function (Dashboard > Edge
      // Functions > create-checkout > Logs); o aluno vê uma mensagem
      // genérica, sem detalhe interno do Mercado Pago.
      console.error("Mercado Pago recusou a preferência:", prefRes.status, JSON.stringify(pref));
      return json({ error: "Não foi possível abrir o pagamento agora. Tente de novo em alguns minutos." }, 502);
    }

    return json({ url: pref.init_point, sandboxUrl: pref.sandbox_init_point, plan: plan.id });
  } catch (e) {
    console.error("create-checkout falhou:", e);
    return json({ error: "Erro inesperado ao abrir o pagamento. Tente de novo." }, 500);
  }
});
