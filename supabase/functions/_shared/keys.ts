// Chaves do Supabase para as edge functions, no formato novo.
//
// As chaves antigas (`anon` e `service_role`, variáveis SUPABASE_ANON_KEY e
// SUPABASE_SERVICE_ROLE_KEY) são JWT assinados pelo segredo do projeto e não
// dá para trocar uma sem trocar todas. A `service_role` vazou num chat em
// setembro de 2026; para desativá-la no painel (Settings > API Keys), nenhuma
// function pode depender dela. Por isso tudo aqui lê as chaves novas:
//
//   SUPABASE_PUBLISHABLE_KEYS  -> no lugar da anon (respeita a RLS)
//   SUPABASE_SECRET_KEYS       -> no lugar da service_role (ignora a RLS)
//
// O Supabase põe as duas variáveis no ambiente de toda function, como JSON
// {nome: chave}. Qual chave usar:
//   1. a de nome SUPABASE_SECRET_KEY_NAME / SUPABASE_PUBLISHABLE_KEY_NAME, se
//      esse segredo existir (`supabase secrets set ...`);
//   2. senão, a de nome "default", que é o nome que o painel dá à primeira;
//   3. senão, a única que houver.
// Com mais de uma chave e nenhuma chamada "default", falha com mensagem clara
// em vez de escolher às cegas.
//
// Guia do Supabase: docs/guides/getting-started/migrating-to-new-api-keys

function pickKey(dictVar: string, nameVar: string): string {
  const raw = Deno.env.get(dictVar);
  if (!raw) throw new Error(`${dictVar} ausente no ambiente da function.`);
  let dict: Record<string, string>;
  try {
    dict = JSON.parse(raw);
  } catch {
    throw new Error(`${dictVar} não é um JSON válido.`);
  }
  const wanted = Deno.env.get(nameVar);
  if (wanted) {
    if (!dict[wanted]) throw new Error(`${dictVar} não tem a chave "${wanted}" (pedida em ${nameVar}).`);
    return dict[wanted];
  }
  if (dict["default"]) return dict["default"];
  const names = Object.keys(dict);
  if (names.length === 1) return dict[names[0]];
  throw new Error(
    `${dictVar} tem ${names.length} chaves (${names.join(", ")}) e nenhuma se chama "default": ` +
      `defina ${nameVar} com o nome da que deve ser usada.`,
  );
}

// Chave pública: usada com o token do aluno para descobrir quem ele é, sob RLS.
export const PUBLISHABLE_KEY = pickKey("SUPABASE_PUBLISHABLE_KEYS", "SUPABASE_PUBLISHABLE_KEY_NAME");

// Chave secreta: só para o que exige passar por cima da RLS (gravar pagamento,
// excluir usuário, ler a fila de redações). Nunca sai da function.
export const SECRET_KEY = pickKey("SUPABASE_SECRET_KEYS", "SUPABASE_SECRET_KEY_NAME");
