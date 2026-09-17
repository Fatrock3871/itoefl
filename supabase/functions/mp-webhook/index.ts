// Recebe a notificação do Mercado Pago depois de um pagamento e libera o
// acesso do aluno, gravando em `entitlements`. Endpoint público (o Mercado
// Pago não manda nenhum header de autenticação) -- a segurança vem de
// SEMPRE reconferir o pagamento direto na API do MP com o access token
// secreto, nunca confiar só no que a notificação em si diz.
//
// Configurar em "notification_url" na criação da preferência (já feito em
// create-checkout/index.ts) -- não precisa cadastrar nada manualmente no
// painel do Mercado Pago.
//
// Segredos necessários (configurar com `supabase secrets set`):
//   MP_ACCESS_TOKEN
// (SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY já existem automaticamente.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const MP_ACCESS_TOKEN = Deno.env.get("MP_ACCESS_TOKEN")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

Deno.serve(async (req) => {
  try {
    const url = new URL(req.url);
    const paymentId = url.searchParams.get("data.id") || url.searchParams.get("id");
    const type = url.searchParams.get("type") || url.searchParams.get("topic");

    // o MP manda vários tipos de notificação (merchant_order, etc.) -- só
    // nos interessa "payment"; qualquer outra coisa é confirmada com 200
    // pra ele parar de reenviar, sem fazer nada
    if (type !== "payment" || !paymentId) {
      return new Response("ok", { status: 200 });
    }

    const payRes = await fetch(`https://api.mercadopago.com/v1/payments/${paymentId}`, {
      headers: { Authorization: `Bearer ${MP_ACCESS_TOKEN}` },
    });
    if (!payRes.ok) {
      return new Response("erro ao consultar pagamento no Mercado Pago", { status: 502 });
    }
    const payment = await payRes.json();

    if (payment.status === "approved" && payment.external_reference) {
      const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
      const { error } = await supabase.from("entitlements").upsert({
        user_id: payment.external_reference,
        paid: true,
        paid_at: new Date().toISOString(),
        mp_payment_id: String(payment.id),
        updated_at: new Date().toISOString(),
      });
      if (error) {
        return new Response("erro ao gravar entitlement: " + error.message, { status: 500 });
      }
    }

    return new Response("ok", { status: 200 });
  } catch (e) {
    return new Response(String(e), { status: 500 });
  }
});
