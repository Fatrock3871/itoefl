# Structured drill data for interactive quiz widgets (modules 1 and 2).
# Each drill: id, title, objective (short instruction), optional shared passage_html,
# and items: [{num, prompt, options{A,B,C,D}, correct, explanation}]

MOD1_DRILLS = [
    {
        "id": "mod1-d1",
        "title": "Drill 1 — Complete the Words: reconstrução de texto",
        "objective": "Para cada lacuna numerada, escolha a opção que reconstrói o texto de forma gramatical, lexicalmente natural e coerente com o sentido geral. Tempo alvo: 6 minutos para os 8 itens.",
        "passage_html": """<p><strong>TEXT: A Message From the Office Manager</strong></p>
<p>Hi team,</p>
<p>I wanted to send a quick note before the long weekend. As most of you already (1)_____, the building's heating system will be shut down for scheduled maintenance from Friday evening through Monday morning. Please make sure you (2)_____ any equipment that shouldn't be left running unattended, and take home anything that might be sensitive to temperature changes over the weekend.</p>
<p>The maintenance crew has assured us that the work will be (3)_____ before Monday, so there shouldn't be any disruption when everyone (4)_____ back to the office. However, if the weather turns unexpectedly cold, the building may take a little longer than usual to (5)_____ up again — so please dress in layers just in case.</p>
<p>If you have any questions or concerns, don't (6)_____ to reach out to facilities directly. We'd rather you ask a question that turns out to be unnecessary than (7)_____ a real problem over the weekend.</p>
<p>Thanks for your patience, and enjoy the (8)_____ time off!</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "know", "B": "knows", "C": "known", "D": "knowing"},
             "correct": "A", "explanation": "\"As most of you already know\" pede presente simples na 3ª pessoa do plural (forma base, sem -s) — construção fixa comum em avisos. (B) quebra a concordância; (C) exigiria auxiliar (\"have known\"); (D) não completa o tempo verbal da oração."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "turn off", "B": "turn down", "C": "turn out", "D": "turn over"},
             "correct": "A", "explanation": "\"Turn off equipment\" = desligar equipamento, a collocation exata para o contexto de manutenção/segurança. (B) = diminuir intensidade; (C) = descobrir-se/comparecer; (D) = virar/entregar — nenhum se encaixa aqui."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "complete", "B": "completing", "C": "completed", "D": "completes"},
             "correct": "C", "explanation": "\"Will be _____\" pede particípio passado para a voz passiva. \"Will be completed\" é a estrutura passiva padrão. As outras formas quebram a estrutura \"be + particípio\"."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "come", "B": "comes", "C": "coming", "D": "will comes"},
             "correct": "B", "explanation": "\"Everyone\" é gramaticalmente singular, então o verbo vai para a 3ª pessoa do singular: \"comes back\". (A) quebra a concordância; (C) exigiria auxiliar; (D) é agramatical (\"will\" nunca é seguido de verbo com -s)."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "warm", "B": "warms", "C": "warmly", "D": "warmth"},
             "correct": "A", "explanation": "\"To _____ up again\" pede o infinitivo (verbo base) após \"to\". \"Warm up\" é o phrasal verb certo para um ambiente recuperando temperatura — as outras opções quebram essa estrutura."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "hesitate", "B": "hesitating", "C": "hesitation", "D": "hesitated"},
             "correct": "A", "explanation": "\"Don't _____ to reach out\" pede verbo base após o imperativo negativo \"don't\". \"Don't hesitate to + verbo\" é expressão fixa clássica em comunicação profissional."},
            {"num": "7", "prompt": "Lacuna (7)", "options": {"A": "miss", "B": "lose", "C": "waste", "D": "fail"},
             "correct": "B", "explanation": "Estrutura paralela \"ask a question... than _____ a real problem\" pede verbo base após \"than\". \"Lose\" mantém o contraste lógico: preferir perguntar a deixar o problema se agravar. \"Miss\"/\"waste\"/\"fail\" não combinam com \"problem\" da mesma forma direta."},
            {"num": "8", "prompt": "Lacuna (8)", "options": {"A": "extend", "B": "extending", "C": "extended", "D": "extension"},
             "correct": "C", "explanation": "\"The _____ time off\" pede um adjetivo (particípio usado como adjetivo) antes do substantivo. \"Extended time off\" = folga prolongada. As outras formas não funcionam como modificador de substantivo nessa posição."},
        ],
    },
    {
        "id": "mod1-d2",
        "title": "Drill 2 — Read in Daily Life: texto curto não-acadêmico",
        "objective": "Leia o texto uma vez, identificando formato, remetente, destinatário e propósito. Responda às 4 questões. Tempo alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: A social media post from a local bakery</strong></p>
<blockquote><p>🥐 <strong>Riverside Bakery</strong> — Posted 2 hours ago</p>
<p>Big news, everyone! Starting next Tuesday, we're extending our weekday hours — open at 6:30 AM instead of 7:00 AM, so early risers can grab their coffee and croissants before work. 🌅</p>
<p>Quick heads-up though: because of the earlier opening, our weekday sourdough batch will now go into the oven the night before instead of first thing in the morning. It'll still be baked fresh daily, just on a slightly different schedule — so if you're used to catching it warm right out of the oven at 8 AM, it might be ready a little earlier now. Come say hi and let us know what you think of the new hours!</p>
<p>Weekend hours are unchanged (8 AM–3 PM, same as always).</p></blockquote>""",
        "items": [
            {"num": "2.1", "prompt": "What is the main purpose of this post?",
             "options": {"A": "To announce that the bakery is closing early on weekdays", "B": "To inform customers about a change to weekday opening hours", "C": "To apologize for a delay in the sourdough baking schedule", "D": "To advertise a new type of bread being introduced"},
             "correct": "B", "explanation": "O post inteiro gira em torno de um único anúncio: abrir mais cedo nos dias de semana. (A) inverte o sentido (é abertura mais cedo, não fechamento); (C) o texto não pede desculpas; (D) nenhum pão novo é introduzido, só o horário de forno muda."},
            {"num": "2.2", "prompt": "According to the post, what will change about the sourdough bread?",
             "options": {"A": "It will no longer be baked fresh every day.", "B": "It will only be available on weekends.", "C": "It will be baked the night before instead of the same morning.", "D": "It will be replaced with a different type of bread."},
             "correct": "C", "explanation": "O texto afirma exatamente isso. (A) o texto diz \"it'll still be baked fresh daily\"; (B) nada indica restrição a fins de semana; (D) não há substituição de produto."},
            {"num": "2.3", "prompt": "What can be inferred about the bakery's weekend hours?",
             "options": {"A": "They will also move to 6:30 AM starting next Tuesday.", "B": "They remain the same as they were before this announcement.", "C": "They have not yet been decided.", "D": "They will be shortened to match the new weekday schedule."},
             "correct": "B", "explanation": "A última linha afirma diretamente: \"Weekend hours are unchanged\". (A) e (D) contradizem o texto; (C) o texto não deixa isso em aberto."},
            {"num": "2.4", "prompt": "The overall tone of this post is best described as:",
             "options": {"A": "formal and apologetic", "B": "friendly and informative", "C": "urgent and cautionary", "D": "neutral and impersonal"},
             "correct": "B", "explanation": "Emojis, saudação casual, convite pessoal e tom positivo caracterizam um registro amigável e informativo. Não há tom apologético, urgência/alerta, ou impessoalidade."},
        ],
    },
    {
        "id": "mod1-d3",
        "title": "Drill 3 — Read an Academic Passage",
        "objective": "Leia a passagem completa uma vez (ela é curta o suficiente para isso). Responda às 6 questões. Tempo alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: Bioluminescence in Marine Organisms</strong></p>
<p>Bioluminescence — the production and emission of light by a living organism — is remarkably common in the ocean, appearing in bacteria, jellyfish, fish, and even some sharks. Unlike the light produced by a bulb, which wastes most of its energy as heat, bioluminescent light is generated through a highly efficient chemical reaction, typically involving a light-emitting molecule called luciferin and an enzyme called luciferase. Because so little energy is lost as heat, biologists sometimes refer to this phenomenon as "cold light."</p>
<p>The functions of bioluminescence vary considerably across species, though three purposes appear again and again. Some organisms use light defensively: certain species of squid release a luminous cloud instead of ink, startling predators and buying time to escape. Others use it as a hunting tool. The anglerfish, perhaps the most famous example, dangles a glowing lure above its mouth to attract smaller prey close enough to seize. Still others use light for communication, particularly in the deep sea, where darkness is nearly absolute and visual signals cannot rely on ambient light. Certain species of ostracods, tiny crustaceans, produce synchronized light displays to attract mates — a strategy so distinctive that in some regions it has been used by local fishers as a marker of species presence.</p>
<p>What makes bioluminescence especially interesting to evolutionary biologists is that it did not evolve just once. Genetic and biochemical evidence indicates that the capacity for bioluminescence has arisen independently dozens of times across unrelated lineages, using different chemical pathways to achieve a similar outcome. This pattern, in which unrelated organisms evolve similar traits independently, is known as convergent evolution, and bioluminescence is considered one of its most striking examples precisely because the same functional result — producing light efficiently — has been "reinvented" so many times by evolution.</p>""",
        "items": [
            {"num": "3.1", "prompt": "What is the main idea of the passage?",
             "options": {"A": "Bioluminescence is a rare adaptation found only in a few deep-sea species.", "B": "Bioluminescence is a widespread, chemically efficient trait that serves multiple functions and evolved independently many times.", "C": "The anglerfish is the most important example of bioluminescence among marine organisms.", "D": "Bioluminescent light is less efficient than artificial light produced by a bulb."},
             "correct": "B", "explanation": "A passagem cobre três eixos: o que é o fenômeno e sua eficiência química, suas múltiplas funções, e sua origem evolutiva independente. Só (B) sintetiza os três. (A) contradiz o texto (\"remarkably common\"); (C) é um detalhe; (D) inverte o sentido do texto."},
            {"num": "3.2", "prompt": "According to the passage, why is bioluminescent light sometimes called \"cold light\"?",
             "options": {"A": "It only occurs in cold, deep-sea environments.", "B": "It is produced by organisms that live in low-temperature waters.", "C": "The chemical reaction that produces it wastes very little energy as heat.", "D": "It appears blue or white in color, resembling ice."},
             "correct": "C", "explanation": "O texto afirma isso diretamente com relação causal explícita (\"because so little energy is lost as heat\"). As outras opções confundem o termo com temperatura ambiente ou cor, o que o texto não sustenta."},
            {"num": "3.3", "prompt": "Which of the following is NOT mentioned in the passage as a function of bioluminescence?",
             "options": {"A": "Startling predators", "B": "Attracting prey", "C": "Attracting mates", "D": "Regulating body temperature"},
             "correct": "D", "explanation": "O parágrafo 2 lista três funções: defesa, caça e comunicação/atração de parceiros. Regulação de temperatura corporal nunca é mencionada — as outras três estão todas explicitamente no texto."},
            {"num": "3.4", "prompt": "It can be inferred from paragraph 2 that in deep-sea environments:",
             "options": {"A": "visual communication is impossible for any species", "B": "organisms rely on producing their own light because there is little to no ambient light", "C": "most species have evolved to lose their sense of sight entirely", "D": "bioluminescence is used exclusively for hunting, not communication"},
             "correct": "B", "explanation": "O texto liga diretamente a comunicação por luz própria à ausência de luz ambiente no fundo do mar. (A) é extremo demais; (C) não é sustentado pelo texto; (D) contradiz o próprio parágrafo, que lista comunicação como função distinta."},
            {"num": "3.5", "prompt": "Why does the author mention that bioluminescence \"did not evolve just once\" in paragraph 3?",
             "options": {"A": "To argue that bioluminescence is less biologically significant than previously thought", "B": "To introduce and support the claim that bioluminescence is a notable example of convergent evolution", "C": "To explain why some marine species have gone extinct", "D": "To compare bioluminescence with the evolution of eyesight in mammals"},
             "correct": "B", "explanation": "A frase é seguida imediatamente por uma menção a evolução convergente — a menção de evolução independente serve para embasar esse conceito, foco do parágrafo. Nenhuma das outras opções tem base no texto."},
            {"num": "3.6", "prompt": "The word \"striking\" in paragraph 3 is closest in meaning to:",
             "options": {"A": "violent", "B": "notable", "C": "accidental", "D": "doubtful"},
             "correct": "B", "explanation": "\"Striking\" no contexto de \"one of its most striking examples\" significa notável/impressionante. \"Violent\" pertence a outro campo semântico; \"accidental\" e \"doubtful\" invertem o tom confiante do texto."},
        ],
    },
]

# PARTE 5 (Action Drills) do M1, Grupo A: Complete the Words — 5 textos,
# 32 itens ao todo. Fonte: consolidated/modulo_1_reading.md PARTE 5/PARTE 6.
MOD1_ACTION_DRILLS_A = [
    {
        "id": "mod1-a1",
        "title": "Drill A1 · nível A2–B1 · alvo: 4 min",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo alvo: 4 minutos.",
        "passage_html": """<p><strong>TEXT: A message to a friend</strong></p>
<p>Hi Marco,</p>
<p>I'm really sorry, but I have to (1)_____ our plans for Saturday. My sister (2)_____ from Recife that morning and I have to pick her up at the airport. I know we (3)_____ this dinner for weeks, and I feel terrible about it.</p>
<p>Would Sunday afternoon (4)_____ instead? There's a new place near the park that everyone (5)_____ about. If Sunday doesn't work for you, just let me (6)_____ and we'll find another day.</p>
<p>Again, I'm sorry for the short notice.</p>
<p>Talk soon, Lia</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "cancel", "B": "canceling", "C": "to cancel", "D": "cancelled"},
             "correct": "A", "explanation": "\"Have to\" + <strong>verbo base</strong>. As opções (B) <em>canceling</em>, (C) <em>to cancel</em> e (D) <em>cancelled</em> quebram a estrutura \"have to + base\"."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "arrive", "B": "arrives", "C": "arriving", "D": "is arriving"},
             "correct": "D", "explanation": "Compromisso futuro já combinado (\"that morning\") → <strong>presente contínuo com valor de futuro</strong>. (A)/(B) presente simples não expressam plano; (C) <em>arriving</em> sozinho não tem auxiliar."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "plan", "B": "planned", "C": "have been planning", "D": "are planning"},
             "correct": "C", "explanation": "\"For weeks\" + ação iniciada no passado e ainda em curso → <strong>presente perfeito contínuo</strong>. (D) <em>are planning</em> ignora o \"for weeks\"; (A)/(B) não conectam passado e presente."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "work", "B": "works", "C": "working", "D": "worked"},
             "correct": "A", "explanation": "Depois do modal <em>would</em> → <strong>base</strong>. \"Would Sunday afternoon work?\""},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "talk", "B": "talks", "C": "talking", "D": "talked"},
             "correct": "B", "explanation": "<em>Everyone</em> = <strong>singular</strong> → verbo + -s. \"Everyone talks about...\""},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "know", "B": "known", "C": "knowing", "D": "to know"},
             "correct": "A", "explanation": "<em>Let</em> + objeto + <strong>base</strong> (\"let me know\": fórmula fixa). (D) \"let me to know\" é agramatical."},
        ],
    },
    {
        "id": "mod1-a2",
        "title": "Drill A2 · nível B1 · alvo: 4 min",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo alvo: 4 minutos.",
        "passage_html": """<p><strong>TEXT: Notice at a community pool</strong></p>
<p>Starting Monday, the main pool (1)_____ closed for its annual maintenance. We expect the work (2)_____ completed by Friday afternoon. During this period, members (3)_____ still use the smaller training pool, which (4)_____ open at its usual hours.</p>
<p>We apologize for any (5)_____ this may cause. If you have questions about your membership or class schedule, please (6)_____ to speak with the front desk staff, who will be happy to help.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "is", "B": "be", "C": "being", "D": "been"},
             "correct": "A", "explanation": "\"The main pool ___ closed\": voz passiva no presente: <strong>is</strong> + particípio (<em>closed</em>)."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "is", "B": "to be", "C": "being", "D": "be"},
             "correct": "B", "explanation": "\"We expect the work ___ completed\": <em>expect</em> + objeto + <strong>to + infinitivo</strong> (aqui infinitivo passivo <em>to be completed</em>)."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "may", "B": "may to", "C": "maying", "D": "mays"},
             "correct": "A", "explanation": "Modal simples; \"members may still use\". (B) \"may to\" é agramatical: modal nunca leva <em>to</em>."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "remain", "B": "remains", "C": "remaining", "D": "to remain"},
             "correct": "B", "explanation": "Sujeito <em>which</em> retoma <em>the smaller training pool</em> (singular) → <strong>+ -s</strong>."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "inconvenient", "B": "inconveniently", "C": "inconvenience", "D": "inconvenienced"},
             "correct": "C", "explanation": "Depois de <em>any</em>, a lacuna é <strong>substantivo</strong>: \"any inconvenience this may cause\"."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "hesitate", "B": "not hesitate", "C": "don't hesitate", "D": "hesitating"},
             "correct": "C", "explanation": "Fórmula fixa: \"please don't hesitate to...\". (B) \"not hesitate\" sem auxiliar é agramatical num pedido; (A) sozinho inverteria o sentido."},
        ],
    },
    {
        "id": "mod1-a3",
        "title": "Drill A3 · nível B2 · alvo: 5 min",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo alvo: 5 minutos.",
        "passage_html": """<p><strong>TEXT: A message from the office manager</strong></p>
<p>Hi team,</p>
<p>I wanted to send a quick note before the long weekend. As most of you already (1)_____, the building's heating system will be shut down for scheduled maintenance from Friday evening through Monday morning. Please make sure you (2)_____ any equipment that shouldn't be left running unattended, and take home anything that might be sensitive to temperature changes over the weekend.</p>
<p>The maintenance crew has assured us that the work will be (3)_____ before Monday, so there shouldn't be any disruption when everyone (4)_____ back to the office. However, if the weather turns unexpectedly cold, the building may take a little longer than usual to (5)_____ up again — so please dress in layers just in case.</p>
<p>If you have any questions or concerns, don't (6)_____ to reach out to facilities directly. We'd rather you ask a question that turns out to be unnecessary than (7)_____ a real problem over the weekend.</p>
<p>Thanks for your patience, and enjoy the (8)_____ time off!</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "know", "B": "knows", "C": "known", "D": "knowing"},
             "correct": "A", "explanation": "\"As most of you already know\" pede presente simples na 3ª pessoa do plural (forma base, sem -s). (B) quebra a concordância; (C) exigiria auxiliar (\"have known\"); (D) não completa o tempo verbal."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "turn off", "B": "turn down", "C": "turn out", "D": "turn over"},
             "correct": "A", "explanation": "\"Turn off equipment\" = desligar equipamento. (B) = diminuir intensidade; (C) = revelar-se/comparecer; (D) = virar/entregar."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "complete", "B": "completing", "C": "completed", "D": "completes"},
             "correct": "C", "explanation": "\"Will be _____\" pede particípio passado para a voz passiva. As outras formas quebram a estrutura \"be + particípio\"."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "come", "B": "comes", "C": "coming", "D": "will comes"},
             "correct": "B", "explanation": "\"Everyone\" é gramaticalmente singular → 3ª pessoa do singular: \"comes back\". (D) é agramatical (\"will\" nunca é seguido de verbo com -s)."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "warm", "B": "warms", "C": "warmly", "D": "warmth"},
             "correct": "A", "explanation": "\"To _____ up again\" pede o infinitivo (verbo base) após \"to\". \"Warm up\" é o phrasal verb certo para um ambiente recuperando temperatura."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "hesitate", "B": "hesitating", "C": "hesitation", "D": "hesitated"},
             "correct": "A", "explanation": "\"Don't _____ to reach out\" pede verbo base após o imperativo negativo \"don't\". \"Don't hesitate to + verbo\" é expressão fixa."},
            {"num": "7", "prompt": "Lacuna (7)", "options": {"A": "miss", "B": "lose", "C": "waste", "D": "fail"},
             "correct": "B", "explanation": "Estrutura paralela \"ask a question... than _____ a real problem\" pede verbo base após \"than\". \"Lose\" mantém o contraste lógico entre perguntar à toa e deixar um problema real sem solução."},
            {"num": "8", "prompt": "Lacuna (8)", "options": {"A": "extend", "B": "extending", "C": "extended", "D": "extension"},
             "correct": "C", "explanation": "\"The _____ time off\" pede um particípio-adjetivo antes do substantivo. \"Extended time off\" = folga prolongada."},
        ],
    },
    {
        "id": "mod1-a4",
        "title": "Drill A4 · nível B2–C1 · alvo: 5 min",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo alvo: 5 minutos.",
        "passage_html": """<p><strong>TEXT: Museum exhibit information card</strong></p>
<p>This exhibit brings together more than two hundred objects (1)_____ over four decades of fieldwork in the region. Many of them (2)_____ never been displayed publicly before. Together, they offer a rare (3)_____ into daily life in a community that written records largely overlooked.</p>
<p>Visitors are (4)_____ to move through the rooms in order, since the layout follows a rough chronology. Labels have been kept deliberately brief; those who wish to (5)_____ deeper into any single object will find extended notes on the tablets provided at the entrance. Photography without flash (6)_____ permitted throughout, except in the final room, where the light-sensitive textiles require complete darkness.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "collect", "B": "collected", "C": "collecting", "D": "collection"},
             "correct": "B", "explanation": "\"Objects ___ over four decades\": particípio reduzido de \"objects <strong>that were collected</strong>\"."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "has", "B": "have", "C": "had", "D": "having"},
             "correct": "B", "explanation": "Sujeito <em>Many of them</em> (plural) + presente perfeito → \"have never been displayed\". (A) quebra a concordância; (C) mudaria para passado perfeito sem marco; (D) não fecha o tempo."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "window", "B": "door", "C": "mirror", "D": "bridge"},
             "correct": "A", "explanation": "\"A rare ___ into daily life\": collocation fixa — <em>a window into/onto</em> = uma janela para (uma visão de). As outras opções não colocam com \"into daily life\" nesse sentido."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "encourage", "B": "encouraged", "C": "encouraging", "D": "encouragement"},
             "correct": "B", "explanation": "\"Visitors are ___ to move\": voz passiva — <em>are encouraged to</em>. (C) mudaria o sujeito; (A)/(D) não formam o passivo."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "delve", "B": "fall", "C": "drop", "D": "sink"},
             "correct": "A", "explanation": "\"Wish to ___ deeper into any single object\": <em>delve into</em> = aprofundar-se em. As outras opções não colocam com \"deeper into [um tema]\" no sentido de investigar."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "is", "B": "are", "C": "being", "D": "be"},
             "correct": "A", "explanation": "\"Photography without flash ___ permitted\": sujeito <em>Photography</em> (incontável, singular) → <strong>is</strong>."},
        ],
    },
    {
        "id": "mod1-a5",
        "title": "Drill A5 · nível C1 · alvo: 5 min",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo alvo: 5 minutos.",
        "passage_html": """<p><strong>TEXT: Excerpt from an editorial</strong></p>
<p>For decades, the standard response to traffic congestion (1)_____ been to add lanes. The logic seems sound. Yet a growing body of research points to the opposite (2)_____: added lanes tend to attract additional drivers until, within a few years, traffic returns to its former level — a phenomenon known as induced demand. Rarely (3)_____ a policy so intuitive prove so consistently ineffective.</p>
<p>This does not mean nothing (4)_____ be done. It means the solution lies elsewhere: in reliable public transit, in pricing that reflects the true cost of road use, and in land-use decisions that reduce the (5)_____ to drive in the first place. None of these is as politically straightforward as pouring concrete, which is (6)_____ they are so often postponed.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "has", "B": "have", "C": "had", "D": "having"},
             "correct": "A", "explanation": "Sujeito \"the standard response\" = <strong>singular</strong> → \"has been\" (presente perfeito: \"For decades... has been\"). (B) quebra a concordância; (C) pediria um marco no passado; (D) não fecha o tempo."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "conclusion", "B": "decision", "C": "opinion", "D": "suggestion"},
             "correct": "A", "explanation": "\"Points to the opposite ___\": <em>point to a conclusion</em> é a collocation. As outras opções não colocam com \"research points to the opposite ___\"."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "does", "B": "do", "C": "is", "D": "has"},
             "correct": "A", "explanation": "Inversão após <em>Rarely</em> no início da frase → auxiliar <strong>does</strong> + sujeito + base (<em>prove</em>). \"Rarely does a policy... prove...\""},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "can", "B": "can't", "C": "must", "D": "should"},
             "correct": "A", "explanation": "\"This does not mean nothing ___ be done\": dupla negação lógica — \"não significa que nada pode ser feito\". (B) inverteria o sentido; (C)/(D) mudam para obrigação/recomendação, não cabimento."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "need", "B": "want", "C": "wish", "D": "hope"},
             "correct": "A", "explanation": "\"Reduce the ___ to drive\": <em>the need to (do something)</em> = a necessidade de. As outras opções não colocam com essa estrutura."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "why", "B": "because", "C": "how", "D": "what"},
             "correct": "A", "explanation": "\"Which is ___ they are so often postponed\": \"which is why...\" = \"razão pela qual\". (B) precisaria de outra estrutura; (C)/(D) não fecham a relativa."},
        ],
    },
]

# PARTE 5 (Action Drills) do M1, Grupo B: Read in Daily Life — 5 textos
# curtos, 14 itens ao todo.
MOD1_ACTION_DRILLS_B = [
    {
        "id": "mod1-b1",
        "title": "Drill B1 · Placa / aviso · alvo: 2 min",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo alvo: 2 minutos.",
        "passage_html": """<p><strong>TEXT: Sign at a nature reserve trailhead</strong></p>
<blockquote><p><strong>RIDGELINE TRAIL: PLEASE READ BEFORE ENTERING</strong></p>
<p>• Trail open sunrise to sunset. Overnight camping is not permitted anywhere on the reserve.<br>
• Dogs welcome on a leash no longer than 2 metres. The upper loop (marked in red) is closed to dogs from 1 April to 15 July to protect ground-nesting birds.<br>
• No bicycles. E-bikes and mobility scooters are exempt from this rule.<br>
• Pack out all rubbish. There are no bins beyond this point.</p></blockquote>""",
        "items": [
            {"num": "B1.1", "prompt": "A visitor with a dog on 20 May may walk:",
             "options": {"A": "anywhere on the reserve", "B": "on all trails except the upper loop", "C": "only on the upper loop", "D": "nowhere, because dogs are banned in summer"},
             "correct": "B", "explanation": "Cães de coleira são permitidos; o <em>upper loop</em> é fechado a cães de 1/abr a 15/jul, e 20 de maio cai nesse período → todas as trilhas <strong>exceto</strong> o upper loop. (A) ignora a restrição; (C) inverte; (D) exagera — cães não são banidos, só do upper loop."},
            {"num": "B1.2", "prompt": "Which of the following is allowed on the trail?",
             "options": {"A": "A regular bicycle", "B": "An overnight tent", "C": "A mobility scooter", "D": "Leaving food scraps in a bin"},
             "correct": "C", "explanation": "\"E-bikes and mobility scooters are exempt\" da proibição de bicicletas. (A) bicicleta comum é proibida; (B) camping é proibido; (D) não há lixeiras além daquele ponto."},
        ],
    },
    {
        "id": "mod1-b2",
        "title": "Drill B2 · Cardápio · alvo: 3 min",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: Café lunch menu (extract)</strong></p>
<blockquote><p><strong>SANDWICHES</strong>: all served on sourdough with a side salad (swap for fries +$2)</p>
<p>• <strong>Garden</strong> — roasted vegetables, hummus, rocket · $9 · <em>vegan</em><br>
• <strong>Classic Club</strong> (chicken, bacon, egg, lettuce) · $12<br>
• <strong>Halloumi Stack</strong> — grilled halloumi, tomato, pesto · $11 · <em>vegetarian (contains nuts)</em></p>
<p><strong>SOUPS</strong> · served with bread · $7 · soup of the day is always vegetarian; ask staff whether today's is vegan.</p>
<p><em>A 10% discount applies to all lunch orders placed before noon.</em></p></blockquote>""",
        "items": [
            {"num": "B2.1", "prompt": "A customer who is vegan and allergic to nuts could safely order:",
             "options": {"A": "the Halloumi Stack", "B": "the Garden sandwich", "C": "the soup of the day, no questions asked", "D": "the Classic Club without bacon"},
             "correct": "B", "explanation": "<em>Garden</em> é vegan e não tem aviso de nozes. (A) Halloumi Stack tem queijo (não vegan) e <em>contains nuts</em>; (C) a sopa é sempre vegetariana mas <strong>pode não ser vegana</strong> — o texto manda perguntar; (D) Classic Club tem frango e ovo."},
            {"num": "B2.2", "prompt": "A customer orders a Classic Club with fries at 11:45 a.m. Before any discount, the price is:",
             "options": {"A": "$12", "B": "$14", "C": "$9", "D": "$16"},
             "correct": "B", "explanation": "$12 do sanduíche + $2 pela troca por fries = $14. O desconto de 10% (pedido antes do meio-dia) se aplica <strong>depois</strong>, mas a pergunta é o preço <strong>antes</strong> do desconto."},
            {"num": "B2.3", "prompt": "According to the menu, the soup of the day:",
             "options": {"A": "is always vegan", "B": "is always vegetarian, and may or may not be vegan", "C": "never contains bread", "D": "costs more than any sandwich"},
             "correct": "B", "explanation": "\"Soup of the day is always vegetarian; ask staff whether today's is vegan\" — sempre vegetariana, veganidade varia."},
        ],
    },
    {
        "id": "mod1-b3",
        "title": "Drill B3 · E-mail formal · alvo: 3 min",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: Email from a course coordinator</strong></p>
<blockquote>
<p><strong>Subject: Re: Request to submit Assignment 2 late</strong></p>
<p>Dear Bruna,</p>
<p>Thank you for letting me know about your situation in advance rather than after the deadline. I'm sorry to hear you've been unwell.</p>
<p>Our department policy does not allow me to grant extensions longer than 48 hours without a medical certificate. If you're able to provide one, I can extend your deadline to the following Monday. If not, I can still accept the assignment up to 48 hours late, though the standard 10% late penalty would apply in that case.</p>
<p>Please let me know which option you'd prefer by Thursday so I can update the system.</p>
<p>Best regards,<br>Dr. Okafor</p>
</blockquote>""",
        "items": [
            {"num": "B3.1", "prompt": "What is the main purpose of this email?",
             "options": {"A": "To refuse Bruna's request", "B": "To explain the options available and ask Bruna to choose", "C": "To inform Bruna that her assignment is now overdue", "D": "To apologise for a mistake the department made"},
             "correct": "B", "explanation": "O e-mail lista duas opções (com ou sem atestado) e pede que Bruna escolha até quinta. (A) não recusa — oferece alternativas; (C) o trabalho ainda não está atrasado; (D) não houve erro do departamento."},
            {"num": "B3.2", "prompt": "If Bruna does NOT provide a medical certificate, she can:",
             "options": {"A": "submit the assignment by the following Monday with no penalty", "B": "submit up to 48 hours late, losing 10% of the marks", "C": "not submit the assignment at all", "D": "choose her own new deadline"},
             "correct": "B", "explanation": "Sem atestado: aceita até 48h de atraso com penalidade padrão de 10%. (A) descreve a opção <strong>com</strong> atestado; (C)/(D) não constam."},
            {"num": "B3.3", "prompt": "Dr. Okafor's tone is best described as:",
             "options": {"A": "annoyed and dismissive", "B": "formal but sympathetic and helpful", "C": "uncertain and apologetic", "D": "casual and friendly"},
             "correct": "B", "explanation": "Registro formal (<em>Dear... Best regards, Dr. Okafor</em>), mas empático (<em>I'm sorry to hear you've been unwell</em>) e prestativo (oferece soluções). (A)/(C)/(D) não batem com o texto."},
        ],
    },
    {
        "id": "mod1-b4",
        "title": "Drill B4 · Horário / tabela · alvo: 2 min",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo alvo: 2 minutos.",
        "passage_html": """<p><strong>TEXT: Shuttle timetable notice</strong></p>
<blockquote><p><strong>CAMPUS ↔ STATION SHUTTLE</strong></p>
<p>Departs Campus Gate: on the hour and at half past, 7:00–19:00, Mon–Fri. Departs Station: at quarter past and quarter to, same times. Journey time: approximately 20 minutes.</p>
<p><em>The half-past and quarter-to services do not run after 17:00: the last half-past departure from Campus Gate is at 16:30. Weekend and holiday service runs on the hour only.</em></p></blockquote>""",
        "items": [
            {"num": "B4.1", "prompt": "A student wants to leave Campus Gate on a Tuesday at 17:30. On that day there is:",
             "options": {"A": "no 17:30 service — after 17:00 the shuttle leaves on the hour only", "B": "a 17:30 service that arrives at the station around 17:50", "C": "a shuttle only if it is a holiday", "D": "a 17:30 service that takes about 45 minutes"},
             "correct": "A", "explanation": "A nota de rodapé é explícita: \"the last half-past departure from Campus Gate is at 16:30\" e, depois das 17:00, o serviço é \"on the hour only\". Logo, não existe 17:30 na terça-feira. Este item treina a leitura da <strong>nota de rodapé</strong> — quem responde (B) leu só a linha principal e ignorou a exceção."},
            {"num": "B4.2", "prompt": "On a Sunday, a shuttle leaves the Station at:",
             "options": {"A": "quarter past and quarter to every hour", "B": "on the hour only", "C": "half past every hour", "D": "the timetable does not say"},
             "correct": "B", "explanation": "Fim de semana: \"Weekend and holiday service runs on the hour only\". A tabela <em>quarter past / quarter to</em> da estação vale só de segunda a sexta."},
        ],
    },
    {
        "id": "mod1-b5",
        "title": "Drill B5 · Post de rede social · alvo: 3 min",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: A social media post from a local bakery</strong></p>
<blockquote><p>🥐 <strong>Riverside Bakery</strong> · Posted 2 hours ago</p>
<p>Big news, everyone! Starting next Tuesday, we're extending our weekday hours — open at 6:30 AM instead of 7:00 AM, so early risers can grab their coffee and croissants before work. 🌅</p>
<p>Quick heads-up though: because of the earlier opening, our weekday sourdough batch will now go into the oven the night before instead of first thing in the morning. It'll still be baked fresh daily, just on a slightly different schedule — so if you're used to catching it warm right out of the oven at 8 AM, it might be ready a little earlier now. Come say hi and let us know what you think of the new hours!</p>
<p>Weekend hours are unchanged (8 AM–3 PM, same as always).</p></blockquote>""",
        "items": [
            {"num": "B5.1", "prompt": "What is the main purpose of this post?",
             "options": {"A": "To announce that the bakery is closing early on weekdays", "B": "To inform customers about a change to weekday opening hours", "C": "To apologise for a delay in the sourdough baking schedule", "D": "To advertise a new type of bread"},
             "correct": "B", "explanation": "O post inteiro gira em torno de um anúncio: abrir mais cedo nos dias de semana. (A) inverte; (C) não pede desculpas; (D) nenhum pão novo."},
            {"num": "B5.2", "prompt": "According to the post, the weekday sourdough will:",
             "options": {"A": "no longer be baked fresh every day", "B": "only be available on weekends", "C": "be baked the night before instead of the same morning", "D": "be replaced with a different bread"},
             "correct": "C", "explanation": "\"Will now go into the oven the night before\". (A) o texto diz \"still be baked fresh daily\"; (B)/(D) não constam."},
            {"num": "B5.3", "prompt": "What can be inferred about the weekend hours?",
             "options": {"A": "They will also move to 6:30 AM", "B": "They stay the same as before this announcement", "C": "They have not been decided yet", "D": "They will be shortened"},
             "correct": "B", "explanation": "\"Weekend hours are unchanged\". (A)/(D) contradizem; (C) já está decidido."},
            {"num": "B5.4", "prompt": "The overall tone of the post is:",
             "options": {"A": "formal and apologetic", "B": "friendly and informative", "C": "urgent and cautionary", "D": "neutral and impersonal"},
             "correct": "B", "explanation": "Emojis, \"Big news, everyone!\", \"Come say hi\", tom positivo."},
        ],
    },
]

# PARTE 5 (Action Drills) do M1, Grupo C: Read an Academic Passage — 3
# passagens, 21 itens ao todo. C3.7 é múltipla seleção (marcar 3 de 6).
MOD1_ACTION_DRILLS_C = [
    {
        "id": "mod1-c1",
        "title": "Drill C1 · Ciências naturais · alvo: 6 min",
        "objective": "Leia a passagem completa uma vez. Responda às 7 questões. Tempo alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: Bioluminescence in Marine Organisms</strong></p>
<p>Bioluminescence (the production and emission of light by a living organism) is remarkably common in the ocean, appearing in bacteria, jellyfish, fish, and even some sharks. Unlike the light produced by a bulb, which wastes most of its energy as heat, bioluminescent light is generated through a highly efficient chemical reaction, typically involving a light-emitting molecule called luciferin and an enzyme called luciferase. Because so little energy is lost as heat, biologists sometimes refer to this phenomenon as "cold light."</p>
<p>The functions of bioluminescence vary considerably across species, though three purposes appear again and again. Some organisms use light defensively: certain species of squid release a luminous cloud instead of ink, startling predators and buying time to escape. Others use it as a hunting tool. The anglerfish, perhaps the most famous example, dangles a glowing lure above its mouth to attract smaller prey close enough to seize. Still others use light for communication, particularly in the deep sea, where darkness is nearly absolute and visual signals cannot rely on ambient light. Certain species of ostracods, tiny crustaceans, produce synchronized light displays to attract mates.</p>
<p>What makes bioluminescence especially interesting to evolutionary biologists is that it did not evolve just once. Genetic and biochemical evidence indicates that the capacity for bioluminescence has arisen independently dozens of times across unrelated lineages, using different chemical pathways to achieve a similar outcome. This pattern, in which unrelated organisms evolve similar traits independently, is known as convergent evolution, and bioluminescence is considered one of its most striking examples.</p>""",
        "items": [
            {"num": "C1.1", "prompt": "Ideia principal. What is the main idea of the passage?",
             "options": {"A": "Bioluminescence is a rare adaptation found only in a few deep-sea species.", "B": "Bioluminescence is a widespread, chemically efficient trait that serves multiple functions and evolved independently many times.", "C": "The anglerfish is the most important example of bioluminescence.", "D": "Bioluminescent light is less efficient than artificial light."},
             "correct": "B", "explanation": "Cobre os três eixos (o que é + eficiência, funções, evolução independente). (A) contradiz \"remarkably common\"; (C) é detalhe; (D) inverte a comparação com a lâmpada."},
            {"num": "C1.2", "prompt": "Detalhe. Why is bioluminescent light sometimes called \"cold light\"?",
             "options": {"A": "It only occurs in cold, deep-sea environments.", "B": "It is produced by organisms that live in low-temperature waters.", "C": "The reaction that produces it wastes very little energy as heat.", "D": "It appears blue or white, resembling ice."},
             "correct": "C", "explanation": "Relação causal explícita: \"Because so little energy is lost as heat...\". (A)/(B) confundem o nome com temperatura ambiente; (D) infere cor sem base."},
            {"num": "C1.3", "prompt": "Detalhe negativo. Which is NOT mentioned as a function of bioluminescence?",
             "options": {"A": "Startling predators", "B": "Attracting prey", "C": "Attracting mates", "D": "Regulating body temperature"},
             "correct": "D", "explanation": "O parágrafo 2 lista defesa, caça e comunicação/atração de parceiros. Regulação de temperatura nunca aparece."},
            {"num": "C1.4", "prompt": "Inferência. It can be inferred from paragraph 2 that in deep-sea environments:",
             "options": {"A": "visual communication is impossible for any species", "B": "organisms rely on producing their own light because there is little to no ambient light", "C": "most species have lost their sense of sight entirely", "D": "bioluminescence is used only for hunting"},
             "correct": "B", "explanation": "\"Where darkness is nearly absolute and visual signals cannot rely on ambient light\" → produzir a própria luz supre a ausência de luz ambiente. (A) é extremo; (C)/(D) sem base."},
            {"num": "C1.5", "prompt": "Propósito retórico. Why does the author state that bioluminescence \"did not evolve just once\"?",
             "options": {"A": "To argue that bioluminescence is less significant than previously thought", "B": "To introduce and support the claim that it is a notable example of convergent evolution", "C": "To explain why some marine species have gone extinct", "D": "To compare bioluminescence with the evolution of eyesight in mammals"},
             "correct": "B", "explanation": "A frase é seguida por \"...one of its most striking examples\" — serve para embasar o conceito de evolução convergente."},
            {"num": "C1.6", "prompt": "Vocabulário em contexto. The word \"striking\" in paragraph 3 is closest in meaning to:",
             "options": {"A": "violent", "B": "notable", "C": "accidental", "D": "doubtful"},
             "correct": "B", "explanation": "\"One of its most striking examples\" = exemplo notável. (A)/(C)/(D) pertencem a outros campos ou invertem o tom."},
            {"num": "C1.7", "prompt": "Simplificação de frase. Which best expresses the essential information in the highlighted sentence? <em>\"This pattern, in which unrelated organisms evolve similar traits independently, is known as convergent evolution, and bioluminescence is considered one of its most striking examples.\"</em>",
             "options": {"A": "Convergent evolution explains why all sea creatures glow.", "B": "When unrelated organisms independently develop the same trait, the process is called convergent evolution, and bioluminescence is a prime example of it.", "C": "Bioluminescence is the only known case of convergent evolution.", "D": "Evolutionary biologists disagree about whether bioluminescence is truly convergent."},
             "correct": "B", "explanation": "A frase original define evolução convergente e diz que a bioluminescência é um exemplo marcante. (B) preserva as duas ideias. (A) exagera (\"all sea creatures\"); (C) inventa exclusividade; (D) inventa controvérsia."},
        ],
    },
    {
        "id": "mod1-c2",
        "title": "Drill C2 · História · alvo: 6 min",
        "objective": "Leia a passagem completa uma vez. Responda às 7 questões. Tempo alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: Coffee Houses in Seventeenth-Century England</strong></p>
<p>The first English coffee house opened in Oxford in 1650; within two decades, London alone had hundreds. <strong>[■A]</strong> For the price of a single cup (a penny) a customer could sit for hours, read the newspapers provided by the house, and join whatever conversation was underway. <strong>[■B]</strong> Because admission was cheap and open to any man who could pay, the coffee house mixed people who rarely met elsewhere: merchants, scholars, clergymen, and minor gentry sat at the same long tables. <strong>[■C]</strong></p>
<p>This mixing had consequences that reached well beyond casual talk. Particular houses became known for particular subjects. Men interested in maritime insurance gathered at Lloyd's; those following scientific debates went to the houses near the Royal Society. <strong>[■D]</strong> Information that had once circulated slowly, by letter or rumour, now moved quickly through these rooms. Some historians argue that the coffee house functioned as an early public sphere: a space where opinion could form through discussion rather than being handed down by church or crown.</p>
<p>The authorities were not comfortable with this. In 1675, the king issued a proclamation ordering the coffee houses closed, on the grounds that they spread "false, malicious and scandalous reports." The order provoked such immediate opposition that it was withdrawn within days. The houses continued to operate for another century, gradually giving way to private clubs and, eventually, to the institutions that had first taken shape around their tables.</p>""",
        "items": [
            {"num": "C2.1", "prompt": "Ideia principal. The passage is mainly about:",
             "options": {"A": "how coffee was first imported into England", "B": "how English coffee houses became important centres of information and public discussion", "C": "why the king disliked coffee", "D": "the architecture of seventeenth-century London"},
             "correct": "B", "explanation": "O texto traça como as coffee houses viraram centros de informação e discussão pública. (A)/(C)/(D) são detalhes ou não constam."},
            {"num": "C2.2", "prompt": "Detalhe. According to the passage, a customer who paid a penny could:",
             "options": {"A": "buy unlimited cups of coffee", "B": "stay for hours, read the newspapers, and take part in conversation", "C": "join the Royal Society", "D": "rent a private room"},
             "correct": "B", "explanation": "\"Could sit for hours, read the newspapers provided by the house, and join whatever conversation was underway\"."},
            {"num": "C2.3", "prompt": "Inferência. It can be inferred that before coffee houses existed, information among these groups:",
             "options": {"A": "did not exist at all", "B": "travelled more slowly and less widely", "C": "was controlled entirely by merchants", "D": "was freely available to everyone"},
             "correct": "B", "explanation": "\"Information that had once circulated slowly, by letter or rumour, now moved quickly\" → antes, mais devagar e menos amplamente. (A) exagera; (C)/(D) sem base."},
            {"num": "C2.4", "prompt": "Propósito retórico. Why does the author mention Lloyd's and the houses near the Royal Society?",
             "options": {"A": "To show that different coffee houses specialised in different topics", "B": "To argue that Lloyd's was the most important coffee house", "C": "To explain how coffee houses were decorated", "D": "To prove that scientists disliked merchants"},
             "correct": "A", "explanation": "\"Particular houses became known for particular subjects\": Lloyd's e as casas perto da Royal Society ilustram a especialização por tema."},
            {"num": "C2.5", "prompt": "Detalhe. The king's 1675 proclamation was:",
             "options": {"A": "enforced for a century", "B": "withdrawn within days after strong opposition", "C": "welcomed by most coffee house owners", "D": "never actually issued"},
             "correct": "B", "explanation": "\"The order provoked such immediate opposition that it was withdrawn within days.\""},
            {"num": "C2.6", "prompt": "Vocabulário em contexto. The word \"provoked\" in paragraph 3 is closest in meaning to:",
             "options": {"A": "prevented", "B": "caused", "C": "delayed", "D": "forgave"},
             "correct": "B", "explanation": "\"Provoked such... opposition\" = causou/gerou oposição."},
            {"num": "C2.7", "prompt": "Inserir frase. Where would the following sentence best fit? <em>\"Even those who could not read had access to the news, since the sheets were often read aloud at the tables.\"</em>",
             "options": {"A": "At [■A]", "B": "At [■B]", "C": "At [■C]", "D": "At [■D]"},
             "correct": "B", "explanation": "A frase estende a ideia dos <em>newspapers provided by the house</em>: \"the sheets\" retoma \"the newspapers\", e \"read aloud at the tables\" continua a descrição do que os clientes faziam. [■A] vem <strong>antes</strong> de os jornais serem mencionados — o pronome \"the sheets\" não teria referente. [■C] separaria a ideia de \"misturar pessoas\" da sua consequência. [■D] está no parágrafo errado."},
        ],
    },
    {
        "id": "mod1-c3",
        "title": "Drill C3 · Ciências sociais · alvo: 6 min",
        "objective": "Leia a passagem completa uma vez. Responda às 7 questões (a última pede 3 respostas). Tempo alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: The Strength of Weak Ties</strong></p>
<p>When people look for a new job, common sense suggests they should turn to their closest contacts: family and good friends who know them well and want to help. In a study of professionals who had recently changed jobs, the sociologist Mark Granovetter found the opposite. Most had heard about their new position not from a close friend but from an acquaintance: someone they saw only occasionally and would not have described as part of their inner circle.</p>
<p>Granovetter's explanation rests on how information moves through social networks. Your close friends tend to know one another and to move in the same circles you do. As a result, they are exposed to more or less the same information you already have; what they can tell you, you have often already heard. An acquaintance, by contrast, moves in a different circle, encounters different people, and hears different news. A weak tie is therefore a bridge to parts of the network you could not otherwise reach.</p>
<p>The finding has been extended well beyond job-hunting. Weak ties have been linked to the spread of new ideas between organisations, to the circulation of information during emergencies, and to innovation within companies, where teams connected to many outside groups tend to produce more original work. Critics note that weak ties are not always advantageous: they carry less trust, and acting on information from a near-stranger involves more risk. But the core insight has held up: the contacts most likely to tell you something genuinely new are often the ones you know least well.</p>""",
        "items": [
            {"num": "C3.1", "prompt": "Ideia principal. The main idea of the passage is that:",
             "options": {"A": "close friends are the best source of job information", "B": "acquaintances (\"weak ties\") are often better than close contacts at providing genuinely new information, because they connect us to other parts of a social network", "C": "social networks have no effect on how people find jobs", "D": "Granovetter's study has been completely disproved"},
             "correct": "B", "explanation": "Tese central: weak ties frequentemente trazem informação mais nova porque conectam a outras partes da rede. (A) contradiz o achado; (C)/(D) distorcem."},
            {"num": "C3.2", "prompt": "Detalhe. In Granovetter's study, most professionals heard about their new job from:",
             "options": {"A": "a family member", "B": "a close friend", "C": "an acquaintance they saw only occasionally", "D": "a recruitment agency"},
             "correct": "C", "explanation": "\"Most had heard about their new position not from a close friend but from an acquaintance.\""},
            {"num": "C3.3", "prompt": "Detalhe. According to the passage, close friends tend to give us information that:",
             "options": {"A": "is completely new to us", "B": "we have often already heard, because they move in the same circles we do", "C": "is always more trustworthy and therefore more useful", "D": "comes from outside our network"},
             "correct": "B", "explanation": "\"They are exposed to more or less the same information you already have; what they can tell you, you have often already heard.\""},
            {"num": "C3.4", "prompt": "Inferência. It can be inferred that a person whose contacts are ALL close friends would:",
             "options": {"A": "have access to a wider range of information than average", "B": "be more likely to hear the same information repeatedly and less likely to hear news from distant parts of the network", "C": "never be able to find a job", "D": "be more innovative at work"},
             "correct": "B", "explanation": "Se todos os contatos são amigos próximos, que circulam nos mesmos círculos → informação repetida, pouca novidade de partes distantes. (A) inverte; (C)/(D) exageram."},
            {"num": "C3.5", "prompt": "Propósito retórico. Why does the author mention innovation within companies in paragraph 3?",
             "options": {"A": "To give an example of how the weak-ties finding applies beyond job-hunting", "B": "To argue that companies should fire employees with weak ties", "C": "To contradict Granovetter's original study", "D": "To explain how companies are structured"},
             "correct": "A", "explanation": "O parágrafo 3 lista extensões do achado além da busca de emprego; a inovação nas empresas é um desses exemplos."},
            {"num": "C3.6", "prompt": "Vocabulário em contexto. The word \"bridge\" in paragraph 2 is closest in meaning to:",
             "options": {"A": "obstacle", "B": "connection", "C": "copy", "D": "competitor"},
             "correct": "B", "explanation": "\"A bridge to parts of the network you could not otherwise reach\" = uma ponte/conexão."},
            {"num": "C3.7", "prompt": "Resumo (marque as 3 ideias principais). Introductory sentence: <em>\"Granovetter's research challenged the assumption that close contacts are the most useful source of information.\"</em> Select the THREE choices that express the most important ideas.",
             "options": {
                 "A": "His study found that most job-changers had heard about their position from an acquaintance rather than a close friend.",
                 "B": "Weak ties are valuable because they connect us to circles (and information) we could not otherwise reach.",
                 "C": "The first English coffee house opened in Oxford in 1650.",
                 "D": "The finding applies well beyond job-hunting, including to the spread of ideas and to workplace innovation.",
                 "E": "Acquaintances are always more trustworthy than close friends.",
                 "F": "Granovetter interviewed exactly one hundred professionals.",
             },
             "correct": "A,B,D", "multi": 3,
             "explanation": "(A), (B) e (D) são as três ideias principais que parágrafos inteiros sustentam. (C) é de outra passagem (coffee houses) — distrator clássico de resumo; (E) contradiz o texto (\"they carry less trust\"); (F) é um detalhe numérico inventado, não consta no texto."},
        ],
    },
]

MOD2_DRILLS = [
    {
        "id": "mod2-d1",
        "title": "Drill 1 — Listen and Choose a Response (Escala 0 — Sem Anotação)",
        "objective": "Leia cada fala UMA vez, sem reler. Escolha a resposta que soa mais natural e pragmaticamente correta. Tempo alvo: 12 segundos por item. Simula o ritmo do router — cada item é um estímulo independente, sem passagem compartilhada.",
        "passage_html": None,
        "items": [
            {"num": "1", "prompt": "Speaker: \"I was going to grab lunch before the seminar, but I don't think there's enough time now.\"",
             "options": {"A": "\"That's fine, I already ate breakfast.\"", "B": "\"Yeah, we should probably just head straight there.\"", "C": "\"The seminar was actually really interesting.\"", "D": "\"I had lunch there last week too.\""},
             "correct": "B", "explanation": "O falante sinaliza falta de tempo para almoçar; a resposta natural reconhece isso e propõe a ação consequente (ir direto). As outras opções ignoram a urgência mencionada."},
            {"num": "2", "prompt": "Speaker: \"Do you mind if I borrow your notes from Tuesday's class? I was out sick.\"",
             "options": {"A": "\"Sure, no problem — I'll send them over tonight.\"", "B": "\"I hope you feel better soon, though.\"", "C": "\"Tuesday's class was canceled, actually.\"", "D": "\"I wasn't there either, unfortunately.\""},
             "correct": "A", "explanation": "Pedido direto exige resposta direta de concessão. (A) concede e oferece um plano concreto; as outras mudam de assunto ou não respondem ao pedido."},
            {"num": "3", "prompt": "Speaker: \"Honestly, I'm not sure this draft is ready to submit.\"",
             "options": {"A": "\"The deadline isn't until Friday, right?\"", "B": "\"What do you think it still needs?\"", "C": "\"I already submitted mine yesterday.\"", "D": "\"That's a great title for it.\""},
             "correct": "B", "explanation": "O falante expressa insegurança sobre a qualidade do rascunho; a resposta natural busca entender o problema específico. As outras ignoram a preocupação expressa."},
            {"num": "4", "prompt": "Speaker: \"You're not still planning to walk to campus in this weather, are you?\"",
             "options": {"A": "\"No, I'll probably catch the bus instead.\"", "B": "\"The campus is only ten minutes away.\"", "C": "\"I walked there yesterday, actually.\"", "D": "\"It rained a lot last semester too.\""},
             "correct": "A", "explanation": "É uma pergunta retórica que expressa preocupação com o plano; a resposta natural revisa o plano. As outras reforçam o plano problemático ou são irrelevantes."},
            {"num": "5", "prompt": "Speaker: \"I heard the registrar's office changed their hours.\"",
             "options": {"A": "\"I registered for four classes this term.\"", "B": "\"Really? Do you know the new schedule?\"", "C": "\"The office is on the second floor.\"", "D": "\"I haven't registered for anything yet.\""},
             "correct": "B", "explanation": "Informação nova é compartilhada; a resposta natural demonstra interesse e busca detalhe. (A) e (D) confundem \"registrar-se\" com \"registrar\" no sentido de horário; (C) não responde à informação dada."},
        ],
    },
    {
        "id": "mod2-d2",
        "title": "Drill 2 — Listen to a Conversation (Escala 1 — Nota Mínima)",
        "objective": "Leia a transcrição UMA vez, anotando apenas o essencial (3–5 palavras por turno relevante). Depois responda às 4 questões usando só suas notas mínimas. Tempo alvo: 3 minutos total.",
        "passage_html": """<p><strong>TRANSCRIPT — AT THE STUDENT ADVISING OFFICE</strong></p>
<p><em>Narrator: Listen to a conversation between a student and an academic advisor.</em></p>
<p><strong>Student:</strong> Hi, I wanted to ask about switching one of my electives. I'm currently in Intro to Statistics, but I think I'd rather take the Data Visualization course instead.</p>
<p><strong>Advisor:</strong> Sure, let me check... okay, Data Visualization does have space. But just so you know, it has Statistics as a prerequisite — have you completed that already?</p>
<p><strong>Student:</strong> No, that's actually why I wanted to switch — I was hoping to take Data Visualization first and Statistics later.</p>
<p><strong>Advisor:</strong> Ah, I see. Unfortunately, that's not possible — the prerequisite is enforced by the system. You'd need to complete Statistics first, or get a written waiver from the Data Visualization instructor.</p>
<p><strong>Student:</strong> Okay, that makes sense. Is it worth asking the instructor directly, or is that rarely approved?</p>
<p><strong>Advisor:</strong> It's approved sometimes, especially if you have relevant experience — like a coding background. Do you have any?</p>
<p><strong>Student:</strong> I do, actually — I took two programming courses last year.</p>
<p><strong>Advisor:</strong> Then it's worth emailing her. I'll send you her contact information right now.</p>""",
        "items": [
            {"num": "1", "prompt": "Gist-Purpose — Why does the student visit the advising office?",
             "options": {"A": "To complain about a scheduling conflict between two required courses", "B": "To request a change from one elective course to another", "C": "To ask for help registering for classes for the first time", "D": "To find out why she was removed from a course roster"},
             "correct": "B", "explanation": "A estudante afirma diretamente que quer trocar de eletiva. Não há conflito de horário mencionado, ela já está matriculada, e (D) nunca é mencionado."},
            {"num": "2", "prompt": "Detail — What problem does the advisor identify?",
             "options": {"A": "The Data Visualization course is already full for the semester", "B": "The student has already failed the Statistics prerequisite once", "C": "Data Visualization requires Statistics as a prerequisite, which the student hasn't completed", "D": "The student is not eligible to take electives outside her major"},
             "correct": "C", "explanation": "A conselheira explica claramente o pré-requisito não cumprido. (A) é o oposto (há vaga); (B) e (D) nunca são mencionados."},
            {"num": "3", "prompt": "Understanding the Function — Why does the advisor ask whether the student has a coding background?",
             "options": {"A": "To determine whether the student qualifies for a separate scholarship", "B": "To suggest that the student consider switching majors entirely", "C": "To assess whether the instructor might realistically grant a prerequisite waiver", "D": "To recommend an entirely different course better suited to her skills"},
             "correct": "C", "explanation": "A pergunta serve para avaliar se a estudante tem chance real de conseguir uma dispensa do pré-requisito. As outras opções não têm base no texto."},
            {"num": "4", "prompt": "Detail — What does the advisor do at the end of the conversation?",
             "options": {"A": "She enrolls the student in Data Visualization immediately", "B": "She provides the student with the instructor's contact information", "C": "She schedules a follow-up meeting for the following week", "D": "She tells the student to wait until the next semester to decide"},
             "correct": "B", "explanation": "A conselheira diz que vai enviar o contato da professora — direto e literal. A matrícula não acontece nesta conversa, e (C)/(D) não são mencionados."},
        ],
    },
    {
        "id": "mod2-d3",
        "title": "Drill 3 — Listen to an Announcement (Escala 1 — Checklist Auditiva)",
        "objective": "Leia UMA vez. Anote apenas os pontos de checklist (data / local / ação / exceção). Tempo alvo: 2 minutos total.",
        "passage_html": """<p><strong>TRANSCRIPT — CAMPUS ANNOUNCEMENT</strong></p>
<p><em>Narrator: Listen to an announcement about a change to library services.</em></p>
<p><strong>Speaker:</strong> Attention, students. Starting next Monday, the Main Library's reading room on the third floor will be closed for renovation through the end of the month. During this period, students will be able to use the East Wing reading room instead, which will remain open on its regular schedule. Please note that reserved study rooms originally booked for the third floor have already been automatically transferred to the East Wing — you do not need to rebook them. However, if your reservation was for a room with audiovisual equipment, please double-check availability, since not all East Wing rooms are equipped. Questions can be directed to the circulation desk.</p>""",
        "items": [
            {"num": "5", "prompt": "Detail — When does the reading room closure begin?",
             "options": {"A": "Immediately, starting today", "B": "Next Monday", "C": "At the end of the month", "D": "Next semester"},
             "correct": "B", "explanation": "\"Starting next Monday... will be closed\" — literal e direto. As outras opções distorcem a data."},
            {"num": "6", "prompt": "Detail — According to the announcement, what happens to previously reserved study rooms?",
             "options": {"A": "They are automatically canceled and must be rebooked", "B": "They are automatically transferred to the East Wing", "C": "They remain in the third floor despite the renovation", "D": "They are only honored if confirmed by email in advance"},
             "correct": "B", "explanation": "O texto afirma isso diretamente. (A) é o oposto; (C) contradiz a informação central; (D) adiciona uma condição não mencionada."},
            {"num": "7", "prompt": "Understanding the Function — Why does the speaker mention audiovisual equipment specifically?",
             "options": {"A": "To announce that all audiovisual equipment is being permanently removed", "B": "To recommend that students avoid using audiovisual equipment during renovations", "C": "To warn students that not every transferred room has the same equipment as before", "D": "To advertise a new audiovisual equipment rental service in the East Wing"},
             "correct": "C", "explanation": "É um aviso prático para quem reservou salas com equipamento, não uma remoção geral nem uma recomendação de evitar uso."},
        ],
    },
    {
        "id": "mod2-d4",
        "title": "Drill 4 — Listen to an Academic Talk (Escala 2 — Template Reduzido)",
        "objective": "Leia UMA vez, preenchendo o template reduzido. Depois responda as 5 questões com o texto coberto. Tempo alvo: 4 minutos total.",
        "passage_html": """<p><strong>TRANSCRIPT — ACADEMIC TALK: THE PARADOX OF CHOICE</strong></p>
<p><em>Narrator: Listen to part of a talk in a psychology class.</em></p>
<p><strong>Professor:</strong> So we've been discussing decision-making, and today I want to bring up something researchers call the paradox of choice. The basic idea is counterintuitive: you'd think more options would always make us happier, but past a certain point, it actually does the opposite.</p>
<p>Here's a classic example. In one well-known study, researchers set up a tasting table in a grocery store — first with six varieties of jam, then later with twenty-four varieties. You'd expect the bigger display to sell more, right? Actually, the smaller display generated significantly more purchases. The larger display attracted more browsers, but far fewer of them actually bought anything.</p>
<p>Why does this happen? Researchers point to two things: decision fatigue and anticipated regret. With more options, comparing them mentally becomes exhausting — that's decision fatigue. And once you do pick something, you start second-guessing whether one of the twenty-three other jams would've been better — that's anticipated regret. Ironically, having more choices can leave people feeling like they're back to square one, unable to commit to anything at all.</p>
<p>Now, this doesn't mean choice itself is bad — a complete absence of options is its own problem. The point is that there's a sweet spot, and past it, additional options stop helping and start actively working against us.</p>""",
        "items": [
            {"num": "8", "prompt": "Gist-Content — What is the main idea of this talk?",
             "options": {"A": "Grocery stores should always minimize the number of products they display", "B": "Beyond a certain point, having more options can reduce satisfaction and hinder decisions", "C": "Consumers always prefer smaller displays regardless of the product involved", "D": "Decision fatigue only affects people making purchases in physical stores"},
             "correct": "B", "explanation": "A tese central é anunciada logo no início e reforçada no fechamento (\"there's a sweet spot...\"). As outras opções são extremas demais ou fora do escopo do texto."},
            {"num": "9", "prompt": "Detail — In the jam study described, what happened with the larger display of 24 varieties?",
             "options": {"A": "It attracted more browsers but resulted in fewer actual purchases", "B": "It resulted in both more browsers and more purchases than the smaller display", "C": "It was removed from the store due to low customer interest", "D": "It produced identical sales results to the smaller display"},
             "correct": "A", "explanation": "Literal: \"attracted more browsers, but far fewer of them actually bought anything.\" (B) é o oposto; (C) e (D) não têm base no texto."},
            {"num": "10", "prompt": "Understanding Organization — Why does the professor describe the grocery store study in detail?",
             "options": {"A": "To criticize the methodology used by the original researchers", "B": "To provide concrete evidence supporting the paradox of choice", "C": "To introduce an unrelated topic about consumer marketing", "D": "To explain how grocery stores design their product displays"},
             "correct": "B", "explanation": "O estudo é apresentado logo após o conceito abstrato ser introduzido — função clássica de exemplo de apoio."},
            {"num": "11", "prompt": "Making Inferences — What can be inferred about the professor's view on having zero options available?",
             "options": {"A": "It would likely be preferable to having too many options", "B": "It would also be problematic, just as too many options are", "C": "It has never been studied by researchers in this field", "D": "It only applies to situations involving grocery shopping"},
             "correct": "B", "explanation": "O professor afirma que \"a complete absence of options is its own problem\" — implica diretamente que zero opções também é problemático."},
            {"num": "12", "prompt": "Vocabulary in Context — What does the professor mean by the expression \"back to square one\"?",
             "options": {"A": "Making a confident, well-informed final decision", "B": "Returning to a starting point without having made any real progress", "C": "Choosing the first option that was originally presented", "D": "Comparing two options systematically before deciding"},
             "correct": "B", "explanation": "É uma expressão idiomática que significa voltar ao ponto de partida sem progresso real — coerente com o contexto de indecisão."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo A: Listen and Choose a Response —
# 12 itens, sem passagem compartilhada (cada item é um estímulo independente,
# igual ao formato do diagnóstico do M0).
MOD2_ACTION_DRILLS_A = [
    {
        "id": "mod2-a",
        "title": None,
        "objective": "Escolha a resposta mais natural e pragmaticamente adequada a cada fala. Tempo alvo: 12 segundos por item.",
        "passage_html": None,
        "items": [
            {"num": "A1", "prompt": "\"I was going to grab lunch before the seminar, but there's no time now.\"",
             "options": {"A": "That's fine, I had a big breakfast.", "B": "Yeah, let's just head straight there.", "C": "The seminar was really interesting.", "D": "I ate there last week too."},
             "correct": "B", "explanation": "O falante sinaliza falta de tempo; a resposta natural propõe a ação consequente. (A)/(C)/(D) ignoram a urgência."},
            {"num": "A2", "prompt": "\"Do you mind if I borrow your notes from Tuesday? I was out sick.\"",
             "options": {"A": "Sure — I'll send them over tonight.", "B": "I hope you feel better soon.", "C": "Tuesday's class was canceled, actually.", "D": "I wasn't there either, unfortunately."},
             "correct": "A", "explanation": "Pedido direto → resposta direta de concessão + plano. (B) é gentil mas não responde ao pedido; (C)/(D) mudam de assunto."},
            {"num": "A3", "prompt": "\"Honestly, I'm not sure this draft is ready to submit.\"",
             "options": {"A": "The deadline's not until Friday, right?", "B": "What do you think it still needs?", "C": "I submitted mine yesterday.", "D": "That's a great title."},
             "correct": "B", "explanation": "Insegurança sobre o rascunho → resposta busca o problema específico. (A) muda para prazo; (C)/(D) ignoram a preocupação."},
            {"num": "A4", "prompt": "\"You're not still planning to walk in this weather, are you?\"",
             "options": {"A": "No, I'll catch the bus instead.", "B": "Campus is only ten minutes away.", "C": "I walked there yesterday.", "D": "It rained a lot last semester too."},
             "correct": "A", "explanation": "Pergunta retórica = alerta educado sobre andar na chuva. Resposta natural revisa o plano. (B)/(C) reforçam o plano problemático."},
            {"num": "A5", "prompt": "\"I heard the registrar's office changed their hours.\"",
             "options": {"A": "I registered for four classes this term.", "B": "Really? Do you know the new schedule?", "C": "The office is on the second floor.", "D": "I haven't registered for anything yet."},
             "correct": "B", "explanation": "Informação nova (mudança de horário) → interesse + pedido de detalhe. (A)/(D) confundem <em>register</em> (matricular-se) com <em>hours</em>. (C) é verdade, mas não é o que foi dito."},
            {"num": "A6", "prompt": "\"Could you run your presentation by me before the meeting?\"",
             "options": {"A": "I ran three miles this morning.", "B": "Sure — are you free around four?", "C": "The meeting's been moved to Thursday.", "D": "I've given that presentation twice already."},
             "correct": "B", "explanation": "\"Run X by me\" = me mostrar antes. Resposta natural marca um horário. (A) toma \"run\" ao pé da letra; (C) muda o foco; (D) ignora o pedido."},
            {"num": "A7", "prompt": "\"I thought the lab report was due next week, not tomorrow.\"",
             "options": {"A": "So did I — let me double-check the syllabus.", "B": "The lab is on the ground floor.", "C": "I finished my report last month.", "D": "Next week works better for me too."},
             "correct": "A", "explanation": "Divergência sobre a data → confirmar juntos, checar o syllabus. (B)/(C)/(D) ignoram a divergência."},
            {"num": "A8", "prompt": "\"Would you rather present first or last?\"",
             "options": {"A": "I presented last time.", "B": "Last, if that's an option — I need time to prepare.", "C": "The presentation is worth 20% of the grade.", "D": "First place goes to the best presentation."},
             "correct": "B", "explanation": "Pergunta de preferência (primeiro ou último) → escolher e justificar. (A)/(C)/(D) não respondem à escolha oferecida."},
            {"num": "A9", "prompt": "\"This bus is taking forever. We should've left earlier.\"",
             "options": {"A": "The bus stop is right over there.", "B": "Tell me about it — I hate cutting it this close.", "C": "I take this bus every day.", "D": "We left at eight, same as always."},
             "correct": "B", "explanation": "Reclamação sobre a demora → \"Tell me about it\" concorda enfaticamente + acrescenta. (A)/(C)/(D) mudam o foco."},
            {"num": "A10", "prompt": "\"Professor Lin said she might cancel Friday's class.\"",
             "options": {"A": "She's a great lecturer, isn't she?", "B": "Did she say why, or was it just a maybe?", "C": "Friday's class is in the east building.", "D": "I've never had a class canceled before."},
             "correct": "B", "explanation": "Notícia incerta (\"might cancel\") → pedir esclarecimento sobre o motivo/certeza. (A)/(C)/(D) desviam."},
            {"num": "A11", "prompt": "\"I've been meaning to ask: how did the interview go?\"",
             "options": {"A": "It's at two o'clock on Thursday.", "B": "Better than I expected, actually. They said they'd call by Friday.", "C": "I've had a lot of interviews lately.", "D": "The company is downtown, near the station."},
             "correct": "B", "explanation": "Pergunta sobre como foi a entrevista → dar o resultado + próximo passo. (A) responde sobre horário; (C)/(D) generalizam/desviam."},
            {"num": "A12", "prompt": "\"Do you think it's worth applying? I doubt I'd get in.\"",
             "options": {"A": "The application fee is fifty dollars.", "B": "You never know unless you try — I'd go for it.", "C": "I applied there two years ago.", "D": "It's a very competitive program."},
             "correct": "B", "explanation": "Dúvida + autodepreciação → encorajamento. (A)/(C)/(D) desviam para custo, experiência passada, competitividade."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo B: Listen to a Conversation — 3
# diálogos, 12 itens ao todo.
MOD2_ACTION_DRILLS_B = [
    {
        "id": "mod2-b1",
        "title": "Drill B1 · Advising Office · alvo: 3 min",
        "objective": "Leia o diálogo (ou peça pra alguém ler em voz alta) e responda às 4 questões. Tempo alvo: 3 minutos.",
        "passage_html": """<p><em>Narrator: Listen to a conversation between a student and an academic advisor.</em></p>
<p><strong>Student:</strong> Hi, I wanted to ask about switching one of my electives. I'm in Intro to Statistics, but I'd rather take Data Visualization instead.</p>
<p><strong>Advisor:</strong> Let me check... okay, Data Visualization has space. But it has Statistics as a prerequisite — have you completed that?</p>
<p><strong>Student:</strong> No, that's why I wanted to switch — I was hoping to take Data Visualization first and Statistics later.</p>
<p><strong>Advisor:</strong> Ah. Unfortunately that's not possible; the prerequisite is enforced by the system. You'd need to finish Statistics first, or get a written waiver from the Data Visualization instructor.</p>
<p><strong>Student:</strong> Is it worth asking her directly, or is that rarely approved?</p>
<p><strong>Advisor:</strong> It's approved sometimes, especially if you have relevant experience — a coding background, say. Do you have any?</p>
<p><strong>Student:</strong> I do, actually — I took two programming courses last year.</p>
<p><strong>Advisor:</strong> Then it's worth emailing her. I'll send you her contact information now.</p>""",
        "items": [
            {"num": "B1.1", "prompt": "Gist-purpose. Why does the student visit the advising office?",
             "options": {"A": "To complain about a scheduling conflict between two required courses", "B": "To request a change from one elective to another", "C": "To register for classes for the first time", "D": "To find out why she was removed from a course"},
             "correct": "B", "explanation": "A estudante quer \"switch one of my electives\". (A) sem conflito de horário; (C) já está matriculada; (D) está fora do que foi dito."},
            {"num": "B1.2", "prompt": "Detail. What problem does the advisor identify?",
             "options": {"A": "Data Visualization is already full", "B": "The student failed Statistics once already", "C": "Data Visualization requires Statistics, which the student hasn't taken", "D": "The student can't take electives outside her major"},
             "correct": "C", "explanation": "\"It has Statistics as a prerequisite... you'd need to complete Statistics first.\" (A) é o oposto (há vaga); (B)/(D) não ditos."},
            {"num": "B1.3", "prompt": "Function. Why does the advisor ask whether the student has a coding background?",
             "options": {"A": "To check whether she qualifies for a scholarship", "B": "To suggest she switch majors", "C": "To assess whether the instructor might realistically grant a waiver", "D": "To recommend a different course"},
             "correct": "C", "explanation": "A pergunta avalia se a professora poderia dar um <em>waiver</em>. (A)/(B)/(D) sem base no diálogo."},
            {"num": "B1.4", "prompt": "Detail. What does the advisor do at the end?",
             "options": {"A": "Enrolls the student in Data Visualization", "B": "Gives the student the instructor's contact information", "C": "Schedules a follow-up meeting", "D": "Tells the student to wait until next semester"},
             "correct": "B", "explanation": "\"I'll send you her contact information now.\" (A) a matrícula não é feita ali; (C)/(D) não ditos."},
        ],
    },
    {
        "id": "mod2-b2",
        "title": "Drill B2 · Library Reserve Desk · alvo: 3 min",
        "objective": "Leia o diálogo (ou peça pra alguém ler em voz alta) e responda às 4 questões. Tempo alvo: 3 minutos.",
        "passage_html": """<p><em>Narrator: Listen to a conversation between a student and a librarian.</em></p>
<p><strong>Student:</strong> Hi — I'm looking for a book my professor put on reserve for the history seminar. It's <em>The Making of the Atlantic World</em>.</p>
<p><strong>Librarian:</strong> Let me look... yes, we have two copies on reserve. Reserve items are two-hour loans, in-library use only. You can't take them out of the building.</p>
<p><strong>Student:</strong> Oh. I was hoping to take it home for the weekend — the essay's due Monday.</p>
<p><strong>Librarian:</strong> For reserve items, no, sorry. But here's an option: there's a circulating copy in the stacks, on the fourth floor. That one you <em>can</em> take out, for three weeks.</p>
<p><strong>Student:</strong> Great, I'll grab that instead. Is it available right now?</p>
<p><strong>Librarian:</strong> The catalog says one copy is in. If it's not on the shelf, come back and I'll place a hold on the reserve copy for you to use here.</p>
<p><strong>Student:</strong> Thanks — I'll check the stacks first.</p>""",
        "items": [
            {"num": "B2.1", "prompt": "Gist-purpose. What is the student trying to do?",
             "options": {"A": "Return an overdue book", "B": "Get a book she needs for an essay due Monday", "C": "Renew a book she already borrowed", "D": "Report that a reserve book is missing"},
             "correct": "B", "explanation": "Ela quer um livro para um ensaio com prazo na segunda. (A) não é devolução; (C) não é renovação; (D) o livro não está perdido."},
            {"num": "B2.2", "prompt": "Detail. What is the rule for reserve items?",
             "options": {"A": "They can be borrowed for three weeks", "B": "They are two-hour loans, for use inside the library only", "C": "They cannot be used by undergraduates", "D": "They must be requested 24 hours in advance"},
             "correct": "B", "explanation": "\"Two-hour loans, in-library use only... can't take them out of the building.\" (A) descreve o exemplar da circulação; (C)/(D) não ditos."},
            {"num": "B2.3", "prompt": "Detail. What does the librarian suggest instead?",
             "options": {"A": "Buying the book at the campus bookstore", "B": "Borrowing the circulating copy from the fourth-floor stacks", "C": "Asking the professor for a personal copy", "D": "Waiting until Monday when more copies arrive"},
             "correct": "B", "explanation": "\"There's a circulating copy in the stacks, on the fourth floor. That one you can take out.\" (A)/(C)/(D) não sugeridos."},
            {"num": "B2.4", "prompt": "Inference. What will the student probably do next?",
             "options": {"A": "Place a hold on the reserve copy immediately", "B": "Go to the fourth floor to look for the circulating copy", "C": "Leave the library without the book", "D": "Ask the professor to extend the deadline"},
             "correct": "B", "explanation": "\"I'll check the stacks first.\" Inferência direta. (A) só se não achar; (C)/(D) contradizem a intenção declarada."},
        ],
    },
    {
        "id": "mod2-b3",
        "title": "Drill B3 · After Class · alvo: 3 min",
        "objective": "Leia o diálogo (ou peça pra alguém ler em voz alta) e responda às 4 questões. Tempo alvo: 3 minutos.",
        "passage_html": """<p><em>Narrator: Listen to a conversation between a student and a professor.</em></p>
<p><strong>Student:</strong> Professor, do you have a minute? I'm a bit lost on the second essay prompt.</p>
<p><strong>Professor:</strong> Of course. Which part?</p>
<p><strong>Student:</strong> It asks us to "evaluate" the argument, and I'm not sure if that means summarize it or agree or disagree with it.</p>
<p><strong>Professor:</strong> Good question — "evaluate" means neither, exactly. It means weigh the argument: where is it strong, where is it weak, and does the evidence actually support the conclusion? You can end up agreeing or disagreeing, but the point is the <em>weighing</em>, not the verdict.</p>
<p><strong>Student:</strong> Okay, that helps. So a summary alone wouldn't be enough.</p>
<p><strong>Professor:</strong> Right. A summary shows you understood it. Evaluation shows you can think about it. Aim for maybe a third summary, two-thirds evaluation.</p>
<p><strong>Student:</strong> Got it. And length — still fifteen hundred words?</p>
<p><strong>Professor:</strong> Fifteen hundred, give or take a hundred. Don't pad it.</p>""",
        "items": [
            {"num": "B3.1", "prompt": "Gist-purpose. Why does the student talk to the professor?",
             "options": {"A": "To ask for an extension on the essay", "B": "To clarify what the essay prompt is asking for", "C": "To dispute a grade on the first essay", "D": "To request a different topic"},
             "correct": "B", "explanation": "\"I'm a bit lost on the second essay prompt.\" (A) não pede prazo; (C) não é sobre nota; (D) não pede outro tema."},
            {"num": "B3.2", "prompt": "Detail. According to the professor, what does \"evaluate\" mean here?",
             "options": {"A": "Summarize the argument accurately", "B": "Simply agree or disagree with the argument", "C": "Weigh the argument's strengths, weaknesses, and use of evidence", "D": "Compare the argument with another author's"},
             "correct": "C", "explanation": "\"Weigh the argument: where is it strong, where is it weak, and does the evidence support the conclusion?\" (A)/(B) o professor diz que \"evaluate\" é <strong>nenhum</strong> dos dois; (D) não dito."},
            {"num": "B3.3", "prompt": "Detail. What balance between summary and evaluation does the professor recommend?",
             "options": {"A": "Half summary, half evaluation", "B": "All evaluation, no summary", "C": "About one-third summary, two-thirds evaluation", "D": "A brief summary followed by a personal opinion"},
             "correct": "C", "explanation": "\"Maybe a third summary, two-thirds evaluation.\""},
            {"num": "B3.4", "prompt": "Attitude. What does the professor mean by \"Don't pad it\"?",
             "options": {"A": "Write more than 1,500 words to be safe", "B": "Don't add filler just to reach the word count", "C": "Use larger margins and spacing", "D": "Include as many quotations as possible"},
             "correct": "B", "explanation": "\"Don't pad it\" = não encher linguiça para bater a contagem de palavras. (A) é o oposto; (C)/(D) estão fora do que foi dito."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo C: Listen to an Announcement — 3
# anúncios, 11 itens ao todo.
MOD2_ACTION_DRILLS_C = [
    {
        "id": "mod2-c1",
        "title": "Drill C1 · Library Services · alvo: 2 min",
        "objective": "Leia o anúncio (ou peça pra alguém ler em voz alta) e responda às 3 questões. Tempo alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about a change to library services.</em></p>
<p><strong>Speaker:</strong> Attention, students. Starting next Monday, the Main Library's third-floor reading room will be closed for renovation through the end of the month. During this period you can use the East Wing reading room instead, which keeps its regular hours. Reserved study rooms originally booked for the third floor have already been transferred automatically to the East Wing — you don't need to rebook. However, if your reservation was for a room with audiovisual equipment, please double-check availability, since not all East Wing rooms are equipped. Questions go to the circulation desk.</p>""",
        "items": [
            {"num": "C1.1", "prompt": "Detail. When does the closure begin?",
             "options": {"A": "Today", "B": "Next Monday", "C": "At the end of the month", "D": "Next semester"},
             "correct": "B", "explanation": "\"Starting next Monday...\" (C) confunde início com fim do período."},
            {"num": "C1.2", "prompt": "Detail. What happens to previously reserved study rooms?",
             "options": {"A": "They are canceled and must be rebooked", "B": "They are automatically transferred to the East Wing", "C": "They stay on the third floor", "D": "They are honored only if confirmed by email"},
             "correct": "B", "explanation": "\"Transferred automatically to the East Wing — you don't need to rebook.\" (A) é o oposto; (D) adiciona uma condição não dita."},
            {"num": "C1.3", "prompt": "Function. Why does the speaker mention audiovisual equipment?",
             "options": {"A": "To announce that all AV equipment is being removed", "B": "To tell students to avoid using AV equipment during renovations", "C": "To warn that not every transferred room has the same equipment as before", "D": "To advertise a new AV rental service"},
             "correct": "C", "explanation": "Aviso prático de que \"not all East Wing rooms are equipped\". (A)/(D) exageram; (B) está fora do que foi dito."},
        ],
    },
    {
        "id": "mod2-c2",
        "title": "Drill C2 · Course Registration · alvo: 2 min",
        "objective": "Leia o anúncio (ou peça pra alguém ler em voz alta) e responda às 4 questões. Tempo alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about course registration.</em></p>
<p><strong>Speaker:</strong> A reminder to all second-year students: registration for spring courses opens this Thursday at 8 a.m. and closes the following Wednesday at midnight. Register early — popular courses fill within hours. If a course you need is full, add yourself to the waitlist rather than emailing the instructor; the system releases spots automatically as students drop, and it works strictly in waitlist order. One change this year: the add/drop period after classes begin has been shortened from two weeks to one, so finalize your schedule before the term starts, not after.</p>""",
        "items": [
            {"num": "C2.1", "prompt": "Detail. When does registration close?",
             "options": {"A": "Thursday at 8 a.m.", "B": "The following Wednesday at midnight", "C": "One week after classes begin", "D": "Two weeks after classes begin"},
             "correct": "B", "explanation": "\"Closes the following Wednesday at midnight.\" (A) é a abertura; (C)/(D) confundem com o add/drop."},
            {"num": "C2.2", "prompt": "Detail. What should a student do if a course is full?",
             "options": {"A": "Email the instructor to ask for a spot", "B": "Register for a different course permanently", "C": "Add themselves to the waitlist", "D": "Wait until the add/drop period"},
             "correct": "C", "explanation": "\"Add yourself to the waitlist rather than emailing the instructor.\" (A) é explicitamente desaconselhado."},
            {"num": "C2.3", "prompt": "Connecting content. What has changed this year?",
             "options": {"A": "Registration now opens earlier in the day", "B": "The add/drop period has been shortened from two weeks to one", "C": "Waitlists are no longer used", "D": "Second-year students register last"},
             "correct": "B", "explanation": "\"The add/drop period... has been shortened from two weeks to one.\" (A)/(C)/(D) não ditos."},
            {"num": "C2.4", "prompt": "Inference. Why does the speaker emphasize finalizing the schedule before the term?",
             "options": {"A": "Because instructors will not answer email during the term", "B": "Because there will be less time to change courses once classes start", "C": "Because spring courses are harder than fall courses", "D": "Because registration reopens midway through the term"},
             "correct": "B", "explanation": "Add/drop mais curto → menos tempo para ajustar depois que as aulas começam. (A) é verdade em outro contexto, mas não é o que foi dito; (C)/(D) sem base."},
        ],
    },
    {
        "id": "mod2-c3",
        "title": "Drill C3 · Campus Event · alvo: 2 min",
        "objective": "Leia o anúncio (ou peça pra alguém ler em voz alta) e responda às 4 questões. Tempo alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about a career event.</em></p>
<p><strong>Speaker:</strong> The annual Career Fair takes place next Wednesday from 10 to 4 in the main gymnasium. Over eighty employers will attend, mostly in engineering, healthcare, and education. A few reminders. Bring several printed copies of your résumé — most recruiters still expect a paper copy. Business-casual dress is recommended, not required. The résumé-review station near the entrance will be open from 9, an hour before the fair, and it operates first-come, first-served, so arrive early if you want feedback before talking to employers. Finally, the 9:30 workshop on interview skills is now full; a recording will be posted next week for those who missed it.</p>""",
        "items": [
            {"num": "C3.1", "prompt": "Detail. What time does the Career Fair itself begin?",
             "options": {"A": "9 a.m.", "B": "9:30 a.m.", "C": "10 a.m.", "D": "4 p.m."},
             "correct": "C", "explanation": "\"From 10 to 4.\" (A) é a abertura da estação de revisão de currículo; (B) é o workshop."},
            {"num": "C3.2", "prompt": "Detail. What does the speaker say about dress?",
             "options": {"A": "Business formal is required", "B": "Business-casual is recommended but not required", "C": "There is no dress guidance", "D": "Recruiters will provide name tags and jackets"},
             "correct": "B", "explanation": "\"Business-casual dress is recommended, not required.\""},
            {"num": "C3.3", "prompt": "Connecting content. A student wants résumé feedback before speaking to employers. What should they do?",
             "options": {"A": "Attend the 9:30 workshop", "B": "Arrive at the résumé-review station around 9, since it is first-come, first-served", "C": "Email their résumé to a recruiter in advance", "D": "Wait until after 4 p.m."},
             "correct": "B", "explanation": "A estação abre às 9, é <em>first-come, first-served</em> → chegar cedo. (A) o workshop é de habilidades de entrevista, não revisão de currículo; (C)/(D) não sugeridos."},
            {"num": "C3.4", "prompt": "Detail. What is true of the 9:30 interview-skills workshop?",
             "options": {"A": "It has open spots", "B": "It is full, but a recording will be posted next week", "C": "It has been moved to next Wednesday", "D": "It requires advance payment"},
             "correct": "B", "explanation": "\"The 9:30 workshop... is now full; a recording will be posted next week.\""},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo D: Listen to an Academic Talk — 3
# palestras, 16 itens ao todo.
MOD2_ACTION_DRILLS_D = [
    {
        "id": "mod2-d1",
        "title": "Drill D1 · Psicologia · alvo: 4 min",
        "objective": "Leia a palestra (ou peça pra alguém ler em voz alta) e responda às 5 questões. Tempo alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a psychology class.</em></p>
<p><strong>Professor:</strong> We've been discussing decision-making, and today I want to bring up something researchers call the paradox of choice. The idea is counterintuitive: you'd think more options would always make us happier, but past a certain point it does the opposite.</p>
<p>A classic example. In one well-known study, researchers set up a tasting table in a grocery store: first with six varieties of jam, then with twenty-four. You'd expect the bigger display to sell more. Actually, the smaller display generated significantly more purchases. The larger one attracted more browsers, but far fewer of them bought anything.</p>
<p>Why? Two things: decision fatigue and anticipated regret. With more options, comparing them mentally becomes exhausting — that's the fatigue. And once you pick, you start second-guessing whether one of the other twenty-three would've been better — that's the regret. Ironically, more choices can leave people feeling back to square one, unable to commit at all.</p>
<p>Now, this doesn't mean choice is bad: a complete absence of options is its own problem. The point is there's a sweet spot, and past it, additional options stop helping and start working against us.</p>""",
        "items": [
            {"num": "D1.1", "prompt": "Gist-content. What is the talk mainly about?",
             "options": {"A": "Grocery stores should minimize the products they display", "B": "Beyond a point, more options can reduce satisfaction and hinder decisions", "C": "Consumers always prefer smaller displays", "D": "Decision fatigue affects only in-store shoppers"},
             "correct": "B", "explanation": "Tese anunciada no início e no fechamento. (A) exagera; (C) \"always\" nunca é dito; (D) está fora do que foi dito."},
            {"num": "D1.2", "prompt": "Detail. What happened with the 24-variety display?",
             "options": {"A": "It attracted more browsers but produced fewer purchases", "B": "It produced both more browsers and more purchases", "C": "It was removed for low interest", "D": "It produced identical sales to the smaller display"},
             "correct": "A", "explanation": "\"Attracted more browsers, but far fewer of them bought anything.\" (B) é o oposto."},
            {"num": "D1.3", "prompt": "Organization. Why does the professor describe the grocery store study in detail?",
             "options": {"A": "To criticize the researchers' methodology", "B": "To give concrete evidence for the paradox of choice", "C": "To introduce an unrelated topic about marketing", "D": "To explain how stores design displays"},
             "correct": "B", "explanation": "Exemplo empírico logo após o conceito abstrato. (A)/(C)/(D) sem base."},
            {"num": "D1.4", "prompt": "Inference. What is the professor's view on having zero options?",
             "options": {"A": "It is preferable to having too many", "B": "It is also a problem, just as too many options are", "C": "It has never been studied", "D": "It applies only to grocery shopping"},
             "correct": "B", "explanation": "\"A complete absence of options is its own problem.\" (A) inverte o sentido."},
            {"num": "D1.5", "prompt": "Idiom in context. What does \"back to square one\" mean here?",
             "options": {"A": "Making a confident final decision", "B": "Returning to a starting point without real progress", "C": "Choosing the first option presented", "D": "Comparing two options systematically"},
             "correct": "B", "explanation": "\"Back to square one\" = voltar ao ponto de partida sem progresso. (A) é o oposto; (C)/(D) distorcem."},
        ],
    },
    {
        "id": "mod2-d2",
        "title": "Drill D2 · Biologia · alvo: 4 min",
        "objective": "Leia a palestra (ou peça pra alguém ler em voz alta) e responda às 5 questões. Tempo alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a biology class.</em></p>
<p><strong>Professor:</strong> When we picture a forest, we tend to see individual trees competing — for light, for water, for space. And that's real. But over the last thirty years, research has revealed something the old picture missed: the trees are also <strong>connected</strong>, underground, through fungi.</p>
<p>Here's how. The roots of most trees are wrapped in a network of fungal threads called mycorrhizae. The fungi pull in water and minerals the tree's roots can't reach efficiently, and hand them to the tree. In return, the tree gives the fungi sugars it makes through photosynthesis. So far, a simple trade.</p>
<p>The surprising part is that a single fungal network can link <strong>many</strong> trees at once — even trees of different species. And things move along those links. Experiments using radioactive tracers have shown carbon flowing from a tree standing in full sun to a shaded seedling of another species nearby. Some researchers describe old, well-connected trees as "hub trees" that support younger ones around them.</p>
<p>Now, a word of caution. This work has captured the public imagination, and some popular accounts overstate it: talking about forests as single cooperative organisms. The jury's still out on how deliberate or widespread the sharing really is. What's solid is that the connections exist and that resources can move through them. How much that reshapes our model of the forest is still being worked out.</p>""",
        "items": [
            {"num": "D2.1", "prompt": "Gist-content. What is the main point of the talk?",
             "options": {"A": "Trees in a forest only compete, never cooperate", "B": "Trees are connected underground through fungal networks, and resources can move between them", "C": "Mycorrhizal fungi are harmful to most trees", "D": "Forests are single cooperative organisms"},
             "correct": "B", "explanation": "O professor admite a competição <strong>mas</strong> acrescenta a conexão. (A) ignora a segunda metade da tese; (C) é o oposto (a relação é benéfica); (D) é exatamente o exagero que ele critica no fim."},
            {"num": "D2.2", "prompt": "Detail. What does the tree give the fungi in the relationship?",
             "options": {"A": "Water it pulls from deep soil", "B": "Minerals from its leaves", "C": "Sugars made through photosynthesis", "D": "Nothing — the relationship is one-directional"},
             "correct": "C", "explanation": "\"The tree gives the fungi sugars it makes through photosynthesis.\" (A)/(B) são o que os fungos fazem pela árvore; (D) é o oposto."},
            {"num": "D2.3", "prompt": "Detail. What did the radioactive-tracer experiments show?",
             "options": {"A": "That fungi kill shaded seedlings", "B": "That carbon can flow from a sunlit tree to a shaded seedling of another species", "C": "That only trees of the same species can be connected", "D": "That the networks do not actually transfer anything"},
             "correct": "B", "explanation": "\"Carbon flowing from a tree standing in full sun to a shaded seedling of another species.\""},
            {"num": "D2.4", "prompt": "Attitude / Organization. Why does the professor add \"a word of caution\" near the end?",
             "options": {"A": "To retract everything said earlier in the talk", "B": "To distinguish what the evidence firmly supports from claims that popular accounts exaggerate", "C": "To argue that the research is worthless", "D": "To introduce a completely different topic"},
             "correct": "B", "explanation": "Ele separa o que a evidência sustenta firmemente do que relatos populares exageram (\"forests as single cooperative organisms\"). (A)/(C) exageram; (D) está fora do que foi dito."},
            {"num": "D2.5", "prompt": "Idiom in context. What does the professor mean by \"the jury's still out\"?",
             "options": {"A": "The question has been definitively settled", "B": "There is not yet a firm conclusion on the matter", "C": "A court case is involved in the research", "D": "The researchers have stopped studying it"},
             "correct": "B", "explanation": "\"The jury's still out\" = ainda não há conclusão firme. (A) é o oposto; (C) é literal demais; (D) não é dito."},
        ],
    },
    {
        "id": "mod2-d3",
        "title": "Drill D3 · História da tecnologia · alvo: 4 min",
        "objective": "Leia a palestra (ou peça pra alguém ler em voz alta) e responda às 6 questões. Tempo alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a history of technology class.</em></p>
<p><strong>Professor:</strong> Look at your keyboard. The top row of letters spells Q-W-E-R-T-Y. It's an odd arrangement — the most common letters aren't under your strongest fingers. So why has it survived, essentially unchanged, for a hundred and fifty years?</p>
<p>The layout dates from the 1870s, from early mechanical typewriters. The common story is that QWERTY was designed to <em>slow typists down</em> so the metal type-bars wouldn't jam. That's probably an oversimplification (the real design pressures were more mixed) but the key point is that the layout was shaped by the constraints of 1870s <strong>machinery</strong>, constraints that vanished decades ago.</p>
<p>Better layouts have been proposed. The best known, Dvorak, was patented in 1936 and, in some studies, allows modestly faster and more comfortable typing. Yet it never caught on. Why not?</p>
<p>This is a textbook case of what economists call <strong>path dependence</strong>, or sometimes "lock-in." Once QWERTY became the standard, everything organized itself around that standard: typewriters were built for it, typing was taught on it, and every new typist learned it because that's what the machines used — and machines used it because that's what typists knew. To switch, a single person gains little unless nearly everyone switches at once. The cost of coordinating that switch is enormous, and no one bears it. So an arrangement that made sense only for 1870s hardware is still, quietly, on every device you own.</p>""",
        "items": [
            {"num": "D3.1", "prompt": "Gist-content. What is the talk mainly about?",
             "options": {"A": "How to type faster using the Dvorak layout", "B": "Why an outdated keyboard layout has persisted, as an example of path dependence", "C": "The mechanical design of 19th-century typewriters", "D": "Why Dvorak is objectively the best possible layout"},
             "correct": "B", "explanation": "A pergunta central é por que um layout ultrapassado sobreviveu — e a resposta é <em>path dependence</em>. (A)/(D) mudam o foco/exageram; (C) é contexto, não o tema."},
            {"num": "D3.2", "prompt": "Detail. What does the professor say about the \"common story\" that QWERTY was designed to slow typists down?",
             "options": {"A": "It is completely accurate", "B": "It is probably an oversimplification, though the layout was shaped by 1870s machinery", "C": "It was invented by economists", "D": "It explains why Dvorak succeeded"},
             "correct": "B", "explanation": "\"That's probably an oversimplification... but the layout was shaped by 1870s machinery.\""},
            {"num": "D3.3", "prompt": "Detail. According to the talk, what happened to the Dvorak layout?",
             "options": {"A": "It became the new standard in the 1940s", "B": "It was patented in 1936 but never caught on", "C": "It was proven to be slower than QWERTY", "D": "It is now used on most smartphones"},
             "correct": "B", "explanation": "\"Patented in 1936... Yet it never caught on.\" (A)/(C)/(D) contradizem."},
            {"num": "D3.4", "prompt": "Organization. Why does the professor describe the cycle of \"typists learned QWERTY because machines used it, and machines used it because typists knew it\"?",
             "options": {"A": "To illustrate how lock-in makes a standard self-reinforcing and hard to change", "B": "To criticize typewriter manufacturers", "C": "To explain how mechanical type-bars work", "D": "To argue that QWERTY is actually well designed"},
             "correct": "A", "explanation": "O ciclo ilustra como o padrão se auto-reforça (<em>lock-in</em>). (B)/(C)/(D) sem base."},
            {"num": "D3.5", "prompt": "Inference. What can be inferred about why an individual rarely switches to Dvorak?",
             "options": {"A": "Dvorak keyboards are illegal in most countries", "B": "The benefit to one person is small unless almost everyone switches together", "C": "Dvorak is much harder to learn than any other layout", "D": "Employers forbid it"},
             "correct": "B", "explanation": "\"A single person gains little unless nearly everyone switches at once.\" (A)/(C)/(D) exageram ou não são ditos."},
            {"num": "D3.6", "prompt": "Idiom in context. When the professor says the old arrangement is \"still, quietly, on every device you own,\" the word \"quietly\" suggests that:",
             "options": {"A": "keyboards make no sound", "B": "most people use QWERTY without noticing that it is an outdated design", "C": "the layout is a secret", "D": "typing should be done silently"},
             "correct": "B", "explanation": "\"Quietly\" sugere que as pessoas usam QWERTY sem perceber que é um design obsoleto. (A)/(C)/(D) tomam a palavra ao pé da letra ou fora de contexto."},
        ],
    },
]
