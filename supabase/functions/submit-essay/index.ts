// Recebe a redação que o aluno enviou para correção (Minha conta ou M4 >
// Correção de redação). Todas as regras do envio são conferidas AQUI, no
// servidor; o que o site confere antes é só para avisar mais cedo:
//   - acesso pago em dia (ou conta corretora, que testa o fluxo);
//   - tema válido e tarefa certa para o tema;
//   - tamanho (caracteres e palavras) e o mínimo de 100 palavras na discussão;
//   - 1 envio a cada 4 dias, contados do último envio;
//   - consentimento LGPD no primeiro envio.
// A data prevista da devolutiva (3 dias úteis, sem fim de semana nem feriado
// nacional) é calculada aqui e gravada junto.
//
// As regras e os números moram em ../_shared/redacao.js, o mesmo arquivo que o
// site usa. A gravação passa pela função de banco create_essay_submission, que
// trava a conta e reconfere o intervalo (dois cliques ao mesmo tempo não
// passam os dois).
//
// (SUPABASE_URL, SUPABASE_ANON_KEY e SUPABASE_SERVICE_ROLE_KEY já existem
// automaticamente no ambiente de toda edge function do projeto.)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import {
  REDACAO_REGRAS,
  redacaoBloqueio,
  redacaoContaPalavras,
  redacaoPrevisao,
} from "../_shared/redacao.js";

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

function fmtDia(ms: number) {
  // DD/MM no horário de Brasília
  const d = new Date(ms - 3 * 3600000);
  return `${String(d.getUTCDate()).padStart(2, "0")}/${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
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

    let body: Record<string, unknown> = {};
    try { body = await req.json(); } catch { /* corpo vazio cai nas recusas abaixo */ }

    // ---- tema e texto ----
    const topic = typeof body.topic === "string" ? body.topic : "";
    const task = (REDACAO_REGRAS.temas as Record<string, string>)[topic];
    if (!task) {
      return json({ error: "Tema inválido. Escolha um dos 10 temas da lista." }, 400);
    }
    const text = typeof body.text === "string" ? body.text.trim() : "";
    if (!text) {
      return json({ error: "A redação está vazia." }, 400);
    }
    if (text.length > REDACAO_REGRAS.maxCaracteres) {
      return json({ error: `A redação passa de ${REDACAO_REGRAS.maxCaracteres} caracteres.` }, 400);
    }
    // a contagem que vale é a do servidor, nunca a que o navegador mandou
    const words = redacaoContaPalavras(text);
    if (words > REDACAO_REGRAS.maxPalavras) {
      return json({ error: `A redação passa de ${REDACAO_REGRAS.maxPalavras} palavras.` }, 400);
    }
    const minWords = (REDACAO_REGRAS.minPalavras as Record<string, number>)[task];
    if (words < minWords) {
      return json({ error: `A discussão precisa de pelo menos ${minWords} palavras (a sua tem ${words}).` }, 400);
    }
    // o tempo vem do cronômetro do navegador: só se aceita dentro do limite da tarefa
    const limit = (REDACAO_REGRAS.minutos as Record<string, number>)[task] * 60;
    const rawSeconds = Number(body.seconds);
    const seconds = Number.isFinite(rawSeconds) ? Math.min(limit, Math.max(0, Math.round(rawSeconds))) : limit;

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
      auth: { autoRefreshToken: false, persistSession: false },
    });

    // ---- acesso pago em dia ----
    const { data: adminRow } = await admin.from("admins").select("user_id").eq("user_id", user.id).maybeSingle();
    if (!adminRow) {
      const { data: ent, error: entErr } = await admin
        .from("entitlements")
        .select("paid, expires_at")
        .eq("user_id", user.id)
        .maybeSingle();
      if (entErr) {
        console.error("Falha ao ler entitlements:", entErr.message);
        return json({ error: "Não deu para conferir o seu acesso agora. Tente de novo em alguns minutos." }, 500);
      }
      const active = !!ent && ent.paid && (!ent.expires_at || new Date(ent.expires_at).getTime() > Date.now());
      if (!active) {
        return json({ error: "O envio de redação é para quem tem acesso em dia. Renove o seu plano em Minha conta." }, 403);
      }
    }

    // ---- 1 envio a cada 4 dias, e consentimento no primeiro ----
    const { data: last, error: lastErr } = await admin
      .from("essay_submissions")
      .select("submitted_at")
      .eq("user_id", user.id)
      .order("submitted_at", { ascending: false })
      .limit(1);
    if (lastErr) {
      console.error("Falha ao ler envios:", lastErr.message);
      return json({ error: "Não deu para registrar a redação agora. Tente de novo em alguns minutos." }, 500);
    }
    const now = Date.now();
    const block = redacaoBloqueio(last || [], now);
    if (block.bloqueado) {
      return json({
        error: `Você já enviou uma redação nos últimos ${REDACAO_REGRAS.intervaloDias} dias. Próximo envio liberado em ${fmtDia(block.liberaEm!)}.`,
        next_at: new Date(block.liberaEm!).toISOString(),
      }, 429);
    }
    const consent = body.consent === true;
    if (!(last && last.length) && !consent) {
      return json({ error: "No primeiro envio é preciso marcar o consentimento sobre o uso da redação." }, 400);
    }

    // ---- grava ----
    const due = redacaoPrevisao(now);
    const { data: row, error: insErr } = await admin.rpc("create_essay_submission", {
      p_user: user.id,
      p_topic: topic,
      p_task: task,
      p_text: text,
      p_words: words,
      p_seconds: seconds,
      p_due: due,
      p_consent: consent,
    });
    if (insErr) {
      if (/intervalo/.test(insErr.message)) {
        return json({ error: `Você já enviou uma redação nos últimos ${REDACAO_REGRAS.intervaloDias} dias.` }, 429);
      }
      if (/consentimento/.test(insErr.message)) {
        return json({ error: "No primeiro envio é preciso marcar o consentimento sobre o uso da redação." }, 400);
      }
      console.error("Falha ao gravar a redação:", insErr.message);
      return json({ error: "Não deu para registrar a redação agora. Tente de novo em alguns minutos." }, 500);
    }

    const sent = Array.isArray(row) ? row[0] : row;
    const submittedMs = new Date(sent.submitted_at).getTime();
    return json({
      id: sent.id,
      topic_id: sent.topic_id,
      task: sent.task,
      word_count: sent.word_count,
      submitted_at: sent.submitted_at,
      due_on: sent.due_on,
      status: sent.status,
      next_at: new Date(submittedMs + REDACAO_REGRAS.intervaloDias * 86400000).toISOString(),
    });
  } catch (e) {
    console.error("submit-essay falhou:", e);
    return json({ error: "Erro inesperado ao enviar a redação. Tente de novo." }, 500);
  }
});
