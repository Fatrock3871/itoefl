// Chamadas à API do Stripe, sem biblioteca: fetch com o corpo em
// application/x-www-form-urlencoded, que é o formato da API.
//
// Segredo necessário (configurar com `supabase secrets set`, nunca aqui):
//   STRIPE_SECRET_KEY   sk_test_... no modo de teste, sk_live_... de verdade
// Toda chamada pede a mesma versão de API (STRIPE_API_VERSION, em
// ./stripe.js), para o formato das respostas não mudar sozinho.

import { STRIPE_API_VERSION, STRIPE_LIVE_STATUSES } from "./stripe.js";

export class StripeError extends Error {
  status: number;
  code: string;
  constructor(status: number, code: string, message: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

export function stripeConfigured(): boolean {
  return !!(Deno.env.get("STRIPE_SECRET_KEY") || "").trim();
}

// params: chaves já no formato da API, ex. "line_items[0][quantity]": 1.
// Valor undefined ou null fica de fora.
export async function stripeRequest(
  method: "GET" | "POST" | "DELETE",
  path: string,
  params?: Record<string, string | number | boolean | null | undefined>,
  idempotencyKey?: string,
): Promise<any> {
  const key = (Deno.env.get("STRIPE_SECRET_KEY") || "").trim();
  if (!key) throw new StripeError(500, "config", "STRIPE_SECRET_KEY ausente no ambiente da function.");
  const form = new URLSearchParams();
  for (const [k, v] of Object.entries(params || {})) {
    if (v !== undefined && v !== null) form.append(k, String(v));
  }
  const headers: Record<string, string> = {
    Authorization: `Bearer ${key}`,
    "Stripe-Version": STRIPE_API_VERSION,
  };
  let url = `https://api.stripe.com${path}`;
  let body: string | undefined;
  if (method === "GET") {
    const q = form.toString();
    if (q) url += (url.includes("?") ? "&" : "?") + q;
  } else {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    body = form.toString();
    if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  }
  const res = await fetch(url, { method, headers, body });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = data?.error || {};
    throw new StripeError(res.status, err.code || err.type || "erro", `Stripe ${res.status}: ${err.message || "sem detalhe"}`);
  }
  return data;
}

// Cancela já uma assinatura que ainda cobra. Assinatura já encerrada (ou
// que não existe mais) não é erro: não há o que cancelar.
export async function stripeCancelSubscription(id: string): Promise<void> {
  const path = `/v1/subscriptions/${encodeURIComponent(id)}`;
  let sub: any;
  try {
    sub = await stripeRequest("GET", path);
  } catch (e) {
    if (e instanceof StripeError && e.status === 404) return;
    throw e;
  }
  if (!STRIPE_LIVE_STATUSES.includes(sub.status)) return;
  await stripeRequest("DELETE", path);
}
