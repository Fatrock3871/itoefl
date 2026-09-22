// Cria uma preferência de checkout no Mercado Pago (Checkout Pro) para o
// aluno autenticado que clicou em "Comprar acesso" na tela de paywall do
// site. Devolve a URL de pagamento; quem libera o acesso de verdade é o
// mp-webhook, depois que o Mercado Pago confirma o pagamento.
//
// Segredos necessários (configurar com `supabase secrets set`, nunca aqui):
//   MP_ACCESS_TOKEN — Access Token de produção da sua conta Mercado Pago
// (SUPABASE_URL e SUPABASE_ANON_KEY já existem automaticamente no ambiente
// de toda edge function do projeto — não precisa configurar.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const MP_ACCESS_TOKEN = Deno.env.get("MP_ACCESS_TOKEN")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;

// TODO: ajuste o preço e o título antes de publicar de verdade.
const PRICE_BRL = 9.9;
const PRODUCT_TITLE = "iTOEFL — Acesso vitalício à plataforma";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: CORS_HEADERS });
  }

  try {
    const authHeader = req.headers.get("Authorization") || "";
    const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
      global: { headers: { Authorization: authHeader } },
    });
    const { data: { user }, error: userErr } = await supabase.auth.getUser();
    if (userErr || !user) {
      return new Response(JSON.stringify({ error: "Não autenticado." }), {
        status: 401,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      });
    }

    let origin = "";
    try {
      const body = await req.json();
      if (typeof body?.origin === "string" && body.origin.startsWith("http")) origin = body.origin;
    } catch { /* corpo vazio é aceitável */ }

    const preferenceBody: Record<string, unknown> = {
      items: [{ title: PRODUCT_TITLE, quantity: 1, unit_price: PRICE_BRL, currency_id: "BRL" }],
      external_reference: user.id,
      notification_url: `${SUPABASE_URL}/functions/v1/mp-webhook`,
    };
    if (user.email) preferenceBody.payer = { email: user.email };
    if (origin) {
      preferenceBody.back_urls = {
        success: `${origin}?mp=success`,
        failure: `${origin}?mp=failure`,
        pending: `${origin}?mp=pending`,
      };
      preferenceBody.auto_return = "approved";
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
      // TEMP: manda o corpo INTEIRO que o Mercado Pago devolveu direto na
      // resposta (em vez de só "message") -- os logs do lado do servidor
      // não estavam mostrando nada útil, então a forma mais rápida de ver
      // o motivo real é aqui, na aba Network do navegador. Tirar depois de
      // resolver, não é algo que faça sentido mostrar pro aluno.
      return new Response(JSON.stringify({ error: "Erro ao criar checkout.", mpStatus: prefRes.status, mpBody: pref }), {
        status: 502,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ url: pref.init_point, sandboxUrl: pref.sandbox_init_point }), {
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
});
