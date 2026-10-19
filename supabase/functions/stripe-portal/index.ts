// Abre o Customer Portal do Stripe para o aluno autenticado: é onde ele
// cancela a assinatura Mensal em 1 clique, troca o cartão e vê as faturas.
// O que pode ser feito lá (cancelar no fim do período, trocar cartão) é
// configurado pelo dono no painel do Stripe (docs/publicar.md).
//
// O cliente do Stripe sai da tabela `billing`, lida com o token do próprio
// aluno (a RLS só deixa ver a própria linha): ninguém abre o portal de outro.
//
// Segredos: STRIPE_SECRET_KEY e SITE_URL (`supabase secrets set`).

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { PUBLISHABLE_KEY } from "../_shared/keys.ts";
import { stripeConfigured, stripeRequest } from "../_shared/stripe_api.ts";

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
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS_HEADERS });
  if (req.method !== "POST") return json({ error: "Método não permitido." }, 405);

  try {
    const supabase = createClient(SUPABASE_URL, PUBLISHABLE_KEY, {
      global: { headers: { Authorization: req.headers.get("Authorization") || "" } },
    });
    const { data: { user }, error: userErr } = await supabase.auth.getUser();
    if (userErr || !user) return json({ error: "Não autenticado." }, 401);
    if (!stripeConfigured()) return json({ error: "O pagamento com cartão ainda não está disponível." }, 503);

    let origin = "";
    try {
      const body = await req.json();
      if (typeof body?.origin === "string" && /^https?:\/\/[^/\s?#]+$/.test(body.origin)) origin = body.origin;
    } catch { /* sem corpo: usa o SITE_URL */ }
    const siteUrl = (Deno.env.get("SITE_URL") || "").trim().replace(/\/+$/, "");
    if (siteUrl) origin = siteUrl;
    if (!origin) return json({ error: "Endereço do site ausente." }, 400);

    const { data: bill, error: billErr } = await supabase
      .from("billing")
      .select("stripe_customer_id")
      .eq("user_id", user.id)
      .maybeSingle();
    if (billErr || !bill?.stripe_customer_id) {
      return json({ error: "Esta conta não tem pagamento no cartão para gerenciar." }, 404);
    }

    const session = await stripeRequest("POST", "/v1/billing_portal/sessions", {
      customer: bill.stripe_customer_id,
      return_url: `${origin}/?portal=1`,
      locale: "pt-BR",
    });
    return json({ url: session.url });
  } catch (e) {
    console.error("stripe-portal falhou:", String(e));
    return json({ error: "Não foi possível abrir o gerenciamento agora. Tente de novo em alguns minutos." }, 502);
  }
});
