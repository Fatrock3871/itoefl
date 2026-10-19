// Os planos de preço, do lado do servidor. Preço, duração e destaque moram
// em ./plans.json, o ÚNICO arquivo com esses valores (decisão do dono,
// 2026-10-18): o servidor lê daqui e o site (app/build.py) lê o mesmo
// arquivo. O navegador manda só o id do plano, nunca o preço.
//
//   interval "month"  assinatura no cartão (Stripe, mode=subscription)
//   interval null     pagamento único de `days` dias, sem renovação
//                     (Stripe mode=payment, ou Pix pelo Mercado Pago)
//
// priceCents em centavos, para não fazer conta de dinheiro com ponto
// flutuante.

import CONFIG from "./plans.json" with { type: "json" };

export type Plan = {
  id: string;
  name: string;
  interval: "month" | null;
  days: number | null;
  priceCents: number;
};

export const PLANS: Plan[] = CONFIG.plans.map((p) => ({
  id: p.id,
  name: p.name,
  interval: p.interval === "month" ? "month" : null,
  days: typeof p.days === "number" ? p.days : null,
  priceCents: p.price_cents,
}));

// Pix pelo Mercado Pago nos planos de pagamento único, enquanto o Stripe não
// libera o Pix na conta. Trocar em ./plans.json ("pix_mercado_pago").
export const PIX_VIA_MERCADO_PAGO: boolean = CONFIG.pix_mercado_pago === true;

export function findPlan(id: unknown): Plan | null {
  if (typeof id !== "string") return null;
  return PLANS.find((p) => p.id === id.trim().toLowerCase()) || null;
}

// external_reference da preferência do Mercado Pago: "<id do usuário>|<id do
// plano>". É o que o mp-webhook lê de volta para saber de quem é o pagamento
// e qual plano foi comprado.
export function buildReference(userId: string, planId: string): string {
  return `${userId}|${planId}`;
}

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function parseReference(ref: unknown): { userId: string; plan: Plan } | null {
  if (typeof ref !== "string") return null;
  const parts = ref.split("|");
  if (parts.length !== 2 || !UUID_RE.test(parts[0])) return null;
  const plan = findPlan(parts[1]);
  return plan ? { userId: parts[0], plan } : null;
}
