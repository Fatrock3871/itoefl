// Recebe os avisos (eventos) do Stripe e mantém o acesso do aluno em dia:
// compra de um plano de dias, cada mês pago do Mensal, cobrança recusada,
// assinatura alterada ou cancelada, e reembolso. Endpoint público: o Stripe
// não manda token do Supabase (por isso verify_jwt = false em config.toml).
//
// Segurança, nesta ordem:
//   1. o corpo cru é conferido contra o cabeçalho Stripe-Signature com o
//      segredo do endpoint. Assinatura inválida ou velha: 400, nada é lido;
//   2. o corpo só diz qual objeto mudou. O estado é relido da API do Stripe
//      (ver ../_shared/stripe.js), nunca tirado do aviso.
//
// Idempotência: o mesmo evento pode chegar mais de uma vez. O id do evento
// vai para `stripe_events` só depois de tudo gravado; evento já gravado volta
// 200 sem refazer nada. E cada gravação também é idempotente por si:
// apply_payment usa o id da fatura ou do pagamento como chave, e
// apply_billing ignora leitura mais antiga que a já gravada. Se algo falhar
// no meio, a resposta é 500 e o Stripe tenta de novo mais tarde.
//
// O que grava: `payments` e, a partir dele, `entitlements` (função de banco
// apply_payment, regras em supabase/migrations/20261018_stripe.sql), e a
// situação da assinatura em `billing` (apply_billing).
//
// Segredos necessários (`supabase secrets set`, nunca aqui):
//   STRIPE_SECRET_KEY       chave secreta da conta (sk_test_... ou sk_live_...)
//   STRIPE_WEBHOOK_SECRET   segredo do endpoint (whsec_...), mostrado no painel
//                           do Stripe ao criar o endpoint deste webhook
// (SUPABASE_URL e a chave secreta do Supabase já existem no ambiente; ver
// ../_shared/keys.ts.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { SECRET_KEY } from "../_shared/keys.ts";
import { findPlan } from "../_shared/plans.ts";
import { STRIPE_EVENTS, stripeHandleEvent, stripeVerifySignature } from "../_shared/stripe.js";
import { stripeCancelSubscription, stripeRequest } from "../_shared/stripe_api.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;

function text(body: string, status: number) {
  return new Response(body, { status, headers: { "Content-Type": "text/plain; charset=utf-8" } });
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return text("método não permitido", 405);

  const webhookSecret = (Deno.env.get("STRIPE_WEBHOOK_SECRET") || "").trim();
  if (!webhookSecret) {
    console.error("stripe-webhook: STRIPE_WEBHOOK_SECRET ausente");
    return text("webhook não configurado", 500);
  }

  // o corpo tem de ser lido cru: qualquer reformatação quebra a assinatura
  const payload = await req.text();
  const valid = await stripeVerifySignature(payload, req.headers.get("Stripe-Signature") || "", webhookSecret);
  if (!valid) return text("assinatura inválida", 400);

  let event: any;
  try {
    event = JSON.parse(payload);
  } catch {
    return text("corpo inválido", 400);
  }
  if (!event || typeof event.id !== "string" || !STRIPE_EVENTS.includes(event.type)) {
    return text("ok", 200); // evento que não interessa: confirma para o Stripe não reenviar
  }

  const db = createClient(SUPABASE_URL, SECRET_KEY, { auth: { autoRefreshToken: false, persistSession: false } });
  const { data: seen, error: seenErr } = await db.from("stripe_events").select("id").eq("id", event.id).maybeSingle();
  if (seenErr) {
    console.error("stripe-webhook: falha ao ler stripe_events", seenErr.message);
    return text("erro no banco", 500);
  }
  if (seen) return text("já processado", 200);

  const deps = {
    get: (path: string) => stripeRequest("GET", path),
    cancelSubscription: (id: string) => stripeCancelSubscription(id),
    now: () => new Date().toISOString(),
    plan: (id: unknown) => {
      const p = findPlan(id);
      return p ? { id: p.id, interval: p.interval, days: p.days } : null;
    },
    findBilling: async (user: string) => {
      const { data, error } = await db.from("billing").select("subscription_id, subscription_status").eq("user_id", user).maybeSingle();
      if (error) throw new Error("leitura de billing: " + error.message);
      return data;
    },
    applyPayment: async (a: any) => {
      const { error } = await db.rpc("apply_payment", {
        p_payment_id: a.id,
        p_user: a.user,
        p_plan: a.plan,
        p_days: a.days,
        p_amount: a.amount,
        p_status: a.status,
        p_approved_at: a.approvedAt,
        p_period_end: a.periodEnd,
      });
      if (error) throw new Error("apply_payment: " + error.message);
    },
    applyBilling: async (a: any) => {
      const { error } = await db.rpc("apply_billing", {
        p_user: a.user,
        p_customer: a.customer,
        p_subscription: a.subscription,
        p_status: a.status,
        p_cancel_at_period_end: a.cancelAtPeriodEnd,
        p_period_end: a.periodEnd,
        p_event_at: a.at,
      });
      if (error) throw new Error("apply_billing: " + error.message);
    },
  };

  try {
    const done = await stripeHandleEvent(event, deps);
    console.log("stripe-webhook", event.type, event.id, done.join(" | "));
  } catch (e) {
    console.error("stripe-webhook: falhou", event.type, event.id, String(e));
    return text("erro ao processar", 500); // o Stripe tenta de novo
  }

  // só depois de tudo gravado. Dois avisos iguais ao mesmo tempo: o segundo
  // esbarra na chave e é ignorado (tudo acima já é idempotente)
  const { error: insErr } = await db.from("stripe_events")
    .upsert({ id: event.id, type: event.type }, { onConflict: "id", ignoreDuplicates: true });
  if (insErr) console.error("stripe-webhook: evento processado, mas não registrado", event.id, insErr.message);
  return text("ok", 200);
});
