// Os três planos de preço, do lado do servidor. É daqui que sai o valor
// cobrado (create-checkout) e o prazo gravado (mp-webhook): o navegador manda
// só o id do plano, nunca o preço.
//
// Tem de dizer o mesmo que app/plans.json, que alimenta as telas do site
// (o smoke test compara id, dias e preço dos dois arquivos). Mudar preço ou
// prazo: editar os dois, rebuildar o site e publicar de novo create-checkout
// e mp-webhook.
//
// priceCents em centavos, para não fazer conta de dinheiro com ponto
// flutuante. days null = acesso sem prazo (vitalício).

export type Plan = {
  id: string;
  name: string;
  days: number | null;
  priceCents: number;
};

export const PLANS: Plan[] = [
  { id: "sprint", name: "Sprint", days: 30, priceCents: 3990 },
  { id: "standard", name: "Standard", days: 90, priceCents: 8990 },
  { id: "premium", name: "Premium", days: null, priceCents: 14990 },
];

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
