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

// Preço cobrado de verdade. Mudar aqui exige mudar também o texto do botão
// em app/build.py (pay_gate).
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
    let couponCode = "";
    try {
      const body = await req.json();
      if (typeof body?.origin === "string" && body.origin.startsWith("http")) origin = body.origin;
      if (typeof body?.coupon === "string") couponCode = body.coupon.trim();
    } catch { /* corpo vazio é aceitável */ }

    let finalPrice = PRICE_BRL;
    let itemTitle = PRODUCT_TITLE;
    if (couponCode) {
      const { data: coupon, error: couponErr } = await supabase
        .from("coupons")
        .select("percent, active")
        .ilike("code", couponCode)
        .maybeSingle();
      if (couponErr || !coupon || !coupon.active) {
        return new Response(JSON.stringify({ error: "Cupom inválido ou expirado." }), {
          status: 400,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
        });
      }
      finalPrice = Math.round(PRICE_BRL * (1 - coupon.percent / 100) * 100) / 100;
      itemTitle = `${PRODUCT_TITLE} (cupom -${coupon.percent}%)`;
    }

    const preferenceBody: Record<string, unknown> = {
      items: [{ title: itemTitle, quantity: 1, unit_price: finalPrice, currency_id: "BRL" }],
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
      return new Response(JSON.stringify({ error: "Não foi possível abrir o pagamento agora. Tente de novo em alguns minutos." }), {
        status: 502,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ url: pref.init_point, sandboxUrl: pref.sandbox_init_point }), {
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("create-checkout falhou:", e);
    return new Response(JSON.stringify({ error: "Erro inesperado ao abrir o pagamento. Tente de novo." }), {
      status: 500,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
});
