// Ações do painel do corretor sobre uma redação enviada. Só para quem tem
// linha na tabela `admins` (conferido aqui, com a chave secreta, e não pelo
// que o navegador diz).
//
//   { action: "start",  id }            na_fila -> em_correcao (o corretor abriu)
//   { action: "return", id, feedback }  grava a devolutiva e devolve ao aluno
//
// Na devolução, a devolutiva é validada pelo mesmo código do site
// (redacaoValidaDevolutiva, em ../_shared/redacao.js) e a nota final e o nível
// são recalculados aqui a partir das 4 notas: o navegador não manda nota final.
// Depois de gravar, avisa o aluno por e-mail se o SMTP estiver configurado
// (../_shared/mail.ts). Sem SMTP, o aviso fica só no site (selo em Minha conta).
//
// Nenhuma IA é chamada aqui: o corretor usa a ferramenta dele fora do site e
// cola o resultado no painel (modelo de correção assistida, 2026-10-14).

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { redacaoNivel, redacaoNotaFinal, redacaoValidaDevolutiva } from "../_shared/redacao.js";
import { sendMail } from "../_shared/mail.ts";
import { PUBLISHABLE_KEY, SECRET_KEY } from "../_shared/keys.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SITE_URL = Deno.env.get("SITE_URL") || "";

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

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

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

    const admin = createClient(SUPABASE_URL, SECRET_KEY, {
      auth: { autoRefreshToken: false, persistSession: false },
    });
    const { data: adminRow } = await admin.from("admins").select("user_id").eq("user_id", user.id).maybeSingle();
    if (!adminRow) {
      return json({ error: "Só a equipe de correção pode fazer isto." }, 403);
    }

    let body: Record<string, unknown> = {};
    try { body = await req.json(); } catch { /* corpo vazio cai nas recusas abaixo */ }
    const id = typeof body.id === "string" && UUID_RE.test(body.id) ? body.id : "";
    if (!id) {
      return json({ error: "Envio não identificado." }, 400);
    }

    if (body.action === "start") {
      // só muda quem ainda está na fila; abrir de novo não faz nada
      const { error } = await admin
        .from("essay_submissions")
        .update({ status: "em_correcao" })
        .eq("id", id)
        .eq("status", "na_fila");
      if (error) {
        console.error("Falha ao marcar em correção:", error.message);
        return json({ error: "Não deu para marcar a redação como em correção." }, 500);
      }
      return json({ ok: true, status: "em_correcao" });
    }

    if (body.action !== "return") {
      return json({ error: "Ação desconhecida." }, 400);
    }

    const feedback = body.feedback as Record<string, any>;
    const check = redacaoValidaDevolutiva(feedback);
    if (!check.ok) {
      return json({ error: "A devolutiva não está no formato.", erros: check.erros }, 400);
    }
    const c = feedback.criterios;
    const notas = {
      cumprimento: c.cumprimento.nota,
      organizacao: c.organizacao.nota,
      gramatica: c.gramatica.nota,
      vocabulario: c.vocabulario.nota,
    };
    const final = redacaoNotaFinal(notas);
    const level = redacaoNivel(final);

    const { data: updated, error: upErr } = await admin
      .from("essay_submissions")
      .update({
        status: "devolvida",
        score_task: notas.cumprimento,
        score_organization: notas.organizacao,
        score_grammar: notas.gramatica,
        score_vocabulary: notas.vocabulario,
        final_score: final,
        level,
        feedback,
        graded_by: user.id,
        returned_at: new Date().toISOString(),
      })
      .eq("id", id)
      .neq("status", "devolvida")
      .select("id, user_id")
      .maybeSingle();
    if (upErr) {
      console.error("Falha ao devolver:", upErr.message);
      return json({ error: "Não deu para gravar a devolutiva agora. Tente de novo." }, 500);
    }
    if (!updated) {
      return json({ error: "Esta redação já foi devolvida (ou não existe)." }, 409);
    }

    // aviso por e-mail: só com SMTP configurado; falha aqui não desfaz a devolução
    let emailed = false;
    const { data: student } = await admin.auth.admin.getUserById(updated.user_id);
    const to = student?.user?.email || "";
    if (to) {
      const link = SITE_URL ? `\n\nPara ver, entre na plataforma: ${SITE_URL}\n(Minha conta > Redações)` : "\n\nPara ver, entre na plataforma e abra Minha conta > Redações.";
      emailed = await sendMail(
        to,
        "Sua redação do iTOEFL foi corrigida",
        `Olá!\n\nA devolutiva da sua redação está pronta: nota ${String(final).replace(".", ",")} de 5, nível estimado ${level}.` +
          link +
          "\n\nA nota é uma estimativa de treino, não a nota oficial da ETS.\n\nEquipe iTOEFL",
      );
    }

    return json({ ok: true, status: "devolvida", final_score: final, level, emailed });
  } catch (e) {
    console.error("review-essay falhou:", e);
    return json({ error: "Erro inesperado. Tente de novo." }, 500);
  }
});
