// Recebe a notificação do Mercado Pago depois de um pagamento e libera o
// acesso do aluno. Endpoint público (o Mercado Pago não manda nenhum header
// de autenticação) -- a segurança vem de SEMPRE reconferir o pagamento direto
// na API do MP com o access token secreto, nunca confiar só no que a
// notificação em si diz.
//
// O que grava: uma linha em `payments` (o extrato) e, a partir dela, o prazo
// em `entitlements`. As duas coisas acontecem dentro da função de banco
// apply_payment(), numa transação só. A regra de renovação, troca de plano e
// reembolso está escrita em supabase/migrations/20261008_planos.sql.
//
// Configurar em "notification_url" na criação da preferência (já feito em
// create-checkout/index.ts) -- não precisa cadastrar nada manualmente no
// painel do Mercado Pago.
//
// Segredos necessários (configurar com `supabase secrets set`):
//   MP_ACCESS_TOKEN
// (SUPABASE_URL e a chave secreta já existem automaticamente; ver
// ../_shared/keys.ts.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { parseReference } from "../_shared/plans.ts";
import { SECRET_KEY } from "../_shared/keys.ts";

const MP_ACCESS_TOKEN = Deno.env.get("MP_ACCESS_TOKEN")!;
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;

// status do Mercado Pago que tiram o acesso dado por um pagamento. Reembolso
// parcial não entra: o MP mantém o status "approved" nesse caso.
const REVOKING = ["refunded", "charged_back", "cancelled"];

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

    const approved = payment.status === "approved";
    const revoked = REVOKING.includes(payment.status);
    if (!approved && !revoked) {
      // pendente, em análise, recusado: nada a gravar ainda
      return new Response("ok", { status: 200 });
    }

    const ref = parseReference(payment.external_reference);
    if (!ref) {
      // referência fora do formato "<usuário>|<plano>": não dá pra saber o
      // que foi comprado. Responde 200 (reenviar não resolveria) e deixa o
      // caso no log, para ser tratado na mão.
      console.error("mp-webhook: external_reference sem plano reconhecido", payment.id, payment.external_reference);
      return new Response("ok", { status: 200 });
    }

    const supabase = createClient(SUPABASE_URL, SECRET_KEY);
    const { error } = await supabase.rpc("apply_payment", {
      p_payment_id: String(payment.id),
      p_user: ref.userId,
      p_plan: ref.plan.id,
      p_days: ref.plan.days,
      p_amount: typeof payment.transaction_amount === "number" ? payment.transaction_amount : null,
      p_status: approved ? "approved" : "refunded",
      p_approved_at: payment.date_approved || new Date().toISOString(),
    });
    if (error) {
      // 500 faz o Mercado Pago tentar de novo mais tarde
      return new Response("erro ao gravar pagamento: " + error.message, { status: 500 });
    }

    return new Response("ok", { status: 200 });
  } catch (e) {
    return new Response(String(e), { status: 500 });
  }
});
