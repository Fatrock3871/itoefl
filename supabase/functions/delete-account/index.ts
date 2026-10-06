// Exclui a conta do aluno autenticado que pediu a exclusão em "Minha conta".
// Precisa rodar no servidor: apagar um usuário do Supabase Auth exige a
// service_role, que nunca pode ir pro navegador.
//
// Quem é apagado é SEMPRE o dono do token que fez a chamada -- a function não
// aceita id de usuário no corpo, então não há como um aluno apagar outro.
//
// Apagar a linha de auth.users leva junto, por `on delete cascade` (ver
// supabase/schema.sql): profiles, user_state e entitlements. Ou seja, some
// também o registro de pagamento, e o acesso comprado é perdido.
//
// (SUPABASE_URL, SUPABASE_ANON_KEY e SUPABASE_SERVICE_ROLE_KEY já existem
// automaticamente no ambiente de toda edge function do projeto.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

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
    const asUser = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
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

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
      auth: { autoRefreshToken: false, persistSession: false },
    });
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
