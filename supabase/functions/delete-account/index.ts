// Exclui a conta do aluno autenticado que pediu a exclusão em "Minha conta".
// Precisa rodar no servidor: apagar um usuário do Supabase Auth exige a
// chave secreta, que nunca pode ir pro navegador.
//
// Quem é apagado é SEMPRE o dono do token que fez a chamada -- a function não
// aceita id de usuário no corpo, então não há como um aluno apagar outro.
//
// Apagar a linha de auth.users leva junto, por `on delete cascade` (ver
// supabase/schema.sql): profiles, user_state, entitlements, payments,
// billing, essay_submissions e admins. Ou seja, somem também as redações e o
// registro de pagamento, e o acesso comprado é perdido. Antes disso, a
// assinatura Mensal, se houver, é cancelada no Stripe.
//
// Segredo: STRIPE_SECRET_KEY (só usado se a conta tiver assinatura).
// (SUPABASE_URL e as chaves pública e secreta já existem automaticamente no
// ambiente de toda edge function do projeto; ver ../_shared/keys.ts.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { PUBLISHABLE_KEY, SECRET_KEY } from "../_shared/keys.ts";
import { STRIPE_LIVE_STATUSES } from "../_shared/stripe.js";
import { stripeCancelSubscription } from "../_shared/stripe_api.ts";

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
  if (req.method !== "POST") {
    return json({ error: "Método não permitido." }, 405);
  }

  try {
    const authHeader = req.headers.get("Authorization") || "";
    const asUser = createClient(SUPABASE_URL, PUBLISHABLE_KEY, {
      global: { headers: { Authorization: authHeader } },
    });
    const { data: { user }, error: userErr } = await asUser.auth.getUser();
    if (userErr || !user) {
      return json({ error: "Não autenticado." }, 401);
    }

    // segunda trava além do token: o site só chama isto depois de o aluno
    // digitar a palavra de confirmação, e a function confere de novo
    let confirm = "";
    try {
      const body = await req.json();
      if (typeof body?.confirm === "string") confirm = body.confirm.trim().toUpperCase();
    } catch { /* corpo vazio cai na recusa abaixo */ }
    if (confirm !== "EXCLUIR") {
      return json({ error: "Confirmação ausente." }, 400);
    }

    const admin = createClient(SUPABASE_URL, SECRET_KEY, {
      auth: { autoRefreshToken: false, persistSession: false },
    });

    // assinatura Mensal ainda cobrando: cancela no Stripe ANTES de apagar,
    // senão o cartão seguiria sendo cobrado sem conta para usar. Se o
    // cancelamento falhar, a conta não é apagada. Banco sem a tabela billing
    // (migração do Stripe não rodada) não tem assinatura para cancelar.
    const { data: bill, error: billErr } = await admin
      .from("billing")
      .select("subscription_id, subscription_status")
      .eq("user_id", user.id)
      .maybeSingle();
    if (billErr && !/does not exist|schema cache/i.test(billErr.message)) {
      console.error("delete-account: falha ao ler billing", user.id, billErr.message);
      return json({ error: "Não foi possível excluir a conta agora. Tente de novo em alguns minutos." }, 500);
    }
    if (bill?.subscription_id && STRIPE_LIVE_STATUSES.includes(bill.subscription_status)) {
      try {
        await stripeCancelSubscription(bill.subscription_id);
      } catch (e) {
        console.error("delete-account: falha ao cancelar a assinatura", user.id, String(e));
        return json({ error: "Não foi possível cancelar a sua assinatura agora, então a conta não foi excluída. Tente de novo em alguns minutos." }, 502);
      }
    }

    const { error: delErr } = await admin.auth.admin.deleteUser(user.id);
    if (delErr) {
      console.error("Falha ao excluir usuário", user.id, delErr.message);
      return json({ error: "Não foi possível excluir a conta agora. Tente de novo em alguns minutos." }, 500);
    }

    return json({ deleted: true });
  } catch (e) {
    console.error("delete-account falhou:", e);
    return json({ error: "Erro inesperado ao excluir a conta. Tente de novo." }, 500);
  }
});
