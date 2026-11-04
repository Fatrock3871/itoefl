// Envio de e-mail pelo SMTP próprio, para avisar o aluno de que a redação
// foi devolvida. Fica DESLIGADO até o dono configurar o SMTP (pendência 0.2
// do ROADMAP): sem os segredos abaixo, sendMail() não tenta nada e devolve
// false, e o aluno é avisado só pelo selo em Minha conta.
//
// Segredos (configurar com `supabase secrets set`, nunca aqui):
//   SMTP_HOST   ex.: smtp.seuprovedor.com
//   SMTP_PORT   465 (TLS direto) ou 587 (STARTTLS). Padrão: 465
//   SMTP_USER   usuário da conta de envio
//   SMTP_PASS   senha ou chave de app
//   SMTP_FROM   remetente, ex.: "PolyPoint <nao-responda@seudominio.com>"
//   SITE_URL    endereço público do site, para o link do e-mail (opcional)
// Passo a passo em docs/deploy-redacao.md.

export function smtpConfigured(): boolean {
  return ["SMTP_HOST", "SMTP_USER", "SMTP_PASS", "SMTP_FROM"].every((k) => !!Deno.env.get(k));
}

export async function sendMail(to: string, subject: string, text: string): Promise<boolean> {
  if (!smtpConfigured() || !to) return false;
  const port = Number(Deno.env.get("SMTP_PORT") || "465");
  try {
    // import só aqui dentro: sem SMTP configurado a biblioteca nem é baixada
    const { SMTPClient } = await import("https://deno.land/x/denomailer@1.6.0/mod.ts");
    const client = new SMTPClient({
      connection: {
        hostname: Deno.env.get("SMTP_HOST")!,
        port,
        tls: port === 465,
        auth: { username: Deno.env.get("SMTP_USER")!, password: Deno.env.get("SMTP_PASS")! },
      },
    });
    await client.send({ from: Deno.env.get("SMTP_FROM")!, to, subject, content: text });
    await client.close();
    return true;
  } catch (e) {
    // a devolução já foi gravada; falha no e-mail só fica no log
    console.error("Falha ao enviar e-mail:", e);
    return false;
  }
}
