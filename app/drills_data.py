# Structured drill data for interactive quiz widgets (modules 1 and 2).
# Each drill: id, title, objective (short instruction), optional shared passage_html,
# and items: [{num, prompt, options{A,B,C,D}, correct, explanation}]

# PARTE 5 (Action Drills) do M1, Grupo A: Complete the Words — 5 textos,
# 32 itens ao todo. Fonte: consolidated/modulo_1_reading.md PARTE 5/PARTE 6.
MOD1_ACTION_DRILLS_A = [
    {
        "id": "mod1-a1",
        "title": "Exercício A1 (meta de 4 min)",
        "level": "A2–B1",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo-alvo: 4 minutos.",
        "passage_html": """<p><strong>TEXT: A message to a friend</strong></p>
<p>Hi Marco,</p>
<p>I'm really sorry, but I have to (1)_____ our plans for Saturday. My sister (2)_____ from Recife that morning and I have to pick her up at the airport. I know we (3)_____ this dinner for weeks, and I feel terrible about it.</p>
<p>Would Sunday afternoon (4)_____ instead? There's a new place near the park that everyone (5)_____ about. If Sunday doesn't work for you, just let me (6)_____ and we'll find another day.</p>
<p>Again, I'm sorry for the short notice.</p>
<p>Talk soon, Lia</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "cancel", "B": "canceling", "C": "to cancel", "D": "cancelled"},
             "correct": "A", "explanation": "\"Have to\" + <strong>verbo base</strong>. As opções (B) <em>canceling</em>, (C) <em>to cancel</em> e (D) <em>cancelled</em> quebram a estrutura \"have to + base\"."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "arrive", "B": "will arriving", "C": "arriving", "D": "is arriving"},
             "correct": "D", "explanation": "Um compromisso futuro já combinado (\"that morning\") pede o <strong>presente contínuo com valor de futuro</strong>. (A) quebra a concordância com <em>my sister</em>; (B) junta <em>will</em> e <em>-ing</em> sem <em>be</em>, o que não existe; (C) <em>arriving</em> sozinho não tem auxiliar. Repare que <em>arrives</em> também estaria certo aqui (horário de voo), e por isso não está entre as opções."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "plan", "B": "planning", "C": "have been planning", "D": "are planning"},
             "correct": "C", "explanation": "\"For weeks\" com uma ação que começou no passado e continua pede o <strong>presente perfeito contínuo</strong>. (D) <em>are planning</em> ignora o \"for weeks\"; (A) não liga passado e presente; (B) <em>planning</em> sozinho não tem auxiliar."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "work", "B": "works", "C": "working", "D": "worked"},
             "correct": "A", "explanation": "Depois do modal <em>would</em> vem o verbo na <strong>forma base</strong>, como em \"Would Sunday afternoon work?\""},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "are talking", "B": "is talking", "C": "talking", "D": "be talking"},
             "correct": "B", "explanation": "<em>Everyone</em> é <strong>singular</strong> e pede <em>is talking</em> (o contínuo é o natural para o que está na moda agora). (A) quebra a concordância; (C) e (D) não têm auxiliar conjugado."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "know", "B": "known", "C": "knowing", "D": "to know"},
             "correct": "A", "explanation": "<em>Let</em> + objeto + <strong>base</strong> (\"let me know\": fórmula fixa). (D) \"let me to know\" é agramatical."},
        ],
    },
    {
        "id": "mod1-a2",
        "title": "Exercício A2 (meta de 4 min)",
        "level": "B1",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo-alvo: 4 minutos.",
        "passage_html": """<p><strong>TEXT: Notice at a community pool</strong></p>
<p>Starting Monday, the main pool (1)_____ closed for its annual maintenance. We expect the work (2)_____ completed by Friday afternoon. During this period, members (3)_____ still use the smaller training pool, which (4)_____ open at its usual hours.</p>
<p>We apologize for any (5)_____ this may cause. If you have questions about your membership or class schedule, please (6)_____ to speak with the front desk staff, who will be happy to help.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "is", "B": "be", "C": "being", "D": "been"},
             "correct": "A", "explanation": "Em \"The main pool ___ closed\" temos a voz passiva no presente, formada por <strong>is</strong> e particípio (<em>closed</em>)."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "is", "B": "to be", "C": "being", "D": "be"},
             "correct": "B", "explanation": "\"We expect the work ___ completed\": <em>expect</em> + objeto + <strong>to + infinitivo</strong> (aqui infinitivo passivo <em>to be completed</em>)."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "may", "B": "may to", "C": "maying", "D": "mays"},
             "correct": "A", "explanation": "Modal simples; \"members may still use\". (B) \"may to\" é agramatical: modal nunca leva <em>to</em>."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "remain", "B": "remains", "C": "remaining", "D": "to remain"},
             "correct": "B", "explanation": "O pronome <em>which</em> retoma <em>the smaller training pool</em>, que é singular, por isso o verbo leva <strong>-s</strong>."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "inconvenient", "B": "inconveniently", "C": "inconvenience", "D": "inconvenienced"},
             "correct": "C", "explanation": "Depois de <em>any</em>, a lacuna é <strong>substantivo</strong>: \"any inconvenience this may cause\"."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "hesitate", "B": "not hesitate", "C": "don't hesitate", "D": "hesitating"},
             "correct": "C", "explanation": "Fórmula fixa: \"please don't hesitate to...\". (B) \"not hesitate\" sem auxiliar é agramatical num pedido; (A) sozinho inverteria o sentido."},
        ],
    },
    {
        "id": "mod1-a3",
        "title": "Exercício A3 (meta de 5 min)",
        "level": "B2",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo-alvo: 5 minutos.",
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
             "correct": "A", "explanation": "\"Turn off equipment\" é desligar o equipamento. (B) significa diminuir a intensidade; (C), revelar-se ou comparecer; (D), virar ou entregar."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "completion", "B": "completing", "C": "completed", "D": "completes"},
             "correct": "C", "explanation": "\"Will be _____\" pede particípio passado (voz passiva): \"will be completed\". (A) é substantivo; (B) daria voz ativa sem objeto; (D) é verbo conjugado, impossível depois de \"be\"."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "come", "B": "comes", "C": "coming", "D": "will comes"},
             "correct": "B", "explanation": "\"Everyone\" é singular na gramática e pede a 3ª pessoa do singular: \"comes back\". (D) não existe, porque \"will\" nunca vem seguido de verbo com -s."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "warm", "B": "warms", "C": "warmly", "D": "warmth"},
             "correct": "A", "explanation": "\"To _____ up again\" pede o infinitivo (verbo base) após \"to\". \"Warm up\" é o phrasal verb certo para um ambiente recuperando temperatura."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "hesitate", "B": "hesitating", "C": "hesitation", "D": "hesitated"},
             "correct": "A", "explanation": "\"Don't _____ to reach out\" pede verbo base após o imperativo negativo \"don't\". \"Don't hesitate to + verbo\" é expressão fixa."},
            {"num": "7", "prompt": "Lacuna (7)", "options": {"A": "miss", "B": "lose", "C": "waste", "D": "fail"},
             "correct": "A", "explanation": "Estrutura paralela \"ask a question... than _____ a real problem\" pede verbo base após \"than\". <em>Miss a problem</em> = não perceber, deixar passar um problema: melhor uma pergunta à toa do que um problema real que ninguém notou. (B) <em>lose a problem</em> não existe; (C) <em>waste</em> pede <em>time/money</em>; (D) <em>fail</em> pede <em>to</em> (\"fail to notice\")."},
            {"num": "8", "prompt": "Lacuna (8)", "options": {"A": "extend", "B": "extending", "C": "extended", "D": "extension"},
             "correct": "C", "explanation": "\"The _____ time off\" pede um particípio com função de adjetivo antes do substantivo. \"Extended time off\" é uma folga prolongada."},
        ],
    },
    {
        "id": "mod1-a4",
        "title": "Exercício A4 (meta de 5 min)",
        "level": "B2–C1",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo-alvo: 5 minutos.",
        "passage_html": """<p><strong>TEXT: Museum exhibit information card</strong></p>
<p>This exhibit brings together more than two hundred objects (1)_____ over four decades of fieldwork in the region. Many of them (2)_____ never been displayed publicly before. Together, they offer a rare (3)_____ into daily life in a community that written records largely overlooked.</p>
<p>Visitors are (4)_____ to move through the rooms in order, since the layout follows a rough chronology. Labels have been kept deliberately brief; those who wish to (5)_____ deeper into any single object will find extended notes on the tablets provided at the entrance. Photography without flash (6)_____ permitted throughout, except in the final room, where the light-sensitive textiles require complete darkness.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "collect", "B": "collected", "C": "collecting", "D": "collection"},
             "correct": "B", "explanation": "\"Objects ___ over four decades\": particípio reduzido de \"objects <strong>that were collected</strong>\"."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "has", "B": "have", "C": "had", "D": "having"},
             "correct": "B", "explanation": "O sujeito <em>Many of them</em> é plural e, com o presente perfeito, forma \"have never been displayed\". (A) quebra a concordância; (C) mudaria para o passado perfeito sem um marco no passado; (D) não fecha o tempo verbal."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "window", "B": "door", "C": "mirror", "D": "bridge"},
             "correct": "A", "explanation": "Em \"A rare ___ into daily life\" está a combinação fixa <em>a window into</em> (ou <em>onto</em>), \"uma janela para\", no sentido de uma visão de algo. As outras opções não combinam com \"into daily life\" nesse sentido."},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "encourage", "B": "encouraged", "C": "encouraging", "D": "encouragement"},
             "correct": "B", "explanation": "Em \"Visitors are ___ to move\" temos a voz passiva <em>are encouraged to</em>. (C) mudaria o sujeito; (A) e (D) não formam a passiva."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "delve", "B": "fall", "C": "drop", "D": "sink"},
             "correct": "A", "explanation": "Em \"Wish to ___ deeper into any single object\", <em>delve into</em> quer dizer aprofundar-se em. As outras opções não combinam com \"deeper into [um tema]\" no sentido de investigar."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "is", "B": "are", "C": "being", "D": "be"},
             "correct": "A", "explanation": "Em \"Photography without flash ___ permitted\", o sujeito <em>Photography</em> é incontável e singular, por isso pede <strong>is</strong>."},
        ],
    },
    {
        "id": "mod1-a5",
        "title": "Exercício A5 (meta de 5 min)",
        "level": "C1",
        "objective": "Leia o texto e escolha a opção que completa cada lacuna corretamente. Tempo-alvo: 5 minutos.",
        "passage_html": """<p><strong>TEXT: Excerpt from an editorial</strong></p>
<p>For decades, the standard response to traffic congestion (1)_____ been to add lanes. The logic seems sound. Yet a growing body of research points to the opposite (2)_____: added lanes tend to attract additional drivers until, within a few years, traffic returns to its former level — a phenomenon known as induced demand. Rarely (3)_____ a policy so intuitive prove so consistently ineffective.</p>
<p>This does not mean nothing (4)_____ be done. It means the solution lies elsewhere: in reliable public transit, in pricing that reflects the true cost of road use, and in land-use decisions that reduce the (5)_____ to drive in the first place. None of these is as politically straightforward as pouring concrete, which is (6)_____ they are so often postponed.</p>""",
        "items": [
            {"num": "1", "prompt": "Lacuna (1)", "options": {"A": "has", "B": "have", "C": "had", "D": "having"},
             "correct": "A", "explanation": "O sujeito \"the standard response\" é <strong>singular</strong> e pede \"has been\" (presente perfeito, com \"For decades... has been\"). (B) quebra a concordância; (C) pediria um marco no passado; (D) não fecha o tempo verbal."},
            {"num": "2", "prompt": "Lacuna (2)", "options": {"A": "conclusion", "B": "decision", "C": "opinion", "D": "suggestion"},
             "correct": "A", "explanation": "\"Points to the opposite ___\": <em>point to a conclusion</em> é a collocation. As outras opções não formam collocation com \"research points to the opposite ___\"."},
            {"num": "3", "prompt": "Lacuna (3)", "options": {"A": "does", "B": "do", "C": "is", "D": "has"},
             "correct": "A", "explanation": "Com <em>Rarely</em> no início da frase há inversão: o auxiliar <strong>does</strong> vem antes do sujeito, e o verbo fica na forma base (<em>prove</em>), como em \"Rarely does a policy... prove...\""},
            {"num": "4", "prompt": "Lacuna (4)", "options": {"A": "can", "B": "can't", "C": "is", "D": "has"},
             "correct": "A", "explanation": "Em \"This does not mean nothing ___ be done\" entra um modal antes de <em>be done</em> (passiva), com o sentido de \"não significa que nada pode ser feito\". (B) inverteria o sentido; (C) e (D) não podem vir antes de \"be\" (\"is be\" e \"has be\" não existem)."},
            {"num": "5", "prompt": "Lacuna (5)", "options": {"A": "need", "B": "want", "C": "wish", "D": "hope"},
             "correct": "A", "explanation": "Em \"Reduce the ___ to drive\", <em>the need to (do something)</em> é \"a necessidade de\". As outras opções não combinam com essa estrutura."},
            {"num": "6", "prompt": "Lacuna (6)", "options": {"A": "why", "B": "because", "C": "how", "D": "what"},
             "correct": "A", "explanation": "Em \"Which is ___ they are so often postponed\", \"which is why...\" quer dizer \"razão pela qual\". (B) precisaria de outra estrutura; (C) e (D) não fecham a oração relativa."},
        ],
    },
]

# PARTE 5 (Action Drills) do M1, Grupo B: Read in Daily Life — 5 textos
# curtos, 13 itens ao todo (conjuntos de 2 ou 3, como na prova).
MOD1_ACTION_DRILLS_B = [
    {
        "id": "mod1-b1",
        "title": "Exercício B1: placa ou aviso (meta de 2 min)",
        "level": "A2–B1",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.",
        "passage_html": """<p><strong>TEXT: Sign at a nature reserve trailhead</strong></p>
<blockquote><p><strong>RIDGELINE TRAIL: PLEASE READ BEFORE ENTERING</strong></p>
<p>• Trail open sunrise to sunset. Overnight camping is not permitted anywhere on the reserve.<br>
• Dogs welcome on a leash no longer than 6 feet. The upper loop (marked in red) is closed to dogs from April 1 to July 15 to protect ground-nesting birds.<br>
• No bicycles. E-bikes and mobility scooters are exempt from this rule.<br>
• Pack out all trash. There are no trash cans beyond this point.</p></blockquote>""",
        "items": [
            {"num": "B1.1", "prompt": "A visitor with a dog on May 20 may walk:",
             "options": {"A": "anywhere on the reserve", "B": "on all trails except the upper loop", "C": "only on the upper loop", "D": "nowhere, because dogs are banned in summer"},
             "correct": "B", "explanation": "Cães na coleira são permitidos, mas o <em>upper loop</em> fica fechado para cães de 1º de abril a 15 de julho, e 20 de maio cai nesse período. Por isso, o visitante pode usar todas as trilhas <strong>exceto</strong> o upper loop. (A) ignora a restrição; (C) inverte a regra; (D) exagera, porque os cães não são proibidos em toda parte, só no upper loop."},
            {"num": "B1.2", "prompt": "Which of the following is allowed on the trail?",
             "options": {"A": "A regular bicycle", "B": "An overnight tent", "C": "A mobility scooter", "D": "Leaving food scraps in a trash can"},
             "correct": "C", "explanation": "\"E-bikes and mobility scooters are exempt\" da proibição de bicicletas. (A) bicicleta comum é proibida; (B) camping é proibido; (D) não há lixeiras além daquele ponto."},
        ],
    },
    {
        "id": "mod1-b2",
        "title": "Exercício B2: cardápio (meta de 3 min)",
        "level": "A2–B1",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: Café lunch menu (extract)</strong></p>
<blockquote><p><strong>SANDWICHES</strong>: all served on sourdough with a side salad (swap for fries +$2)</p>
<p>• <strong>Garden</strong> — roasted vegetables, hummus, arugula · $9 · <em>vegan</em><br>
• <strong>Classic Club</strong> (chicken, bacon, egg, lettuce) · $12<br>
• <strong>Halloumi Stack</strong> — grilled halloumi, tomato, pesto · $11 · <em>vegetarian (contains nuts)</em></p>
<p><strong>SOUPS</strong> · served with bread · $7 · soup of the day is always vegetarian; ask staff whether today's is vegan.</p>
<p><em>A 10% discount applies to all lunch orders placed before noon.</em></p></blockquote>""",
        "items": [
            {"num": "B2.1", "prompt": "A customer who is vegan and allergic to nuts could safely order:",
             "options": {"A": "the Halloumi Stack", "B": "the Garden sandwich", "C": "the soup of the day, no questions asked", "D": "the Classic Club without bacon"},
             "correct": "B", "explanation": "<em>Garden</em> é vegan e não tem aviso de nozes. (A) Halloumi Stack tem queijo (não vegan) e <em>contains nuts</em>; (C) a sopa é sempre vegetariana mas <strong>pode não ser vegana</strong>: o texto manda perguntar; (D) Classic Club tem frango e ovo."},
            {"num": "B2.2", "prompt": "A customer orders a Classic Club with fries at 11:45 a.m. Before any discount, the price is:",
             "options": {"A": "$12", "B": "$14", "C": "$12.60", "D": "$16"},
             "correct": "B", "explanation": "São $12 do sanduíche mais $2 pela troca por fries, o que dá $14. O desconto de 10% (pedido antes do meio-dia) entra <strong>depois</strong>, mas a pergunta é o preço <strong>antes</strong> do desconto. (C) $12.60 é o valor <strong>com</strong> o desconto, que a pergunta exclui; (A) esquece a troca por fries."},
            {"num": "B2.3", "prompt": "According to the menu, the soup of the day:",
             "options": {"A": "is always vegan", "B": "is always vegetarian, and may or may not be vegan", "C": "never contains bread", "D": "costs more than any sandwich"},
             "correct": "B", "explanation": "\"Soup of the day is always vegetarian; ask staff whether today's is vegan\": sempre vegetariana, veganidade varia."},
        ],
    },
    {
        "id": "mod1-b3",
        "title": "Exercício B3: e-mail formal (meta de 3 min)",
        "level": "B1–B2",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: Email from a course coordinator</strong></p>
<blockquote>
<p><strong>Subject: Re: Request to submit Assignment 2 late</strong></p>
<p>Dear Bruna,</p>
<p>Thank you for letting me know about your situation in advance rather than after the deadline. I'm sorry to hear you've been unwell.</p>
<p>Our department policy does not allow me to grant an extension without a doctor's note. If you're able to provide one, I can extend your deadline to next Monday. If not, I can still accept the assignment up to 48 hours late, though the standard 10% late penalty would apply in that case.</p>
<p>Please let me know which option you'd prefer by Thursday so I can update the system.</p>
<p>Best regards,<br>Dr. Okafor</p>
</blockquote>""",
        "items": [
            {"num": "B3.1", "prompt": "What is the main purpose of this email?",
             "options": {"A": "To refuse Bruna's request", "B": "To explain the options available and ask Bruna to choose", "C": "To inform Bruna that her assignment is now overdue", "D": "To apologize for a mistake the department made"},
             "correct": "B", "explanation": "O e-mail lista duas opções (com ou sem atestado) e pede que Bruna escolha até quinta. (A) não recusa, oferece alternativas; (C) o trabalho ainda não está atrasado; (D) não houve erro do departamento."},
            {"num": "B3.2", "prompt": "If Bruna does NOT provide a doctor's note, she can:",
             "options": {"A": "submit the assignment by next Monday with no penalty", "B": "submit up to 48 hours late, losing 10% of the grade", "C": "not submit the assignment at all", "D": "choose her own new deadline"},
             "correct": "B", "explanation": "Sem atestado: aceita até 48h de atraso com penalidade padrão de 10%. (A) descreve a opção <strong>com</strong> atestado; (C)/(D) não constam."},
            {"num": "B3.3", "prompt": "Dr. Okafor's tone is best described as:",
             "options": {"A": "annoyed and dismissive", "B": "formal but sympathetic and helpful", "C": "uncertain and apologetic", "D": "casual and friendly"},
             "correct": "B", "explanation": "Registro formal (<em>Dear... Best regards, Dr. Okafor</em>), mas empático (<em>I'm sorry to hear you've been unwell</em>) e prestativo (oferece soluções). (A)/(C)/(D) não batem com o texto."},
        ],
    },
    {
        "id": "mod1-b4",
        "title": "Exercício B4: horário ou tabela (meta de 2 min)",
        "level": "B1–B2",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.",
        "passage_html": """<p><strong>TEXT: Shuttle timetable notice</strong></p>
<blockquote><p><strong>CAMPUS ↔ STATION SHUTTLE</strong></p>
<p>Departs Campus Gate: on the hour and at half past, 7:00–19:00, Mon–Fri. Departs Station: at quarter past and quarter to, same times. Journey time: approximately 20 minutes.</p>
<p><em>The half-past and quarter-to services do not run after 17:00: the last half-past departure from Campus Gate is at 16:30. On weekends and holidays, shuttles leave both stops on the hour only.</em></p></blockquote>""",
        "items": [
            {"num": "B4.1", "prompt": "A student wants to leave Campus Gate on a Tuesday at 17:30. On that day there is:",
             "options": {"A": "no 17:30 service — after 17:00 the shuttle leaves on the hour only", "B": "a 17:30 service that arrives at the station around 17:50", "C": "a shuttle only if it is a holiday", "D": "a 17:30 service that takes about 45 minutes"},
             "correct": "A", "explanation": "A nota de rodapé é clara: \"the last half-past departure from Campus Gate is at 16:30\", e depois das 17:00 o serviço é \"on the hour only\". Logo, não existe saída às 17:30 na terça-feira. Este item treina a leitura da <strong>nota de rodapé</strong>, e quem marca (B) leu só a linha principal e deixou passar a exceção."},
            {"num": "B4.2", "prompt": "On a Sunday, a shuttle leaves the Station at:",
             "options": {"A": "quarter past and quarter to every hour", "B": "on the hour only", "C": "half past every hour", "D": "the timetable does not say"},
             "correct": "B", "explanation": "Fim de semana: \"On weekends and holidays, shuttles leave both stops on the hour only\". A tabela <em>quarter past / quarter to</em> da estação vale só de segunda a sexta."},
        ],
    },
    {
        "id": "mod1-b5",
        "title": "Exercício B5: post de rede social (meta de 3 min)",
        "level": "A2–B1",
        "objective": "Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.",
        "passage_html": """<p><strong>TEXT: A social media post from a local bakery</strong></p>
<blockquote><p>🥐 <strong>Riverside Bakery</strong> · Posted 2 hours ago</p>
<p>Big news, everyone! Starting next Tuesday, we're extending our weekday hours — open at 6:30 AM instead of 7:00 AM, so early risers can grab their coffee and croissants before work. 🌅</p>
<p>Quick heads-up though: because of the earlier opening, our weekday sourdough batch will now go into the oven the night before instead of first thing in the morning. It'll still be baked fresh daily, just on a slightly different schedule — so if you're used to grabbing a loaf warm out of the oven at 8 AM, you'll now find it ready on the shelf as soon as we open. Come say hi and let us know what you think of the new hours!</p>
<p>Weekend hours are unchanged (8 AM–3 PM, same as always).</p></blockquote>""",
        "items": [
            {"num": "B5.1", "prompt": "What is the main purpose of this post?",
             "options": {"A": "To announce that the bakery is closing early on weekdays", "B": "To inform customers about a change to weekday opening hours", "C": "To apologize for a delay in the sourdough baking schedule", "D": "To advertise a new type of bread"},
             "correct": "B", "explanation": "O post inteiro gira em torno de um anúncio: abrir mais cedo nos dias de semana. (A) inverte; (C) não pede desculpas; (D) nenhum pão novo."},
            {"num": "B5.2", "prompt": "According to the post, the weekday sourdough will:",
             "options": {"A": "no longer be baked fresh every day", "B": "only be available on weekends", "C": "be baked the night before instead of the same morning", "D": "be replaced with a different bread"},
             "correct": "C", "explanation": "\"Will now go into the oven the night before\". (A) o texto diz \"still be baked fresh daily\"; (B)/(D) não constam."},
            {"num": "B5.3", "prompt": "What does the post say about the weekend hours?",
             "options": {"A": "They will also move to 6:30 AM", "B": "They stay the same as before this announcement", "C": "They have not been decided yet", "D": "They will be shortened"},
             "correct": "B", "explanation": "\"Weekend hours are unchanged\". (A)/(D) contradizem; (C) já está decidido."},
        ],
    },
]

# PARTE 5 (Action Drills) do M1, Grupo C: Read an Academic Passage — 3
# passagens de 180 a 220 palavras com 5 perguntas cada (15 itens), como na
# prova de 2026. Os tipos do formato antigo (simplificação de frase, inserir
# frase e resumo) saíram em 2026-10-18.
MOD1_ACTION_DRILLS_C = [
    {
        "id": "mod1-c1",
        "title": "Exercício C1: ciências naturais (meta de 6 min)",
        "level": "B2–C1",
        "objective": "Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: Bioluminescence in Marine Organisms</strong></p>
<p>Bioluminescence, the production of light by a living organism, is remarkably common in the ocean, appearing in bacteria, jellyfish, fish, and even some sharks. Unlike an incandescent bulb, which wastes most of its energy as heat, bioluminescent light comes from a highly efficient chemical reaction between a molecule called luciferin and an enzyme called luciferase. Because so little energy is lost as heat, biologists sometimes call it "cold light."</p>
<p>Organisms use this light in several ways. Some use it defensively: certain squid release a glowing cloud instead of ink, startling predators long enough to escape. Others use it to hunt. The anglerfish, perhaps the most famous example, dangles a glowing lure above its mouth to attract prey close enough to seize. Still others use light to communicate. In the deep sea, darkness is nearly absolute, so visual signals cannot rely on ambient light at all, and even in shallow water at night, tiny crustaceans called ostracods produce synchronized displays to attract mates.</p>
<p>What especially interests evolutionary biologists is that bioluminescence did not evolve just once. Genetic and biochemical evidence shows that it has arisen independently dozens of times in unrelated lineages, often through different chemical pathways. This pattern, in which unrelated organisms evolve similar traits independently, is known as convergent evolution, and bioluminescence is one of its most striking examples.</p>""",
        "items": [
            {"num": "C1.1", "prompt": "Ideia principal. What is the main idea of the passage?",
             "options": {"A": "Bioluminescence is a rare adaptation found only in a few deep-sea species.", "B": "Bioluminescence is a widespread, chemically efficient trait that serves multiple functions and evolved independently many times.", "C": "The anglerfish, which uses a glowing lure to catch its prey, is the most important example of bioluminescence.", "D": "Bioluminescent light is less efficient than artificial light because much of its energy is lost as heat."},
             "correct": "B", "explanation": "Cobre os três eixos (o que é + eficiência, funções, evolução independente). (A) contradiz \"remarkably common\"; (C) é detalhe, e o texto diz \"perhaps the most famous\", não \"o mais importante\"; (D) inverte a comparação com a lâmpada."},
            {"num": "C1.2", "prompt": "Detalhe negativo. Which is NOT mentioned as a function of bioluminescence?",
             "options": {"A": "Startling predators", "B": "Attracting prey", "C": "Attracting mates", "D": "Regulating body temperature"},
             "correct": "D", "explanation": "O parágrafo 2 lista defesa, caça e comunicação/atração de parceiros. Regulação de temperatura nunca aparece."},
            {"num": "C1.3", "prompt": "Inferência. It can be inferred from paragraph 2 that in deep-sea environments:",
             "options": {"A": "visual communication is impossible for any species", "B": "organisms rely on producing their own light because there is little to no ambient light", "C": "most species have lost their sense of sight entirely", "D": "bioluminescence is used only for hunting"},
             "correct": "B", "explanation": "O texto diz que \"In the deep sea, darkness is nearly absolute, so visual signals cannot rely on ambient light at all\". Produzir a própria luz resolve a falta de luz ambiente. (A) é extrema; (C) e (D) não têm base no texto."},
            {"num": "C1.4", "prompt": "Propósito retórico. Why does the author state that bioluminescence \"did not evolve just once\"?",
             "options": {"A": "To argue that bioluminescence is less significant than previously thought", "B": "To introduce and support the claim that it is a notable example of convergent evolution", "C": "To explain why some marine species have gone extinct", "D": "To compare bioluminescence with the evolution of eyesight in mammals"},
             "correct": "B", "explanation": "A frase abre o parágrafo e prepara a definição de evolução convergente, que vem duas frases depois: serve para apresentar e embasar a tese de que a bioluminescência é um exemplo notável desse padrão. (A), (C) e (D) não têm base no texto."},
            {"num": "C1.5", "prompt": "Vocabulário em contexto. The word \"striking\" in paragraph 3 is closest in meaning to:",
             "options": {"A": "violent", "B": "notable", "C": "accidental", "D": "doubtful"},
             "correct": "B", "explanation": "\"One of its most striking examples\" é um exemplo notável. (A), (C) e (D) vêm de outros campos de sentido ou invertem o tom."},
        ],
    },
    {
        "id": "mod1-c2",
        "title": "Exercício C2: história (meta de 6 min)",
        "level": "B2–C1",
        "objective": "Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: Coffee Houses in Seventeenth-Century England</strong></p>
<p>The first English coffee house opened in Oxford in 1650; within two decades, London alone had hundreds. For the price of a single cup, a customer could sit for hours, read the newspapers provided by the house, and join whatever conversation was underway. Because admission was cheap and open to any man who could pay, merchants, scholars, clergymen, and minor gentry sat at the same long tables.</p>
<p>This mixing had consequences well beyond casual talk. Particular houses became known for particular subjects: men interested in maritime insurance gathered at Lloyd's, while those following scientific debates went to the houses near the Royal Society. Information that had once circulated slowly, by letter or rumor, now moved quickly through these rooms. Some historians argue that the coffee house functioned as an early public sphere: a space where opinion could form through discussion rather than being handed down by church or crown.</p>
<p>The authorities were uneasy. In 1675, the king issued a proclamation ordering the coffee houses closed, on the grounds that they spread "false, malicious and scandalous reports." The order provoked such immediate opposition that it was withdrawn within days, and the houses continued to operate for another century.</p>""",
        "items": [
            {"num": "C2.1", "prompt": "Ideia principal. The passage is mainly about:",
             "options": {"A": "how coffee was first imported into England", "B": "how English coffee houses became important centers of information and public discussion", "C": "why the king disliked coffee", "D": "the architecture of seventeenth-century London"},
             "correct": "B", "explanation": "O texto traça como as coffee houses viraram centros de informação e discussão pública. (A)/(C)/(D) são detalhes ou não constam."},
            {"num": "C2.2", "prompt": "Inferência. It can be inferred that before coffee houses existed, information among these groups:",
             "options": {"A": "did not exist at all", "B": "traveled more slowly and less widely", "C": "was controlled entirely by merchants", "D": "was freely available to everyone"},
             "correct": "B", "explanation": "O texto diz que \"Information that had once circulated slowly, by letter or rumor, now moved quickly\", ou seja, antes a informação corria mais devagar e chegava a menos gente. (A) exagera; (C) e (D) não têm base no texto."},
            {"num": "C2.3", "prompt": "Propósito retórico. Why does the author mention Lloyd's and the houses near the Royal Society?",
             "options": {"A": "To show that different coffee houses specialized in different topics", "B": "To argue that Lloyd's was the most important coffee house", "C": "To explain how coffee houses were decorated", "D": "To prove that scientists disliked merchants"},
             "correct": "A", "explanation": "\"Particular houses became known for particular subjects\": Lloyd's e as casas perto da Royal Society ilustram a especialização por tema."},
            {"num": "C2.4", "prompt": "Detalhe. The king's 1675 proclamation was:",
             "options": {"A": "enforced for a century", "B": "withdrawn within days after strong opposition", "C": "welcomed by most coffee house owners", "D": "never actually issued"},
             "correct": "B", "explanation": "\"The order provoked such immediate opposition that it was withdrawn within days\". (A) troca a ordem pelas casas, que continuaram funcionando por mais um século; (C) não tem base, e (D) contradiz \"the king issued a proclamation\"."},
            {"num": "C2.5", "prompt": "Vocabulário em contexto. The word \"provoked\" in paragraph 3 is closest in meaning to:",
             "options": {"A": "prevented", "B": "caused", "C": "delayed", "D": "forgave"},
             "correct": "B", "explanation": "\"Provoked such... opposition\" quer dizer que a ordem causou, gerou oposição."},
        ],
    },
    {
        "id": "mod1-c3",
        "title": "Exercício C3: ciências sociais (meta de 6 min)",
        "level": "C1",
        "objective": "Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.",
        "passage_html": """<p><strong>PASSAGE: The Strength of Weak Ties</strong></p>
<p>When people look for a new job, common sense suggests they should turn to their closest contacts: family and good friends who know them well and want to help. Yet when the sociologist Mark Granovetter studied professionals who had recently changed jobs, he found the opposite. Of those who had found their position through a personal contact, most had heard about it not from a close friend but from an acquaintance — someone they saw only occasionally.</p>
<p>Granovetter's explanation rests on how information moves through social networks. Your close friends tend to know one another and move in the same circles you do, so they mostly hear the same news you already have. An acquaintance, by contrast, moves in a different circle and hears different news. A weak tie is therefore a bridge to parts of the network you could not otherwise reach.</p>
<p>The finding has been extended beyond job-hunting: weak ties have been linked to the spread of new ideas between organizations and to innovation within companies, where teams connected to many outside groups tend to produce more original work. Critics note that weak ties carry less trust, so acting on their information involves more risk. But the core insight has held up: the contacts most likely to tell you something new are often the ones you know least well.</p>""",
        "items": [
            {"num": "C3.1", "prompt": "Ideia principal. The main idea of the passage is that:",
             "options": {"A": "close friends are usually the most reliable source of job leads, since they know us well and want to help", "B": "weak ties often supply new information because they link us to other parts of a network", "C": "social networks have no effect on how people find jobs", "D": "Granovetter's study has been completely disproved"},
             "correct": "B", "explanation": "Tese central: weak ties frequentemente trazem informação mais nova porque conectam a outras partes da rede. (A) contradiz o achado; (C)/(D) distorcem."},
            {"num": "C3.2", "prompt": "Detalhe. In Granovetter's study, most of those who found a job through a personal contact heard about it from:",
             "options": {"A": "a family member", "B": "a close friend", "C": "an acquaintance they saw only occasionally", "D": "a recruitment agency"},
             "correct": "C", "explanation": "\"Most had heard about it not from a close friend but from an acquaintance.\""},
            {"num": "C3.3", "prompt": "Inferência. It can be inferred that a person whose contacts are ALL close friends would:",
             "options": {"A": "have access to a wider range of information than average", "B": "tend to hear the same information over and over", "C": "never be able to find a job", "D": "be more innovative at work, since close-knit teams produce more original work"},
             "correct": "B", "explanation": "Se todos os contatos são amigos próximos, que andam nos mesmos círculos, a informação se repete e pouca novidade chega de partes distantes da rede. (A) inverte; (C) exagera; (D) contradiz o parágrafo 3, que liga a inovação a equipes conectadas a muitos grupos de fora."},
            {"num": "C3.4", "prompt": "Propósito retórico. Why does the author mention innovation within companies in paragraph 3?",
             "options": {"A": "To give an example of how the weak-ties finding applies beyond job-hunting", "B": "To argue that companies should fire employees with weak ties", "C": "To contradict Granovetter's original study", "D": "To explain how companies are structured"},
             "correct": "A", "explanation": "O parágrafo 3 lista extensões do achado além da busca de emprego; a inovação nas empresas é um desses exemplos."},
            {"num": "C3.5", "prompt": "Vocabulário em contexto. The word \"bridge\" in paragraph 2 is closest in meaning to:",
             "options": {"A": "obstacle", "B": "connection", "C": "copy", "D": "competitor"},
             "correct": "B", "explanation": "\"A bridge to parts of the network you could not otherwise reach\" é uma ponte, uma conexão."},
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
        "level": "B1–B2",
        "objective": "Ouça cada fala e escolha a resposta mais natural. A fala aparece escrita depois que você responde. Tempo-alvo: 12 segundos por item.",
        "passage_html": None,
        "items": [
            {"num": "A1", "prompt": "\"I was going to grab lunch before the seminar, but there's no time now.\"",
             "options": {"A": "I usually have lunch at the café downstairs.", "B": "Yeah, let's just head straight there.", "C": "The seminar was really interesting.", "D": "I ate there last week too."},
             "correct": "B", "explanation": "O falante sinaliza falta de tempo; a resposta natural propõe a ação consequente. (A) reaproveita <em>lunch</em> sem reagir à falta de tempo; (C)/(D) ignoram a urgência."},
            {"num": "A2", "prompt": "\"Do you mind if I borrow your notes from Tuesday? I was out sick.\"",
             "options": {"A": "Sure, I'll send them over tonight.", "B": "I hope you feel better soon.", "C": "I borrowed a book from the library on Tuesday.", "D": "Tuesday's class starts at nine."},
             "correct": "A", "explanation": "A um pedido direto, a resposta natural é aceitar e combinar um plano. (B) é gentil, mas não responde ao pedido; (C) e (D) só repetem palavras da fala (<em>borrow</em>, <em>Tuesday</em>)."},
            {"num": "A3", "prompt": "\"Honestly, I'm not sure this draft is ready to submit.\"",
             "options": {"A": "I'm sure the printer is ready.", "B": "What do you think it still needs?", "C": "I submitted mine yesterday.", "D": "That's a great title."},
             "correct": "B", "explanation": "Diante da insegurança sobre o rascunho, a resposta natural procura o problema específico. (A) repete <em>ready</em> sem tratar da preocupação; (C) e (D) ignoram a preocupação."},
            {"num": "A4", "prompt": "\"You're not still planning to walk in this weather, are you?\"",
             "options": {"A": "No, I'll catch the bus instead.", "B": "The weather report comes on at six.", "C": "I walked there yesterday.", "D": "It rained a lot last semester too."},
             "correct": "A", "explanation": "A pergunta retórica é um alerta educado sobre ir a pé com esse tempo, e a resposta natural muda o plano. (B) só repete <em>weather</em>; (C) e (D) falam de outro momento e ignoram o alerta."},
            {"num": "A5", "prompt": "\"I heard the registrar's office changed their hours.\"",
             "options": {"A": "I registered for four classes this term.", "B": "Really? Do you know the new schedule?", "C": "The office is on the second floor.", "D": "I haven't registered for anything yet."},
             "correct": "B", "explanation": "Diante de uma informação nova (a mudança de horário), a resposta natural mostra interesse e pede um detalhe. (A) e (D) aproveitam o som de <em>registrar</em> em <em>register</em> (matricular-se), mas não reagem à notícia; (C) dá a localização do escritório, que ninguém perguntou."},
            {"num": "A6", "prompt": "\"Could you run your presentation by me before the meeting?\"",
             "options": {"A": "I ran three miles this morning.", "B": "Sure, are you free around four?", "C": "The meeting's been moved to Thursday.", "D": "I gave my first presentation in high school."},
             "correct": "B", "explanation": "\"Run X by me\" é \"me mostrar antes\", e a resposta natural marca um horário. (A) toma \"run\" ao pé da letra; (C) muda o foco; (D) repete <em>presentation</em> sem responder ao pedido."},
            {"num": "A7", "prompt": "\"I thought the lab report was due next week, not tomorrow.\"",
             "options": {"A": "So did I. Let me double-check the syllabus.", "B": "The lab is on the ground floor.", "C": "I finished my report last month.", "D": "Next week works better for me too."},
             "correct": "A", "explanation": "Diante da dúvida sobre a data, a resposta natural é conferir junto no syllabus. (B), (C) e (D) ignoram a dúvida."},
            {"num": "A8", "prompt": "\"Would you rather present first or last?\"",
             "options": {"A": "The last presentation ran over time.", "B": "Last, if that's an option. I need time to prepare.", "C": "The presentation is worth 20% of the grade.", "D": "First place goes to the best presentation."},
             "correct": "B", "explanation": "Numa pergunta de preferência (primeiro ou último), a resposta natural escolhe e justifica. (A), (C) e (D) não respondem à escolha oferecida."},
            {"num": "A9", "prompt": "\"This bus is taking forever. We should've left earlier.\"",
             "options": {"A": "The bus stop is right over there.", "B": "Tell me about it. I hate cutting it this close.", "C": "I take this bus every day.", "D": "I left my umbrella on the bus once."},
             "correct": "B", "explanation": "Diante da reclamação sobre a demora, \"Tell me about it\" concorda com ênfase e acrescenta algo. (A), (C) e (D) repetem <em>bus</em> ou <em>left</em> sem reagir à reclamação."},
            {"num": "A10", "prompt": "\"Professor Lin said she might cancel Friday's class.\"",
             "options": {"A": "She's a great lecturer, isn't she?", "B": "Did she say why, or was it just a maybe?", "C": "Friday's class is in the east building.", "D": "I've never had a class canceled before."},
             "correct": "B", "explanation": "Diante de uma notícia incerta (\"might cancel\"), a resposta natural pede esclarecimento sobre o motivo ou a certeza. (A), (C) e (D) desviam do assunto."},
            {"num": "A11", "prompt": "\"I've been meaning to ask: how did the interview go?\"",
             "options": {"A": "It's at two o'clock on Thursday.", "B": "Better than I expected, actually. They said they'd call by Friday.", "C": "I've had a lot of interviews lately.", "D": "The company is downtown, near the station."},
             "correct": "B", "explanation": "A pergunta é sobre como foi a entrevista, e a resposta natural conta o resultado e o próximo passo. (A) responde sobre horário; (C) e (D) generalizam ou desviam."},
            {"num": "A12", "prompt": "\"Do you think it's worth applying? I doubt I'd get in.\"",
             "options": {"A": "The application fee is fifty dollars.", "B": "You never know unless you try. I'd go for it.", "C": "I applied there two years ago.", "D": "The program starts in September."},
             "correct": "B", "explanation": "Diante de dúvida e autocrítica, a resposta natural é encorajar. (A), (C) e (D) desviam para custo, experiência passada e calendário."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo B: Listen to a Conversation — 3
# diálogos com 2 perguntas cada (6 itens), como na prova de 2026.
MOD2_ACTION_DRILLS_B = [
    {
        "id": "mod2-b1",
        "title": "Exercício B1: Advising Office (meta de 3 min)",
        "level": "B1–B2",
        "objective": "Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 3 minutos.",
        "passage_html": """<p><em>Narrator: Listen to a conversation between a student and an academic advisor.</em></p>
<p><strong>Student:</strong> Hi, I wanted to ask about switching one of my electives. I'm in Intro to Statistics, but I'd rather take Data Visualization this term.</p>
<p><strong>Advisor:</strong> Let me check... okay, Data Visualization has space. But it has Statistics as a prerequisite — have you completed that?</p>
<p><strong>Student:</strong> No, I'm taking it right now. I was hoping to take Data Visualization first and Statistics later.</p>
<p><strong>Advisor:</strong> Ah. Unfortunately that's not possible; the prerequisite is enforced by the system. You'd need to finish Statistics first, or get a written waiver from the Data Visualization instructor.</p>
<p><strong>Student:</strong> Is it worth asking the instructor directly, or is that rarely approved?</p>
<p><strong>Advisor:</strong> It's approved sometimes, especially if you have relevant experience — a coding background, say. Do you have any?</p>
<p><strong>Student:</strong> I do, actually — I took two programming courses last year.</p>
<p><strong>Advisor:</strong> Then it's worth emailing her. I'll send you her contact information now.</p>""",
        "items": [
            {"num": "B1.1", "prompt": "Gist-purpose. Why does the student visit the advising office?",
             "options": {"A": "To complain about a scheduling conflict between two required courses", "B": "To request a change from one elective to another", "C": "To register for classes for the first time", "D": "To find out why she was removed from a course"},
             "correct": "B", "explanation": "A estudante quer \"switch one of my electives\". (A) sem conflito de horário; (C) já está matriculada; (D) está fora do que foi dito."},
            {"num": "B1.2", "prompt": "Function. Why does the advisor ask whether the student has a coding background?",
             "options": {"A": "To check whether she qualifies for a scholarship", "B": "To suggest she switch majors", "C": "To assess whether the instructor might realistically grant a waiver", "D": "To recommend a different course"},
             "correct": "C", "explanation": "A pergunta avalia se a professora poderia dar um <em>waiver</em>. (A)/(B)/(D) sem base no diálogo."},
        ],
    },
    {
        "id": "mod2-b2",
        "title": "Exercício B2: Library Reserve Desk (meta de 3 min)",
        "level": "B1–B2",
        "objective": "Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 3 minutos.",
        "passage_html": """<p><em>Narrator: Listen to a conversation between a student and a librarian.</em></p>
<p><strong>Student:</strong> Hi — I'm looking for a book my professor put on reserve for the history seminar. It's <em>The Making of the Atlantic World</em>.</p>
<p><strong>Librarian:</strong> Let me look... yes, we have two copies on reserve. Reserve items are two-hour loans, in-library use only. You can't take them out of the building.</p>
<p><strong>Student:</strong> Oh. I was hoping to take it home for the weekend — the essay's due Monday.</p>
<p><strong>Librarian:</strong> For reserve items, no, sorry. But here's an option: there's a circulating copy in the stacks, on the fourth floor. That one you <em>can</em> take out, for three weeks.</p>
<p><strong>Student:</strong> Great, I'll grab that instead. Is it available right now?</p>
<p><strong>Librarian:</strong> The catalog says one copy is in. If it's not on the shelf, come back and I'll place a hold on the reserve copy for you to use here.</p>
<p><strong>Student:</strong> Thanks — I'll check the stacks first.</p>""",
        "items": [
            {"num": "B2.1", "prompt": "Detail. What is the rule for reserve items?",
             "options": {"A": "They can be borrowed for three weeks", "B": "They are two-hour loans, for use inside the library only", "C": "They cannot be used by undergraduates", "D": "They must be requested 24 hours in advance"},
             "correct": "B", "explanation": "\"Two-hour loans, in-library use only... can't take them out of the building.\" (A) descreve o exemplar da circulação; (C)/(D) não ditos."},
            {"num": "B2.2", "prompt": "Inference. What will the student probably do next?",
             "options": {"A": "Place a hold on the reserve copy immediately", "B": "Go to the fourth floor to look for the circulating copy", "C": "Leave the library without the book", "D": "Ask the professor to extend the deadline"},
             "correct": "B", "explanation": "\"I'll check the stacks first.\" Inferência direta. (A) só se não achar; (C)/(D) contradizem a intenção declarada."},
        ],
    },
    {
        "id": "mod2-b3",
        "title": "Exercício B3: After Class (meta de 3 min)",
        "level": "B1–B2",
        "objective": "Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 3 minutos.",
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
            {"num": "B3.1", "prompt": "Detail. According to the professor, what does \"evaluate\" mean here?",
             "options": {"A": "Summarize the argument accurately", "B": "Simply agree or disagree with the argument", "C": "Weigh the argument's strengths, weaknesses, and use of evidence", "D": "Compare the argument with another author's"},
             "correct": "C", "explanation": "\"Weigh the argument: where is it strong, where is it weak, and does the evidence actually support the conclusion?\" (A)/(B) o professor diz que \"evaluate\" é <strong>nenhum</strong> dos dois; (D) não dito."},
            {"num": "B3.2", "prompt": "Meaning of an expression. What does the professor mean by \"Don't pad it\"?",
             "options": {"A": "Write more than 1,500 words to be safe", "B": "Don't add filler just to reach the word count", "C": "Use larger margins and spacing", "D": "Include as many quotations as possible"},
             "correct": "B", "explanation": "\"Don't pad it\" é \"não encha linguiça\" só para chegar ao número de palavras. (A) diz o oposto; (C) e (D) estão fora do que foi dito."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo C: Listen to an Announcement — 3
# anúncios com 2 perguntas cada (6 itens), como na prova de 2026.
MOD2_ACTION_DRILLS_C = [
    {
        "id": "mod2-c1",
        "title": "Exercício C1: Library Services (meta de 2 min)",
        "level": "B1",
        "objective": "Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about a change to library services.</em></p>
<p><strong>Speaker:</strong> Attention, students. Starting next Monday, the Main Library's third-floor reading room will be closed for renovation through the end of the month. During this period you can use the East Wing reading room instead, which keeps its regular hours. Reserved study rooms originally booked for the third floor have already been transferred automatically to the East Wing — you don't need to rebook. However, if your reservation was for a room with audiovisual equipment, please double-check availability, since not all East Wing rooms are equipped. Questions go to the circulation desk.</p>""",
        "items": [
            {"num": "C1.1", "prompt": "Detail. What happens to previously reserved study rooms?",
             "options": {"A": "They are canceled and must be rebooked", "B": "They are automatically transferred to the East Wing", "C": "They stay on the third floor", "D": "They are honored only if confirmed by email"},
             "correct": "B", "explanation": "\"Transferred automatically to the East Wing — you don't need to rebook.\" (A) é o oposto; (D) adiciona uma condição não dita."},
            {"num": "C1.2", "prompt": "Function. Why does the speaker mention audiovisual equipment?",
             "options": {"A": "To announce that all AV equipment is being removed", "B": "To tell students to avoid using AV equipment during renovations", "C": "To warn that not every transferred room has the same equipment as before", "D": "To advertise a new AV rental service"},
             "correct": "C", "explanation": "Aviso prático de que \"not all East Wing rooms are equipped\". (A)/(D) exageram; (B) está fora do que foi dito."},
        ],
    },
    {
        "id": "mod2-c2",
        "title": "Exercício C2: Course Registration (meta de 2 min)",
        "level": "B1",
        "objective": "Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about course registration.</em></p>
<p><strong>Speaker:</strong> A reminder to all second-year students: registration for spring courses opens this Thursday at 8 a.m. and closes the following Wednesday at midnight. Register early — popular courses fill within hours. If a course you need is full, add yourself to the waitlist rather than emailing the instructor; the system releases spots automatically as students drop, and it works strictly in waitlist order. One change this year: the add/drop period after classes begin has been shortened from two weeks to one, so finalize your schedule before the term starts, not after.</p>""",
        "items": [
            {"num": "C2.1", "prompt": "Detail. What should a student do if a course is full?",
             "options": {"A": "Email the instructor to ask for a spot", "B": "Register for a different course permanently", "C": "Add themselves to the waitlist", "D": "Wait until the add/drop period"},
             "correct": "C", "explanation": "\"Add yourself to the waitlist rather than emailing the instructor.\" (A) é explicitamente desaconselhado."},
            {"num": "C2.2", "prompt": "Inference. Why does the speaker emphasize finalizing the schedule before the term?",
             "options": {"A": "Because instructors will not answer email during the term", "B": "Because there will be less time to change courses once classes start", "C": "Because spring courses are harder than fall courses", "D": "Because registration reopens midway through the term"},
             "correct": "B", "explanation": "Com o período de add/drop mais curto, sobra menos tempo para ajustar a matrícula depois que as aulas começam. (A), (C) e (D) não são ditos no anúncio."},
        ],
    },
    {
        "id": "mod2-c3",
        "title": "Exercício C3: Campus Event (meta de 2 min)",
        "level": "B1",
        "objective": "Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 2 minutos.",
        "passage_html": """<p><em>Narrator: Listen to an announcement about a career event.</em></p>
<p><strong>Speaker:</strong> The annual Career Fair takes place next Wednesday from 10 to 4 in the main gymnasium. Over eighty employers will attend, mostly in engineering, healthcare, and education. A few reminders. Bring several printed copies of your résumé — most recruiters still expect a paper copy. Business-casual dress is recommended, not required. The résumé-review station near the entrance will be open from 9, an hour before the fair, and it operates first-come, first-served, so arrive early if you want feedback before talking to employers. Finally, the 9:30 workshop on interview skills is now full; a recording will be posted next week for those who missed it.</p>""",
        "items": [
            {"num": "C3.1", "prompt": "Detail. What time does the Career Fair itself begin?",
             "options": {"A": "9 a.m.", "B": "9:30 a.m.", "C": "10 a.m.", "D": "4 p.m."},
             "correct": "C", "explanation": "\"From 10 to 4.\" (A) é a abertura da estação de revisão de currículo; (B) é o workshop."},
            {"num": "C3.2", "prompt": "Connecting content. A student wants résumé feedback before speaking to employers. What should they do?",
             "options": {"A": "Attend the 9:30 workshop", "B": "Arrive at the résumé-review station around 9, since it is first-come, first-served", "C": "Email their résumé to a recruiter in advance", "D": "Wait until after 4 p.m."},
             "correct": "B", "explanation": "A estação abre às 9 e funciona por ordem de chegada (<em>first-come, first-served</em>), por isso vale chegar cedo. (A) erra porque o workshop é de entrevista, não de revisão de currículo; (C) e (D) não são sugeridos."},
        ],
    },
]

# PARTE 5 (Action Drills) do M2, Grupo D: Listen to an Academic Talk — 3
# palestras com 4 perguntas cada (12 itens), como na prova de 2026.
MOD2_ACTION_DRILLS_D = [
    {
        "id": "mod2-d1",
        "title": "Exercício D1: psicologia (meta de 4 min)",
        "level": "B2–C1",
        "objective": "Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a psychology class.</em></p>
<p><strong>Professor:</strong> We've been discussing decision-making, and today I want to bring up something researchers call the paradox of choice. The idea is counterintuitive: you'd think more options would always make us happier, but past a certain point it does the opposite.</p>
<p>A classic example. In one well-known study, researchers set up a tasting table in a grocery store: first with six varieties of jam, then with twenty-four. You'd expect the bigger display to sell more. Actually, the smaller display generated significantly more purchases. The larger one attracted more browsers, but far fewer of them bought anything.</p>
<p>Why? Two things: decision fatigue and anticipated regret. With more options, comparing them mentally becomes exhausting — that's the fatigue. And even before you pick, you start worrying that one of the other twenty-three might be better and that you'll regret your choice — that's the regret. Ironically, more choices can leave people stuck at square one, unable to commit at all.</p>
<p>Now, this doesn't mean choice is bad: a complete absence of options is its own problem. The point is there's a sweet spot, and past it, additional options stop helping and start working against us. To be fair, later studies haven't always replicated the jam result, so the size of the effect is still debated.</p>""",
        "items": [
            {"num": "D1.1", "prompt": "Gist-content. What is the talk mainly about?",
             "options": {"A": "Grocery stores should minimize the products they display", "B": "Beyond a point, more options can reduce satisfaction and hinder decisions", "C": "Consumers always prefer smaller displays", "D": "Decision fatigue affects only in-store shoppers"},
             "correct": "B", "explanation": "Tese anunciada no início e no fechamento. (A) exagera; (C) também exagera (\"always\") e generaliza um único estudo; (D) está fora do que foi dito."},
            {"num": "D1.2", "prompt": "Detail. What happened with the 24-variety display?",
             "options": {"A": "It attracted more browsers but produced fewer purchases", "B": "It produced both more browsers and more purchases", "C": "It was removed for low interest", "D": "It produced identical sales to the smaller display"},
             "correct": "A", "explanation": "\"Attracted more browsers, but far fewer of them bought anything.\" (B) é o oposto."},
            {"num": "D1.3", "prompt": "Organization. Why does the professor describe the grocery store study in detail?",
             "options": {"A": "To criticize the researchers' methodology", "B": "To give concrete evidence for the paradox of choice", "C": "To introduce an unrelated topic about marketing", "D": "To explain how stores design displays"},
             "correct": "B", "explanation": "Exemplo empírico logo após o conceito abstrato. (A)/(C)/(D) sem base."},
            {"num": "D1.4", "prompt": "Idiom in context. What does \"stuck at square one\" mean here?",
             "options": {"A": "Making a confident final decision", "B": "Unable to make any progress toward a decision", "C": "Choosing the first option presented", "D": "Comparing two options systematically"},
             "correct": "B", "explanation": "\"Stuck at square one\" é ficar sem sair do ponto de partida. (A) diz o oposto; (C) e (D) distorcem o sentido."},
        ],
    },
    {
        "id": "mod2-d2",
        "title": "Exercício D2: biologia (meta de 4 min)",
        "level": "B2–C1",
        "objective": "Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a biology class.</em></p>
<p><strong>Professor:</strong> When we picture a forest, we tend to see individual trees competing — for light, for water, for space. And that's real. But over the last thirty years, research has revealed something the old picture missed: the trees are also <strong>connected</strong>, underground, through fungi.</p>
<p>Here's how. The roots of most trees are wrapped in a network of fungal threads; this partnership between root and fungus is called a mycorrhiza. The fungi pull in water and minerals the tree's roots can't reach efficiently, and hand them to the tree. In return, the tree gives the fungi sugars it makes through photosynthesis. So far, a simple trade.</p>
<p>The surprising part is that a single fungal network can link <strong>many</strong> trees at once — even trees of different species. And things move along those links. Experiments using radioactive tracers have shown carbon flowing from a tree standing in full sun to a shaded seedling of another species nearby. Some researchers describe old, well-connected trees as "hub trees" that support younger ones around them.</p>
<p>Now, a word of caution. This work has captured the public imagination, and some popular accounts overstate it: talking about forests as single cooperative organisms. The jury's still out on how deliberate or widespread the sharing really is. What's solid is that the connections exist and that resources can move through them. How much that reshapes our model of the forest is still being worked out.</p>""",
        "items": [
            {"num": "D2.1", "prompt": "Gist-content. What is the main point of the talk?",
             "options": {"A": "Trees in a forest only compete, never cooperate", "B": "Trees are connected underground through fungal networks, and resources can move between them", "C": "Mycorrhizal fungi are harmful to most trees", "D": "Forests are single cooperative organisms"},
             "correct": "B", "explanation": "O professor admite a competição <strong>mas</strong> acrescenta a conexão. (A) ignora a segunda metade da tese; (C) é o oposto (a relação é benéfica); (D) é exatamente o exagero que ele critica no fim."},
            {"num": "D2.2", "prompt": "Detail. What does the tree give the fungi in the relationship?",
             "options": {"A": "Water it pulls from deep soil", "B": "Minerals from its leaves", "C": "Sugars made through photosynthesis", "D": "Nothing — the relationship is one-directional"},
             "correct": "C", "explanation": "\"The tree gives the fungi sugars it makes through photosynthesis.\" (A)/(B) são o que os fungos fazem pela árvore; (D) é o oposto."},
            {"num": "D2.3", "prompt": "Attitude / Organization. Why does the professor add \"a word of caution\" near the end?",
             "options": {"A": "To retract everything said earlier in the talk", "B": "To distinguish what the evidence firmly supports from claims that popular accounts exaggerate", "C": "To argue that the research is worthless", "D": "To introduce a completely different topic"},
             "correct": "B", "explanation": "Ele separa o que a evidência sustenta firmemente do que relatos populares exageram (\"forests as single cooperative organisms\"). (A)/(C) exageram; (D) está fora do que foi dito."},
            {"num": "D2.4", "prompt": "Idiom in context. What does the professor mean by \"the jury's still out\"?",
             "options": {"A": "The question has been definitively settled", "B": "There is not yet a firm conclusion on the matter", "C": "A court case is involved in the research", "D": "The researchers have stopped studying it"},
             "correct": "B", "explanation": "\"The jury's still out\" quer dizer que ainda não há conclusão firme. (A) diz o oposto; (C) é literal demais; (D) não é dito."},
        ],
    },
    {
        "id": "mod2-d3",
        "title": "Exercício D3: história da tecnologia (meta de 4 min)",
        "level": "B2–C1",
        "objective": "Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. Tempo-alvo: 4 minutos.",
        "passage_html": """<p><em>Narrator: Listen to part of a talk in a history of technology class.</em></p>
<p><strong>Professor:</strong> Look at your keyboard. The top row of letters spells Q-W-E-R-T-Y. It's an odd arrangement — the most common letters aren't under your strongest fingers. So why has it survived, essentially unchanged, for a hundred and fifty years?</p>
<p>The layout dates from the 1870s, from early mechanical typewriters. The common story is that QWERTY was designed to <em>slow typists down</em> so the metal type-bars wouldn't jam. That's probably an oversimplification (the real design pressures were more mixed), but the key point is that the layout was shaped by the constraints of 1870s <strong>machinery</strong>, constraints that vanished decades ago.</p>
<p>Better layouts have been proposed. The best known, Dvorak, was patented in 1936 and, in some studies, allows modestly faster and more comfortable typing. Yet it never caught on. Why not?</p>
<p>This is a textbook case of what economists call <strong>path dependence</strong>, or sometimes "lock-in." Once QWERTY became the standard, everything organized itself around that standard: typewriters were built for it, typing was taught on it, and every new typist learned it because that's what the machines used — and machines used it because that's what typists knew. To switch, a single person gains little unless nearly everyone switches at once. The cost of coordinating that switch is enormous, and no one bears it. So an arrangement that made sense only for 1870s hardware is still, quietly, on every device you own.</p>""",
        "items": [
            {"num": "D3.1", "prompt": "Gist-content. What is the talk mainly about?",
             "options": {"A": "How to type faster using the Dvorak layout", "B": "Why an outdated keyboard layout has persisted, as an example of path dependence", "C": "The mechanical design of 19th-century typewriters", "D": "Why Dvorak is objectively the best possible layout"},
             "correct": "B", "explanation": "A pergunta central é por que um layout ultrapassado sobreviveu, e a resposta é <em>path dependence</em>. (A)/(D) mudam o foco/exageram; (C) é contexto, não o tema."},
            {"num": "D3.2", "prompt": "Detail. What does the professor say about the \"common story\" that QWERTY was designed to slow typists down?",
             "options": {"A": "It is completely accurate", "B": "It is probably an oversimplification, though the layout was shaped by 1870s machinery", "C": "It was invented by economists", "D": "It explains why Dvorak succeeded"},
             "correct": "B", "explanation": "\"That's probably an oversimplification... but the layout was shaped by 1870s machinery.\""},
            {"num": "D3.3", "prompt": "Organization. Why does the professor describe how typists learned QWERTY because machines used it, and machines used it because typists knew it?",
             "options": {"A": "To illustrate how lock-in makes a standard self-reinforcing and hard to change", "B": "To criticize typewriter manufacturers", "C": "To explain how mechanical type-bars work", "D": "To argue that QWERTY is actually well designed"},
             "correct": "A", "explanation": "O ciclo ilustra como o padrão se autorreforça (<em>lock-in</em>). (B)/(C)/(D) sem base."},
            {"num": "D3.4", "prompt": "Word in context. When the professor says the old arrangement is \"still, quietly, on every device you own,\" the word \"quietly\" suggests that:",
             "options": {"A": "the change from typewriters to computers happened slowly", "B": "most people use QWERTY without noticing that it is an outdated design", "C": "manufacturers have hidden the layout's origins", "D": "QWERTY is gradually disappearing from new devices"},
             "correct": "B", "explanation": "\"Quietly\" sugere que as pessoas usam QWERTY sem perceber que é um design obsoleto. (A) não tem relação com a palavra; (C) lê \"quietly\" como segredo, ideia que a palestra não sustenta; (D) contradiz \"on every device you own\"."},
        ],
    },
]


# PARTE 7 do M5 (Registro): os exercícios de elevação, antes só texto, em
# múltipla escolha. Rascunho do Gemini revisado pelo Claude em 2026-11-07
# (itoefl-gerencia/m5m6/REVISAO-claude.md). "fonte" = linha do .md original.
# Contam nos pontos fracos em Registro.
MOD5_DRILLS = [{'id': 'mod5-x-1',
  'title': 'Exercício 1: Elevação de frases para B2 (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Escolha a opção que eleva cada frase de nível B1 para o nível B2 com precisão vocabular e controle '
               'gramatical, mantendo o sentido original. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '1.1',
             'prompt': 'Frase original (B1): "Technology is important because it helps people work faster."',
             'options': {'A': 'Technology matters because it lets people work far more efficiently than before.',
                         'B': 'Technology is crucial because it makes people to work much faster than before.',
                         'C': 'Technology matters although it lets people work far more efficiently than before.',
                         'D': 'Technology is important so that it helps people working much faster every day.'},
             'correct': 'A',
             'explanation': 'Você ganha precisão em B2 ao trocar <em>is important</em> por <strong>matters</strong> e '
                            '<em>work faster</em> por <em>work far more efficiently</em>. A melhor armadilha é a (C), '
                            'que usa o mesmo vocabulário, mas troca <em>because</em> por <em>although</em> e quebra a '
                            'relação de causa; já a (B) erra a regência em <em>makes people to work</em>.',
             'fonte': 'Parte 7, Exercício 1, item 1 (linhas 639 e 652)'},
            {'num': '1.2',
             'prompt': 'Frase original (B1): "Many students feel stressed during exams. This is a problem."',
             'options': {'A': 'Exam-related stress are widespread and affects student performance.',
                         'B': 'Exam-related stress is widespread and affects performance.',
                         'C': 'Many students feel stressed in exams, which it is a big problem.',
                         'D': 'Because exam-related stress is widespread, it benefits performance.'},
             'correct': 'B',
             'explanation': 'A opção (B) comprime as duas frases soltas em uma única oração densa usando o grupo '
                            'nominal <strong>exam-related stress</strong>. A alternativa (A) chega perto, mas desliza '
                            'na concordância com <em>stress are</em>; a (C) repete o pronome em <em>which it is</em> e '
                            'mantém o nível B1.',
             'fonte': 'Parte 7, Exercício 1, item 2 (linhas 640 e 653)'},
            {'num': '1.3',
             'prompt': 'Frase original (B1): "Remote work is good but it can make people feel alone."',
             'options': {'A': 'Remote work has clear benefits, therefore isolation is a real cost.',
                         'B': 'Remote work is very good, despite isolation is a real cost.',
                         'C': 'Remote work has clear benefits, though isolation is a real cost.',
                         'D': 'Remote work has clear benefits, because isolation is a real cost.'},
             'correct': 'C',
             'explanation': 'Em (C), você substitui o adjetivo genérico <em>good</em> por <strong>clear '
                            'benefits</strong> e marca a concessão com <em>though</em>. A opção (B) é um ponto de '
                            'atenção clássico: <em>despite</em> pede um grupo nominal, e não uma oração completa como '
                            '<em>isolation is a real cost</em>. Já (A) e (D) trocam o contraste por conclusão ou '
                            'causa.',
             'fonte': 'Parte 7, Exercício 1, item 3 (linhas 641 e 654)'},
            {'num': '1.4',
             'prompt': 'Frase original (B1): "The city built a new park. Now more people exercise outside."',
             'options': {'A': 'Before the city opened a new park, outdoor exercise rose noticeably.',
                         'B': 'After the city opened a new park, outdoor exercise fell noticeably.',
                         'C': 'Although the city opened a new park, outdoor exercise rose noticeably.',
                         'D': 'After the city opened a new park, outdoor exercise rose noticeably.'},
             'correct': 'D',
             'explanation': 'A alternativa (D) integra a sequência temporal com <em>After</em> e eleva o vocabulário '
                            'em <strong>outdoor exercise rose noticeably</strong>. A opção (C) é a armadilha mais '
                            'próxima, mas usa <em>Although</em> onde não há oposição entre abrir o parque e o aumento '
                            'de exercício.',
             'fonte': 'Parte 7, Exercício 1, item 4 (linhas 642 e 655)'},
            {'num': '1.5',
             'prompt': 'Frase original (B1): "Learning a second language is useful for getting a job."',
             'options': {'A': 'A second language is a substantial advantage at the job market.',
                         'B': 'A second language is a substantial advantage in the job market.',
                         'C': 'A second language is a small advantage in the job market today.',
                         'D': 'Learning a second language is useful for get a good job today.'},
             'correct': 'B',
             'explanation': 'A opção (B) troca <em>useful for getting a job</em> pela colocação natural '
                            '<strong>substantial advantage in the job market</strong>. A alternativa (A) parece '
                            'idêntica, mas tropeça na preposição ao usar <em>at the job market</em> em vez de '
                            '<em>in</em>.',
             'fonte': 'Parte 7, Exercício 1, item 5 (linhas 643 e 656)'}]},
 {'id': 'mod5-x-2',
  'title': 'Exercício 2: Elevação de frases para C1 (meta de 5 min)',
  'level': 'C1–C2',
  'objective': 'Escolha a opção que transforma cada frase de nível B1 em uma construção de nível C1 com foco analítico '
               'e densidade sintática. Tempo-alvo: 5 minutos.',
  'passage_html': None,
  'items': [{'num': '2.1',
             'prompt': 'Frase original (B1): "Social media connects people but it also spreads false information."',
             'options': {'A': 'The same architecture that lets social media connect people at scale is what lets '
                              'falsehoods travel at that scale.',
                         'B': 'The same architecture that lets social media to connect people at scale is what lets '
                              'falsehoods travel at scale.',
                         'C': 'What makes social media important is that it connects many people and also spreads '
                              'false information very fast.',
                         'D': 'Notwithstanding that social media connects people at scale, the architecture prevents '
                              'falsehoods from traveling far.'},
             'correct': 'A',
             'explanation': 'A opção (A) atinge o nível C1 ao explicar o <strong>mecanismo</strong> comum aos dois '
                            'efeitos com paralelismo e frase clivada. A alternativa (B) é quase igual, mas erra a '
                            'gramática ao incluir <em>to</em> após o verbo <em>let</em> (<em>lets social media to '
                            'connect</em>).',
             'fonte': 'Parte 7, Exercício 1, item 6 (linhas 644 e 657)'},
            {'num': '2.2',
             'prompt': 'Frase original (B1): "The company hired more staff. The waiting time went down."',
             'options': {'A': 'It was the staffing increase, not the new software, what brought waiting times down.',
                         'B': 'What brought waiting times down was that the staffing increase hired more staff.',
                         'C': 'It was the staffing increase, not the new software, that brought waiting times down.',
                         'D': 'Not only the staffing increase brought waiting times down, but it also helped staff.'},
             'correct': 'C',
             'explanation': 'A alternativa (C) aplica com perfeição a estrutura <strong>it-cleft</strong> (<em>It was '
                            'X, not Y, that...</em>) combinada à nominalização <em>staffing increase</em>. A opção (A) '
                            'traz um deslize muito frequente: usar <em>what</em> no lugar de <em>that</em> para fechar '
                            'uma frase clivada com <em>It was</em>.',
             'fonte': 'Parte 7, Exercício 1, item 7 (linhas 645 e 658)'},
            {'num': '2.3',
             'prompt': 'Frase original (B1): "Reading books is better than watching videos for learning."',
             'options': {'A': 'Reading moves at a pace the video sets; the reader sets its own, and comprehension '
                              'quietly rises to match.',
                         'B': 'Reading moves at a pace the reader sets; video sets its own, and comprehension quietly '
                              'drops to match.',
                         'C': 'Reading books is better than videos; because the reader sets the pace, and learning is '
                              'much more good.',
                         'D': 'Reading moves at a pace the reader sets; video sets its own, so comprehension quickly '
                              'rises to match it.'},
             'correct': 'B',
             'explanation': 'Em (B), você substitui o adjetivo vago <em>better</em> pelo mecanismo real de controle de '
                            'ritmo, criando <strong>densidade analítica</strong>. A opção (D) mantém a estrutura, mas '
                            'inverte o sentido final ao dizer que a compreensão sobe com o ritmo imposto pelo vídeo.',
             'fonte': 'Parte 7, Exercício 1, item 8 (linhas 646 e 659)'},
            {'num': '2.4',
             'prompt': 'Frase original (B1): "Public transport is cheaper than driving. It is also better for the '
                       'air."',
             'options': {'A': 'Public transport is the rare option that is more expensive for the individual and '
                              'cleaner for everyone else at the same time.',
                         'B': 'Public transport is the rare option that is cheaper for the individual nor cleaner for '
                              'everyone else at the same time.',
                         'C': 'Public transport is the rare option who is cheaper for the individual and cleaner for '
                              'everyone else at the same time.',
                         'D': 'Public transport is the rare option that is cheaper for the individual and cleaner for '
                              'everyone else at the same time.'},
             'correct': 'D',
             'explanation': 'A resposta (D) integra os dois benefícios em uma única frase com '
                            '<strong>paralelismo</strong> (<em>cheaper for the individual and cleaner for everyone '
                            'else</em>). A opção (C) erra o pronome relativo ao usar <em>who</em> para '
                            '<em>option</em>, e a (A) inverte o sentido de <em>cheaper</em>.',
             'fonte': 'Parte 7, Exercício 1, item 9 (linhas 647 e 660)'},
            {'num': '2.5',
             'prompt': 'Frase original (B1): "Some students cheat on tests. Schools should stop this."',
             'options': {'A': 'Cheating is more a discipline problem than a design one: it thrives whenever the stakes '
                              'are low and the format is hard to game.',
                         'B': 'Cheating is less a design problem than a discipline one: it disappears wherever the '
                              'stakes are high and the format is easy to game.',
                         'C': 'Cheating is less a discipline problem than a design one: it thrives wherever the stakes '
                              'are high and the format is easy to game.',
                         'D': 'Cheating is less a discipline problem than a design one: it thrives wherever the stakes '
                              'are high or the format are easy to game.'},
             'correct': 'C',
             'explanation': 'A alternativa (C) faz um <strong>reenquadramento</strong> de nível C1 ao deslocar o foco '
                            'da disciplina para o desenho da avaliação. A opção (D) é quase idêntica, mas quebra a '
                            'concordância verbal no final com <em>the format are</em>.',
             'fonte': 'Parte 7, Exercício 1, item 10 (linhas 648 e 661)'}]},
 {'id': 'mod5-x-3',
  'title': 'Exercício 3: Nominalização de processos (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Escolha o grupo nominal que transforma corretamente o verbo em destaque em uma nominalização de nível '
               'C1 (Marcador 6). Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '3.1',
             'prompt': 'Frase-base: "Fewer people are reading newspapers."',
             'options': {'A': 'the growth in newspaper readership',
                         'B': 'the decline of reading newspapers people',
                         'C': 'the decline in newspaper readership',
                         'D': 'the decreasing on newspaper readers'},
             'correct': 'C',
             'explanation': 'O grupo nominal <strong>the decline in newspaper readership</strong> comprime a oração '
                            'inteira com a preposição correta (<em>decline in</em>). A opção (D) usa <em>decreasing '
                            'on</em>, que falha na colocação de preposição, enquanto (A) inverte o sentido de '
                            '<em>fewer</em>.',
             'fonte': 'Parte 7, Exercício 2, item 1 (linhas 667 e 680)'},
            {'num': '3.2',
             'prompt': 'Frase-base: "The climate is changing quickly."',
             'options': {'A': 'the pace of climate change',
                         'B': 'the quickness in climate changing',
                         'C': 'the fastly changing of climate',
                         'D': 'the pace on climatic changes'},
             'correct': 'A',
             'explanation': 'Em (A), o advérbio <em>quickly</em> vira o substantivo de medida em <strong>the pace of '
                            'climate change</strong>. A opção (B) soa artificial com <em>quickness in climate '
                            'changing</em>, e (C) inventa a forma <em>fastly</em>.',
             'fonte': 'Parte 7, Exercício 2, item 2 (linhas 668 e 681)'},
            {'num': '3.3',
             'prompt': 'Frase-base: "Cities are growing faster than infrastructure can keep up."',
             'options': {'A': 'the equality between urban growth and infrastructure',
                         'B': 'the mismatch between urban growth and infrastructure',
                         'C': 'the mismatch among cities growing and infrastructure',
                         'D': 'the fastness of urban growth over the infrastructure'},
             'correct': 'B',
             'explanation': 'A opção (B) sintetiza a diferença de ritmo no substantivo <strong>mismatch</strong> '
                            'seguido de <em>between X and Y</em>. A alternativa (C) usa <em>among</em> para apenas '
                            'dois termos e mantém o verbo <em>cities growing</em> sem nominalizar de forma limpa.',
             'fonte': 'Parte 7, Exercício 2, item 3 (linhas 669 e 682)'},
            {'num': '3.4',
             'prompt': 'Frase-base: "People trust institutions less than they used to."',
             'options': {'A': 'the surge of trust in institutions',
                         'B': 'the erosion on institutional trusting',
                         'C': 'the trusting less of institutions now',
                         'D': 'the erosion of trust in institutions'},
             'correct': 'D',
             'explanation': 'A expressão <strong>the erosion of trust in institutions</strong> é uma das '
                            'nominalizações mais valorizadas no Writing acadêmico. A opção (B) erra a regência com '
                            '<em>erosion on</em> e <em>trusting</em>, e (A) troca a queda por aumento '
                            '(<em>surge</em>).',
             'fonte': 'Parte 7, Exercício 2, item 4 (linhas 670 e 683)'},
            {'num': '3.5',
             'prompt': 'Frase-base: "Companies depend more on remote teams now."',
             'options': {'A': "companies' growing reliance in remote teams",
                         'B': "companies' growing reliance on remote teams",
                         'C': "companies' declining reliance on remote teams",
                         'D': 'the growing dependance of companies to teams'},
             'correct': 'B',
             'explanation': 'O verbo <em>depend on</em> vira o substantivo <strong>reliance on</strong>, mantendo a '
                            'mesma preposição exigida pelo verbo. A opção (A) é uma armadilha clássica de preposição '
                            '(<em>reliance in</em>), e (D) erra tanto a grafia (<em>dependance</em>) quanto a '
                            'preposição (<em>to</em>).',
             'fonte': 'Parte 7, Exercício 2, item 5 (linhas 671 e 684)'}]},
 {'id': 'mod5-x-4',
  'title': 'Exercício 4: Nominalização de estados e eventos (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Escolha a nominalização que substitui a estrutura verbal ou adjetiva mantendo a precisão e as '
               'colocações naturais do inglês acadêmico. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '4.1',
             'prompt': 'Frase-base: "The population is aging across most of Europe."',
             'options': {'A': 'the aging of the population across much of Europe',
                         'B': 'the youth of the population across much of Europe',
                         'C': 'the aging in the population between most of Europe',
                         'D': 'the oldness of population across most in Europe'},
             'correct': 'A',
             'explanation': 'A construção <strong>the aging of the population</strong> empacota o processo contínuo em '
                            'um sujeito abstrato pronto para abrir a frase. A opção (C) usa <em>between</em> com um '
                            'único termo coletivo (<em>Europe</em>), o que não funciona.',
             'fonte': 'Parte 7, Exercício 2, item 6 (linhas 672 e 685)'},
            {'num': '4.2',
             'prompt': 'Frase-base: "The two departments failed to communicate."',
             'options': {'A': 'the communication success between the two departments',
                         'B': 'the communication failure among the two departments',
                         'C': 'the communication failure between the two departments',
                         'D': 'the failing for communicate of the two departments'},
             'correct': 'C',
             'explanation': 'O verbo <em>failed</em> se transforma no substantivo <strong>communication failure '
                            'between</strong> os dois setores. Repare que a opção (B) troca <em>between</em> por '
                            '<em>among</em> mesmo falando de exatamente dois departamentos.',
             'fonte': 'Parte 7, Exercício 2, item 7 (linhas 673 e 686)'},
            {'num': '4.3',
             'prompt': 'Frase-base: "Students are aware of the risks now more than before."',
             'options': {'A': 'a marked decline in student awareness of the risks',
                         'B': 'a marked increase of student aware about the risks',
                         'C': 'a marked increase on students awareness to the risks',
                         'D': 'a marked increase in student awareness of the risks'},
             'correct': 'D',
             'explanation': 'O adjetivo <em>aware</em> recebe o sufixo <em>-ness</em> e entra na colocação '
                            '<strong>increase in student awareness of</strong>. A alternativa (B) deixa o adjetivo '
                            '<em>aware</em> sem transformar em substantivo, e (C) erra as preposições (<em>on</em> e '
                            '<em>to</em>).',
             'fonte': 'Parte 7, Exercício 2, item 8 (linhas 674 e 687)'},
            {'num': '4.4',
             'prompt': 'Frase-base: "The market collapsed in a matter of weeks."',
             'options': {'A': 'the collapse of the market within weeks',
                         'B': 'the recovery of the market within weeks',
                         'C': 'the collapsing on the market during weeks',
                         'D': 'the collapse in the market since weeks'},
             'correct': 'A',
             'explanation': 'Em (A), você comprime a frase em <strong>the collapse of the market within '
                            'weeks</strong>, ótimo para funcionar como sujeito ou objeto. A opção (C) erra a '
                            'preposição com <em>on the market</em> e usa <em>during weeks</em> em vez de <em>within '
                            'weeks</em>.',
             'fonte': 'Parte 7, Exercício 2, item 9 (linhas 675 e 688)'},
            {'num': '4.5',
             'prompt': 'Frase-base: "The rules were applied inconsistently."',
             'options': {'A': 'the consistent application of the rules',
                         'B': 'the inconsistent appliance of the rules',
                         'C': 'the inconsistently applying on the rules',
                         'D': 'the inconsistent application of the rules'},
             'correct': 'D',
             'explanation': 'Na nominalização, o verbo <em>applied</em> vira <em>application</em> e o advérbio '
                            '<em>inconsistently</em> vira o adjetivo em <strong>the inconsistent application of the '
                            'rules</strong>. A opção (B) é um ponto de atenção lexical porque <em>appliance</em> '
                            'significa aparelho doméstico, e não aplicação de uma regra.',
             'fonte': 'Parte 7, Exercício 2, item 10 (linhas 676 e 689)'}]},
 {'id': 'mod5-x-5',
  'title': 'Exercício 5: Conectivos de nível C1 (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Leia o parágrafo de base e escolha a opção que substitui cada conectivo simples por um marcador de '
               'nível C1 da Parte 2, mantendo o sentido original. Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>PARÁGRAFO ORIGINAL (B1–B2):</strong></p><blockquote><p>Online courses are cheaper than '
                  'traditional ones. <strong>(1) Also</strong>, they are more flexible. <strong>(2) However</strong>, '
                  'they have higher dropout rates. <strong>(3) So</strong>, universities should not rely on them '
                  'completely. <strong>(4) Because of this</strong>, a mixed model works better.</p></blockquote>',
  'items': [{'num': '5.1',
             'prompt': 'Trecho (1): Como substituir "Also, they are more flexible." em nível C1?',
             'options': {'A': 'Notwithstanding this, they are more flexible.',
                         'B': 'Compounding this problem, they are more flexible.',
                         'C': 'Consequently, they are much more flexible.',
                         'D': 'Beyond this, they are more flexible.'},
             'correct': 'D',
             'explanation': 'O marcador <strong>Beyond this</strong> adiciona uma nova vantagem em registro C1. A '
                            'melhor armadilha é a (B): como vimos no Atlas Linguístico, <em>Compounding this '
                            'problem</em> só pode ser usado para somar um problema a outro, e não uma qualidade '
                            'positiva como flexibilidade.',
             'fonte': 'Parte 7, Exercício 3 (linhas 695 e 698)'},
            {'num': '5.2',
             'prompt': 'Trecho (2): Como substituir "However, they have higher dropout rates." em nível C1?',
             'options': {'A': 'This is not to say that they are flawless: they have higher dropout rates.',
                         'B': 'What is more, they are flawless, since they have higher dropout rates.',
                         'C': 'This gives rise to the fact that they are flawless: dropout rates are low.',
                         'D': 'Notwithstanding that they have higher dropout rates, they are flawless.'},
             'correct': 'A',
             'explanation': 'A estrutura <strong>This is not to say that</strong> introduz a ressalva com sofisticação '
                            'antes de apontar a taxa de evasão. A opção (B) usa <em>What is more</em>, que é conectivo '
                            'de adição, onde o parágrafo pede contraste.',
             'fonte': 'Parte 7, Exercício 3 (linhas 695 e 698)'},
            {'num': '5.3',
             'prompt': 'Trecho (3): Como substituir "So, universities should not rely on them completely." em nível '
                       'C1?',
             'options': {'A': 'In contrast, universities should not rely on them completely.',
                         'B': 'What this implies is that universities should not rely on them completely.',
                         'C': 'What this implies is universities should rely on them completely.',
                         'D': 'Whereas this implies that universities should not rely on them completely.'},
             'correct': 'B',
             'explanation': 'O molde <strong>What this implies is that</strong> substitui o <em>So</em> básico e '
                            'explicita o elo lógico entre a evasão e a recomendação. A opção (D) cria uma frase '
                            'incompleta com <em>Whereas</em>, e a (C) inverte a conclusão ao tirar o <em>not</em>.',
             'fonte': 'Parte 7, Exercício 3 (linhas 695 e 698)'},
            {'num': '5.4',
             'prompt': 'Trecho (4): Como substituir "Because of this, a mixed model works better." em nível C1?',
             'options': {'A': 'The consequence of this is that a mixed model works worse.',
                         'B': 'The consequence in this is what a mixed model works better.',
                         'C': 'The consequence of this is that a mixed model works better.',
                         'D': 'Admittedly, the consequence is that a mixed model works better.'},
             'correct': 'C',
             'explanation': 'A expressão <strong>The consequence of this is that</strong> fecha a cadeia de causa e '
                            'efeito sem repetir o marcador anterior. A alternativa (B) erra a preposição (<em>in</em> '
                            'em vez de <em>of</em>) e troca a conjunção integrante <em>that</em> por <em>what</em>.',
             'fonte': 'Parte 7, Exercício 3 (linhas 695 e 698)'}]},
 {'id': 'mod5-x-6',
  'title': 'Exercício 6: Precisão e cortesia no Write an Email (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Leia o e-mail com excesso de cerimônia (código RG1) e escolha a melhor reescrita para cada parte da '
               'mensagem em registro formal, direto e educado. Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>RASCUNHO COM EXCESSO DE CERIMÔNIA:</strong></p><blockquote><p>Dear Professor, I would '
                  'like to take this opportunity to very humbly and respectfully reach out to you in order to kindly '
                  'inquire whether it might perhaps somehow be possible, if it is not too much of an inconvenience for '
                  'you, to consider the possibility of granting me a small extension on the assignment, as I have '
                  'unfortunately been feeling somewhat unwell. Thank you so very much in advance for your kind '
                  'consideration. Most respectfully yours.</p></blockquote>',
  'items': [{'num': '6.1',
             'prompt': 'Parte 1 (Saudação e propósito): Qual abertura substitui o rodeio inicial com o registro ideal '
                       'para o Write an Email?',
             'options': {'A': "Hey Professor Lima, I'm writing because I really need more time on Friday's essay.",
                         'B': 'Dear Professor Lima, I am writing to ask whether I could have a short extension on the '
                              'essay due Friday.',
                         'C': 'Dear Professor Lima, I humbly beg your permission to postpone the essay due Friday.',
                         'D': 'Dear Professor Lima, I am writing to demand a short extension on the essay due Friday.'},
             'correct': 'B',
             'explanation': 'Em (B), você apresenta o objetivo logo na primeira frase usando <strong>I am writing to '
                            'ask whether I could</strong>, sem contrações e sem rodeios. A opção (A) cai no registro '
                            "informal com <em>Hey</em> e <em>I'm</em>, enquanto a (C) mantém a cerimônia exagerada com "
                            '<em>humbly beg</em>.',
             'fonte': 'Parte 7, Exercício 4 (linhas 704 e 707)'},
            {'num': '6.2',
             'prompt': 'Parte 2 (Justificativa): Como explicar o motivo do pedido de forma profissional e objetiva?',
             'options': {'A': "I was unwell for much of this week and can provide a doctor's note if needed.",
                         'B': "I've been feeling super sick all week and it's not fair to grade me right now.",
                         'C': 'I was unfortunately afflicted by a malady and might perhaps bring a medical paper.',
                         'D': "I was unwell for much of this week, so you must accept my doctor's note now."},
             'correct': 'A',
             'explanation': 'A frase (A) informa o problema com sobriedade (<em>unwell</em>) e já oferece a '
                            "comprovação concreta em <strong>can provide a doctor's note if needed</strong>. A opção "
                            '(C) exagera no floreio com <em>afflicted by a malady</em>, e a (B) usa gíria e desabafo '
                            'emocional.',
             'fonte': 'Parte 7, Exercício 4 (linhas 704 e 707)'},
            {'num': '6.3',
             'prompt': 'Parte 3 (Pedido específico): Como propor a nova data de entrega em uma frase curta e cortês?',
             'options': {'A': 'Can it maybe be on Monday?',
                         'B': 'Will you give me Monday?',
                         'C': 'Must I hand it in Monday?',
                         'D': 'Would Monday be acceptable?'},
             'correct': 'D',
             'explanation': 'A pergunta <strong>Would Monday be acceptable?</strong> usa um único modal de cortesia em '
                            'uma frase limpa e fácil de localizar. A alternativa (A) mistura modal informal com '
                            'hesitação (<em>Can it maybe</em>), e a (B) soa direta demais para um pedido acadêmico.',
             'fonte': 'Parte 7, Exercício 4 (linhas 704 e 707)'},
            {'num': '6.4',
             'prompt': 'Parte 4 (Fechamento): Qual encerramento substitui "Thank you so very much in advance... Most '
                       'respectfully yours" na medida certa?',
             'options': {'A': 'Thanks a lot for everything. See you soon, [Name]',
                         'B': 'I remain forever grateful to your esteemed person. Yours, [Name]',
                         'C': 'Thank you for considering it. Best regards, [Name]',
                         'D': 'Thank you for granting my extension right now. Sincerely, [Name]'},
             'correct': 'C',
             'explanation': 'O fechamento <strong>Thank you for considering it. Best regards</strong> agradece sem '
                            'exagero e respeita a decisão do professor. A opção (D) dá o pedido como já aprovado antes '
                            'da resposta, o que soa impositivo.',
             'fonte': 'Parte 7, Exercício 4 (linhas 704 e 707)'}]},
 {'id': 'mod5-x-7',
  'title': 'Exercício 7: Combinação de orações e densidade (meta de 6 min)',
  'level': 'B1–B2',
  'objective': 'Escolha a opção que reúne cada grupo de frases curtas em uma única frase densa e fluida, usando '
               'subordinação, particípio ou aposto (seção 4.3). Tempo-alvo: 6 minutos.',
  'passage_html': None,
  'items': [{'num': '7.1',
             'prompt': 'Frases originais: "The library extended its hours. Students asked for this. It happened last '
                       'semester."',
             'options': {'A': 'Last semester, in response to student requests, the library extended its hours.',
                         'B': 'Asking for this last semester, the library extended its hours for the students.',
                         'C': 'Last semester, despite student requests, the library extended its hours.',
                         'D': 'The library extended its hours last semester, because it asked for the students.'},
             'correct': 'A',
             'explanation': 'Em (A), você comprime a segunda frase na locução prepositiva <strong>in response to '
                            'student requests</strong> e abre com o marco temporal. A opção (B) cai na armadilha do '
                            'particípio solto (<em>dangling participle</em>), fazendo parecer que a própria biblioteca '
                            'pediu a mudança.',
             'fonte': 'Parte 7, Exercício 5, item 1 (linhas 713 e 724)'},
            {'num': '7.2',
             'prompt': 'Frases originais: "Granovetter published a paper in 1973. It was about weak ties. It became '
                       'very influential."',
             'options': {'A': 'Granovetter, who was a 1973 paper on weak ties, proved highly influential.',
                         'B': "Granovetter's 1973 paper on weak ties proved highly influential.",
                         'C': "Publishing in 1973, weak ties made Granovetter's paper highly influential.",
                         'D': "Granovetter's 1973 paper on weak ties, which it proved highly influential."},
             'correct': 'B',
             'explanation': 'A opção (B) reúne três frases em apenas nove palavras usando o grupo nominal compacto '
                            "<strong>Granovetter's 1973 paper on weak ties</strong> como sujeito. A alternativa (C) "
                            'cria um particípio solto (como se <em>weak ties</em> tivesse publicado o artigo), e a (D) '
                            'fica sem verbo principal.',
             'fonte': 'Parte 7, Exercício 5, item 2 (linhas 714 e 725)'},
            {'num': '7.3',
             'prompt': 'Frases originais: "The plan lowered costs. Because of this, it gained support. The support '
                       'came from the finance team."',
             'options': {'A': 'By lowering costs, the finance team was lowered by the support of the plan.',
                         'B': 'Despite lowering costs, the plan won the support of the finance team.',
                         'C': 'By lowering costs, the plan lost the support of the finance team.',
                         'D': 'By lowering costs, the plan won the support of the finance team.'},
             'correct': 'D',
             'explanation': 'A estrutura <strong>By lowering costs</strong> usa preposição e gerúndio para expressar o '
                            'meio pelo qual o plano conquistou o apoio, mantendo o mesmo sujeito (<em>the plan</em>) '
                            'nas duas partes. A opção (B) troca a relação de causa por concessão ao usar '
                            '<em>Despite</em>.',
             'fonte': 'Parte 7, Exercício 5, item 3 (linhas 715 e 726)'},
            {'num': '7.4',
             'prompt': 'Frases originais: "The city invested in bike lanes. Cycling doubled. Car traffic fell '
                       'slightly."',
             'options': {'A': 'Before the city invested in bike lanes, cycling doubled while car traffic fell '
                              'slightly.',
                         'B': 'After the city invested in bike lanes, cycling doubled because car traffic rose '
                              'slightly.',
                         'C': 'After the city invested in bike lanes, cycling doubled while car traffic fell slightly.',
                         'D': 'Investing in bike lanes, cycling doubled while car traffic fell slightly in the city.'},
             'correct': 'C',
             'explanation': 'Em (C), você articula três eventos com duas conjunções precisas: <em>After</em> para a '
                            'causa temporal e <strong>while</strong> para contrastar os dois resultados simultâneos. A '
                            'alternativa (D) deixa o particípio <em>Investing</em> solto, pois o sujeito seguinte é '
                            '<em>cycling</em> e não <em>the city</em>.',
             'fonte': 'Parte 7, Exercício 5, item 4 (linhas 716 e 727)'},
            {'num': '7.5',
             'prompt': 'Frases originais: "The study had a small sample. The results were still striking. They matched '
                       'earlier work."',
             'options': {'A': 'Despite a small sample, the study produced striking results that matched earlier work.',
                         'B': 'Because of a small sample, the study produced striking results that matched earlier '
                              'work.',
                         'C': 'Despite that the sample was small, the study produced striking results matching earlier '
                              'work.',
                         'D': 'Despite a small sample, the study produced striking results that contradicted earlier '
                              'work.'},
             'correct': 'A',
             'explanation': 'A opção (A) comprime a concessão em <strong>Despite a small sample</strong> e encaixa a '
                            'terceira frase em uma oração relativa (<em>that matched earlier work</em>). A alternativa '
                            '(C) comete o deslize de usar <em>Despite that</em> seguido de oração, em vez de grupo '
                            'nominal.',
             'fonte': 'Parte 7, Exercício 5, item 5 (linhas 717 e 728)'},
            {'num': '7.6',
             'prompt': 'Frases originais: "The app was free. It had ads. Many users left because of the ads."',
             'options': {'A': 'The app was free and ad-supported, so the ads kept many users staying.',
                         'B': 'The app was free but ad-supported, and the ads drove many users away.',
                         'C': 'Being ad-supported and free, many users were driven away by the app.',
                         'D': 'The app was free because ad-supported, though the ads drove users away.'},
             'correct': 'B',
             'explanation': 'Em (B), a segunda frase vira o adjetivo composto <strong>ad-supported</strong> e a '
                            'terceira usa o verbo expressivo <em>drove many users away</em>. A opção (C) cria um '
                            'particípio solto ao ligar <em>Being ad-supported and free</em> ao sujeito <em>many '
                            'users</em>.',
             'fonte': 'Parte 7, Exercício 5, item 6 (linhas 718 e 729)'},
            {'num': '7.7',
             'prompt': 'Frases originais: "The professor posts recordings. Students who miss class can catch up. '
                       'Attendance has not dropped."',
             'options': {'A': 'Because the professor posts recordings so that students who miss class can catch up, '
                              'attendance has dropped.',
                         'B': 'Although the professor posts recordings unless students who miss class can catch up, '
                              'attendance has not dropped.',
                         'C': 'Although the professor posts recordings so that students who miss class can catch up, '
                              'attendance has not dropped.',
                         'D': 'Posting recordings so that students who miss class can catch up, attendance has not '
                              'dropped in the course.'},
             'correct': 'C',
             'explanation': 'A alternativa (C) combina concessão (<strong>Although</strong>) e finalidade (<em>so '
                            'that</em>) na mesma frase, mantendo a leitura clara. A opção (D) cai novamente na '
                            'armadilha do particípio solto, já que <em>attendance</em> não é quem publica as '
                            'gravações.',
             'fonte': 'Parte 7, Exercício 5, item 7 (linhas 719 e 730)'},
            {'num': '7.8',
             'prompt': 'Frases originais: "The report was written by an external panel. It criticized the process. '
                       'Management accepted most of it."',
             'options': {'A': "The external panel's report, supportive of the process, was largely rejected by "
                              'management.',
                         'B': "Written by management, the external panel's report was critical of the process and "
                              'accepted.',
                         'C': "The external panel's report, critical of the process, was largely rejected by "
                              'management.',
                         'D': "The external panel's report, critical of the process, was largely accepted by "
                              'management.'},
             'correct': 'D',
             'explanation': "A opção (D) transforma a primeira frase em posse (<em>The external panel's report</em>) e "
                            'reduz a segunda ao aposto adjetivo <strong>critical of the process</strong>. As '
                            'alternativas (A), (B) e (C) alteram quem escreveu o relatório ou invertem a aceitação '
                            'pela chefia.',
             'fonte': 'Parte 7, Exercício 5, item 8 (linhas 720 e 731)'}]},
 {'id': 'mod5-x-8',
  'title': 'Exercício 8: Frases clivadas para dar foco (meta de 5 min)',
  'level': 'C1–C2',
  'objective': 'Escolha a frase clivada (it-cleft ou wh-cleft, seção 4.4) que destaca corretamente o elemento indicado '
               'no enunciado. Tempo-alvo: 5 minutos.',
  'passage_html': None,
  'items': [{'num': '8.1',
             'prompt': 'Destaque "Feedback" na frase: "Feedback, not testing, drives improvement."',
             'options': {'A': 'It is feedback, not testing, that drives improvement.',
                         'B': 'It is feedback, not testing, what drives improvement.',
                         'C': 'What drives improvement is testing, not feedback at all.',
                         'D': 'It is feedback, not testing, that drive improvement now.'},
             'correct': 'A',
             'explanation': 'O molde <strong>It is X, not Y, that</strong> coloca a causa sob o holofote logo na '
                            'abertura. A opção (B) troca <em>that</em> por <em>what</em> em uma <em>it-cleft</em>, e a '
                            '(D) erra a concordância com o singular <em>feedback</em> ao usar <em>drive</em>.',
             'fonte': 'Parte 7, Exercício 6, item 1 (linhas 737 e 746)'},
            {'num': '8.2',
             'prompt': 'Destaque "the cost of maintenance" na frase: "The policy ignores the cost of maintenance."',
             'options': {'A': 'What the policy ignores are the cost of maintenance.',
                         'B': 'What the policy ignores is the cost of maintenance.',
                         'C': 'It is the policy that ignores the cost of maintenance.',
                         'D': 'What ignores the cost of maintenance is the policy.'},
             'correct': 'B',
             'explanation': 'A estrutura <strong>What the policy ignores is</strong> (<em>wh-cleft</em>) cria '
                            'expectativa na primeira metade e entrega o foco no final. As opções (C) e (D) destacam '
                            '<em>the policy</em> em vez de <em>the cost of maintenance</em>, e a (A) erra a '
                            'concordância com <em>are</em>.',
             'fonte': 'Parte 7, Exercício 6, item 2 (linhas 738 e 747)'},
            {'num': '8.3',
             'prompt': 'Destaque "The follow-up call" na frase: "The follow-up call closes most sales."',
             'options': {'A': 'It is most sales that the follow-up call closes.',
                         'B': 'It is the follow-up call who closes most sales.',
                         'C': 'It is the follow-up call that closes most sales.',
                         'D': 'What the follow-up call closes is that most sales.'},
             'correct': 'C',
             'explanation': 'Em (C), a <strong>it-cleft</strong> destaca o sujeito <em>the follow-up call</em> usando '
                            'o conector <em>that</em>. A alternativa (B) usa <em>who</em> para uma coisa inanimada '
                            '(<em>call</em>), e a (A) desloca o foco para <em>most sales</em>.',
             'fonte': 'Parte 7, Exercício 6, item 3 (linhas 739 e 748)'},
            {'num': '8.4',
             'prompt': 'Destaque "the long-term effect" na frase: "This argument misses the long-term effect."',
             'options': {'A': 'It is this argument that misses the long-term effect.',
                         'B': 'What this argument misses that is the long-term effect.',
                         'C': 'What misses the long-term effect is this argument here.',
                         'D': 'What this argument misses is the long-term effect.'},
             'correct': 'D',
             'explanation': 'A <em>wh-cleft</em> em <strong>What this argument misses is</strong> direciona a atenção '
                            'exatamente para o objeto que faltou no argumento. A opção (A) destaca <em>this '
                            'argument</em> em vez do efeito de longo prazo, e a (B) sobra um <em>that</em> antes de '
                            '<em>is</em>.',
             'fonte': 'Parte 7, Exercício 6, item 4 (linhas 740 e 749)'},
            {'num': '8.5',
             'prompt': 'Destaque "The sustained investment" na frase: "The sustained investment turned the '
                       'neighborhood around."',
             'options': {'A': 'It was the sustained investment that turned the neighborhood around.',
                         'B': 'It is the sustained investment what turned the neighborhood around.',
                         'C': 'It was the neighborhood that the sustained investment turned around.',
                         'D': 'What the sustained investment turned around was the neighborhood.'},
             'correct': 'A',
             'explanation': 'Como o verbo original (<em>turned</em>) está no passado, a clivada mantém o tempo verbal '
                            'em <strong>It was the sustained investment that</strong>. As opções (C) e (D) colocam o '
                            'foco no bairro (<em>the neighborhood</em>), e não no investimento.',
             'fonte': 'Parte 7, Exercício 6, item 5 (linhas 741 e 750)'},
            {'num': '8.6',
             'prompt': 'Destaque "when the funding was cut" usando uma frase clivada em: "We only saw the problem when '
                       'the funding was cut."',
             'options': {'A': 'It was only when the funding was cut what we saw the problem.',
                         'B': 'It was only when the funding was cut that we saw the problem.',
                         'C': 'It was the problem that we only saw when the funding was cut.',
                         'D': 'Only when the funding was cut we saw the problem clearly.'},
             'correct': 'B',
             'explanation': 'A estrutura <strong>It was only when... that</strong> destaca o marco temporal com uma '
                            'clivada completa. Vale notar que a inversão <em>Only when the funding was cut did we see '
                            'the problem</em> também seria boa gramática (embora não seja clivada), mas a (D) esquece '
                            'de inverter o auxiliar <em>did</em>.',
             'fonte': 'Parte 7, Exercício 6, item 6 (linhas 742 e 751)'}]},
 {'id': 'mod5-x-9',
  'title': 'Exercício 9: Escala de formalidade no Writing acadêmico (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Leia o parágrafo informal e escolha a opção que eleva cada trecho para o registro acadêmico (seção '
               '4.6), incluindo 1 ou 2 verbos mais formais por frase sem exagerar. Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>PARÁGRAFO INFORMAL:</strong></p><blockquote><p><strong>(1)</strong> The new rule made '
                  'things a lot worse for small shops. <strong>(2)</strong> It put off a lot of customers because '
                  "prices went up. <strong>(3)</strong> The city didn't look at the data before it brought in the "
                  'change, <strong>(4)</strong> and now it has to deal with the fallout.</p></blockquote>',
  'items': [{'num': '9.1',
             'prompt': 'Trecho (1): Como elevar "The new rule made things a lot worse for small shops" com '
                       'naturalidade?',
             'options': {'A': 'The new regulation markedly improved conditions for small shops.',
                         'B': 'The novel statutory mandate catastrophically deteriorated retail establishments.',
                         'C': 'The new rule made things a bit worse for small shops.',
                         'D': 'The new regulation markedly worsened conditions for small shops.'},
             'correct': 'D',
             'explanation': 'Em (D), você troca <em>rule</em> por <em>regulation</em>, <em>a lot</em> por '
                            '<em>markedly</em> e <em>made things worse</em> por <strong>worsened conditions</strong>. '
                            'A opção (B) cai na armadilha de trocar todas as palavras simples por termos pomposos, o '
                            'que deixa o texto artificial.',
             'fonte': 'Parte 7, Exercício 7 (linhas 757 e 760)'},
            {'num': '9.2',
             'prompt': 'Trecho (2): Como elevar "It put off a lot of customers because prices went up"?',
             'options': {'A': 'It postponed many customers as prices declined,',
                         'B': 'It deterred many customers as prices rose,',
                         'C': 'It put off plenty of buyers since prices went up,',
                         'D': 'It deterred many customers although prices fell,'},
             'correct': 'B',
             'explanation': 'No contexto de afastar clientes, <em>put off</em> equivale a <strong>deterred</strong>, e '
                            '<em>went up</em> vira <em>rose</em>. A alternativa (A) é uma ótima armadilha: '
                            '<em>postpone</em> traduz <em>put off</em> apenas no sentido de adiar uma reunião, e não '
                            'de desencorajar pessoas.',
             'fonte': 'Parte 7, Exercício 7 (linhas 757 e 760)'},
            {'num': '9.3',
             'prompt': 'Trecho (3): Como elevar "The city didn\'t look at the data before it brought in the change"?',
             'options': {'A': 'and because the city did not watch the data before bringing the change,',
                         'B': 'and although the city examined the data before introducing the change,',
                         'C': 'and because the city did not examine the data before introducing the change,',
                         'D': "and because the city didn't look into the data after introducing the change,"},
             'correct': 'C',
             'explanation': "A opção (C) desfaz a contração <em>didn't</em> e substitui os verbos frasais por "
                            '<strong>examine</strong> e <em>introducing</em>. A alternativa (A) usa <em>watch the '
                            'data</em>, que não forma colocação em inglês.',
             'fonte': 'Parte 7, Exercício 7 (linhas 757 e 760)'},
            {'num': '9.4',
             'prompt': 'Trecho (4): Como elevar "and now it has to deal with the fallout"?',
             'options': {'A': 'it must now ignore the consequences.',
                         'B': 'it can now deal with the big fallout.',
                         'C': 'it might perhaps tackle the things.',
                         'D': 'it must now address the consequences.'},
             'correct': 'D',
             'explanation': 'Na tabela da seção 4.6, <em>deal with</em> passa a <strong>address</strong> e '
                            '<em>fallout</em> ganha precisão com <em>the consequences</em>. A opção (C) mistura '
                            'hesitação excessiva (<em>might perhaps</em>) com o substantivo vago <em>things</em>.',
             'fonte': 'Parte 7, Exercício 7 (linhas 757 e 760)'}]},
 {'id': 'mod5-x-10',
  'title': 'Exercício 10: Calibragem de hedging (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Suavize afirmações absolutas demais (Parte A) e dê firmeza ao que está evasivo demais (Parte B), '
               'aplicando o hedging calibrado da seção 4.2. Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>PARTE A (absoluto demais):</strong> "Video games cause violence. Every child who plays '
                  'them becomes aggressive. Technology destroys family communication completely."</p><p><strong>PARTE '
                  'B (evasivo demais):</strong> "Maybe reading could possibly perhaps sometimes in some cases help a '
                  'little bit with vocabulary, but I\'m not really sure and it might not be true for everyone."</p>',
  'items': [{'num': '10.1',
             'prompt': 'Parte A (1): Como reescrever "Video games cause violence. Every child who plays them becomes '
                       'aggressive" com hedging de nível C1?',
             'options': {'A': 'Video games definitely cause violence in most children, and players always become '
                              'aggressive in the short term.',
                         'B': 'Maybe video games might possibly perhaps cause a bit of violence in some children who '
                              'play them sometimes.',
                         'C': 'Some research suggests a link between heavy gaming and short-term aggression, though '
                              'the effect appears small and does not hold for all players.',
                         'D': 'Research proves that heavy gaming never causes any aggression, so the effect does not '
                              'hold for any players at all.'},
             'correct': 'C',
             'explanation': 'Em (C), você substitui a afirmação absoluta por cautela calibrada com <strong>suggests a '
                            'link</strong>, <em>appears small</em> e delimitação de escopo (<em>heavy gaming</em>, '
                            '<em>not for all players</em>). A opção (B) sai do extremo absoluto direto para o extremo '
                            'inseguro, empilhando quatro marcadores de dúvida seguidos.',
             'fonte': 'Parte 7, Exercício 8, Parte A (linhas 765 e 772)'},
            {'num': '10.2',
             'prompt': 'Parte A (2): Como suavizar "Technology destroys family communication completely" mantendo um '
                       'argumento forte e defensável?',
             'options': {'A': 'Heavy device use may also weaken face-to-face communication within families, at least '
                              'for some age groups.',
                         'B': 'Heavy device use will undoubtedly destroy all face-to-face communication within '
                              'families of every age group.',
                         'C': 'Perhaps technology could maybe possibly affect family communication a little bit in '
                              'some situations.',
                         'D': 'Heavy device use always strengthens face-to-face communication within families across '
                              'all age groups.'},
             'correct': 'A',
             'explanation': 'A opção (A) especifica o sujeito (<em>Heavy device use</em>), usa o modal <strong>may '
                            'also weaken</strong> no lugar de <em>destroys</em> e limita o alcance com <em>at least '
                            'for some age groups</em>. A alternativa (B) mantém o tom 100% absoluto com '
                            '<em>undoubtedly destroy all</em>.',
             'fonte': 'Parte 7, Exercício 8, Parte A (linhas 765 e 772)'},
            {'num': '10.3',
             'prompt': 'Parte B (1): Como dar firmeza à primeira metade de "Maybe reading could possibly perhaps '
                       'sometimes in some cases help a little bit with vocabulary..."?',
             'options': {'A': 'Reading is the only way that ever builds vocabulary for every person,',
                         'B': 'Regular reading is one of the most reliable ways to build vocabulary,',
                         'C': 'Maybe regular reading might perhaps help a bit with vocabulary,',
                         'D': 'Regular reading rarely helps anyone build vocabulary in practice,'},
             'correct': 'B',
             'explanation': 'A construção <strong>one of the most reliable ways</strong> transmite segurança acadêmica '
                            'sem cair no exagero absoluto de dizer <em>the only way</em> como na opção (A). Já a (C) '
                            'mantém o excesso de hesitação do rascunho original.',
             'fonte': 'Parte 7, Exercício 8, Parte B (linhas 768 e 773)'},
            {'num': '10.4',
             'prompt': 'Parte B (2): Como substituir "...but I\'m not really sure and it might not be true for '
                       'everyone" por uma condição específica de nível C1?',
             'options': {'A': 'and I am completely sure that this works the exact same way for every single reader who '
                              'tries it.',
                         'B': 'but I really do not know if this is true for all students who study new words at home '
                              'or not.',
                         'C': 'because readers who memorize isolated lists without any context always learn much more '
                              'quickly.',
                         'D': 'though the gain is larger for readers who encounter unfamiliar words in context rather '
                              'than in lists.'},
             'correct': 'D',
             'explanation': "Em vez de confessar insegurança pessoal (<em>I'm not really sure</em>), a opção (D) "
                            'explica em qual condição o efeito varia usando <strong>though the gain is larger '
                            'for</strong>. A alternativa (B) apenas repete a dúvida subjetiva sem acrescentar critério '
                            'analítico.',
             'fonte': 'Parte 7, Exercício 8, Parte B (linhas 768 e 773)'}]},
 {'id': 'mod5-x-11',
  'title': 'Exercício 11: Substituição de vocabulário repetido (meta de 5 min)',
  'level': 'B1–B2',
  'objective': 'Para cada palavra repetida com frequência nos treinos de Writing, escolha a alternativa que traz '
               'apenas substitutos de registro acadêmico adequados ao contexto. Tempo-alvo: 5 minutos.',
  'passage_html': None,
  'items': [{'num': '11.1',
             'prompt': 'Para evitar repetir o adjetivo "important" ao longo do parágrafo, qual grupo reúne os '
                       'substitutos acadêmicos recomendados?',
             'options': {'A': 'crucial, central, decisive, key, significant',
                         'B': 'huge, nice, cool, minor, optional',
                         'C': 'crucial, trivial, negligible, slight, faint',
                         'D': 'big, funny, casual, secondary, marginal'},
             'correct': 'A',
             'explanation': 'O grupo <strong>crucial, central, decisive, key, significant</strong> permite variar a '
                            'palavra-chave mantendo a precisão do registro acadêmico. A opção (C) mistura '
                            '<em>crucial</em> com antônimos que significam irrelevante (<em>trivial, negligible</em>).',
             'fonte': 'Parte 7, Exercício 9 (linha 779)'},
            {'num': '11.2',
             'prompt': 'Em vez de repetir o adjetivo genérico "good", qual conjunto oferece boas opções de '
                       'substituição para o Writing?',
             'options': {'A': 'awesome, great, lovely, pleasant',
                         'B': 'beneficial, sound, effective, valuable',
                         'C': 'beneficial, harmful, flawed, doubtful',
                         'D': 'enjoyable, funny, casual, friendly'},
             'correct': 'B',
             'explanation': 'As palavras <strong>beneficial, sound, effective, valuable</strong> especificam por que '
                            'algo é positivo (traz benefício, é sólido, funciona ou tem valor). As opções (A) e (D) '
                            'trazem adjetivos coloquiais ou emocionais, e a (C) inclui termos negativos.',
             'fonte': 'Parte 7, Exercício 9 (linha 780)'},
            {'num': '11.3',
             'prompt': 'Para substituir "bad" com precisão analítica em um texto argumentativo, qual grupo você deve '
                       'escolher?',
             'options': {'A': 'unpleasant, terrible, horrible, disappointing',
                         'B': 'harmful, beneficial, constructive, favorable',
                         'C': 'harmful, damaging, counterproductive, detrimental',
                         'D': 'unfair, frustrating, annoying, inconvenient'},
             'correct': 'C',
             'explanation': 'Os adjetivos <strong>harmful, damaging, counterproductive, detrimental</strong> apontam o '
                            'prejuízo ou efeito contrário de uma medida em tom analítico. A alternativa (A) usa '
                            'palavras de reação emocional, e a (B) mistura adjetivos positivos.',
             'fonte': 'Parte 7, Exercício 9 (linha 781)'},
            {'num': '11.4',
             'prompt': 'Quando a palavra "problem" já apareceu no parágrafo, qual lista traz equivalentes adequados '
                       'para retomar a ideia sem repetição?',
             'options': {'A': 'benefit, advantage, asset, gain, strength',
                         'B': 'mess, trouble, headache, pain, drama',
                         'C': 'issue, solution, remedy, answer, fix',
                         'D': 'issue, challenge, drawback, obstacle, shortcoming'},
             'correct': 'D',
             'explanation': 'O repertório <strong>issue, challenge, drawback, obstacle, shortcoming</strong> permite '
                            'variar entre questão geral, desafio, desvantagem, obstáculo e limitação. A opção (B) é '
                            'informal demais, e a (C) mistura problema com solução.',
             'fonte': 'Parte 7, Exercício 9 (linha 782)'},
            {'num': '11.5',
             'prompt': 'Em vez de repetir o verbo "help" várias vezes, quais verbos de registro B2 e C1 cumprem essa '
                       'função com naturalidade?',
             'options': {'A': 'support, aid, facilitate, contribute to',
                         'B': 'hinder, block, prevent, undermine',
                         'C': 'help out, give a hand, fix up, back up',
                         'D': 'support, prevent, worsen, obstruct'},
             'correct': 'A',
             'explanation': 'Os verbos <strong>support, aid, facilitate, contribute to</strong> elevam o registro '
                            'lexical no Writing sem perder a clareza. A opção (C) usa apenas verbos frasais informais, '
                            'e a (B) traz verbos com o sentido oposto (atrapalhar ou impedir).',
             'fonte': 'Parte 7, Exercício 9 (linha 783)'},
            {'num': '11.6',
             'prompt': 'Para variar o verbo de opinião "think" ao apresentar posições no Writing acadêmico, qual '
                       'conjunto é o mais adequado?',
             'options': {'A': 'guess, wonder, hope, wish, feel like',
                         'B': 'believe, hold, contend, maintain, argue',
                         'C': 'believe, deny, refute, reject, dismiss',
                         'D': 'reckon, figure, bet, suppose, dream'},
             'correct': 'B',
             'explanation': 'Com <strong>believe, hold, contend, maintain, argue</strong>, você introduz teses '
                            'próprias ou de colegas com vocabulário acadêmico preciso. A alternativa (C) mistura '
                            'verbos de defender uma ideia com verbos de rejeitá-la (<em>deny, refute</em>), e (D) traz '
                            'termos coloquiais.',
             'fonte': 'Parte 7, Exercício 9 (linha 784)'},
            {'num': '11.7',
             'prompt': 'Como substituir a palavra genérica "people" nomeando grupos mais específicos ou formais na '
                       'resposta?',
             'options': {'A': 'guys, folks, kids, everybody',
                         'B': 'things, cases, factors, elements',
                         'C': 'individuals, students, users, the public',
                         'D': 'somebody, anybody, nobody, everyone'},
             'correct': 'C',
             'explanation': 'Nomear o grupo exato com <strong>individuals, students, users, the public</strong> '
                            'aumenta tanto a variedade lexical quanto a concretude do argumento. A opção (A) é '
                            'coloquial, e a (D) troca um termo genérico por pronomes indefinidos ainda mais vagos.',
             'fonte': 'Parte 7, Exercício 9 (linha 785)'}]},
 {'id': 'mod5-x-12',
  'title': 'Exercício 12: Elevação na Academic Discussion (meta de 5 min)',
  'level': 'C1–C2',
  'objective': 'Acompanhe a construção de um parágrafo C1 para o Prompt A e escolha a frase que executa cada um dos 4 '
               'movimentos retóricos pedidos. Tempo-alvo: 5 minutos.',
  'passage_html': '<p><strong>PROMPT A:</strong> <em>"Is it better for a company to promote from within or to hire '
                  'experienced people from outside?"</em></p><p><strong>Daniel:</strong> "Promoting from within keeps '
                  'morale high and preserves company knowledge."<br><strong>Mei:</strong> "Outside hires bring fresh '
                  'ideas and challenge groupthink."</p>',
  'items': [{'num': '12.1',
             'prompt': 'Movimento 1 (Abertura com concessão integrada, Marcador 5): Qual frase abre o parágrafo '
                       'reconhecendo o ponto de Daniel antes de apresentar a tese?',
             'options': {'A': 'I agree with Mei because outside hires are always much better than promoting people '
                              'from within.',
                         'B': 'Notwithstanding that Daniel is right about morale, promoting from within is completely '
                              'wrong for any company today.',
                         'C': 'Daniel says that promoting from within keeps morale high, and Mei says outside hires '
                              'bring ideas.',
                         'D': 'While Daniel is right that internal promotion protects institutional memory, the '
                              'stronger position is a deliberate mix.'},
             'correct': 'D',
             'explanation': 'Em (D), você abre com a concessão <strong>While Daniel is right that</strong>, substitui '
                            '<em>company knowledge</em> pela colocação C1 <em>institutional memory</em> e já firma uma '
                            'tese equilibrada. A opção (C) apenas resume os colegas sem assumir posição, e a (B) '
                            'reconhece Daniel, mas fecha num absoluto (<em>completely wrong</em>) que desfaz a '
                            'concessão.',
             'fonte': 'Parte 7, Exercício 11, Prompt A (linhas 795, 797 e 802)'},
            {'num': '12.2',
             'prompt': 'Movimento 2 (Razão com mecanismo, Marcador 1): Qual frase explica por que contratar de fora '
                       'funciona, indo além do clichê "fresh ideas"?',
             'options': {'A': "What makes an outside hire valuable is not the 'fresh ideas' in the abstract but the "
                              'fact that they have not yet learned which questions the organization has stopped '
                              'asking.',
                         'B': 'What makes an outside hire valuable is that they are very valuable to the team and '
                              'bring a lot of fresh ideas that everyone in the organization already knows how to ask.',
                         'C': 'Outside hires are always good for a big company because they have many fresh ideas in '
                              'the abstract and they also come from other organizations that work in the same market.',
                         'D': "What makes an outside hire valuable is not the 'fresh ideas' in the abstract, because "
                              'they have already learned all the old questions that the organization keeps asking.'},
             'correct': 'A',
             'explanation': 'A opção (A) usa a <em>wh-cleft</em> <strong>What makes an outside hire valuable is not X '
                            'but Y</strong> para mostrar o mecanismo exato por trás das ideias novas. A alternativa '
                            '(B) cai no erro circular apontado na Parte 3 (<em>what makes X valuable is that they are '
                            'valuable</em>).',
             'fonte': 'Parte 7, Exercício 11, Prompt A (linhas 795 e 802)'},
            {'num': '12.3',
             'prompt': 'Movimento 3 (Contraste concreto): Qual frase desenvolve o mecanismo comparando o comportamento '
                       'da equipe interna com o de quem vem de fora?',
             'options': {'A': 'A team that promotes from within never works well on any daily process; someone who '
                              'comes from outside always fixes every single problem in the company right away.',
                         'B': 'A team that has only ever promoted from within tends to optimize the process it already '
                              'has; someone from outside is the one who asks why that process exists at all.',
                         'C': 'For example, my uncle worked at a large traditional company for ten years; he liked his '
                              'coworkers a lot, and they always used the same computer system every day.',
                         'D': 'A team that has only ever promoted from within asks why the process exists at all; '
                              'someone hired from outside just tries to optimize the routine it already has.'},
             'correct': 'B',
             'explanation': 'A frase (B) usa <em>hedging</em> calibrado (<strong>tends to optimize</strong>) e '
                            'paralelismo com ponto e vírgula para ilustrar a diferença prática entre otimizar uma '
                            'rotina e questionar sua existência. A opção (D) inverte os papéis, e a (C) traz um '
                            'exemplo vago que não prova a tese.',
             'fonte': 'Parte 7, Exercício 11, Prompt A (linhas 795 e 802)'},
            {'num': '12.4',
             'prompt': 'Movimento 4 (Diálogo final e condição): Qual fechamento responde à preocupação de Daniel sobre '
                       'moral da equipe e amarra a síntese?',
             'options': {'A': 'So I think both Daniel and Mei make very good points about the company, and managers '
                              'should just do whatever they want when they need to hire or promote people.',
                         'B': 'The morale cost is completely imaginary, so internal candidates should never be given a '
                              'path to promotion even when the current thinking in the team is working well.',
                         'C': 'The morale cost is real, but it is manageable if internal candidates are given a '
                              'genuine path and outside hires are reserved for roles where the current thinking has '
                              'visibly stalled.',
                         'D': 'Were the morale cost real for the company, internal candidates will be given a genuine '
                              'path and outside hires will be reserved for roles where the current thinking has '
                              'stalled.'},
             'correct': 'C',
             'explanation': 'O fechamento (C) reconhece o custo apontado por Daniel (<strong>The morale cost is real, '
                            'but it is manageable if</strong>) e estabelece a condição clara em que o modelo misto '
                            'funciona. A opção (D) mistura os tempos da condicional invertida ao usar <em>will</em> '
                            'depois de <em>Were</em>.',
             'fonte': 'Parte 7, Exercício 11, Prompt A (linhas 795 e 802)'}]},
 {'id': 'mod5-x-13',
  'title': 'Exercício 13: Coesão com substantivo sumarizador (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Substitua cada "this" ou "it" solto do parágrafo original por um substantivo sumarizador que retome a '
               'ideia anterior com precisão (seção 4.5). Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>PARÁGRAFO COM PRONOMES SOLTOS:</strong></p><blockquote><p><strong>(1)</strong> '
                  'Enrollment fell for three years. This forced the budget cuts. <strong>(2)</strong> It also meant '
                  'two programs closed. <strong>(3)</strong> This was hard for the students in them. '
                  '<strong>(4)</strong> It shows the college needs a new plan.</p></blockquote>',
  'items': [{'num': '13.1',
             'prompt': 'Trecho (1): Como reescrever "Enrollment fell for three years. This forced the budget cuts" com '
                       'substantivo sumarizador?',
             'options': {'A': 'Enrollment fell for three years running. This sustained decline forced the budget cuts',
                         'B': 'Enrollment fell for three years running. This sustained growth forced the budget cuts',
                         'C': 'Enrollment fell for three years running. This thing forced the budget cuts',
                         'D': 'Enrollment fell for three years running. These constraints forced the enrollment'},
             'correct': 'A',
             'explanation': 'Em vez de deixar o pronome <em>This</em> sozinho no início da frase, a opção (A) retoma a '
                            'queda nas matrículas com <strong>This sustained decline</strong>. A alternativa (B) usa '
                            '<em>growth</em> (crescimento), contradizendo <em>fell</em>, e a (C) usa a palavra vaga '
                            '<em>thing</em>.',
             'fonte': 'Parte 7, Exercício 12 (linhas 808 e 811)'},
            {'num': '13.2',
             'prompt': 'Trecho (2): Como integrar "It also meant two programs closed" à frase dos cortes '
                       'orçamentários, eliminando o "It" solto?',
             'options': {'A': 'and, with it, two programs also opened.',
                         'B': 'and, with them, the closure of two programs.',
                         'C': 'and this also meant that it closed two.',
                         'D': 'and, despite them, the opening of programs.'},
             'correct': 'B',
             'explanation': 'A continuação <strong>and, with them, the closure of two programs</strong> retoma '
                            '<em>budget cuts</em> no plural (<em>them</em>) e transforma <em>two programs closed</em> '
                            'na nominalização <em>the closure of two programs</em>. A opção (C) mantém os pronomes '
                            'vagos <em>this</em> e <em>it</em>.',
             'fonte': 'Parte 7, Exercício 12 (linhas 808 e 811)'},
            {'num': '13.3',
             'prompt': 'Trecho (3): Como reescrever "This was hard for the students in them" nomeando o impacto do '
                       'fechamento dos cursos?',
             'options': {'A': 'That benefit fell hardest on the students already enrolled in those programs.',
                         'B': 'This was very hard for the students who were inside of them.',
                         'C': 'That disruption fell hardest on the students already enrolled in those programs.',
                         'D': 'Those improvements were hard for the students enrolled in that.'},
             'correct': 'C',
             'explanation': 'O grupo nominal <strong>That disruption</strong> resume o fechamento dos cursos com '
                            'exatidão, e <em>in those programs</em> substitui o pronome solto <em>them</em>. As opções '
                            '(A) e (D) trocam o problema por palavras positivas (<em>benefit, improvements</em>).',
             'fonte': 'Parte 7, Exercício 12 (linhas 808 e 811)'},
            {'num': '13.4',
             'prompt': 'Trecho (4): Como fechar o parágrafo substituindo "It shows the college needs a new plan"?',
             'options': {'A': 'It shows that the college is in need of a same old strategy.',
                         'B': 'This thing points to a college that does not need any strategy.',
                         'C': 'The whole episode hides that the college needs a new plan.',
                         'D': 'The whole episode points to a college in need of a new strategy.'},
             'correct': 'D',
             'explanation': 'A expressão <strong>The whole episode</strong> amarra toda a sequência de eventos narrada '
                            'no parágrafo e eleva <em>shows... needs a new plan</em> para <em>points to a college in '
                            'need of a new strategy</em>. A opção (A) mantém o <em>It</em> solto na abertura.',
             'fonte': 'Parte 7, Exercício 12 (linhas 808 e 811)'}]},
 {'id': 'mod5-x-14',
  'title': 'Exercício 14: Colocações acadêmicas (meta de 5 min)',
  'level': 'B1–B2',
  'objective': 'Complete cada frase com o verbo ou a preposição que forma a colocação acadêmica natural em inglês '
               '(seção 4.7). Tempo-alvo: 5 minutos.',
  'passage_html': None,
  'items': [{'num': '14.1',
             'prompt': '"Access to clean water ___ a central role in public health."',
             'options': {'A': 'plays', 'B': 'makes', 'C': 'does', 'D': 'puts'},
             'correct': 'A',
             'explanation': 'Em inglês, a combinação natural para desempenhar um papel é <strong>play a role</strong>, '
                            'conjugada no singular (<em>plays</em>) para concordar com o sujeito <em>Access</em>. A '
                            'opção (B) <em>makes</em> é uma interferência comum do português ("faz um papel").',
             'fonte': 'Parte 7, Exercício 13, item 1 (linhas 819 e 828)'},
            {'num': '14.2',
             'prompt': '"The study ___ compelling evidence that the effect is real."',
             'options': {'A': 'poses', 'B': 'provides', 'C': 'reaches', 'D': 'undergoes'},
             'correct': 'B',
             'explanation': 'Com <em>compelling evidence</em>, o verbo que forma colocação acadêmica é '
                            '<strong>provides</strong> (fornece evidências convincentes). A opção (A) <em>poses</em> '
                            'combina com <em>a challenge</em> ou <em>a threat</em>, e não com <em>evidence</em>.',
             'fonte': 'Parte 7, Exercício 13, item 2 (linhas 820 e 828)'},
            {'num': '14.3',
             'prompt': '"There has been a sharp increase ___ applications this year."',
             'options': {'A': 'on', 'B': 'to', 'C': 'in', 'D': 'at'},
             'correct': 'C',
             'explanation': 'Antes daquilo que aumentou (<em>applications</em>), usamos <strong>increase in</strong>. '
                            'Lembre-se da distinção da seção 4.7: <em>an increase in applications</em> (o que subiu), '
                            'mas <em>an increase of 10%</em> (a quantidade que subiu). A opção (A) <em>on</em> é uma '
                            'armadilha frequente.',
             'fonte': 'Parte 7, Exercício 13, item 3 (linhas 821 e 828)'},
            {'num': '14.4',
             'prompt': '"The report ___ concerns about the timeline."',
             'options': {'A': 'gains', 'B': 'plays', 'C': 'meets', 'D': 'raises'},
             'correct': 'D',
             'explanation': 'Para levantar preocupações ou dúvidas, a colocação fixa é <strong>raises '
                            'concerns</strong>. A alternativa (C) <em>meets</em> combina com <em>a need</em> ou <em>a '
                            'deadline</em>, mas não com <em>concerns</em>.',
             'fonte': 'Parte 7, Exercício 13, item 4 (linhas 822 e 828)'},
            {'num': '14.5',
             'prompt': '"Researchers are trying to ___ insight ___ how the disease spreads."',
             'options': {'A': 'gain ... into', 'B': 'make ... about', 'C': 'take ... over', 'D': 'do ... onto'},
             'correct': 'A',
             'explanation': 'O substantivo <em>insight</em> pede o verbo <em>gain</em> antes dele e a preposição '
                            '<em>into</em> depois, formando <strong>gain insight into</strong>. A opção (B) traduz '
                            'literalmente "sobre" por <em>about</em>, mas <em>insight</em> exige <em>into</em>.',
             'fonte': 'Parte 7, Exercício 13, item 5 (linhas 823 e 828)'},
            {'num': '14.6',
             'prompt': '"The two approaches differ ___ one fundamental respect."',
             'options': {'A': 'on', 'B': 'in', 'C': 'to', 'D': 'at'},
             'correct': 'B',
             'explanation': 'Com a palavra <em>respect</em> no sentido de aspecto ou ponto ("em um aspecto '
                            'fundamental"), a preposição correta é <strong>in</strong> (<em>in one fundamental '
                            'respect</em>). A opção (A) <em>on</em> não forma colocação com <em>respect</em>.',
             'fonte': 'Parte 7, Exercício 13, item 6 (linhas 824 e 828)'},
            {'num': '14.7',
             'prompt': '"The policy had a significant impact ___ rural clinics."',
             'options': {'A': 'in', 'B': 'to', 'C': 'on', 'D': 'of'},
             'correct': 'C',
             'explanation': 'Tanto <em>impact</em> quanto <em>effect</em> pedem a preposição <strong>on</strong> para '
                            'indicar quem recebe o impacto (<em>a significant impact on rural clinics</em>). A '
                            'alternativa (A) <em>in</em> é uma transferência comum de "impacto em".',
             'fonte': 'Parte 7, Exercício 13, item 7 (linhas 825 e 828)'},
            {'num': '14.8',
             'prompt': '"This ___ a serious challenge to the standard model."',
             'options': {'A': 'gains', 'B': 'plays', 'C': 'reaches', 'D': 'poses'},
             'correct': 'D',
             'explanation': 'Para dizer que algo representa um desafio, usamos a colocação <strong>poses a serious '
                            'challenge to</strong>. As opções (A), (B) e (C) formam par com outros substantivos da '
                            'seção 4.7 (<em>gain insight</em>, <em>play a role</em>, <em>reach a conclusion</em>).',
             'fonte': 'Parte 7, Exercício 13, item 8 (linhas 826 e 828)'}]}]


# PARTE 9 do M6 (Vocabulário): os exercícios de vocabulário, antes só texto,
# em múltipla escolha. Mesma revisão. Contam nos pontos fracos em Vocabulário.
MOD6_DRILLS = [{'id': 'mod6-x-1',
  'title': 'Exercício 1: Forma exata da palavra (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Identifique a função sintática da lacuna e escolha a palavra completa que preenche cada frase com a '
               'forma gramatical exata. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '1.1',
             'prompt': '"The committee will ass___ the proposal before the vote."',
             'options': {'A': 'assessment', 'B': 'assess', 'C': 'assessing', 'D': 'assessed'},
             'correct': 'B',
             'explanation': 'Depois do modal <em>will</em>, a frase pede o verbo na forma base: '
                            '<strong>assess</strong>. A opção (A) <em>assessment</em> é um substantivo, enquanto (C) e '
                            '(D) trazem formas verbais que não entram diretamente após <em>will</em> na voz ativa.',
             'fonte': 'Parte 9, Exercício 1, item 1 (linhas 538 e 554)'},
            {'num': '1.2',
             'prompt': '"A thorough ass___ of the risks is still pending."',
             'options': {'A': 'assess', 'B': 'assessing', 'C': 'assessed', 'D': 'assessment'},
             'correct': 'D',
             'explanation': 'Entre o adjetivo <em>thorough</em> e a preposição <em>of</em>, você precisa de um '
                            'substantivo contável no singular: <strong>assessment</strong>. A alternativa (A) '
                            '<em>assess</em> é verbo, e (B) <em>assessing</em> não funciona como núcleo nominal depois '
                            'de artigo indefinido e adjetivo nessa estrutura.',
             'fonte': 'Parte 9, Exercício 1, item 2 (linhas 539 e 554)'},
            {'num': '1.3',
             'prompt': '"The results were stat___ significant."',
             'options': {'A': 'statistically', 'B': 'statistical', 'C': 'statistics', 'D': 'statistician'},
             'correct': 'A',
             'explanation': 'Para modificar o adjetivo <em>significant</em>, a posição exige um advérbio terminado em '
                            '<em>-ly</em>: <strong>statistically</strong>. A opção (B) <em>statistical</em> é adjetivo '
                            'e só caberia antes de um substantivo, como em <em>statistical significance</em>.',
             'fonte': 'Parte 9, Exercício 1, item 3 (linhas 540 e 554)'},
            {'num': '1.4',
             'prompt': '"Researchers must control for every conf___ variable."',
             'options': {'A': 'confound', 'B': 'confoundedly', 'C': 'confounding', 'D': 'confounder'},
             'correct': 'C',
             'explanation': 'Antes do substantivo <em>variable</em>, usamos o adjetivo que forma o termo técnico de '
                            'pesquisa <strong>confounding</strong> (<em>confounding variable</em>, ou variável de '
                            'confundimento). A opção (A) <em>confound</em> está na forma verbal base, e (B) é um '
                            'advérbio.',
             'fonte': 'Parte 9, Exercício 1, item 4 (linhas 541 e 554)'},
            {'num': '1.5',
             'prompt': '"The two theories offer comp___ explanations of the same data." (no sentido de concorrentes ou '
                       'rivais)',
             'options': {'A': 'competition', 'B': 'competitively', 'C': 'competitor', 'D': 'competing'},
             'correct': 'D',
             'explanation': 'Para qualificar <em>explanations</em> no sentido de teorias rivais que disputam a '
                            'explicação dos mesmos dados, a colocação acadêmica exata é <strong>competing</strong>. A '
                            'opção (A) <em>competition</em> é substantivo abstrato, e (B) é advérbio.',
             'fonte': 'Parte 9, Exercício 1, item 5 (linhas 542 e 554)'},
            {'num': '1.6',
             'prompt': '"Her argument rests on a questionable assum___."',
             'options': {'A': 'assumption', 'B': 'assuming', 'C': 'assumed', 'D': 'assumes'},
             'correct': 'A',
             'explanation': 'O artigo <em>a</em> e o adjetivo <em>questionable</em> anunciam um substantivo contável '
                            'no singular: <strong>assumption</strong> (premissa ou suposição). A opção (C) '
                            '<em>assumed</em> é adjetivo ou particípio e deixaria a frase sem um substantivo no final.',
             'fonte': 'Parte 9, Exercício 1, item 6 (linhas 543 e 554)'},
            {'num': '1.7',
             'prompt': '"The city failed to pri___ infrastructure spending."',
             'options': {'A': 'priority', 'B': 'prioritizing', 'C': 'prioritize', 'D': 'priorities'},
             'correct': 'C',
             'explanation': 'A estrutura <em>failed to</em> pede um verbo no infinitivo, formado aqui pelo sufixo '
                            'verbal <em>-ize</em>: <strong>prioritize</strong>. A opção (A) <em>priority</em> é '
                            'substantivo, e (B) <em>prioritizing</em> usa gerúndio onde o <em>to</em> funciona como '
                            'marca de infinitivo.',
             'fonte': 'Parte 9, Exercício 1, item 7 (linhas 544 e 554)'},
            {'num': '1.8',
             'prompt': '"The evidence is far from concl___."',
             'options': {'A': 'conclusion', 'B': 'conclusive', 'C': 'conclusively', 'D': 'conclude'},
             'correct': 'B',
             'explanation': 'Na expressão predicativa <em>is far from...</em>, a lacuna descreve o sujeito <em>the '
                            'evidence</em> e pede o adjetivo <strong>conclusive</strong> (conclusiva). A alternativa '
                            '(A) <em>conclusion</em> é substantivo, e (C) <em>conclusively</em> é advérbio.',
             'fonte': 'Parte 9, Exercício 1, item 8 (linhas 545 e 554)'}]},
 {'id': 'mod6-x-2',
  'title': 'Exercício 2: Forma exata da palavra, nível avançado (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Complete cada frase escolhendo a palavra acadêmica que começa com as letras indicadas e atende à '
               'função gramatical da lacuna. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '2.1',
             'prompt': '"The lecture elab___ on a point the reading only mentions."',
             'options': {'A': 'elaborate', 'B': 'elaboration', 'C': 'elaborates', 'D': 'elaborately'},
             'correct': 'C',
             'explanation': 'O sujeito singular <em>The lecture</em> pede o verbo conjugado na terceira pessoa do '
                            'singular do presente simples: <strong>elaborates</strong>. A opção (A) <em>elaborate</em> '
                            'não flexiona o verbo para concordar com <em>lecture</em>, e (B) é um substantivo.',
             'fonte': 'Parte 9, Exercício 1, item 9 (linhas 546 e 554)'},
            {'num': '2.2',
             'prompt': '"Such policies tend to perp___ existing inequalities."',
             'options': {'A': 'perpetual', 'B': 'perpetuate', 'C': 'perpetually', 'D': 'perpetuation'},
             'correct': 'B',
             'explanation': 'Após <em>tend to</em>, precisamos do verbo na forma base: <strong>perpetuate</strong> '
                            '(perpetuar ou manter ativo). A opção (A) <em>perpetual</em> é adjetivo, e (D) '
                            '<em>perpetuation</em> é substantivo.',
             'fonte': 'Parte 9, Exercício 1, item 10 (linhas 547 e 554)'},
            {'num': '2.3',
             'prompt': '"The findings were later corrob___ by an independent team."',
             'options': {'A': 'corroborate', 'B': 'corroboration', 'C': 'corroborating', 'D': 'corroborated'},
             'correct': 'D',
             'explanation': 'A estrutura <em>were later ... by</em> está na voz passiva e exige o particípio passado '
                            '<strong>corroborated</strong> (confirmados). A alternativa (A) deixa o verbo sem a '
                            'terminação <em>-ed</em>, e (C) formaria a voz ativa contínua, incompatível com o agente '
                            'introduzido por <em>by</em>.',
             'fonte': 'Parte 9, Exercício 1, item 11 (linhas 548 e 554)'},
            {'num': '2.4',
             'prompt': '"There is considerable variat___ between the regions."',
             'options': {'A': 'variation', 'B': 'variations', 'C': 'variational', 'D': 'variatively'},
             'correct': 'A',
             'explanation': 'Com o verbo no singular (<em>There is</em>) e o adjetivo <em>considerable</em>, a lacuna '
                            'pede o substantivo incontável no singular: <strong>variation</strong>. A opção (B) '
                            '<em>variations</em> está no plural e entraria em conflito com <em>There is</em>, enquanto '
                            '(C) é adjetivo.',
             'fonte': 'Parte 9, Exercício 1, item 12 (linhas 549 e 554)'},
            {'num': '2.5',
             'prompt': '"The professor\'s account is more nu___ than the textbook\'s."',
             'options': {'A': 'nuance', 'B': 'nuances', 'C': 'nuanced', 'D': 'nuancing'},
             'correct': 'C',
             'explanation': 'A estrutura comparativa <em>is more ... than</em> descreve o substantivo <em>account</em> '
                            'e pede o adjetivo <strong>nuanced</strong> (nuançado, com distinções sutis). A opção (A) '
                            '<em>nuance</em> é substantivo e não funciona diretamente como predicativo depois de '
                            '<em>is more</em>.',
             'fonte': 'Parte 9, Exercício 1, item 13 (linhas 550 e 554)'},
            {'num': '2.6',
             'prompt': '"This raises an important episte___ question about how we know what we claim to know."',
             'options': {'A': 'epistemology', 'B': 'epistemically', 'C': 'epistemologies', 'D': 'epistemic'},
             'correct': 'D',
             'explanation': 'Antes do substantivo <em>question</em>, você precisa do adjetivo '
                            '<strong>epistemic</strong> (relativo à natureza e à validade do conhecimento). A '
                            'alternativa (A) <em>epistemology</em> é o substantivo que nomeia a área da filosofia, e '
                            '(B) é advérbio.',
             'fonte': 'Parte 9, Exercício 1, item 14 (linhas 551 e 554)'},
            {'num': '2.7',
             'prompt': '"The intervention produced only a marg___ improvement."',
             'options': {'A': 'margin', 'B': 'marginal', 'C': 'marginally', 'D': 'marginalize'},
             'correct': 'B',
             'explanation': 'Entre o artigo <em>a</em> e o substantivo <em>improvement</em>, a frase pede o adjetivo '
                            '<strong>marginal</strong> (pequeno, mínimo). A opção (C) <em>marginally</em> é advérbio, '
                            'e (A) <em>margin</em> é substantivo.',
             'fonte': 'Parte 9, Exercício 1, item 15 (linhas 552 e 554)'}]},
 {'id': 'mod6-x-3',
  'title': 'Exercício 3: Família e forma da palavra (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Escolha a forma correta da palavra derivada da raiz entre parênteses para preencher cada lacuna com '
               'precisão gramatical. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '3.1',
             'prompt': '"The study\'s methodological ___ (ROBUST) has been widely praised."',
             'options': {'A': 'robustly', 'B': 'robustness', 'C': 'robust', 'D': 'robusts'},
             'correct': 'B',
             'explanation': "Depois do possessivo <em>The study's</em> e do adjetivo <em>methodological</em>, o núcleo "
                            'do sujeito precisa ser um substantivo abstrato: <strong>robustness</strong> (solidez). A '
                            'opção (C) <em>robust</em> é adjetivo, e (D) <em>robusts</em> não existe porque adjetivos '
                            'em inglês não levam plural.',
             'fonte': 'Parte 9, Exercício 2, item 1 (linhas 560 e 573)'},
            {'num': '3.2',
             'prompt': '"These findings ___ (SUBSTANTIAL) the earlier hypothesis."',
             'options': {'A': 'substantiate', 'B': 'substantially', 'C': 'substantiation', 'D': 'substantiates'},
             'correct': 'A',
             'explanation': 'A oração precisa de um verbo principal que concorde com o sujeito plural <em>These '
                            'findings</em>: <strong>substantiate</strong> (comprovam ou fundamentam). A alternativa '
                            '(D) <em>substantiates</em> está no singular, e (B) <em>substantially</em> é advérbio.',
             'fonte': 'Parte 9, Exercício 2, item 2 (linhas 561 e 573)'},
            {'num': '3.3',
             'prompt': '"The two accounts differ ___ (SIGNIFICANT) in their conclusions."',
             'options': {'A': 'significance', 'B': 'significant', 'C': 'signify', 'D': 'significantly'},
             'correct': 'D',
             'explanation': 'Para qualificar o verbo de ação <em>differ</em>, você deve usar o advérbio '
                            '<strong>significantly</strong>. A opção (B) <em>significant</em> é adjetivo e só '
                            'modificaria um substantivo, enquanto (A) <em>significance</em> é substantivo.',
             'fonte': 'Parte 9, Exercício 2, item 3 (linhas 562 e 573)'},
            {'num': '3.4',
             'prompt': '"A ___ (PERSIST) gap remains between policy and practice."',
             'options': {'A': 'persistence', 'B': 'persistently', 'C': 'persistent', 'D': 'persists'},
             'correct': 'C',
             'explanation': 'Entre o artigo <em>A</em> e o substantivo <em>gap</em>, a colocação consagrada pede o '
                            'adjetivo <strong>persistent</strong> (<em>a persistent gap</em>, uma lacuna persistente). '
                            'A opção (A) <em>persistence</em> é substantivo, e (B) <em>persistently</em> é advérbio.',
             'fonte': 'Parte 9, Exercício 2, item 4 (linhas 563 e 573)'},
            {'num': '3.5',
             'prompt': '"The data must be interpreted with ___ (CAUTION)."',
             'options': {'A': 'caution', 'B': 'cautious', 'C': 'cautiously', 'D': 'cautionary'},
             'correct': 'A',
             'explanation': 'A preposição <em>with</em> exige um substantivo como complemento, formando a expressão '
                            '<strong>with caution</strong> (com cautela). Se não houvesse a preposição <em>with</em>, '
                            'você usaria o advérbio <em>cautiously</em> da opção (C); já (B) <em>cautious</em> é '
                            'adjetivo.',
             'fonte': 'Parte 9, Exercício 2, item 5 (linhas 564 e 573)'},
            {'num': '3.6',
             'prompt': '"The model ___ (SIMPLE) a process that is in fact highly complex." (use o prefixo over-)',
             'options': {'A': 'oversimplify', 'B': 'oversimplifies', 'C': 'oversimplifying', 'D': 'oversimplification'},
             'correct': 'B',
             'explanation': 'O sujeito singular <em>The model</em> e o tempo presente da segunda oração (<em>is in '
                            'fact</em>) pedem o verbo na terceira pessoa do singular: <strong>oversimplifies</strong> '
                            '(simplifica em excesso). A opção (A) <em>oversimplify</em> não faz a concordância com '
                            '<em>The model</em>, e (D) é substantivo.',
             'fonte': 'Parte 9, Exercício 2, item 6 (linhas 565 e 573)'}]},
 {'id': 'mod6-x-4',
  'title': 'Exercício 4: Sufixos e derivação lexical (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Identifique a classe gramatical exigida pela estrutura da frase e escolha a derivação correta da '
               'palavra entre parênteses. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '4.1',
             'prompt': '"Their ___ (RELY) on a single data source weakens the argument."',
             'options': {'A': 'reliable', 'B': 'reliably', 'C': 'reliance', 'D': 'reliant'},
             'correct': 'C',
             'explanation': 'Depois do pronome possessivo <em>Their</em> e antes da preposição <em>on</em>, a posição '
                            'pede o substantivo <strong>reliance</strong> (dependência). A alternativa (D) '
                            '<em>reliant</em> e a (A) <em>reliable</em> são adjetivos e não podem ocupar o núcleo do '
                            'sujeito.',
             'fonte': 'Parte 9, Exercício 2, item 7 (linhas 566 e 573)'},
            {'num': '4.2',
             'prompt': '"The phenomenon has been documented ___ (EXTENSIVE)."',
             'options': {'A': 'extensive', 'B': 'extension', 'C': 'extend', 'D': 'extensively'},
             'correct': 'D',
             'explanation': 'Para modificar o verbo na voz passiva <em>has been documented</em>, precisamos do '
                            'advérbio <strong>extensively</strong> (amplamente). A opção (A) <em>extensive</em> é '
                            'adjetivo e só funcionaria antes de um substantivo, como em <em>extensive '
                            'documentation</em>.',
             'fonte': 'Parte 9, Exercício 2, item 8 (linhas 567 e 573)'},
            {'num': '4.3',
             'prompt': '"The committee reached a ___ (CONCLUDE) after months of review."',
             'options': {'A': 'conclusive', 'B': 'conclusion', 'C': 'conclusively', 'D': 'concluding'},
             'correct': 'B',
             'explanation': 'O artigo indefinido <em>a</em> e o verbo <em>reached</em> formam a colocação clássica '
                            '<em>reach a conclusion</em>, exigindo o substantivo <strong>conclusion</strong>. As '
                            'opções (A) <em>conclusive</em> e (D) <em>concluding</em> são formas adjetivas que '
                            'deixariam o artigo sem substantivo.',
             'fonte': 'Parte 9, Exercício 2, item 9 (linhas 568 e 573)'},
            {'num': '4.4',
             'prompt': '"The reform was ___ (TRANSFORM) rather than incremental."',
             'options': {'A': 'transformative', 'B': 'transformation', 'C': 'transform', 'D': 'transformatively'},
             'correct': 'A',
             'explanation': 'A estrutura paralela <em>was ... rather than incremental</em> compara dois adjetivos '
                            'predicativos, pedindo <strong>transformative</strong> (transformadora). A alternativa (B) '
                            '<em>transformation</em> é substantivo e quebraria o paralelismo com o adjetivo '
                            '<em>incremental</em>.',
             'fonte': 'Parte 9, Exercício 2, item 10 (linhas 569 e 573)'},
            {'num': '4.5',
             'prompt': '"The claim is ___ (DEMONSTRATE) false."',
             'options': {'A': 'demonstrable', 'B': 'demonstration', 'C': 'demonstrative', 'D': 'demonstrably'},
             'correct': 'D',
             'explanation': 'Antes do adjetivo <em>false</em>, a função sintática é de advérbio modificador: '
                            '<strong>demonstrably</strong> (comprovadamente falso). A opção (A) <em>demonstrable</em> '
                            'é adjetivo e não pode modificar outro adjetivo.',
             'fonte': 'Parte 9, Exercício 2, item 11 (linhas 570 e 573)'},
            {'num': '4.6',
             'prompt': '"Such ___ (VARY) is expected in samples of this size."',
             'options': {'A': 'various', 'B': 'variously', 'C': 'variation', 'D': 'variables'},
             'correct': 'C',
             'explanation': 'O determinante <em>Such</em> seguido do verbo singular <em>is expected</em> pede um '
                            'substantivo no singular como núcleo do sujeito: <strong>variation</strong> (note que '
                            '<em>variability</em> também caberia nesse contexto, por isso não está entre as '
                            'alternativas). A opção (A) <em>various</em> é adjetivo, e (D) <em>variables</em> está no '
                            'plural.',
             'fonte': 'Parte 9, Exercício 2, item 12 (linhas 571 e 573)'}]},
 {'id': 'mod6-x-5',
  'title': 'Exercício 5: Collocations com verbo âncora (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Escolha o verbo âncora que forma a colocação acadêmica natural em cada frase, conforme a tabela da '
               'Parte 4. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '5.1',
             'prompt': '"The researchers ___ a longitudinal study over fifteen years."',
             'options': {'A': 'posed', 'B': 'yielded', 'C': 'conducted', 'D': 'reached'},
             'correct': 'C',
             'explanation': 'Com substantivos como <em>study</em>, <em>research</em> ou <em>experiment</em>, a '
                            'colocação acadêmica padrão é <strong>conducted</strong> (conduziram). A opção (B) '
                            '<em>yielded</em> combina com os resultados gerados pelo estudo (<em>yield results</em>), '
                            'e não com o estudo em si.',
             'fonte': 'Parte 9, Exercício 3, item 1 (linhas 579 e 588)'},
            {'num': '5.2',
             'prompt': '"It is too early to ___ firm conclusions."',
             'options': {'A': 'draw', 'B': 'pose', 'C': 'conduct', 'D': 'exert'},
             'correct': 'A',
             'explanation': 'Para expressar a ideia de tirar conclusões a partir de dados, o inglês acadêmico usa a '
                            'combinação <strong>draw</strong> (<em>draw firm conclusions</em>). A opção (B) '
                            '<em>pose</em> forma par com <em>a threat</em> ou <em>a question</em>, mas não com '
                            '<em>conclusions</em>.',
             'fonte': 'Parte 9, Exercício 3, item 2 (linhas 580 e 588)'},
            {'num': '5.3',
             'prompt': '"The lecture ___ a serious objection to the reading\'s assumption."',
             'options': {'A': 'conducts', 'B': 'reaches', 'C': 'meets', 'D': 'raises'},
             'correct': 'D',
             'explanation': 'Para levantar uma objeção, dúvida ou preocupação, o verbo âncora correto é '
                            '<strong>raises</strong> (<em>raises a serious objection</em>). A alternativa (B) '
                            '<em>reaches</em> combina com <em>a consensus</em> ou <em>a conclusion</em>, e não com '
                            '<em>objection</em>.',
             'fonte': 'Parte 9, Exercício 3, item 3 (linhas 581 e 588)'},
            {'num': '5.4',
             'prompt': '"Algorithmic bias ___ a direct threat to fair hiring."',
             'options': {'A': 'draws', 'B': 'poses', 'C': 'conducts', 'D': 'reaches'},
             'correct': 'B',
             'explanation': 'Com <em>a threat</em>, <em>a risk</em> ou <em>a challenge</em>, o verbo que forma '
                            'colocação natural é <strong>poses</strong> (representa uma ameaça direta). As opções (A) '
                            '<em>draws</em> e (D) <em>reaches</em> pertencem a outros grupos de colocação.',
             'fonte': 'Parte 9, Exercício 3, item 4 (linhas 582 e 588)'},
            {'num': '5.5',
             'prompt': '"Early education programs ___ large long-term returns."',
             'options': {'A': 'yield', 'B': 'pose', 'C': 'draw', 'D': 'reach'},
             'correct': 'A',
             'explanation': 'No sentido de gerar resultados, dados ou retornos sobre um investimento, a escolha '
                            'precisa é <strong>yield</strong> (<em>yield large long-term returns</em>). A opção (B) '
                            '<em>pose</em> é usada para problemas ou ameaças, e não para retornos positivos.',
             'fonte': 'Parte 9, Exercício 3, item 5 (linhas 583 e 588)'},
            {'num': '5.6',
             'prompt': '"The new evidence ___ the conventional explanation."',
             'options': {'A': 'conducts', 'B': 'yields', 'C': 'reaches', 'D': 'challenges'},
             'correct': 'D',
             'explanation': 'Quando novos dados colocam em xeque uma teoria ou o senso comum, usamos '
                            '<strong>challenges</strong> (<em>challenges the conventional explanation</em>). A opção '
                            '(B) <em>yields</em> significaria que a evidência gerou a explicação tradicional, o oposto '
                            'do contexto.',
             'fonte': 'Parte 9, Exercício 3, item 6 (linhas 584 e 588)'},
            {'num': '5.7',
             'prompt': '"The reading fails to ___ the implementation costs."',
             'options': {'A': 'draw on', 'B': 'account for', 'C': 'reach for', 'D': 'pose as'},
             'correct': 'B',
             'explanation': 'A expressão <strong>account for</strong> significa levar em conta ou explicar um fator '
                            'importante na análise (<em>fails to account for the implementation costs</em>). A opção '
                            '(A) <em>draw on</em> significa recorrer a uma fonte, o que mudaria o sentido da crítica.',
             'fonte': 'Parte 9, Exercício 3, item 7 (linhas 585 e 588)'},
            {'num': '5.8',
             'prompt': '"After long debate, the panel ___ a consensus."',
             'options': {'A': 'posed', 'B': 'yielded', 'C': 'reached', 'D': 'conducted'},
             'correct': 'C',
             'explanation': 'Em inglês, você chega a um consenso, acordo ou conclusão usando o verbo '
                            '<strong>reached</strong> (<em>reached a consensus</em>). A alternativa (D) '
                            '<em>conducted</em> combina com <em>a study</em> ou <em>a debate</em>, mas não com '
                            '<em>consensus</em>.',
             'fonte': 'Parte 9, Exercício 3, item 8 (linhas 586 e 588)'}]},
 {'id': 'mod6-x-6',
  'title': 'Exercício 6: Substituição por sinônimo acadêmico (meta de 3 min)',
  'level': 'C1–C2',
  'objective': 'Escolha o termo acadêmico de alto impacto que substitui com exatidão a expressão em destaque, mantendo '
               'o sentido da frase original. Tempo-alvo: 3 minutos.',
  'passage_html': None,
  'items': [{'num': '6.1',
             'prompt': 'Substitua o trecho em destaque por um único verbo acadêmico em: "The policy '
                       '<strong>made</strong> the problem <strong>worse</strong>."',
             'options': {'A': 'exacerbated', 'B': 'mitigated', 'C': 'corroborated', 'D': 'elucidated'},
             'correct': 'A',
             'explanation': 'Para dizer que uma medida agravou ou piorou um problema já existente, o verbo de alto '
                            'impacto exato é <strong>exacerbated</strong> (<em>The policy exacerbated the '
                            'problem</em>). A opção (B) <em>mitigated</em> tem o sentido oposto: atenuar ou reduzir o '
                            'problema.',
             'fonte': 'Parte 9, Exercício 4, item 1 (linhas 594 e 605)'},
            {'num': '6.2',
             'prompt': 'Substitua o verbo simples por um equivalente acadêmico que enfatize a relevância do ponto em: '
                       '"This <strong>shows</strong> the importance of early action."',
             'options': {'A': 'precludes', 'B': 'circumvents', 'C': 'underscores', 'D': 'undermines'},
             'correct': 'C',
             'explanation': 'O verbo <strong>underscores</strong> substitui <em>shows</em> ou <em>emphasizes</em> com '
                            'força analítica, ressaltando a importância da ação precoce. A alternativa (D) '
                            '<em>undermines</em> significa enfraquecer ou minar, invertendo o argumento.',
             'fonte': 'Parte 9, Exercício 4, item 2 (linhas 595 e 605)'},
            {'num': '6.3',
             'prompt': 'Substitua o trecho em destaque pela expressão acadêmica correspondente em: "The two studies '
                       '<strong>agree with each other</strong>."',
             'options': {'A': 'contradict one another',
                         'B': 'preclude one another',
                         'C': 'exacerbate one another',
                         'D': 'corroborate one another'},
             'correct': 'D',
             'explanation': 'Quando dois estudos independentes confirmam os mesmos resultados, dizemos que eles '
                            '<strong>corroborate one another</strong> (corroboram um ao outro). A opção (A) '
                            '<em>contradict one another</em> indica o oposto (contradição), e (B) indica que um impede '
                            'o outro.',
             'fonte': 'Parte 9, Exercício 4, item 3 (linhas 596 e 605)'},
            {'num': '6.4',
             'prompt': 'Substitua a palavra em destaque pelo adjetivo acadêmico mais preciso em: "The theory is '
                       '<strong>weak</strong> and easily challenged."',
             'options': {'A': 'robust', 'B': 'tenuous', 'C': 'compelling', 'D': 'pervasive'},
             'correct': 'B',
             'explanation': 'Para qualificar uma teoria, conexão ou argumento como frágil e pouco convincente, o '
                            'adjetivo de nível C1 é <strong>tenuous</strong> (tênue). As opções (A) <em>robust</em> e '
                            '(C) <em>compelling</em> descrevem justamente o contrário: evidências sólidas e '
                            'convincentes.',
             'fonte': 'Parte 9, Exercício 4, item 4 (linhas 597 e 605)'},
            {'num': '6.5',
             'prompt': 'Substitua o verbo em destaque pelo termo técnico adequado em: "Green spaces can '
                       '<strong>reduce</strong> urban heat."',
             'options': {'A': 'mitigate', 'B': 'exacerbate', 'C': 'perpetuate', 'D': 'precipitate'},
             'correct': 'A',
             'explanation': 'No contexto de reduzir a gravidade ou o impacto de um problema ambiental, o verbo preciso '
                            'é <strong>mitigate</strong> (mitigar ou atenuar). A alternativa (B) <em>exacerbate</em> '
                            'significa agravar, e (C) <em>perpetuate</em> significa manter o problema ativo.',
             'fonte': 'Parte 9, Exercício 4, item 5 (linhas 598 e 605)'}]},
 {'id': 'mod6-x-7',
  'title': 'Exercício 7: Verbos e adjetivos de alto registro (meta de 3 min)',
  'level': 'C1–C2',
  'objective': 'Substitua a palavra simples em destaque pelo verbo ou adjetivo acadêmico que expressa a nuance exata '
               'pedida no contexto. Tempo-alvo: 3 minutos.',
  'passage_html': None,
  'items': [{'num': '7.1',
             'prompt': 'Substitua o verbo em destaque indicando que o professor propõe a ideia como hipótese ou '
                       'premissa teórica: "The professor <strong>says</strong> the cause is economic."',
             'options': {'A': 'concedes', 'B': 'posits', 'C': 'refutes', 'D': 'ignores'},
             'correct': 'B',
             'explanation': 'Quando um pesquisador ou professor postula uma hipótese como ponto de partida de um '
                            'argumento, o verbo ideal é <strong>posits</strong>. A opção (A) <em>concedes</em> seria '
                            'usada apenas se ele estivesse admitindo um ponto contrário à própria tese.',
             'fonte': 'Parte 9, Exercício 4, item 6 (linhas 599 e 605)'},
            {'num': '7.2',
             'prompt': 'Substitua o verbo em destaque indicando que os críticos defendem uma tese firme em um debate: '
                       '"Critics <strong>say</strong> the model ignores regional gaps."',
             'options': {'A': 'concede', 'B': 'recall', 'C': 'hinder', 'D': 'contend'},
             'correct': 'D',
             'explanation': 'Para relatar que um grupo sustenta ou defende uma posição argumentativa forte, usamos '
                            '<strong>contend</strong>. A alternativa (A) <em>concede</em> indicaria recuo ou admissão '
                            'de falha, e não um argumento de ataque dos críticos.',
             'fonte': 'Parte 9, Exercício 4, item 7 (linhas 600 e 605)'},
            {'num': '7.3',
             'prompt': 'Substitua o trecho de sentido simples pelo adjetivo acadêmico equivalente em: "The result was '
                       '<strong>surprising given common sense</strong>."',
             'options': {'A': 'counterintuitive', 'B': 'arbitrary', 'C': 'ostensible', 'D': 'negligible'},
             'correct': 'A',
             'explanation': 'Aquilo que contraria o que a intuição ou o senso comum esperaria é definido pelo adjetivo '
                            '<strong>counterintuitive</strong> (contraintuitivo). A opção (B) <em>arbitrary</em> '
                            'significa aleatório ou sem critério, e (D) <em>negligible</em> significa insignificante.',
             'fonte': 'Parte 9, Exercício 4, item 8 (linhas 601 e 605)'},
            {'num': '7.4',
             'prompt': 'Substitua a palavra em destaque por um adjetivo de registro acadêmico em: "The influence of '
                       'social media is <strong>everywhere</strong>."',
             'options': {'A': 'marginal', 'B': 'tenuous', 'C': 'pervasive', 'D': 'negligible'},
             'correct': 'C',
             'explanation': 'Para descrever uma influência ou tendência que se espalhou por toda parte na sociedade, o '
                            'adjetivo preciso é <strong>pervasive</strong> (difuso ou generalizado). As opções (A) '
                            '<em>marginal</em> e (D) <em>negligible</em> dizem o contrário: uma influência pequena.',
             'fonte': 'Parte 9, Exercício 4, item 9 (linhas 602 e 605)'},
            {'num': '7.5',
             'prompt': 'Substitua a palavra em destaque pelo adjetivo metodológico adequado em: "The finding held up '
                       'across many <strong>strong</strong> studies."',
             'options': {'A': 'ostensible', 'B': 'robust', 'C': 'plausible', 'D': 'salient'},
             'correct': 'B',
             'explanation': 'Em ciência e pesquisa, estudos ou resultados metodologicamente fortes e resistentes a '
                            'falhas são chamados de <strong>robust</strong> (sólidos ou robustos). A alternativa (C) '
                            '<em>plausible</em> diz apenas que algo parece possível na teoria, sem confirmar solidez '
                            'empírica.',
             'fonte': 'Parte 9, Exercício 4, item 10 (linhas 603 e 605)'}]},
 {'id': 'mod6-x-8',
  'title': 'Exercício 8: Pares de nuance e regência (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Escolha a alternativa que preenche cada frase com precisão lexical e gramatical no registro acadêmico '
               'formal (Parte 6.1). Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '8.1',
             'prompt': '"The new rule will ___ attendance."',
             'options': {'A': 'effect', 'B': 'effects', 'C': 'affect', 'D': 'affective'},
             'correct': 'C',
             'explanation': 'Após o auxiliar <em>will</em>, a frase pede um verbo no sentido de influenciar: '
                            '<strong>affect</strong>. Lembre-se de que <em>effect</em> na opção (A) é quase sempre '
                            'substantivo (o resultado), enquanto <em>affect</em> é o verbo de ação.',
             'fonte': 'Parte 9, Exercício 5, item 1 (linhas 611 e 624)'},
            {'num': '8.2',
             'prompt': '"The ___ on attendance was minimal."',
             'options': {'A': 'effect', 'B': 'affect', 'C': 'affecting', 'D': 'effective'},
             'correct': 'A',
             'explanation': 'Entre o artigo <em>The</em> e a preposição <em>on</em>, o núcleo do sujeito exige o '
                            'substantivo <strong>effect</strong> (o efeito ou resultado sobre a presença). A opção (B) '
                            '<em>affect</em> é verbo no uso geral, e (D) <em>effective</em> é adjetivo.',
             'fonte': 'Parte 9, Exercício 5, item 2 (linhas 612 e 624)'},
            {'num': '8.3',
             'prompt': '"The author ___ that the data are unreliable." (o autor dá a entender isso, sem dizer '
                       'diretamente)',
             'options': {'A': 'infers', 'B': 'inferring', 'C': 'imply', 'D': 'implies'},
             'correct': 'D',
             'explanation': 'Quem escreve ou fala dá a entender algo, por isso o sujeito <em>The author</em> pede '
                            '<strong>implies</strong> (sugere indiretamente). A opção (A) <em>infers</em> cabe a quem '
                            'lê ou ouve e tira uma dedução a partir do texto.',
             'fonte': 'Parte 9, Exercício 5, item 3 (linhas 613 e 624)'},
            {'num': '8.4',
             'prompt': '"From the tone, we ___ skepticism."',
             'options': {'A': 'implies', 'B': 'infer', 'C': 'imply', 'D': 'infers'},
             'correct': 'B',
             'explanation': 'Como somos nós (os leitores ou ouvintes) que deduzimos o ceticismo a partir do tom, o '
                            'verbo exato é <strong>infer</strong>. A alternativa (C) <em>imply</em> descreveria a ação '
                            'do autor ao emitir a pista, e não a nossa conclusão ao interpretá-la.',
             'fonte': 'Parte 9, Exercício 5, item 4 (linhas 614 e 624)'},
            {'num': '8.5',
             'prompt': '"The report ___ five chapters." (escolha a forma recomendada no registro acadêmico formal)',
             'options': {'A': 'is comprised of', 'B': 'comprise of', 'C': 'comprises', 'D': 'constitutes of'},
             'correct': 'C',
             'explanation': 'No registro acadêmico formal, o todo abrange as partes diretamente na voz ativa: '
                            '<strong>comprises</strong> (sem preposição). Evite a construção passiva <em>is comprised '
                            'of</em> da opção (A), que é rejeitada por manuais de estilo formais; caso queira a '
                            'passiva, use <em>is composed of</em>.',
             'fonte': 'Parte 9, Exercício 5, item 5 (linhas 615 e 624)'},
            {'num': '8.6',
             'prompt': '"There were ___ objections than expected."',
             'options': {'A': 'less', 'B': 'lesser', 'C': 'amount of', 'D': 'fewer'},
             'correct': 'D',
             'explanation': 'Como <em>objections</em> é um substantivo contável no plural, o comparativo de '
                            'inferioridade correto é <strong>fewer</strong>. A opção (A) <em>less</em> acompanha '
                            'apenas termos incontáveis no singular, como <em>less resistance</em> ou <em>less '
                            'variation</em>.',
             'fonte': 'Parte 9, Exercício 5, item 6 (linhas 616 e 624)'}]},
 {'id': 'mod6-x-9',
  'title': 'Exercício 9: Precisão lexical e falsos amigos (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Escolha a palavra que completa cada frase com o sentido exato exigido pelo contexto acadêmico (Partes '
               '6.1 e 6.2). Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '9.1',
             'prompt': '"The ___ of participants was small."',
             'options': {'A': 'amount', 'B': 'number', 'C': 'quantity', 'D': 'volume'},
             'correct': 'B',
             'explanation': 'Para seres e itens contáveis no plural como <em>participants</em>, usamos sempre '
                            '<strong>number</strong> (<em>the number of participants</em>). A opção (A) '
                            '<em>amount</em> é reservada para substantivos incontáveis, como em <em>the amount of '
                            'data</em>.',
             'fonte': 'Parte 9, Exercício 5, item 7 (linhas 617 e 624)'},
            {'num': '9.2',
             'prompt': '"Compared ___ the control group, the treatment group improved."',
             'options': {'A': 'by', 'B': 'at', 'C': 'from', 'D': 'with'},
             'correct': 'D',
             'explanation': 'Para comparar dois grupos da mesma categoria, como tratamento e controle, os manuais de '
                            'estilo recomendam <strong>with</strong> (<em>compared with</em>). As opções <em>by</em>, '
                            '<em>at</em> e <em>from</em> não formam regência com <em>compared</em>. O <em>to</em> '
                            'também é aceito no uso geral, e por isso ficou de fora.',
             'fonte': 'Parte 9, Exercício 5, item 8 (linhas 618 e 624)'},
            {'num': '9.3',
             'prompt': '"The ___ reason is cost."',
             'options': {'A': 'principal', 'B': 'principle', 'C': 'principally', 'D': 'principles'},
             'correct': 'A',
             'explanation': 'Antes do substantivo <em>reason</em>, precisamos do adjetivo que significa principal ou '
                            'mais importante: <strong>principal</strong>. A alternativa (B) <em>principle</em> tem '
                            'pronúncia parecida, mas é sempre um substantivo que significa princípio ou regra '
                            'fundamental.',
             'fonte': 'Parte 9, Exercício 5, item 9 (linhas 619 e 624)'},
            {'num': '9.4',
             'prompt': '"The measures are ___ given the uncertainty."',
             'options': {'A': 'sensitive', 'B': 'sensitively', 'C': 'sensible', 'D': 'sensibility'},
             'correct': 'C',
             'explanation': 'Diante de um cenário de incerteza, medidas equilibradas e de bom senso são descritas pelo '
                            'adjetivo <strong>sensible</strong> (sensatas). A opção (A) <em>sensitive</em> é um falso '
                            'cognato clássico e significa sensível ou delicado, não sensato.',
             'fonte': 'Parte 9, Exercício 5, item 10 (linhas 620 e 624)'},
            {'num': '9.5',
             'prompt': '"The scandal ___ the resignation."',
             'options': {'A': 'proceeded', 'B': 'preceded', 'C': 'proceeds', 'D': 'preceding'},
             'correct': 'B',
             'explanation': 'Para dizer que o escândalo veio antes da renúncia, o verbo transitivo correto é '
                            '<strong>preceded</strong> (precedeu, com o prefixo <em>pre-</em> de anterioridade). A '
                            'opção (A) <em>proceeded</em> significa prosseguir ou avançar.',
             'fonte': 'Parte 9, Exercício 5, item 11 (linhas 621 e 624)'},
            {'num': '9.6',
             'prompt': '"The survey was designed to ___ candid responses."',
             'options': {'A': 'elicit', 'B': 'illicit', 'C': 'illicitly', 'D': 'elicited'},
             'correct': 'A',
             'explanation': 'Depois de <em>designed to</em>, precisamos de um verbo no infinitivo que signifique obter '
                            'ou extrair respostas: <strong>elicit</strong>. A opção (B) <em>illicit</em> tem som '
                            'parecido, mas é um adjetivo que significa ilícito ou ilegal.',
             'fonte': 'Parte 9, Exercício 5, item 12 (linhas 622 e 624)'}]},
 {'id': 'mod6-x-10',
  'title': 'Exercício 10: Vocabulário em passagem científica (meta de 6 min)',
  'level': 'C1–C2',
  'objective': 'Leia o parágrafo acadêmico e escolha o termo que preenche cada lacuna, de (1) a (10), com precisão '
               'conceitual. Tempo-alvo: 6 minutos.',
  'passage_html': '<p><strong>PASSAGE: Screen Time and Adolescent Sleep</strong></p><blockquote><p>"The paper reports '
                  'a strong (1)_____ between screen time and poor sleep in teenagers. But correlation is not (2)_____, '
                  'and the study does not identify the (3)_____ by which screens would disrupt sleep. A likely '
                  '(4)_____ variable is simply that anxious teenagers both sleep poorly and use phones more. Until an '
                  'independent team can (5)_____ the result under controlled conditions, the causal claim remains '
                  '(6)_____. The authors are right, however, that the broader trend is real and that its drivers are '
                  'largely (7)_____: a product of how devices and apps are designed. Any (8)_____ strategy should '
                  'therefore target design, not just individual willpower. The (9)_____ evidence we do have supports '
                  'modest limits; it does not support the alarmist framing that lets commentators (10)_____ from a '
                  'small effect to a generational crisis."</p></blockquote>',
  'items': [{'num': '10.1',
             'prompt': 'Lacuna (1): "The paper reports a strong ___(1) between screen time and poor sleep in '
                       'teenagers."',
             'options': {'A': 'mitigation', 'B': 'mechanism', 'C': 'correlation', 'D': 'replication'},
             'correct': 'C',
             'explanation': 'Quando um estudo observa que duas variáveis se movem juntas (tempo de tela e sono ruim) '
                            'sem ainda provar causa direta, ele relata uma <strong>correlation</strong> (correlação '
                            'estatística). A frase seguinte inclusive retoma esse termo para contrastá-lo com '
                            'causalidade.',
             'fonte': 'Parte 9, Exercício 6, item 1 (linhas 630 e 632)'},
            {'num': '10.2',
             'prompt': 'Lacuna (2): "But correlation is not ___(2), and the study does not identify..."',
             'options': {'A': 'causation', 'B': 'mitigation', 'C': 'symmetry', 'D': 'paradigm'},
             'correct': 'A',
             'explanation': 'O princípio metodológico clássico da ciência afirma que correlação não equivale a '
                            '<strong>causation</strong> (relação direta de causa e efeito). As opções (B), (C) e (D) '
                            'não estabelecem a oposição conceitual com <em>correlation</em>.',
             'fonte': 'Parte 9, Exercício 6, item 2 (linhas 630 e 632)'},
            {'num': '10.3',
             'prompt': 'Lacuna (3): "...and the study does not identify the ___(3) by which screens would disrupt '
                       'sleep."',
             'options': {'A': 'correlation', 'B': 'mitigation', 'C': 'hypothesis', 'D': 'mechanism'},
             'correct': 'D',
             'explanation': 'A estrutura <em>the ... by which screens would disrupt sleep</em> refere-se ao processo '
                            'subjacente que explica como um fator produz o outro: o <strong>mechanism</strong>. A '
                            'opção (C) <em>hypothesis</em> é uma suposição a ser testada, e não o processo físico ou '
                            'biológico em si.',
             'fonte': 'Parte 9, Exercício 6, item 3 (linhas 630 e 632)'},
            {'num': '10.4',
             'prompt': 'Lacuna (4): "A likely ___(4) variable is simply that anxious teenagers both sleep poorly and '
                       'use phones more."',
             'options': {'A': 'empirical', 'B': 'confounding', 'C': 'systemic', 'D': 'tenuous'},
             'correct': 'B',
             'explanation': 'Um fator oculto (como a ansiedade) que afeta ao mesmo tempo as duas variáveis estudadas e '
                            'cria uma falsa aparência de causa é chamado de <strong>confounding</strong> '
                            '(<em>confounding variable</em>). A opção (A) <em>empirical</em> significa baseado em '
                            'dados, o que não define esse tipo de viés.',
             'fonte': 'Parte 9, Exercício 6, item 4 (linhas 630 e 632)'},
            {'num': '10.5',
             'prompt': 'Lacuna (5): "Until an independent team can ___(5) the result under controlled conditions..."',
             'options': {'A': 'extrapolate', 'B': 'exacerbate', 'C': 'replicate', 'D': 'circumvent'},
             'correct': 'C',
             'explanation': 'Para validar uma descoberta, uma equipe independente precisa reproduzir o experimento e '
                            'chegar ao mesmo achado, ou seja, <strong>replicate</strong> (replicar o resultado). A '
                            'opção (A) <em>extrapolate</em> significa projetar dados além do que foi testado.',
             'fonte': 'Parte 9, Exercício 6, item 5 (linhas 630 e 632)'},
            {'num': '10.6',
             'prompt': 'Lacuna (6): "Until an independent team can replicate the result under controlled conditions, '
                       'the causal claim remains ___(6)."',
             'options': {'A': 'robust', 'B': 'empirical', 'C': 'systemic', 'D': 'tenuous'},
             'correct': 'D',
             'explanation': 'Enquanto o estudo não for replicado com controle de variáveis, a afirmação de causa e '
                            'efeito continua frágil e pouco convincente: <strong>tenuous</strong>. A alternativa (A) '
                            '<em>robust</em> diria que a afirmação já é sólida, contradizendo a ressalva anterior.',
             'fonte': 'Parte 9, Exercício 6, item 6 (linhas 630 e 632)'},
            {'num': '10.7',
             'prompt': 'Lacuna (7): "...the broader trend is real and that its drivers are largely ___(7): a product '
                       'of how devices and apps are designed."',
             'options': {'A': 'tenuous', 'B': 'systemic', 'C': 'empirical', 'D': 'marginal'},
             'correct': 'B',
             'explanation': 'Como a explicação após os dois-pontos atribui o problema à arquitetura dos aparelhos e '
                            'aplicativos (e não apenas a escolhas individuais), as causas são estruturais: '
                            '<strong>systemic</strong>. A opção (D) <em>marginal</em> diminuiria a importância dos '
                            'fatores citados.',
             'fonte': 'Parte 9, Exercício 6, item 7 (linhas 630 e 632)'},
            {'num': '10.8',
             'prompt': 'Lacuna (8): "Any ___(8) strategy should therefore target design, not just individual '
                       'willpower."',
             'options': {'A': 'mitigation', 'B': 'causation', 'C': 'correlation', 'D': 'proliferation'},
             'correct': 'A',
             'explanation': 'Uma estratégia voltada a reduzir os danos de um problema é uma estratégia de '
                            '<strong>mitigation</strong> (<em>mitigation strategy</em>). A opção (D) '
                            '<em>proliferation</em> significa expansão rápida, o oposto de conter o problema.',
             'fonte': 'Parte 9, Exercício 6, item 8 (linhas 630 e 632)'},
            {'num': '10.9',
             'prompt': 'Lacuna (9): "The ___(9) evidence we do have supports modest limits..."',
             'options': {'A': 'systemic', 'B': 'confounding', 'C': 'ostensible', 'D': 'empirical'},
             'correct': 'D',
             'explanation': 'Para se referir às evidências concretas obtidas por observação e dados (em contraste com '
                            'o alarmismo especulativo), usamos o adjetivo <strong>empirical</strong> (<em>empirical '
                            'evidence</em>). A opção (C) <em>ostensible</em> significaria evidência apenas aparente ou '
                            'suposta.',
             'fonte': 'Parte 9, Exercício 6, item 9 (linhas 630 e 632)'},
            {'num': '10.10',
             'prompt': 'Lacuna (10): "...it does not support the alarmist framing that lets commentators ___(10) from '
                       'a small effect to a generational crisis."',
             'options': {'A': 'replicate', 'B': 'corroborate', 'C': 'extrapolate', 'D': 'substantiate'},
             'correct': 'C',
             'explanation': 'A estrutura <em>from [um efeito pequeno] to [uma crise geracional]</em> descreve o salto '
                            'de projetar conclusões exageradas além do alcance real dos dados: '
                            '<strong>extrapolate</strong>. As opções (B) e (D) significam confirmar ou comprovar com '
                            'base sólida.',
             'fonte': 'Parte 9, Exercício 6, item 10 (linhas 630 e 632)'}]},
 {'id': 'mod6-x-11',
  'title': 'Exercício 11: Verbos de reporte e postura (meta de 4 min)',
  'level': 'C1–C2',
  'objective': 'Escolha o verbo de reporte que expressa com exatidão a postura indicada entre colchetes, conforme a '
               'tabela da Parte 6.3. Tempo-alvo: 4 minutos.',
  'passage_html': None,
  'items': [{'num': '11.1',
             'prompt': '"The author ___ that the sample was small." [postura: reconhece uma limitação do próprio '
                       'estudo]',
             'options': {'A': 'acknowledges', 'B': 'demonstrates', 'C': 'disputes', 'D': 'refutes'},
             'correct': 'A',
             'explanation': 'Quando o autor admite uma limitação ou ponto sensível do próprio trabalho, o verbo '
                            'adequado é <strong>acknowledges</strong> (reconhece). A opção (C) <em>disputes</em> '
                            'indicaria que ele está contestando o fato de a amostra ser pequena, e não admitindo.',
             'fonte': 'Parte 9, Exercício 7, item 1 (linhas 638 e 645)'},
            {'num': '11.2',
             'prompt': '"The lecturer ___, with new data, that the reading\'s model is wrong." [postura: prova com '
                       'evidências]',
             'options': {'A': 'claims', 'B': 'concedes', 'C': 'demonstrates', 'D': 'implies'},
             'correct': 'C',
             'explanation': 'Quando você endossa que o palestrante comprovou seu ponto com dados sólidos (<em>with new '
                            'data</em>), o verbo exato é <strong>demonstrates</strong>. A alternativa (A) '
                            '<em>claims</em> carregaria um tom de ceticismo, como se ele afirmasse sem provas.',
             'fonte': 'Parte 9, Exercício 7, item 2 (linhas 639 e 645)'},
            {'num': '11.3',
             'prompt': '"The reading ___ that the method is flawless, but offers no support." [postura: afirma sem '
                       'comprovação]',
             'options': {'A': 'demonstrates', 'B': 'claims', 'C': 'establishes', 'D': 'concedes'},
             'correct': 'B',
             'explanation': 'Para sinalizar que o texto faz uma alegação sem apresentar evidências suficientes '
                            '(<em>offers no support</em>), usamos <strong>claims</strong>. As opções (A) '
                            '<em>demonstrates</em> e (C) <em>establishes</em> indicariam que o texto provou a '
                            'afirmação.',
             'fonte': 'Parte 9, Exercício 7, item 3 (linhas 640 e 645)'},
            {'num': '11.4',
             'prompt': '"The professor ___ the reading\'s central assumption." [postura: contesta diretamente]',
             'options': {'A': 'notes', 'B': 'concedes', 'C': 'corroborates', 'D': 'disputes'},
             'correct': 'D',
             'explanation': 'Para mostrar que o professor questiona ou contesta a premissa central do texto, o verbo '
                            'transitivo adequado é <strong>disputes</strong>. A opção (C) <em>corroborates</em> tem o '
                            'sentido oposto (confirmar a premissa), e (A) <em>notes</em> é apenas neutro.',
             'fonte': 'Parte 9, Exercício 7, item 4 (linhas 641 e 645)'},
            {'num': '11.5',
             'prompt': '"The passage ___ that enrollment rose in 2024." [postura: registra um fato de forma neutra]',
             'options': {'A': 'notes', 'B': 'alleges', 'C': 'disputes', 'D': 'concedes'},
             'correct': 'A',
             'explanation': 'Ao relatar um dado objetivo (o aumento de matrículas em 2024) sem tom de dúvida ou '
                            'debate, a escolha neutra é <strong>notes</strong>. A opção (B) <em>alleges</em> sugeriria '
                            'uma acusação sem provas, inadequada para um registro factual simples.',
             'fonte': 'Parte 9, Exercício 7, item 5 (linhas 642 e 645)'},
            {'num': '11.6',
             'prompt': '"While she ___ the cost is real, she argues the benefit is larger." [postura: admite um ponto '
                       'contrário antes de rebater]',
             'options': {'A': 'refutes', 'B': 'concedes', 'C': 'disputes', 'D': 'claims'},
             'correct': 'B',
             'explanation': 'Na oração concessiva introduzida por <em>While</em>, a autora reconhece um argumento do '
                            'lado oposto antes de defender sua tese principal, o que pede <strong>concedes</strong> '
                            '(admite ou concede). As opções (A) <em>refutes</em> e (C) <em>disputes</em> negariam que '
                            'o custo é real.',
             'fonte': 'Parte 9, Exercício 7, item 6 (linhas 643 e 645)'}]},
 {'id': 'mod6-x-12',
  'title': 'Exercício 12: Caça ao erro de vocabulário (meta de 5 min)',
  'level': 'C1–C2',
  'objective': 'Cada frase original contém um deslize de vocabulário (falso cognato, colocação, forma da palavra ou '
               'nuance). Escolha a opção que corrige a frase mantendo o sentido pretendido. Tempo-alvo: 5 minutos.',
  'passage_html': None,
  'items': [{'num': '12.1',
             'prompt': 'Corrija o falso cognato na frase: "Eventually, the study has three limitations that the '
                       'authors admit."',
             'options': {'A': 'Actually, the study pretends three limitations that the authors admit.',
                         'B': 'Eventual, the study has three limitations that the authors admit.',
                         'C': 'The study has three limitations that the authors admit.',
                         'D': 'Eventually, the study has three limitations that the authors pretend.'},
             'correct': 'C',
             'explanation': 'Em inglês, <em>eventually</em> significa no fim ou depois de muito tempo, e não '
                            'eventualmente. Como a frase apenas apresenta um fato sobre o estudo, a correção mais '
                            'limpa é cortar o falso cognato e escrever <strong>The study has three limitations that '
                            'the authors admit</strong>. As opções (A) e (D) introduzem o falso cognato '
                            '<em>pretend</em> (fingir).',
             'fonte': 'Parte 9, Exercício 9, item 1 (linhas 659 e 670)'},
            {'num': '12.2',
             'prompt': 'Corrija o deslize de uso formal na frase: "The data are comprised of responses from 400 '
                       'students."',
             'options': {'A': 'The data comprise responses from 400 students.',
                         'B': 'The data comprise of responses from 400 students.',
                         'C': 'The data constitutes of responses from 400 students.',
                         'D': 'The data are composed by responses from 400 students.'},
             'correct': 'A',
             'explanation': 'No registro formal, evitamos <em>are comprised of</em> e usamos o verbo ativo sem '
                            'preposição em <strong>The data comprise responses</strong> (ou a passiva <em>are composed '
                            'of</em>). A opção (B) mantém a preposição indevida <em>of</em> após <em>comprise</em>, e '
                            '(D) usa <em>by</em> em vez de <em>of</em> com <em>composed</em>.',
             'fonte': 'Parte 9, Exercício 9, item 2 (linhas 660 e 671)'},
            {'num': '12.3',
             'prompt': 'Corrija a estrutura após a preposição na frase: "This raises a concern about if the method is '
                       'valid."',
             'options': {'A': 'This poses a concern about if the method is valid.',
                         'B': 'This raises a concern about that the method is valid.',
                         'C': 'This conducts a concern about whether the method is valid.',
                         'D': 'This raises a concern about whether the method is valid.'},
             'correct': 'D',
             'explanation': 'Logo após uma preposição (como <em>about</em>), o inglês formal exige <strong>about '
                            'whether</strong> para introduzir uma dúvida indireta, e nunca <em>about if</em>. A '
                            'alternativa (C) acerta o <em>whether</em>, mas quebra a colocação ao trocar <em>raises a '
                            'concern</em> por <em>conducts a concern</em>.',
             'fonte': 'Parte 9, Exercício 9, item 3 (linhas 661 e 672)'},
            {'num': '12.4',
             'prompt': 'Corrija o falso cognato no verbo de reporte em: "The professor pretends that the effect is '
                       'purely cultural."',
             'options': {'A': 'The professor realizes that the effect is purely cultural.',
                         'B': 'The professor argues that the effect is purely cultural.',
                         'C': 'The professor intends that the effect is purely cultural.',
                         'D': 'The professor sensitizes that the effect is purely cultural.'},
             'correct': 'B',
             'explanation': 'O verbo <em>pretend</em> é um falso amigo que significa fingir. Para relatar a tese '
                            'defendida pelo professor em aula, trocamos por <strong>argues</strong> (ou '
                            '<em>claims</em>). A opção (C) <em>intends</em> significa ter a intenção de fazer algo e '
                            'não introduz uma tese teórica dessa forma.',
             'fonte': 'Parte 9, Exercício 9, item 4 (linhas 662 e 673)'},
            {'num': '12.5',
             'prompt': 'Corrija a regência verbal na frase: "The two results corroborate to each other."',
             'options': {'A': 'The two results corroborate with each other.',
                         'B': 'The two results corroborate on each other.',
                         'C': 'The two results corroborate each other.',
                         'D': 'The two results corroborate for each other.'},
             'correct': 'C',
             'explanation': 'O verbo <em>corroborate</em> é transitivo direto e não aceita preposição antes do objeto, '
                            'por isso a forma correta é <strong>corroborate each other</strong>. As alternativas (A), '
                            '(B) e (D) mantêm preposições indevidas (<em>with</em>, <em>on</em>, <em>for</em>).',
             'fonte': 'Parte 9, Exercício 9, item 5 (linhas 663 e 674)'},
            {'num': '12.6',
             'prompt': 'Corrija a escolha da palavra na frase: "The policy had a big affect on rural clinics."',
             'options': {'A': 'The policy had a big effect on rural clinics.',
                         'B': 'The policy had a big affecting on rural clinics.',
                         'C': 'The policy made a big affect on rural clinics.',
                         'D': 'The policy had a big effective on rural clinics.'},
             'correct': 'A',
             'explanation': 'Depois de <em>had a big...</em>, a função sintática é de substantivo, exigindo '
                            '<strong>effect</strong> (<em>had a big effect on</em>). Na frase original, '
                            '<em>affect</em> foi usado por engano no lugar do substantivo.',
             'fonte': 'Parte 9, Exercício 9, item 6 (linhas 664 e 675)'},
            {'num': '12.7',
             'prompt': 'Corrija a forma da palavra no final da frase: "The evidence for this connection is very strong '
                       'and robusts."',
             'options': {'A': 'The evidence for this connection is very strong and robustness.',
                         'B': 'The evidence for this connection is very strong and robustly.',
                         'C': 'The evidence for this connection are very strong and robust.',
                         'D': 'The evidence for this connection is very strong and robust.'},
             'correct': 'D',
             'explanation': 'Em inglês, adjetivos nunca recebem <em>-s</em> de plural ou de terceira pessoa, mantendo '
                            'a forma invariável <strong>robust</strong> ao lado de <em>strong</em>. A opção (C) '
                            'corrige <em>robust</em>, mas erra ao usar o verbo plural <em>are</em> com o substantivo '
                            'incontável <em>evidence</em>.',
             'fonte': 'Parte 9, Exercício 9, item 7 (linhas 665 e 676)'},
            {'num': '12.8',
             'prompt': 'Corrija a colocação na frase: "The lecture makes an emphasis on the second mechanism."',
             'options': {'A': 'The lecture does an emphasis on the second mechanism.',
                         'B': 'The lecture emphasizes on the second mechanism.',
                         'C': 'The lecture places emphasis on the second mechanism.',
                         'D': 'The lecture conducts emphasis on the second mechanism.'},
             'correct': 'C',
             'explanation': 'O substantivo <em>emphasis</em> não forma colocação com o verbo <em>make</em>; o natural '
                            'é usar <strong>places emphasis on</strong> (ou diretamente o verbo transitivo '
                            '<em>emphasizes the second mechanism</em>, sem preposição). Repare que a opção (B) erra ao '
                            'colocar <em>on</em> depois do verbo <em>emphasizes</em>.',
             'fonte': 'Parte 9, Exercício 9, item 8 (linhas 666 e 677)'}]}]


# >>> EXERCÍCIOS NOVOS DO M1 E DO M2 (gerado por itoefl-gerencia/m1m2/aplicar_revisao.py)
# Rascunho do Gemini revisado pelo Claude em 2026-11-16 (itoefl-gerencia/m1m2/REVISAO-claude.md).
# Entram nos grupos existentes do M1 (B e C) e do M2 (A a D), que viraram rodadas sorteadas.
# Para mudar uma questão, editar aqui mesmo e rodar bank/tools/migrate.py.
MOD1_NOVOS_B = [{'id': 'mod1-bn1',
  'title': 'Exercício B6: placa ou aviso (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.',
  'passage_html': '<p><strong>TEXT: Sign in a dormitory laundry room</strong></p>\n'
                  '<blockquote><p><strong>NORTH HALL LAUNDRY ROOM: RULES FOR RESIDENTS</strong></p>\n'
                  '<p>• Open daily from 6:00 a.m. to 11:00 p.m. The door locks automatically at 11:00 p.m.<br>\n'
                  '• All machines use your student ID card. Cash and coins are not accepted.<br>\n'
                  '• Please remove your clothes within 30 minutes after your cycle ends so others can use the '
                  'machines.<br>\n'
                  '• Forgotten items are placed in the blue basket by the door and donated every Friday '
                  'afternoon.</p></blockquote>',
  'items': [{'num': 'B6.1',
             'prompt': 'How do students pay to use the washing machines?',
             'options': {'A': 'With coins at the machine',
                         'B': 'With cash at the front desk',
                         'C': 'With their student ID card',
                         'D': 'With a mobile banking app'},
             'correct': 'C',
             'explanation': 'O aviso informa diretamente que <em>All machines use your student ID card</em>, '
                            'confirmando a opção (C) como <strong>pagamento pelo cartão de estudante</strong>. A '
                            'alternativa (A) é uma armadilha comum porque lavanderias costumam aceitar moedas, mas o '
                            'texto avisa que <em>Cash and coins are not accepted</em>.'},
            {'num': 'B6.2',
             'prompt': 'On Friday afternoon, what happens to forgotten items in the blue basket?',
             'options': {'A': 'They are given away as donations',
                         'B': 'They are washed again by the staff',
                         'C': 'They are locked inside the machines',
                         'D': "They are sent to the resident's room"},
             'correct': 'A',
             'explanation': 'A última linha explica que os itens esquecidos vão para o cesto azul e são '
                            '<strong>doados na sexta-feira à tarde</strong> (<em>donated every Friday '
                            'afternoon</em>), o que corresponde a <em>given away as donations</em> em (A). A opção '
                            '(C) confunde o trancamento automático da porta às 23h com o destino das roupas.'}]},
 {'id': 'mod1-bn2',
  'title': 'Exercício B7: cardápio (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.',
  'passage_html': '<p><strong>TEXT: Student Union Coffee Cart menu</strong></p>\n'
                  '<blockquote><p><strong>HOT AND ICED DRINKS</strong> (oat or almond milk +$0.50; bring your own '
                  'mug for $0.50 off)</p>\n'
                  '<p>• <strong>House Coffee</strong> — medium roast, hot or iced — $3.00<br>\n'
                  '• <strong>Café Latte</strong> — espresso with steamed milk — $4.50<br>\n'
                  '• <strong>Matcha Green Tea</strong> — sweetened or unsweetened — $4.00</p>\n'
                  '<p><strong>MORNING PASTRIES</strong> — $3.50 each, or $2.00 when ordered with any drink before '
                  '10:00 a.m.<br>\n'
                  '• <strong>Blueberry Muffin</strong> (vegetarian) • <strong>Banana Bread</strong> (contains '
                  'walnuts) • <strong>Cinnamon Roll</strong> (vegan)</p></blockquote>',
  'items': [{'num': 'B7.1',
             'prompt': 'A student orders a House Coffee and a Cinnamon Roll at 9:15 a.m. without bringing a mug. '
                       'What is the total price?',
             'options': {'A': '$3.50', 'B': '$4.50', 'C': '$6.50', 'D': '$5.00'},
             'correct': 'D',
             'explanation': 'O café custa $3.00 e, como o pedido é feito antes das 10h junto com uma bebida, o doce '
                            'sai pelo <strong>preço promocional de $2.00</strong>, somando $5.00 na opção (D). A '
                            'alternativa (C) é a armadilha mais próxima porque soma o valor cheio do doce ($3.50) e '
                            'esquece o desconto da manhã.'},
            {'num': 'B7.2',
             'prompt': 'Which item should a customer with a nut allergy avoid?',
             'options': {'A': 'The Blueberry Muffin',
                         'B': 'The Banana Bread',
                         'C': 'The Cinnamon Roll',
                         'D': 'The Matcha Green Tea'},
             'correct': 'B',
             'explanation': 'No fim do cardápio, o aviso ao lado de <em>Banana Bread</em> indica <em>contains '
                            'walnuts</em> (nozes), apontando a opção (B) como <strong>item com oleaginosas</strong>. '
                            'A alternativa (C) traz apenas a marcação <em>vegan</em>, sem menção a nozes ou '
                            'castanhas.'}]},
 {'id': 'mod1-bn3',
  'title': 'Exercício B8: anúncio de campus (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.',
  'passage_html': '<p><strong>TEXT: Notice on a residence hall bulletin board</strong></p>\n'
                  '<blockquote><p><strong>BASEMENT BIKE ROOM CLEANUP — NOVEMBER 18</strong></p>\n'
                  '<p>Next Monday, Campus Security will clear old bicycles from the basement storage room. If you '
                  'keep a bike downstairs, please pick up a free yellow tag at the front desk and attach it to your '
                  'handlebars by Sunday at 8:00 p.m.</p>\n'
                  '<p>Any bike without a yellow tag on Monday morning will be moved to the main storage shed behind '
                  'the gym. You can still claim it there during office hours by showing your student '
                  'ID.</p></blockquote>',
  'items': [{'num': 'B8.1',
             'prompt': 'What is the main purpose of the notice?',
             'options': {'A': 'To tell residents how to keep their bikes from being moved',
                         'B': 'To announce that the basement bike room is closing forever',
                         'C': 'To sell old bicycles to students at a low price',
                         'D': 'To ask students to park their bikes behind the gym'},
             'correct': 'A',
             'explanation': 'O objetivo do aviso é orientar os moradores a colocarem a etiqueta amarela para '
                            '<strong>manter a bicicleta no subsolo</strong>, como resume a opção (A). A alternativa '
                            '(B) exagera ao dizer que a sala fechará para sempre, quando haverá apenas uma limpeza '
                            '(<em>cleanup</em>).'},
            {'num': 'B8.2',
             'prompt': 'What must a resident do by Sunday at 8:00 p.m.?',
             'options': {'A': 'Pay a storage fee at the front desk',
                         'B': 'Move their bicycle to the main gym',
                         'C': 'Put a yellow tag on their bicycle',
                         'D': 'Show their student ID to security'},
             'correct': 'C',
             'explanation': 'O primeiro parágrafo pede que o morador pegue a etiqueta gratuita na recepção e faça a '
                            '<strong>identificação no guidão até domingo às 20h</strong> (<em>attach it to your '
                            'handlebars by Sunday at 8:00 p.m.</em>), confirmando (C). A opção (A) inventa uma taxa, '
                            'mas o texto diz <em>free yellow tag</em>.'},
            {'num': 'B8.3',
             'prompt': 'What will happen to a bicycle that has no tag on Monday morning?',
             'options': {'A': 'It will be thrown away immediately',
                         'B': 'It will be locked in the front office',
                         'C': 'It will be given to another student',
                         'D': 'It will be taken to a shed behind the gym'},
             'correct': 'D',
             'explanation': 'O segundo parágrafo explica que a bicicleta sem etiqueta será <strong>levada ao galpão '
                            'atrás do ginásio</strong> (<em>moved to the main storage shed behind the gym</em>), '
                            'onde o dono ainda pode recuperá-la, validando (D). A opção (A) erra porque nenhuma '
                            'bicicleta é jogada fora na segunda-feira.'}]},
 {'id': 'mod1-bn4',
  'title': 'Exercício B9: horário ou tabela (meta de 2 min)',
  'level': 'B1–B2',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 2 minutos.',
  'passage_html': '<p><strong>TEXT: Campus Writing Center schedule</strong></p>\n'
                  '<blockquote><p><strong>WRITING CENTER HOURS (FALL SEMESTER)</strong></p>\n'
                  '<p>• <strong>Monday–Thursday, 9:00 a.m.–1:00 p.m.:</strong> 45-minute appointments only (book '
                  'online).<br>\n'
                  '• <strong>Monday–Thursday, 1:00 p.m.–5:00 p.m.:</strong> 20-minute drop-in sessions (no booking '
                  'needed).<br>\n'
                  '• <strong>Friday, 10:00 a.m.–2:00 p.m.:</strong> Online consultations only.</p>\n'
                  '<p><em>Note: During final exam week, drop-in hours are suspended. All in-person and online '
                  'sessions require an appointment booked at least 24 hours in advance, with a limit of one session '
                  'per student.</em></p></blockquote>',
  'items': [{'num': 'B9.1',
             'prompt': 'During a regular week, a student who wants help in person without an appointment should '
                       'visit on:',
             'options': {'A': 'Tuesday at 10:30 a.m.',
                         'B': 'Wednesday at 2:30 p.m.',
                         'C': 'Friday at 11:00 a.m.',
                         'D': 'Thursday at 9:30 a.m.'},
             'correct': 'B',
             'explanation': 'O atendimento presencial sem hora marcada (<em>drop-in sessions</em>) funciona de '
                            'segunda a quinta, das 13h às 17h, faixa em que se encaixa a <strong>quarta-feira às '
                            '14h30</strong> na opção (B). As alternativas (A) e (D) caem no turno da manhã, que '
                            'exige agendamento, e a (C) é na sexta, quando o atendimento é só on-line.'},
            {'num': 'B9.2',
             'prompt': 'How does the schedule change during final exam week?',
             'options': {'A': 'Every session must be reserved a day ahead',
                         'B': 'Students may attend up to two drop-in sessions',
                         'C': 'The center closes completely on Fridays',
                         'D': 'Appointments are offered only in the morning'},
             'correct': 'A',
             'explanation': 'A nota de rodapé avisa que, na semana de provas finais, o atendimento sem hora marcada '
                            'é suspenso e todas as sessões exigem <strong>reserva com 24 horas de '
                            'antecedência</strong> (<em>booked at least 24 hours in advance</em>), como diz (A). '
                            'Quem marca (B) deixou passar que os horários de <em>drop-in</em> ficam suspensos nessa '
                            'semana.'}]},
 {'id': 'mod1-bn5',
  'title': 'Exercício B10: e-mail formal (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.',
  'passage_html': '<p><strong>TEXT: Email from the University Housing Office</strong></p>\n'
                  '<blockquote><p><strong>Subject: Winter Break Residence Hall Closing</strong></p>\n'
                  '<p>Dear Residents,</p>\n'
                  '<p>All campus residence halls will close for winter break on Friday, December 20, at 6:00 p.m. '
                  'and reopen on Saturday, January 11, at 9:00 a.m.</p>\n'
                  '<p>International students and varsity athletes who need to remain on campus during the break may '
                  'apply for temporary housing in Maple Court. This accommodation is free of charge if you submit '
                  'the online form by December 6. Applications received after December 6 will still be accepted '
                  'until December 13, but a $35 late processing fee will apply.</p>\n'
                  '<p>Before leaving on December 20, all residents — including those moving temporarily to Maple '
                  'Court — must unplug mini-fridges and lamps in their regular rooms.</p>\n'
                  '<p>Sincerely,<br>Office of Residential Life</p></blockquote>',
  'items': [{'num': 'B10.1',
             'prompt': 'What is required of an international student who applies for winter break housing on '
                       'December 9?',
             'options': {'A': 'Finding housing off campus for the whole break',
                         'B': 'Moving into Maple Court before December 13',
                         'C': 'Paying a $35 fee for applying after December 6',
                         'D': 'Getting a signature from a varsity sports coach'},
             'correct': 'C',
             'explanation': 'A inscrição até 6 de dezembro é gratuita, mas pedidos enviados entre 6 e 13 de dezembro '
                            'pagam <strong>taxa de processamento de $35</strong> (<em>a $35 late processing fee will '
                            'apply</em>), o que torna (C) correta. A opção (A) ignora que o formulário ainda é '
                            'aceito até o dia 13.'},
            {'num': 'B10.2',
             'prompt': 'According to the email, who must unplug appliances in their regular rooms before December '
                       '20?',
             'options': {'A': 'Students who are leaving campus for the break',
                         'B': 'Students who are moving to Maple Court',
                         'C': 'Students who missed the December 6 deadline',
                         'D': 'All residents, whether or not they stay on campus'},
             'correct': 'D',
             'explanation': 'O último parágrafo destaca que "all residents — including those moving temporarily to '
                            'Maple Court — must unplug mini-fridges and lamps", ou seja, <strong>todos os moradores '
                            'sem exceção</strong>, confirmando (D). A alternativa (A) é a armadilha clássica de quem '
                            'acha que a regra só vale para quem viaja.'},
            {'num': 'B10.3',
             'prompt': 'When can students return to their regular residence hall rooms?',
             'options': {'A': 'On December 13 at 6:00 p.m.',
                         'B': 'On January 11 at 9:00 a.m.',
                         'C': 'On December 20 at 6:00 p.m.',
                         'D': 'On January 6 at 9:00 a.m.'},
             'correct': 'B',
             'explanation': 'O primeiro parágrafo informa que os prédios reabrem no <strong>sábado, 11 de janeiro, '
                            'às 9h</strong> (<em>reopen on Saturday, January 11, at 9:00 a.m.</em>), exatamente como '
                            'em (B). A opção (C) traz a data em que os alojamentos fecham, e não a de reabertura.'}]},
 {'id': 'mod1-bn6',
  'title': 'Exercício B11: post de rede social (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.',
  'passage_html': '<p><strong>TEXT: A social media post from a campus club</strong></p>\n'
                  '<blockquote><p>🥾 <strong>Pinecrest Outdoor Club</strong> · Posted 4 hours ago</p>\n'
                  "<p>Quick update about tomorrow's Saturday hike! With heavy rain in the forecast for tonight, the "
                  'river crossing on the Lower Canyon Trail will almost certainly be flooded. Instead of canceling '
                  "the trip, we're switching to the East Crest Trail, which stays on higher ground and gives us "
                  'great views of the valley.</p>\n'
                  '<p>Our departure time from the Student Union parking lot is still 7:30 a.m. sharp, but because '
                  "the East Crest route is about two miles shorter, we'll be back on campus around 2:00 p.m. instead "
                  "of 4:00 p.m. Waterproof hiking boots are required for the muddy sections — if you don't own a "
                  'pair, stop by the club gear shed before 5:00 p.m. today to borrow a pair for '
                  'free!</p></blockquote>',
  'items': [{'num': 'B11.1',
             'prompt': 'What is the main purpose of this social media post?',
             'options': {'A': 'To inform club members about a change of trail and return time',
                         'B': 'To cancel a weekend hiking trip because of dangerous weather',
                         'C': 'To advertise a sale on waterproof boots at the club gear shed',
                         'D': 'To ask students to vote on two possible routes for Saturday'},
             'correct': 'A',
             'explanation': 'A publicação avisa que o passeio foi mantido, mas com <strong>mudança de trilha e de '
                            'horário de volta</strong> por causa da chuva, como resume (A). A opção (B) cai na '
                            'armadilha da palavra <em>canceling</em>, embora o texto diga explicitamente <em>Instead '
                            'of canceling the trip</em>.'},
            {'num': 'B11.2',
             'prompt': 'Why will the group return to campus earlier than originally planned?',
             'options': {'A': 'They are leaving the parking lot two hours earlier',
                         'B': 'The replacement trail is shorter than the original one',
                         'C': 'Another storm is expected at 2:00 p.m. on Saturday',
                         'D': 'The club van has to be returned by mid-afternoon'},
             'correct': 'B',
             'explanation': 'O segundo parágrafo explica a volta mais cedo ao dizer que <em>because the East Crest '
                            "route is about two miles shorter, we'll be back on campus around 2:00 p.m.</em>, ou "
                            'seja, <strong>o novo percurso é mais curto</strong>, confirmando (B). A opção (A) '
                            'contradiz o trecho que mantém a saída às 7h30.'},
            {'num': 'B11.3',
             'prompt': 'What should a participant without waterproof boots do?',
             'options': {'A': 'Rent a pair at the trailhead on Saturday morning',
                         'B': 'Wear regular running shoes and stay on higher ground',
                         'C': 'Borrow a pair from the club shed by 5:00 p.m. today',
                         'D': 'Wait until the next hike on the Lower Canyon Trail'},
             'correct': 'C',
             'explanation': 'A frase final orienta quem não tem botas impermeáveis a <strong>pegar um par emprestado '
                            'gratuitamente no galpão do clube</strong> até as 17h de hoje (<em>stop by the club gear '
                            'shed before 5:00 p.m. today to borrow a pair for free</em>), como está em (C). A '
                            'alternativa (A) inventa um aluguel no início da trilha.'}]},
 {'id': 'mod1-bn7',
  'title': 'Exercício B12: instruções de laboratório (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.',
  'passage_html': '<p><strong>TEXT: Guidelines at the Engineering Makerspace</strong></p>\n'
                  '<blockquote><p><strong>3D PRINTING QUEUE — UNDERGRADUATE GUIDELINES</strong></p>\n'
                  '<p>1. <strong>Safety Orientation:</strong> Before submitting your first print job, you must pass '
                  'the 20-minute online safety quiz on the student portal with a score of 100%.</p>\n'
                  '<p>2. <strong>Scheduling:</strong> Upload your file to the lab queue. Print jobs estimated at '
                  'under 3 hours run during daytime hours (9:00 a.m.–6:00 p.m.). Any job requiring 3 hours or more '
                  'is automatically scheduled for the overnight batch and will be ready the next morning.</p>\n'
                  '<p>3. <strong>Cost and Pickup:</strong> Filament is billed at $0.08 per gram. Each student '
                  'receives a $10.00 credit per semester for required coursework; personal projects do not qualify '
                  'for this credit. Completed prints not picked up within 5 business days are '
                  'recycled.</p></blockquote>',
  'items': [{'num': 'B12.1',
             'prompt': 'A student uploads a print job at 11:00 a.m. that the system estimates will take 4 hours. '
                       'When will it be printed?',
             'options': {'A': 'Immediately, finishing around 3:00 p.m. that afternoon',
                         'B': 'Only after the student retakes the online safety quiz',
                         'C': 'After 5 business days, once shorter jobs are finished',
                         'D': 'Overnight, becoming available the following morning'},
             'correct': 'D',
             'explanation': 'A regra 2 estabelece que qualquer impressão de 3 horas ou mais entra no <strong>lote '
                            'noturno para entrega na manhã seguinte</strong> (<em>automatically scheduled for the '
                            'overnight batch and will be ready the next morning</em>), validando (D). A opção (A) '
                            'aplica a regra de projetos com menos de 3 horas.'},
            {'num': 'B12.2',
             'prompt': 'When can a student use the $10.00 semester credit?',
             'options': {'A': 'When printing an item for an assigned university course',
                         'B': 'When printing a personal gift that weighs under 100 grams',
                         'C': 'When picking up a completed print within 24 hours',
                         'D': 'When volunteering to recycle unclaimed prints in the lab'},
             'correct': 'A',
             'explanation': 'O item 3 especifica que o crédito de $10.00 por semestre vale para <strong>trabalhos '
                            'exigidos em disciplinas</strong> (<em>for required coursework</em>) e exclui projetos '
                            'pessoais, confirmando (A). A alternativa (B) é uma armadilha direta porque o texto diz '
                            '<em>personal projects do not qualify</em>.'},
            {'num': 'B12.3',
             'prompt': 'What happens to a finished print that is left in the Makerspace for two weeks?',
             'options': {'A': "It is mailed to the student's campus address",
                         'B': 'It is kept at the desk for a storage fee',
                         'C': 'It is sent to be recycled by the lab',
                         'D': 'It is displayed in the engineering showcase'},
             'correct': 'C',
             'explanation': 'A última frase informa que peças prontas não retiradas em até 5 dias úteis são '
                            '<strong>enviadas para reciclagem</strong> (<em>Completed prints not picked up within 5 '
                            'business days are recycled</em>), o que leva à opção (C). As demais alternativas trazem '
                            'procedimentos que não existem no aviso.'}]},
 {'id': 'mod1-bn8',
  'title': 'Exercício B13: e-mail formal (meta de 3 min)',
  'level': 'B2–C1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.',
  'passage_html': '<p><strong>TEXT: Email from the Undergraduate Research Grant Committee</strong></p>\n'
                  '<blockquote><p><strong>Subject: Conditional Approval — Summer Fieldwork Grant '
                  '(#UG-409)</strong></p>\n'
                  '<p>Dear Lucas,</p>\n'
                  '<p>The committee was impressed by your proposal to survey native pollinators in urban community '
                  'gardens and is pleased to offer conditional funding of $2,400. Before the funds can be disbursed, '
                  'however, two revisions are required.</p>\n'
                  '<p>First, because three of your proposed study sites lie on municipal park land, you must attach '
                  'either a city research permit or a signed note from your faculty advisor confirming that the '
                  "biology department's blanket permit covers your fieldwork. Second, your budget allocates $600 for "
                  'a digital camera; under university policy, grant funds may purchase equipment only if it remains '
                  'departmental property after the project concludes.</p>\n'
                  '<p>Please upload your revised packet by April 14 so we can release the award.</p>\n'
                  '<p>Sincerely,<br>Prof. Elena Vance, Committee Chair</p></blockquote>',
  'items': [{'num': 'B13.1',
             'prompt': 'Why is the committee withholding the $2,400 grant for now?',
             'options': {'A': 'Lucas submitted his initial research proposal after the deadline',
                         'B': 'Two permit and budget issues must be resolved before payment',
                         'C': 'The biology department has run out of funding for summer fieldwork',
                         'D': 'The committee wants Lucas to choose sites outside the city'},
             'correct': 'B',
             'explanation': 'A aprovação é condicional (<em>conditional funding</em>) e o pagamento depende de '
                            '<strong>duas revisões de licença e orçamento</strong> (<em>Before the funds can be '
                            'disbursed, however, two revisions are required</em>), como aponta (B). A opção (D) '
                            'distorce o texto, que pede apenas a licença para os parques municipais, e não a troca '
                            'de local.'},
            {'num': 'B13.2',
             'prompt': "How can Lucas satisfy the committee's first requirement without applying for a new city "
                       'permit?',
             'options': {'A': 'By surveying fewer community gardens in the city',
                         'B': 'By agreeing not to collect any insect specimens',
                         'C': 'By moving his fieldwork from summer to fall',
                         'D': 'By having his advisor confirm the department permit applies'},
             'correct': 'D',
             'explanation': 'O segundo parágrafo oferece dois caminhos: anexar uma licença municipal ou apresentar '
                            '<strong>declaração do orientador confirmando a cobertura da licença do '
                            'departamento</strong> (<em>a signed note from your faculty advisor confirming that the '
                            "biology department's blanket permit covers your fieldwork</em>), o que valida (D). A "
                            'opção (A) não resolve a exigência para os locais remanescentes.'},
            {'num': 'B13.3',
             'prompt': "What does university policy state about the $600 camera listed in Lucas's budget?",
             'options': {'A': 'It is allowed only if the department keeps it afterward',
                         'B': 'It must be rented from the media center instead',
                         'C': 'It costs more than the equipment price limit',
                         'D': 'It is approved because photos are essential'},
             'correct': 'A',
             'explanation': 'Pela regra da universidade, a verba da bolsa só pode comprar equipamentos que '
                            '<strong>permaneçam como patrimônio do departamento</strong> após o término do projeto '
                            '(<em>only if it remains departmental property after the project concludes</em>), '
                            'confirmando (A). A alternativa (C) inventa um teto de preço que o e-mail não '
                            'menciona.'}]},
 {'id': 'mod1-bn9',
  'title': 'Exercício B14: anúncio de campus (meta de 3 min)',
  'level': 'B2–C1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 3 minutos.',
  'passage_html': '<p><strong>TEXT: Notice from the University Health Center</strong></p>\n'
                  '<blockquote><p><strong>IMMUNIZATION COMPLIANCE AND SPRING REGISTRATION HOLDS</strong></p>\n'
                  '<p>While incoming first-year undergraduates must submit complete immunization records prior to '
                  'dorm move-in, transfer and graduate students are granted a 30-day grace period from the first day '
                  'of fall classes to upload missing documentation. Our records show that roughly 300 students in '
                  'this latter group still have provisional status.</p>\n'
                  '<p>Any student whose file remains incomplete after October 25 will have an administrative hold '
                  'placed on their account. This hold does not affect current fall courses, dining plans, or library '
                  'privileges, but it will block spring course registration until the Health Center verifies the '
                  'uploaded records — a review that takes up to three business days. Students awaiting the second '
                  'dose of a two-part vaccine series may request a temporary medical extension at Window '
                  '3.</p></blockquote>',
  'items': [{'num': 'B14.1',
             'prompt': 'Which group of students is the primary target of this warning?',
             'options': {'A': 'Incoming first-year students who have not yet moved into their dorms',
                         'B': 'All undergraduates who plan to use the campus health clinic this fall',
                         'C': 'Transfer and graduate students who have not finished submitting vaccine records',
                         'D': 'Faculty members who need to verify class rosters for the spring term'},
             'correct': 'C',
             'explanation': 'O primeiro parágrafo contrasta os calouros com os alunos de transferência e de '
                            'pós-graduação e foca nos cerca de 300 estudantes desse segundo grupo (<em>this latter '
                            'group</em>) que ainda têm <strong>documentação de vacina pendente</strong>, como diz '
                            '(C). A opção (A) confunde a referência de <em>latter group</em> (o último citado) com o '
                            'primeiro grupo mencionado na frase.'},
            {'num': 'B14.2',
             'prompt': 'What is the immediate consequence of having an administrative hold placed on an account '
                       'after October 25?',
             'options': {'A': 'The student is dropped from their current fall semester classes',
                         'B': 'The student is prevented from enrolling in spring semester courses',
                         'C': 'The student loses borrowing privileges at the university library',
                         'D': 'The student is charged a daily fine until the records are verified'},
             'correct': 'B',
             'explanation': 'O segundo parágrafo esclarece que o bloqueio não afeta as aulas atuais nem a '
                            'biblioteca, mas <strong>impede a matrícula nas disciplinas da primavera</strong> '
                            '(<em>it will block spring course registration</em>), tornando (B) correta. As '
                            'alternativas (A) e (C) citam exatamente o que o aviso diz que não será afetado '
                            '(<em>does not affect</em>).'},
            {'num': 'B14.3',
             'prompt': 'What can be inferred about a student who uploads missing records on the morning of spring '
                       'registration?',
             'options': {'A': 'Their hold will be removed by the portal right away',
                         'B': 'They must register in person at Window 3',
                         'C': 'Their records will be rejected as too late',
                         'D': 'They may wait up to three days to register'},
             'correct': 'D',
             'explanation': 'Como o bloqueio só sai depois que o centro de saúde confere os documentos e essa '
                            'análise leva <strong>até três dias úteis</strong> (<em>a review that takes up to three '
                            'business days</em>), enviar os papéis na manhã da matrícula pode atrasar a inscrição, '
                            'como infere (D). A opção (A) ignora esse prazo de conferência.'}]},
 {'id': 'mod1-bn10',
  'title': 'Exercício B15: aviso de biblioteca (meta de 4 min)',
  'level': 'C1',
  'objective': 'Leia o texto e responda às questões de compreensão. Tempo-alvo: 4 minutos.',
  'passage_html': '<p><strong>TEXT: Policy notice from the University Archives and Special Collections</strong></p>\n'
                  '<blockquote><p><strong>RESEARCHER ACCESS AND REPRODUCTION GUIDELINES</strong></p>\n'
                  "<p>Unlike the main library's general holdings, materials housed in Special Collections are "
                  'non-circulating and may be consulted only in the Reading Room by appointment. Requests for '
                  'archival boxes should be submitted through the online catalog at least two business days prior to '
                  'your visit, as nearly half of our holdings are kept in a climate-controlled off-site facility '
                  'from which deliveries arrive only on Tuesday and Thursday mornings.</p>\n'
                  '<p>Researchers are welcome to take reference photographs using handheld devices with the flash '
                  'turned off. However, high-resolution digital scans intended for publication or public display '
                  'require a formal reproduction request and written permission from the copyright holder, unless '
                  'the work has entered the public domain. To protect fragile manuscripts, fountain pens, '
                  'highlighters, and coats are prohibited at the reading tables; lockers and pencils are supplied in '
                  'the entry hall.</p></blockquote>',
  'items': [{'num': 'B15.1',
             'prompt': 'Why does the archive ask researchers to request materials at least two business days in '
                       'advance?',
             'options': {'A': 'Many items are stored off campus and are transported only twice a week',
                         'B': 'Archivists must inspect every manuscript for damage before each appointment',
                         'C': 'The Reading Room has seating for only a small number of visitors each day',
                         'D': 'Copyright permission must be verified before any archival box is opened'},
             'correct': 'A',
             'explanation': 'O primeiro parágrafo explica o motivo da antecedência com o conector <em>as</em>: quase '
                            'metade do acervo fica em uma instalação externa e <strong>as entregas ocorrem apenas às '
                            'terças e quintas</strong> (<em>deliveries arrive only on Tuesday and Thursday '
                            'mornings</em>), confirmando (A). A opção (D) mistura a regra de publicação do segundo '
                            'parágrafo com a consulta local.'},
            {'num': 'B15.2',
             'prompt': 'Under what condition may a researcher publish a high-resolution scan without contacting a '
                       'copyright holder?',
             'options': {'A': 'When the image is taken with a personal phone and no flash',
                         'B': 'When the scan is used only for a university thesis or dissertation',
                         'C': 'When the material being reproduced is already in the public domain',
                         'D': 'When the item is stored in the main library rather than off-site'},
             'correct': 'C',
             'explanation': 'O segundo parágrafo exige autorização por escrito do detentor dos direitos autorais, '
                            '<strong>a menos que a obra esteja em domínio público</strong> (<em>unless the work has '
                            'entered the public domain</em>), o que valida (C). A alternativa (A) descreve fotos de '
                            'referência para estudo, e não digitalizações para publicação.'},
            {'num': 'B15.3',
             'prompt': 'Which of the following is a researcher allowed to bring to a Reading Room table?',
             'options': {'A': 'A fountain pen for taking detailed notes',
                         'B': 'A winter coat draped over the chair',
                         'C': 'A yellow highlighter for marking photocopies',
                         'D': 'A smartphone with its camera flash disabled'},
             'correct': 'D',
             'explanation': 'O texto autoriza o uso de <strong>dispositivos portáteis com o flash desligado</strong> '
                            'para fotos de referência (<em>handheld devices with the flash turned off</em>), '
                            'confirmando (D). Já canetas-tinteiro (A), casacos (B) e marca-textos (C) são '
                            'explicitamente proibidos nas mesas de leitura (<em>prohibited at the reading '
                            'tables</em>).'}]}]
MOD1_ACTION_DRILLS_B = MOD1_ACTION_DRILLS_B + MOD1_NOVOS_B
MOD1_NOVOS_C = [{'id': 'mod1-cn1',
  'title': 'Exercício C4: ecologia urbana (meta de 5 min)',
  'level': 'A2–B1',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 5 minutos.',
  'passage_html': '<p><strong>PASSAGE: Green Roofs in Modern Cities</strong></p>\n'
                  '<p>Many modern cities are replacing dark, flat building roofs with "green roofs" covered in soil '
                  'and low-growing plants. Unlike traditional dark roofs, which absorb sunlight and make buildings '
                  'very hot, green roofs use living plants to shade the surface and cool the air through '
                  'evaporation.</p>\n'
                  '<p>This simple design brings two main benefits to urban neighborhoods. First, it lowers indoor '
                  'temperatures during the summer, so people inside the building use less electricity for air '
                  'conditioning. Second, the layer of soil acts like a sponge during heavy rain, holding water that '
                  'would otherwise flood city streets and storm drains.</p>\n'
                  '<p>However, not every building can support a green roof right away. Wet soil is heavy, so '
                  'engineers must first check the strength of the roof structure. For older buildings, owners often '
                  'choose thin layers of hardy succulent plants called sedums, which need very little soil or '
                  'watering to survive.</p>',
  'items': [{'num': 'C4.1',
             'prompt': 'Ideia principal. What is the main idea of the passage?',
             'options': {'A': 'Green roofs help cool buildings and manage rainwater, though their weight requires '
                              'careful planning.',
                         'B': 'Traditional dark roofs are cheaper to build and last much longer than modern green '
                              'roofs.',
                         'C': 'City engineers want to remove all plants from older buildings to prevent roof damage.',
                         'D': 'Succulent plants called sedums are the only plants that can grow on city roofs.'},
             'correct': 'A',
             'explanation': 'A passagem apresenta o que são os telhados verdes, seus dois benefícios principais no '
                            'calor e na chuva, e o cuidado com o peso na estrutura, o que resume a <strong>visão '
                            'geral dos telhados verdes</strong> na opção (A). A alternativa (D) pega um exemplo '
                            'específico do último parágrafo e o transforma em regra única.'},
            {'num': 'C4.2',
             'prompt': 'Detalhe. According to paragraph 2, how do green roofs help cities during heavy rain?',
             'options': {'A': 'They heat the rainwater so that it evaporates before reaching the ground.',
                         'B': "They send extra water directly into the building's air conditioning system.",
                         'C': 'They absorb rainwater in the soil and reduce flooding in the streets.',
                         'D': 'They block rain clouds from forming above tall urban buildings.'},
             'correct': 'C',
             'explanation': 'O segundo parágrafo explica que a terra funciona como uma esponja na chuva forte, '
                            'promovendo a <strong>retenção da água para evitar alagamentos</strong> (<em>holding '
                            'water that would otherwise flood city streets</em>), como diz (C). A opção (A) mistura '
                            'a evaporação citada no primeiro parágrafo com o controle de enchentes.'},
            {'num': 'C4.3',
             'prompt': 'Detalhe negativo. Which of the following is NOT mentioned as a feature or benefit of green '
                       'roofs?',
             'options': {'A': 'Shading the roof surface from sunlight',
                         'B': 'Lowering electricity use for air conditioning',
                         'C': 'Holding rainwater during heavy storms',
                         'D': 'Growing fresh vegetables for local restaurants'},
             'correct': 'D',
             'explanation': 'O texto menciona sombra na superfície (A), economia de ar-condicionado (B) e absorção '
                            'de chuva (C), mas em nenhum momento fala em <strong>produzir vegetais para '
                            'restaurantes</strong>, o que marca (D). Cuidado para não trazer conhecimentos externos '
                            'sobre hortas urbanas que não aparecem na passagem.'},
            {'num': 'C4.4',
             'prompt': 'Propósito retórico. Why does the author mention "sedums" in paragraph 3?',
             'options': {'A': 'To explain why wet soil is too heavy for modern steel roofs',
                         'B': 'To give an example of plants that work well in thin soil on older roofs',
                         'C': 'To show that succulents cannot survive in rainy city climates',
                         'D': 'To argue that building owners should avoid planting on flat roofs'},
             'correct': 'B',
             'explanation': 'O autor cita os <em>sedums</em> logo depois de explicar o limite de peso em prédios '
                            'antigos para dar um <strong>exemplo de planta que exige pouca terra</strong> (<em>need '
                            'very little soil or watering to survive</em>), confirmando (B). A alternativa (A) '
                            'confunde o problema do peso com a solução usada nos prédios antigos.'},
            {'num': 'C4.5',
             'prompt': 'Vocabulário em contexto. The word "hardy" in paragraph 3 is closest in meaning to:',
             'options': {'A': 'tough', 'B': 'rare', 'C': 'tall', 'D': 'bright'},
             'correct': 'A',
             'explanation': 'No trecho, plantas <em>hardy</em> são aquelas que sobrevivem com pouca terra e quase '
                            'sem rega, ou seja, <strong>plantas resistentes e fortes</strong> (<em>tough</em>), '
                            'validando (A). A opção (C) contradiz o primeiro parágrafo, que fala em plantas baixas '
                            '(<em>low-growing plants</em>).'}]},
 {'id': 'mod1-cn2',
  'title': 'Exercício C5: zoologia (meta de 5 min)',
  'level': 'A2–B1',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 5 minutos.',
  'passage_html': '<p><strong>PASSAGE: How Sea Otters Protect Kelp Forests</strong></p>\n'
                  '<p>Along the cool coast of the North Pacific, giant kelp grows from the ocean floor toward the '
                  'sunlight, forming thick underwater forests. These kelp forests provide food and shelter for '
                  'hundreds of marine species, including young fish, crabs, and seals.</p>\n'
                  '<p>Sea otters play a central role in keeping these forests healthy. Otters eat large numbers of '
                  'sea urchins, which are small, spiny animals that crawl along the rocks and feed on the base of '
                  'kelp stems. When sea otters are present, they keep the urchin population small, allowing the kelp '
                  'to grow tall and dense.</p>\n'
                  '<p>When sea otters disappear from an area, the natural balance changes quickly. Without their '
                  'main predator, sea urchins multiply and chew through the kelp until almost nothing is left. '
                  'Biologists call this empty seafloor an "urchin barren," and it shows how a single predator can '
                  'protect an entire ecosystem.</p>',
  'items': [{'num': 'C5.1',
             'prompt': 'Ideia principal. The passage is mainly about:',
             'options': {'A': 'how giant kelp uses sunlight to grow in the cold waters of the North Pacific',
                         'B': 'how sea otters keep kelp forests healthy by controlling sea urchin numbers',
                         'C': 'why young fish and seals leave the coast during the winter months',
                         'D': 'why biologists are trying to move sea urchins to deeper ocean waters'},
             'correct': 'B',
             'explanation': 'O fio condutor do texto mostra como as lontras-marinhas comem ouriços-do-mar e garantem '
                            'a <strong>proteção das florestas de kelp</strong>, exatamente como resume (B). A opção '
                            '(A) fica restrita à abertura do primeiro parágrafo e deixa de fora a relação entre '
                            'lontras e ouriços.'},
            {'num': 'C5.2',
             'prompt': 'Detalhe. According to paragraph 2, how do sea urchins harm giant kelp?',
             'options': {'A': 'They block sunlight from reaching the top of the kelp forest.',
                         'B': 'They chase away the fish and crabs that clean the kelp leaves.',
                         'C': 'They poison the water around the roots of the kelp plants.',
                         'D': 'They eat the lower part of the kelp stems along the rocks.'},
             'correct': 'D',
             'explanation': 'O segundo parágrafo diz que os ouriços rastejam pelas pedras e <strong>comem a base dos '
                            'caules de kelp</strong> (<em>feed on the base of kelp stems</em>), o que corresponde a '
                            '(D). As demais opções inventam formas de dano que não aparecem no texto.'},
            {'num': 'C5.3',
             'prompt': 'Inferência. What can be inferred from the passage about young fish and crabs in an "urchin '
                       'barren"?',
             'options': {'A': 'They learn to hunt sea urchins when the sea otters disappear.',
                         'B': 'They grow faster because there is more open space on the rocks.',
                         'C': 'They lose the food and shelter that the kelp forest once provided.',
                         'D': 'They help the giant kelp grow back within a few weeks.'},
             'correct': 'C',
             'explanation': 'O primeiro parágrafo afirma que a floresta de kelp dá alimento e abrigo a peixes jovens '
                            'e caranguejos; logo, quando os ouriços destroem tudo no <em>urchin barren</em>, esses '
                            'animais sofrem a <strong>perda de alimento e refúgio</strong>, confirmando (C). A opção '
                            '(B) ignora que o fundo vazio deixa essas espécies desprotegidas.'},
            {'num': 'C5.4',
             'prompt': 'Propósito retórico. Why does the author describe what happens when sea otters disappear in '
                       'paragraph 3?',
             'options': {'A': 'To show how important sea otters are to the survival of the ecosystem',
                         'B': 'To prove that sea urchins can live without eating giant kelp',
                         'C': 'To explain why sea otters prefer warm water over the North Pacific',
                         'D': 'To argue that predators have very little effect on ocean plants'},
             'correct': 'A',
             'explanation': 'Ao mostrar a destruição do kelp na ausência das lontras, o autor comprova na prática a '
                            '<strong>importância desse predador para todo o ecossistema</strong> (<em>how a single '
                            'predator can protect an entire ecosystem</em>), validando (A). A alternativa (D) afirma '
                            'o oposto da conclusão do parágrafo.'},
            {'num': 'C5.5',
             'prompt': 'Vocabulário em contexto. The word "multiply" in paragraph 3 is closest in meaning to:',
             'options': {'A': 'hide', 'B': 'travel', 'C': 'shrink', 'D': 'increase'},
             'correct': 'D',
             'explanation': 'Sem seu predador principal, a população de ouriços passa a <em>multiply</em>, ou seja, '
                            'a <strong>aumentar em quantidade</strong> (<em>increase</em>), o que torna (D) correta. '
                            'A opção (C) tem o sentido contrário, de encolher ou diminuir.'}]},
 {'id': 'mod1-cn3',
  'title': 'Exercício C6: arqueologia (meta de 6 min)',
  'level': 'B1–B2',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.',
  'passage_html': '<p><strong>PASSAGE: Roman Concrete and Volcanic Ash</strong></p>\n'
                  '<p>Modern steel-reinforced concrete is strong, yet harbor walls made with it often begin to crack '
                  'and crumble after only a few decades in saltwater. By contrast, concrete piers and breakwaters '
                  'built by Roman engineers more than two thousand years ago still stand intact along the '
                  'Mediterranean coast, battered daily by waves.</p>\n'
                  '<p>For a long time, researchers knew that the Roman recipe mixed lime and volcanic rock with a '
                  'powdery volcanic ash called pozzolana, taken from the region around the Bay of Naples. Only '
                  'recently, however, did mineralogists discover what happens inside this mixture over time. As '
                  'seawater filters through tiny pores in the concrete, it dissolves part of the volcanic ash and '
                  'reacts with the lime to grow rare, interlocking crystal plates.</p>\n'
                  '<p>Instead of weakening the structure, seawater actually reinforces it: whenever a microscopic '
                  'crack opens, new crystals form and seal the gap before it can spread. Material scientists are now '
                  'studying this self-healing chemistry in hopes of designing modern marine concrete that lasts '
                  'longer and requires fewer costly repairs.</p>',
  'items': [{'num': 'C6.1',
             'prompt': 'Ideia principal. What is the main idea of the passage?',
             'options': {'A': 'Roman engineers avoided building harbors where Mediterranean waves were strong.',
                         'B': 'Volcanic ash from the Bay of Naples can no longer be used in construction.',
                         'C': 'Roman marine concrete endures because seawater reacts with its volcanic ash.',
                         'D': 'Modern steel-reinforced concrete lasts longer in saltwater than ancient materials.'},
             'correct': 'C',
             'explanation': 'A passagem inteira explica por que o concreto marítimo romano dura milênios, destacando '
                            'a <strong>reação entre cinza vulcânica e água do mar</strong> que fortalece a '
                            'estrutura, como resume (C). A opção (D) inverte a comparação feita logo no primeiro '
                            'parágrafo.'},
            {'num': 'C6.2',
             'prompt': 'Detalhe. According to paragraph 2, what happens when seawater enters the tiny pores of Roman '
                       'concrete?',
             'options': {'A': 'It triggers a chemical reaction that forms interlocking crystals.',
                         'B': 'It washes away the lime and leaves large empty spaces inside the rock.',
                         'C': 'It rusts the internal steel bars that hold the piers together.',
                         'D': 'It cools the volcanic ash so the mixture can dry more quickly.'},
             'correct': 'A',
             'explanation': 'O segundo parágrafo detalha que a água do mar dissolve parte da cinza e reage com a cal '
                            'para produzir <strong>placas cristalinas entrelaçadas</strong> (<em>reacts with the '
                            'lime to grow rare, interlocking crystal plates</em>), confirmando (A). A alternativa '
                            '(C) confunde o concreto romano com o concreto moderno armado com aço.'},
            {'num': 'C6.3',
             'prompt': 'Inferência. It can be inferred from the passage that modern marine concrete differs from '
                       'Roman concrete in that modern concrete:',
             'options': {'A': 'contains larger amounts of volcanic rock from southern Italy',
                         'B': 'is gradually damaged by saltwater rather than strengthened by it',
                         'C': 'takes more than two thousand years to harden completely',
                         'D': 'can seal its own microscopic cracks without human repair'},
             'correct': 'B',
             'explanation': 'Enquanto o concreto romano fica mais forte em contato com a água salgada, o primeiro '
                            'parágrafo mostra que o concreto moderno sofre <strong>degradação gradual na água do '
                            'mar</strong> (<em>crack and crumble after only a few decades in saltwater</em>), '
                            'validando (B). A opção (D) descreve uma qualidade do concreto romano, e não do '
                            'moderno.'},
            {'num': 'C6.4',
             'prompt': 'Propósito retórico. Why does the author mention in paragraph 3 that new crystals seal '
                       'microscopic cracks?',
             'options': {'A': 'To explain why Roman harbors were more expensive to build than modern ones',
                         'B': 'To show that seawater prevents volcanic ash from mixing with lime',
                         'C': 'To argue that ancient structures still need frequent repairs by engineers',
                         'D': 'To explain how the self-healing process keeps the concrete from breaking apart'},
             'correct': 'D',
             'explanation': 'O autor descreve o fechamento das fendas pelos cristais para explicar na prática o '
                            '<strong>mecanismo de autorreparo do concreto romano</strong> (<em>seal the gap before '
                            'it can spread</em>), como aponta (D). A alternativa (C) contradiz o final do parágrafo, '
                            'que busca justamente reduzir reparos caros.'},
            {'num': 'C6.5',
             'prompt': 'Vocabulário em contexto. The word "intact" in paragraph 1 is closest in meaning to:',
             'options': {'A': 'underwater', 'B': 'unfinished', 'C': 'undamaged', 'D': 'unnoticed'},
             'correct': 'C',
             'explanation': 'Em contraste com os muros modernos que racham e se desfazem, os píeres romanos '
                            'permanecem <em>intact</em>, isto é, <strong>intactos e sem danos</strong> '
                            '(<em>undamaged</em>), tornando (C) a resposta certa. A opção (A) é tentadora pelo '
                            'contexto marítimo, mas não traduz o sentido de conservação.'}]},
 {'id': 'mod1-cn4',
  'title': 'Exercício C7: psicologia cognitiva (meta de 6 min)',
  'level': 'B1–B2',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.',
  'passage_html': '<p><strong>PASSAGE: The Testing Effect in Memory Retention</strong></p>\n'
                  '<p>When preparing for an exam, most students rely on rereading their notes or textbook chapters '
                  'until the material feels familiar. Although this habit builds confidence in the short term, '
                  'cognitive psychologists have repeatedly shown that passive review is one of the least effective '
                  'ways to store information for the long run.</p>\n'
                  '<p>A far stronger strategy is retrieval practice, often called the "testing effect." In classic '
                  'experiments, students who read a passage once and then practiced recalling its key points from '
                  'memory without looking at the text scored much higher on a test a week later than students who '
                  'spent the same amount of time rereading the passage four times.</p>\n'
                  '<p>Researchers explain that the act of pulling a memory out of storage alters the memory trace '
                  'itself, strengthening the neural pathways connected to that knowledge. Even when a student '
                  'struggles or fails to recall an answer at first, the effort makes the subsequent correction stick '
                  'more firmly. Because rereading feels smooth and effortless, learners often mistake temporary '
                  'fluency for lasting mastery.</p>',
  'items': [{'num': 'C7.1',
             'prompt': 'Ideia principal. The main idea of the passage is that:',
             'options': {'A': 'students should read a textbook chapter at least four times before taking any '
                              'practice test',
                         'B': 'feeling confident while studying is the most reliable sign of long-term memory '
                              'retention',
                         'C': 'written exams should be replaced with classroom discussions because tests cause '
                              'anxiety',
                         'D': 'actively recalling information from memory produces stronger long-term learning than '
                              'rereading'},
             'correct': 'D',
             'explanation': 'A tese central contrasta a revisão passiva com a prática de recordação e mostra que '
                            '<strong>recuperar a informação na memória gera aprendizado duradouro</strong>, '
                            'validando (D). As opções (A) e (B) defendem justamente a releitura passiva que o estudo '
                            'refuta.'},
            {'num': 'C7.2',
             'prompt': 'Detalhe. In the experiments described in paragraph 2, which group performed better on the '
                       'test given a week later?',
             'options': {'A': 'Students who reread the passage four times without taking notes',
                         'B': 'Students who read the passage once and practiced recalling it from memory',
                         'C': 'Students who waited until the morning of the test to read the passage',
                         'D': 'Students who copied the entire passage by hand while looking at the book'},
             'correct': 'B',
             'explanation': 'O segundo parágrafo relata que os alunos que leram uma vez e treinaram lembrar sem '
                            'olhar o texto tiveram <strong>nota muito maior uma semana depois</strong> (<em>scored '
                            'much higher on a test a week later</em>), confirmando (B). A alternativa (A) cita o '
                            'grupo que teve desempenho inferior no experimento.'},
            {'num': 'C7.3',
             'prompt': 'Inferência. What can be inferred from paragraph 3 about a student who answers a practice '
                       'question incorrectly before checking the right answer?',
             'options': {'A': 'The attempt to remember still helps the student retain the correct answer afterward.',
                         'B': 'The mistake permanently weakens the neural pathways connected to that topic.',
                         'C': 'The student would have learned more by rereading the chapter instead of guessing.',
                         'D': 'The student will inevitably repeat the same error on the final exam a week later.'},
             'correct': 'A',
             'explanation': 'O terceiro parágrafo afirma que, mesmo quando o aluno falha ao tentar lembrar de '
                            'início, o esforço faz a correção seguinte fixar melhor (<em>the effort makes the '
                            'subsequent correction stick more firmly</em>), o que sustenta a <strong>retenção '
                            'fortalecida após a tentativa</strong> em (A). A opção (B) diz o oposto do que ocorre '
                            'nas vias neurais.'},
            {'num': 'C7.4',
             'prompt': 'Propósito retórico. Why does the author state that "rereading feels smooth and effortless" '
                       'in paragraph 3?',
             'options': {'A': 'To recommend rereading for subjects that require very little memorization',
                         'B': 'To prove that textbook authors now write in a simpler style than in the past',
                         'C': 'To explain why students often believe rereading is more effective than it really is',
                         'D': 'To show that retrieval practice takes less mental energy than passive review'},
             'correct': 'C',
             'explanation': 'A frase explica a ilusão de competência: como reler parece fácil e fluido, os '
                            'estudantes caem na armadilha de <strong>confundir familiaridade passageira com domínio '
                            'real</strong> (<em>mistake temporary fluency for lasting mastery</em>), como resume '
                            '(C). A alternativa (D) inverte qual método exige menos esforço.'},
            {'num': 'C7.5',
             'prompt': 'Vocabulário em contexto. The word "subsequent" in paragraph 3 is closest in meaning to:',
             'options': {'A': 'previous', 'B': 'following', 'C': 'partial', 'D': 'sudden'},
             'correct': 'B',
             'explanation': 'Depois que o aluno tenta lembrar e erra, a correção <em>subsequent</em> é a que vem em '
                            'seguida, ou seja, a <strong>correção posterior ou seguinte</strong> '
                            '(<em>following</em>), confirmando (B). A opção (A) significa anterior, invertendo a '
                            'ordem dos fatos.'}]},
 {'id': 'mod1-cn5',
  'title': 'Exercício C8: astronomia (meta de 6 min)',
  'level': 'B2–C1',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.',
  'passage_html': '<p><strong>PASSAGE: Subsurface Oceans on Icy Moons</strong></p>\n'
                  '<p>For decades, astronomers searching for liquid water beyond Earth focused on the "habitable '
                  'zone," the orbital band around a star where a planet\'s surface is warm enough for liquid water '
                  'but not so hot that it boils away. By that standard, the outer solar system seemed far too cold '
                  'to host liquid oceans, since sunlight at the distance of Jupiter and Saturn is a tiny fraction of '
                  'what reaches Earth.</p>\n'
                  '<p>Space probe missions forced scientists to revise that view. Beneath the fractured ice crusts '
                  "of moons such as Jupiter's Europa and Saturn's Enceladus lie global oceans of liquid saltwater. "
                  'The heat that keeps these oceans from freezing solid does not come from the Sun, but from tidal '
                  'flexing: as a moon travels along a slightly oval orbit, the immense gravitational pull of its '
                  "giant planet stretches and compresses the moon's interior, generating friction and warmth.</p>\n"
                  '<p>At Enceladus, the Cassini spacecraft even flew through plumes of water vapor erupting from '
                  'cracks near the south pole, detecting salts, organic molecules, and molecular hydrogen, a gas '
                  'that on Earth forms around deep-sea hydrothermal vents. Such findings suggest that habitable '
                  'environments may not require a warm planetary surface at all, greatly expanding the number of '
                  'worlds where microbial life might arise.</p>',
  'items': [{'num': 'C8.1',
             'prompt': 'Ideia principal. What is the main idea of the passage?',
             'options': {'A': 'Tidal heating maintains liquid oceans beneath the ice of outer-planet moons, '
                              'broadening where scientists look for habitable worlds.',
                         'B': 'The Sun has gradually grown warmer, allowing frozen moons around Jupiter and Saturn '
                              'to melt into surface oceans.',
                         'C': 'The Cassini spacecraft proved that Enceladus is the only body in the solar system '
                              'with deep-sea hydrothermal vents.',
                         'D': 'Astronomers have abandoned the search for water on planets outside our solar system '
                              'to focus solely on Europa.'},
             'correct': 'A',
             'explanation': 'O texto mostra como o aquecimento de maré mantém oceanos líquidos sob o gelo de luas '
                            'distantes e provoca a <strong>ampliação da busca por ambientes habitáveis</strong>, '
                            'exatamente como em (A). A opção (B) atribui o calor ao Sol, quando o segundo parágrafo '
                            'diz <em>does not come from the Sun</em>.'},
            {'num': 'C8.2',
             'prompt': 'Detalhe. According to paragraph 2, what prevents the subsurface oceans of Europa and '
                       'Enceladus from freezing?',
             'options': {'A': 'Thick clouds of water vapor that trap solar heat above the ice crust',
                         'B': 'Radioactive metals floating near the surface of the saltwater oceans',
                         'C': 'Warm ocean currents flowing from the equator toward the south pole',
                         'D': 'Internal friction caused by the gravitational pull of their giant planets'},
             'correct': 'D',
             'explanation': 'O segundo parágrafo explica que a gravidade do planeta gigante estica e comprime o '
                            'interior da lua em órbita oval, gerando <strong>atrito interno e calor por flexão de '
                            "maré</strong> (<em>stretches and compresses the moon's interior, generating friction "
                            'and warmth</em>), confirmando (D). A alternativa (A) contradiz a ausência de calor '
                            'solar suficiente.'},
            {'num': 'C8.3',
             'prompt': 'Detalhe negativo. Which of the following was NOT detected by the Cassini spacecraft in the '
                       'plumes of Enceladus?',
             'options': {'A': 'Salts from the subsurface water',
                         'B': 'Organic molecules in the vapor',
                         'C': 'Living microbial cells from the ocean floor',
                         'D': 'Molecular hydrogen gas'},
             'correct': 'C',
             'explanation': 'No terceiro parágrafo, a sonda Cassini detectou sais (A), moléculas orgânicas (B) e '
                            'hidrogênio molecular (D), mas não encontrou <strong>células microbianas vivas</strong>, '
                            'o que marca (C). Repare que o texto fala apenas que a vida microbiana <em>might '
                            'arise</em> (poderia surgir) nesses mundos.'},
            {'num': 'C8.4',
             'prompt': 'Propósito retórico. Why does the author discuss the traditional "habitable zone" in '
                       'paragraph 1?',
             'options': {'A': 'To explain why Jupiter and Saturn receive more sunlight than Earth',
                         'B': 'To present an older assumption that later discoveries called into question',
                         'C': 'To argue that liquid water cannot exist anywhere inside our solar system',
                         'D': 'To show how astronomers calculate the exact distance between a star and its moons'},
             'correct': 'B',
             'explanation': 'O primeiro parágrafo apresenta a visão clássica da zona habitável para criar um '
                            'contraste com o segundo parágrafo, servindo para <strong>introduzir uma premissa antiga '
                            'superada pelas sondas espaciais</strong> (<em>Space probe missions forced scientists to '
                            'revise that view</em>), como diz (B). A opção (A) inverte a quantidade de luz solar '
                            'citada.'},
            {'num': 'C8.5',
             'prompt': 'Vocabulário em contexto. The word "revise" in paragraph 2 is closest in meaning to:',
             'options': {'A': 'defend', 'B': 'ignore', 'C': 'confirm', 'D': 'modify'},
             'correct': 'D',
             'explanation': 'Diante da descoberta de oceanos subterrâneos, os cientistas tiveram de <em>revise that '
                            'view</em>, isto é, <strong>modificar ou ajustar aquela visão anterior</strong> '
                            '(<em>modify</em>), validando (D). Cuidado com (A) e (C), que sugerem manter a ideia '
                            'antiga sem mudança.'}]},
 {'id': 'mod1-cn6',
  'title': 'Exercício C9: economia e energia (meta de 6 min)',
  'level': 'C1',
  'objective': 'Leia a passagem completa uma vez. Responda às 5 questões. Tempo-alvo: 6 minutos.',
  'passage_html': '<p><strong>PASSAGE: The Jevons Paradox and Energy Efficiency</strong></p>\n'
                  '<p>Intuitively, technological improvements that make machines more fuel-efficient should reduce '
                  'overall fuel consumption. In 1865, however, the English economist William Stanley Jevons observed '
                  "that the introduction of James Watt's far more efficient steam engine had produced the opposite "
                  "result: Britain's total coal consumption soared rather than declined.</p>\n"
                  "<p>Jevons argued that efficiency lowers the effective cost of using a resource. Because Watt's "
                  'engine burned much less coal per unit of work, operating steam power became profitable in '
                  'industries and factories where it had previously been too expensive. As steam engines spread into '
                  'textiles, mining, and railways, the surge in new uses more than offset the fuel saved by each '
                  'individual machine, a rebound effect now known as the Jevons paradox.</p>\n'
                  '<p>Contemporary energy economists point out that the paradox does not occur with identical force '
                  'in every sector. When demand for a service is already largely saturated, such as home '
                  'refrigeration in wealthy countries, efficiency gains genuinely cut total electricity use. Where '
                  'lower operating costs unlock substantial new demand, however, engineers and policymakers cannot '
                  'rely on efficiency alone to curb resource depletion, and must pair technical advances with '
                  'conservation policies or pricing limits.</p>',
  'items': [{'num': 'C9.1',
             'prompt': 'Ideia principal. The passage is mainly about:',
             'options': {'A': 'how nineteenth-century British railways replaced coal with cheaper fuels',
                         'B': 'why modern engineers have stopped improving household appliances',
                         'C': 'how greater energy efficiency can raise total fuel use by making a resource cheaper',
                         'D': "why Jevons opposed the use of Watt's steam engine in textile mills"},
             'correct': 'C',
             'explanation': 'A passagem apresenta o paradoxo de Jevons, explicando como <strong>ganhos de eficiência '
                            'podem elevar o consumo total de energia</strong> ao baratear seu uso e quando esse '
                            'efeito ocorre hoje, como sintetiza (C). A opção (A) distorce o texto, pois as ferrovias '
                            'aumentaram o uso de carvão.'},
            {'num': 'C9.2',
             'prompt': "Detalhe. According to paragraph 2, why did Britain's total coal use rise after Watt's "
                       'improved steam engine was introduced?',
             'options': {'A': 'Lower fuel costs per unit of work made steam power economical for many new '
                              'industries.',
                         'B': 'Each individual Watt engine burned more coal per hour than earlier steam engines.',
                         'C': 'The British government lowered taxes on coal mines to encourage railway construction.',
                         'D': 'Factories had to run their engines twice as long because the new machines were '
                              'slower.'},
             'correct': 'A',
             'explanation': 'O segundo parágrafo explica que, como a máquina de Watt gastava menos carvão por '
                            'unidade de trabalho, o vapor ficou mais barato e houve <strong>expansão lucrativa para '
                            'novos setores industriais</strong> (<em>operating steam power became profitable in '
                            'industries and factories where it had previously been too expensive</em>), confirmando '
                            '(A). A alternativa (B) contradiz o fato de que cada máquina individual economizava '
                            'combustível.'},
            {'num': 'C9.3',
             'prompt': 'Inferência. It can be inferred from paragraph 3 that if household refrigerators become 30 '
                       'percent more energy-efficient in a wealthy country, most households will:',
             'options': {'A': 'buy a second refrigerator to spend the money they save',
                         'B': 'use less electricity overall than they did before',
                         'C': 'spend more on electricity each month than before',
                         'D': 'need pricing limits to keep their energy use down'},
             'correct': 'B',
             'explanation': 'O terceiro parágrafo usa a refrigeração doméstica em países ricos como exemplo de '
                            'demanda já saturada, em que a maior eficiência gera <strong>redução real no consumo '
                            'total de eletricidade</strong> (<em>efficiency gains genuinely cut total electricity '
                            'use</em>), validando (B). A opção (C) aplica o efeito rebote a um setor onde o próprio '
                            'texto diz que ele não ocorre.'},
            {'num': 'C9.4',
             'prompt': 'Propósito retórico. Why does the author mention home refrigeration in paragraph 3?',
             'options': {'A': 'To show that home appliances waste more energy than railways',
                         'B': 'To prove that the paradox applies equally to every industry',
                         'C': 'To criticize wealthy countries for using too much electricity',
                         'D': 'To give an example where efficiency really lowers total use'},
             'correct': 'D',
             'explanation': 'O exemplo da geladeira entra logo após a afirmação de que o paradoxo não age com a '
                            'mesma força em todo setor, servindo para <strong>ilustrar um mercado de demanda '
                            'saturada</strong> em que a eficiência reduz o gasto total, como diz (D). A alternativa '
                            '(B) afirma exatamente o oposto da frase de abertura do parágrafo.'},
            {'num': 'C9.5',
             'prompt': 'Vocabulário em contexto. The word "offset" in paragraph 2 is closest in meaning to:',
             'options': {'A': 'counterbalance', 'B': 'accelerate', 'C': 'measure', 'D': 'restrict'},
             'correct': 'A',
             'explanation': 'Na frase, a explosão de novos usos <em>more than offset</em> a economia de cada '
                            'máquina, ou seja, mais do que <strong>compensou ou contrabalançou</strong> '
                            '(<em>counterbalance</em>) o combustível poupado, tornando (A) correta. A opção (D) '
                            'significa restringir, o que não encaixa na relação entre novos usos e economia '
                            'unitária.'}]}]
MOD1_ACTION_DRILLS_C = MOD1_ACTION_DRILLS_C + MOD1_NOVOS_C
MOD2_NOVOS_A = [{'id': 'mod2-an1',
  'title': 'Exercício A2: rotina e espaços do campus (meta de 1 min)',
  'level': 'A2–B1',
  'objective': 'Ouça cada fala e escolha a resposta mais natural. A fala aparece escrita depois que você responde. '
               'Tempo-alvo: 12 segundos por item.',
  'passage_html': None,
  'items': [{'num': 'A13',
             'prompt': '"Excuse me, is this seat next to you taken?"',
             'options': {'A': 'No, go right ahead and sit down.',
                         'B': 'Yes, I took the exam yesterday.',
                         'C': 'The seats in the back are blue.',
                         'D': 'I usually sit near the window.'},
             'correct': 'A',
             'explanation': 'Quando alguém pergunta <em>is this seat next to you taken?</em>, quer saber se o lugar '
                            'está livre para sentar, por isso (A) responde com naturalidade ao <strong>liberar o '
                            'assento</strong>. Se você pensou em (B), repare que ela usa o verbo <em>took</em>, mas '
                            'fala de uma prova de ontem e não do lugar ao lado.'},
            {'num': 'A14',
             'prompt': '"Oh, wait, I left my student ID card in my dorm room."',
             'options': {'A': 'My dorm room is on the third floor.',
                         'B': 'We can wait here while you grab it.',
                         'C': 'The student center closes at eight.',
                         'D': 'I got my new card last September.'},
             'correct': 'B',
             'explanation': 'Ao dizer <em>I left my student ID card in my dorm room</em>, quem fala percebe que '
                            'esqueceu o cartão agora, e (B) traz a <strong>reação prática de esperar</strong> '
                            'enquanto a pessoa busca o documento. A opção (A) é uma armadilha comum porque repete '
                            '<em>dorm room</em>, mas só informa o andar do quarto sem ajudar na situação.'},
            {'num': 'A15',
             'prompt': '"Do you know what time the campus bookstore closes today?"',
             'options': {'A': 'I bought two notebooks there yesterday.',
                         'B': 'The bookstore is right across the quad.',
                         'C': 'I think it closes at five today.',
                         'D': 'Yes, the textbooks are pretty expensive.'},
             'correct': 'C',
             'explanation': 'A pergunta <em>what time the campus bookstore closes today</em> pede o <strong>horário '
                            'de fechamento da livraria</strong>, que (C) informa de modo natural. Já a alternativa '
                            '(B) fala da localização da loja no campus, respondendo a onde ela fica e não a que '
                            'horas fecha.'},
            {'num': 'A16',
             'prompt': '"It\'s a bit cold in this classroom, don\'t you think?"',
             'options': {'A': 'Class starts at ten every Monday.',
                         'B': 'Winter is my favorite season here.',
                         'C': 'I think the professor is outside.',
                         'D': "Yeah, I'll go shut the window now."},
             'correct': 'D',
             'explanation': "O comentário <em>It's a bit cold in this classroom, don't you think?</em> busca "
                            'concordância sobre o frio na sala, e (D) <strong>concorda e oferece uma '
                            'solução</strong> fechando a janela. A opção (B) puxa o assunto para o inverno em geral '
                            'e ignora o desconforto da sala agora.'},
            {'num': 'A17',
             'prompt': '"I can\'t find the biology lab on this campus map."',
             'options': {'A': "I'm heading there now, so follow me.",
                         'B': 'Biology is a required class for me.',
                         'C': 'The campus map is free for students.',
                         'D': 'Our lab partner finished the chart.'},
             'correct': 'A',
             'explanation': "Diante da dificuldade em <em>I can't find the biology lab on this campus map</em>, quem "
                            'fala precisa de ajuda para chegar ao local, e (A) resolve isso ao <strong>convidar para '
                            'ir junto</strong>. A alternativa (C) repete <em>campus map</em>, mas fala do preço do '
                            'mapa em vez de indicar o caminho.'},
            {'num': 'A18',
             'prompt': '"Are you still using that dictionary, or can I borrow it?"',
             'options': {'A': 'I looked up three new words today.',
                         'B': "It's all yours, I'm done with it.",
                         'C': 'The library has a lot of computers.',
                         'D': 'You can buy one at the main store.'},
             'correct': 'B',
             'explanation': 'A pergunta <em>Are you still using that dictionary, or can I borrow it?</em> é um '
                            'pedido para usar o dicionário agora, e (B) responde de forma direta ao <strong>avisar '
                            'que já terminou de usar</strong>. A opção (A) fala de palavras pesquisadas no dia, mas '
                            'não diz se o livro está livre.'}]},
 {'id': 'mod2-an2',
  'title': 'Exercício A3: aulas, biblioteca e estudos (meta de 1 min)',
  'level': 'B1–B2',
  'objective': 'Ouça cada fala e escolha a resposta mais natural. A fala aparece escrita depois que você responde. '
               'Tempo-alvo: 12 segundos por item.',
  'passage_html': None,
  'items': [{'num': 'A19',
             'prompt': '"I\'m swamped with readings this week, so I might skip the club meeting."',
             'options': {'A': 'The reading room on the second floor is quiet.',
                         'B': 'Our club meets every Wednesday in the lounge.',
                         'C': "No worries, I'll fill you in on what you miss.",
                         'D': 'I finished reading that chapter last weekend.'},
             'correct': 'C',
             'explanation': "Quando quem fala avisa <em>I'm swamped with readings this week, so I might skip the "
                            'club meeting</em>, está explicando que deve faltar à reunião por excesso de leitura, e '
                            '(C) acolhe a ausência e <strong>promete passar o resumo depois</strong>. A opção (B) '
                            'apenas informa o dia fixo do encontro, sem reagir ao aviso de falta.'},
            {'num': 'A20',
             'prompt': '"Did you manage to get a seat in Professor Patel\'s seminar for next term?"',
             'options': {'A': 'Her office hours are on Tuesday afternoons.',
                         'B': 'The seminar room is in the history building.',
                         'C': 'I took an introductory class with her once.',
                         'D': "No, it filled up fast, so I'm on the waitlist."},
             'correct': 'D',
             'explanation': "A pergunta <em>Did you manage to get a seat in Professor Patel's seminar</em> trata de "
                            'conseguir vaga na matrícula, e (D) responde diretamente ao contar que a turma lotou e '
                            'restou a <strong>lista de espera da disciplina</strong>. A alternativa (B) confunde '
                            '<em>get a seat</em> na matéria com a localização física da sala.'},
            {'num': 'A21',
             'prompt': '"Wait, didn\'t the teaching assistant say the quiz would only cover chapter four?"',
             'options': {'A': 'Actually, she added chapter five in an email.',
                         'B': 'The teaching assistant grades all our papers.',
                         'C': 'Chapter four was much shorter than the others.',
                         'D': 'We have a short quiz every other Friday morning.'},
             'correct': 'A',
             'explanation': "Ao perguntar <em>didn't the teaching assistant say the quiz would only cover chapter "
                            'four?</em>, quem fala quer confirmar a matéria do teste, e (A) esclarece a dúvida com a '
                            '<strong>atualização enviada por e-mail</strong>. A opção (C) comenta o tamanho do '
                            'capítulo quatro, mas não confirma o conteúdo cobrado na avaliação.'},
            {'num': 'A22',
             'prompt': '"If we don\'t reserve a group study room soon, they\'ll all be booked for finals."',
             'options': {'A': 'The library bought new tables last month.',
                         'B': "Good point, I'll log in and book one now.",
                         'C': 'Final exams always last for a whole week.',
                         'D': 'Our study group has four people this term.'},
             'correct': 'B',
             'explanation': "O alerta <em>If we don't reserve a group study room soon, they'll all be booked</em> "
                            'aponta a urgência de garantir uma sala antes que acabe, e (B) reage na hora ao '
                            '<strong>fazer a reserva no sistema</strong>. A alternativa (D) fala do tamanho do grupo '
                            'de estudo, mas deixa de lado o risco de ficar sem sala.'},
            {'num': 'A23',
             'prompt': '"I was hoping to talk to my advisor today, but her door\'s closed."',
             'options': {'A': 'My advisor helped me pick my major last year.',
                         'B': 'The door to the main building locks at nine.',
                         'C': "She's usually back from lunch around one-thirty.",
                         'D': 'Advising appointments take about twenty minutes.'},
             'correct': 'C',
             'explanation': "Diante da frustração em <em>I was hoping to talk to my advisor today, but her door's "
                            'closed</em>, a resposta mais prestativa é informar quando ela deve voltar, como faz (C) '
                            'ao indicar o <strong>horário de retorno do almoço</strong>. A opção (B) repete a '
                            'palavra <em>door</em>, mas fala da porta do prédio à noite.'},
            {'num': 'A24',
             'prompt': '"How come you\'re printing your slides here instead of at the computer lab?"',
             'options': {'A': 'I need about fifteen slides for my talk.',
                         'B': 'The computer lab is in the north wing.',
                         'C': 'Printing costs five cents a page there.',
                         'D': 'Both printers over there are jammed again.'},
             'correct': 'D',
             'explanation': "Em <em>How come you're printing your slides here instead of at the computer lab?</em>, "
                            'a expressão <em>how come</em> pede o motivo da escolha, e (D) apresenta a <strong>causa '
                            'prática do problema</strong> nas impressoras do laboratório. A alternativa (B) apenas '
                            'diz onde fica o laboratório, sem explicar a troca de lugar.'}]},
 {'id': 'mod2-an3',
  'title': 'Exercício A4: secretaria, projetos e laboratório (meta de 1 min)',
  'level': 'B2–C1',
  'objective': 'Ouça cada fala e escolha a resposta mais natural. A fala aparece escrita depois que você responde. '
               'Tempo-alvo: 12 segundos por item.',
  'passage_html': None,
  'items': [{'num': 'A25',
             'prompt': '"I\'d double-check those survey numbers before sending the file to Dr. Evans, if I were '
                       'you."',
             'options': {'A': 'Dr. Evans teaches the advanced research methods course.',
                         'B': 'Did you spot an error in one of the spreadsheet columns?',
                         'C': 'How many students ended up responding to the survey?',
                         'D': 'The file was saved in the shared folder yesterday.'},
             'correct': 'B',
             'explanation': "A estrutura <em>I'd double-check those survey numbers... if I were you</em> funciona "
                            'como um alerta indireto de que algo parece errado nos dados, por isso (B) reage na hora '
                            'perguntando se houve um <strong>erro específico na planilha</strong>. A opção (C) '
                            'também faz uma pergunta sobre a pesquisa, mas ignora completamente o aviso de revisão.'},
            {'num': 'A26',
             'prompt': '"Wait, so our funding proposal for the robotics project is still up in the air?"',
             'options': {'A': "The robotics team won second place at last year's fair.",
                         'B': 'Our project focuses on small aerial drones for mapping.',
                         'C': 'Yeah, the committee postponed its final vote until Monday.',
                         'D': 'The funding form needs to be signed in blue or black ink.'},
             'correct': 'C',
             'explanation': 'Na pergunta <em>so our funding proposal for the robotics project is still up in the '
                            'air?</em>, a expressão <em>up in the air</em> significa indefinido, o que (C) confirma '
                            'ao explicar o <strong>adiamento da votação final</strong>. A alternativa (B) é uma '
                            'armadilha clássica porque leva <em>in the air</em> ao pé da letra e fala de drones '
                            'aéreos.'},
            {'num': 'A27',
             'prompt': '"I was under the impression that the internship required a letter from the dean."',
             'options': {'A': "The dean's office moved to the administration building.",
                         'B': 'Internships are a great way to build work experience.',
                         'C': 'I wrote a cover letter for that position last night.',
                         'D': 'Actually, they dropped that requirement this year.'},
             'correct': 'D',
             'explanation': 'A abertura <em>I was under the impression that...</em> indica uma suposição que pede '
                            'confirmação ou correção, e (D) corrige a suposição ao contar que <strong>a exigência '
                            'caiu</strong> este ano. A opção (C) repete a palavra <em>letter</em>, mas troca a carta '
                            'da direção por uma carta de apresentação pessoal.'},
            {'num': 'A28',
             'prompt': '"We\'d better iron out the timeline for our lab experiment before we meet with the TA."',
             'options': {'A': "Agreed, let's sit down after lunch and map out each step.",
                         'B': 'The lab equipment is made of stainless steel and iron.',
                         'C': 'Our teaching assistant holds office hours on Wednesdays.',
                         'D': 'The experiment took much longer than anyone expected.'},
             'correct': 'A',
             'explanation': "Em <em>We'd better iron out the timeline for our lab experiment</em>, o phrasal verb "
                            '<em>iron out</em> quer dizer acertar os detalhes pendentes, e (A) concorda propondo '
                            '<strong>definir cada etapa depois do almoço</strong>. A alternativa (B) cai na '
                            'armadilha literal de <em>iron</em> como ferro ou metal do equipamento.'},
            {'num': 'A29',
             'prompt': '"You didn\'t happen to pick up an extra copy of the syllabus on your way out, did you?"',
             'options': {'A': 'The syllabus lists three major papers for this semester.',
                         'B': 'I dropped that class during the first week of the term.',
                         'C': 'No, sorry, but the professor posted the PDF online too.',
                         'D': 'The copy machine in the department lounge is working.'},
             'correct': 'C',
             'explanation': "A pergunta <em>You didn't happen to pick up an extra copy of the syllabus... did "
                            'you?</em> é um jeito educado de pedir uma cópia caso a pessoa tenha pego uma a mais, e '
                            '(C) responde e <strong>indica a versão em PDF online</strong>. A opção (D) aproveita a '
                            'palavra <em>copy</em> para falar da copiadora, sem responder ao pedido.'},
            {'num': 'A30',
             'prompt': '"Getting a summer research grant as a first-year student is a bit of a long shot, isn\'t '
                       'it?"',
             'options': {'A': 'Maybe, but a couple of freshmen got funded last summer.',
                         'B': 'The photography club is taking shots of the campus quad.',
                         'C': 'Summer classes run from early June through mid-August.',
                         'D': 'Grant applications must be submitted to the main office.'},
             'correct': 'A',
             'explanation': 'Quando quem fala diz que conseguir a bolsa no primeiro ano é <em>a bit of a long '
                            'shot</em>, quer dizer que a chance parece baixa, e (A) reconhece a dificuldade mas '
                            '<strong>anima com exemplos reais</strong> do verão passado. A alternativa (B) '
                            'interpreta <em>shot</em> ao pé da letra como foto, fugindo do assunto.'}]},
 {'id': 'mod2-an4',
  'title': 'Exercício A5: pesquisa, orientação e seminários (meta de 1 min)',
  'level': 'C1',
  'objective': 'Ouça cada fala e escolha a resposta mais natural. A fala aparece escrita depois que você responde. '
               'Tempo-alvo: 12 segundos por item.',
  'passage_html': None,
  'items': [{'num': 'A31',
             'prompt': '"Well, the peer reviewers didn\'t exactly jump for joy over our methodology section."',
             'options': {'A': 'The methodology section comes right after the introduction.',
                         'B': "I'm glad the reviewers were so enthusiastic about our work.",
                         'C': 'Peer review for that journal usually takes about six weeks.',
                         'D': "That's rough, but hopefully their comments are easy to fix."},
             'correct': 'D',
             'explanation': "Ao dizer que os pareceristas <em>didn't exactly jump for joy over our methodology "
                            'section</em>, quem fala usa uma atenuação irônica para contar que a seção recebeu '
                            'críticas, e (D) capta esse tom ao <strong>lamentar o revés e focar nos '
                            "ajustes</strong>. A opção (B) perde a ironia do <em>didn't exactly</em> e acha que o "
                            'retorno foi entusiasmado.'},
            {'num': 'A32',
             'prompt': '"Since our archive access was denied, I guess we\'re back to square one on the thesis '
                       'topic."',
             'options': {'A': 'Not necessarily, we could use the digitized collection instead.',
                         'B': 'The main archive is located in the basement of the old library.',
                         'C': 'Square tables work best when we have a large seminar discussion.',
                         'D': 'Our thesis advisor approved the initial outline two months ago.'},
             'correct': 'A',
             'explanation': "Em <em>I guess we're back to square one on the thesis topic</em>, a expressão <em>back "
                            'to square one</em> indica a sensação de ter de recomeçar do zero, e (A) responde '
                            'propondo uma <strong>alternativa viável com o acervo digitalizado</strong>. A opção (D) '
                            'cita a aprovação antiga do esboço e ignora o bloqueio atual ao arquivo.'},
            {'num': 'A33',
             'prompt': '"Had I known Professor Kim\'s seminar was this heavy on econometrics, I\'d have audited it '
                       'instead."',
             'options': {'A': 'Professor Kim earned her doctorate in economics ten years ago.',
                         'B': "The add-drop window's still open if you want to switch status.",
                         'C': "Auditing a course means you don't receive a letter grade for it.",
                         'D': 'The seminar meets twice a week in the graduate wing downstairs.'},
             'correct': 'B',
             'explanation': "A inversão condicional <em>Had I known... I'd have audited it instead</em> expressa "
                            'arrependimento por não cursar a disciplina apenas como ouvinte, e (B) traz uma saída '
                            'prática lembrando que o <strong>prazo de ajuste ainda permite mudar</strong> a '
                            'modalidade. A alternativa (C) explica o que é <em>audit</em>, algo que quem fala já '
                            'domina.'},
            {'num': 'A34',
             'prompt': '"Look, far be it from me to tell you how to structure your talk, but ten case studies in '
                       'fifteen minutes?"',
             'options': {'A': 'The conference panel allots fifteen minutes to each presenter.',
                         'B': 'Case studies are widely used in qualitative social research.',
                         'C': 'Fair point, I should probably trim it down to two or three.',
                         'D': 'Your presentation last semester was really well structured.'},
             'correct': 'C',
             'explanation': 'Mesmo suavizada por <em>far be it from me</em>, a pergunta final <em>but ten case '
                            'studies in fifteen minutes?</em> é uma crítica educada ao excesso de exemplos para '
                            'pouco tempo, e (C) entende o recado ao <strong>reduzir a quantidade de casos</strong>. '
                            'A opção (A) apenas repete a regra dos quinze minutos sem resolver a sobrecarga.'},
            {'num': 'A35',
             'prompt': '"Take what the department chair said about next year\'s teaching fellowships with a grain of '
                       'salt."',
             'options': {'A': "The department chair's term ends after the spring semester.",
                         'B': 'Teaching fellowships cover full tuition plus a small stipend.',
                         'C': 'The campus dining hall cut back on salt in most of its meals.',
                         'D': "Right, nothing's official until the budget is signed in May."},
             'correct': 'D',
             'explanation': 'A expressão <em>take... with a grain of salt</em> recomenda cautela diante do que foi '
                            'dito sobre as bolsas de monitoria, e (D) acompanha esse cuidado lembrando que '
                            '<strong>nada é oficial antes da assinatura do orçamento</strong>. A alternativa (B) '
                            'descreve os benefícios da bolsa, mas ignora o alerta de incerteza.'},
            {'num': 'A36',
             'prompt': '"I wouldn\'t put off booking the spectrometer if you want your samples analyzed before the '
                       'colloquium."',
             'options': {'A': 'The annual colloquium features speakers from three universities.',
                         'B': 'True, the lab sign-up sheet always fills up weeks in advance.',
                         'C': 'I put the spectrometer manual back on the top shelf yesterday.',
                         'D': 'The rock samples were collected during our field trip in June.'},
             'correct': 'B',
             'explanation': "Em <em>I wouldn't put off booking the spectrometer</em>, o phrasal verb <em>put "
                            'off</em> significa adiar, então a fala aconselha a reservar o aparelho logo, e (B) '
                            'concorda lembrando que a <strong>agenda do equipamento lota semanas antes</strong>. A '
                            'opção (C) confunde <em>put off</em> com guardar um manual na estante.'}]}]
MOD2_ACTION_DRILLS_A = MOD2_ACTION_DRILLS_A + MOD2_NOVOS_A
MOD2_NOVOS_B = [{'id': 'mod2-bn1',
  'title': 'Exercício B4: Campus Health Clinic (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and a receptionist at the campus '
                  'health clinic.</em></p>\n'
                  '<p><strong>Student:</strong> Hi, um, I need a nurse to sign this health form for my summer '
                  'volunteer program. Can I do that today?</p>\n'
                  "<p><strong>Receptionist:</strong> Let's see. Have you uploaded your vaccination record to the "
                  'student health portal yet?</p>\n'
                  '<p><strong>Student:</strong> Oh, no, I brought the paper copy with me right here.</p>\n'
                  "<p><strong>Receptionist:</strong> Well, our nurses can't sign the form until the file is in the "
                  'system. You can scan it with your phone and upload it tonight.</p>\n'
                  "<p><strong>Student:</strong> Okay, that's easy enough. Do I need an appointment after I upload "
                  'it?</p>\n'
                  '<p><strong>Receptionist:</strong> No, just come back during walk-in hours tomorrow morning '
                  'between nine and eleven, and a nurse will sign it at the front desk.</p>',
  'items': [{'num': 'B4.1',
             'prompt': 'Gist-purpose. Why does the student go to the campus health clinic?',
             'options': {'A': 'To get a signature on a required health form',
                         'B': 'To schedule a vaccination before summer break',
                         'C': 'To pick up a paper copy of her medical record',
                         'D': 'To apply for a part-time job at the front desk'},
             'correct': 'A',
             'explanation': 'Logo no começo, a estudante explica que precisa que alguém assine o formulário do '
                            'programa de voluntariado (<em>I need a nurse to sign this health form</em>), o que '
                            'confirma a opção (A) como <strong>pedido de assinatura no documento</strong>. Se você '
                            'pensou em (B), repare que ela já tomou as vacinas e trouxe o comprovante impresso, sem '
                            'pedir aplicação nova.'},
            {'num': 'B4.2',
             'prompt': 'Detail. What must the student do before a nurse can sign her form?',
             'options': {'A': 'Pay a processing fee at the main office',
                         'B': 'Book an afternoon appointment with a doctor',
                         'C': 'Upload her vaccination record to the online portal',
                         'D': 'Request a new paper form from her program director'},
             'correct': 'C',
             'explanation': 'O recepcionista avisa que a assinatura só é feita depois que o comprovante estiver no '
                            'sistema (<em>until the file is in the system</em> e <em>upload it tonight</em>), '
                            'validando (C) como <strong>envio digital na plataforma</strong>. A alternativa (B) é '
                            'uma armadilha porque fala em agendar horário, mas o funcionário diz claramente <em>No, '
                            'just come back during walk-in hours</em>.'}]},
 {'id': 'mod2-bn2',
  'title': 'Exercício B5: Dining Services Office (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and a staff member at the dining '
                  'services office.</em></p>\n'
                  '<p><strong>Student:</strong> Excuse me, I have a question about my campus meal plan. The semester '
                  'ends in two weeks, and I still have fifteen lunches left.</p>\n'
                  '<p><strong>Staff Member:</strong> Are you on the weekly plan or the semester block plan?</p>\n'
                  '<p><strong>Student:</strong> Um, the semester block plan, I think. I paid for a hundred meals at '
                  'the start of the term.</p>\n'
                  "<p><strong>Staff Member:</strong> Good news, then. Unused block meals don't expire until the last "
                  'day of final exams, and you can also trade up to ten of them for coffee shop points.</p>\n'
                  '<p><strong>Student:</strong> Oh, nice! I use the library café every morning anyway. How do I make '
                  'that switch?</p>\n'
                  '<p><strong>Staff Member:</strong> Just tap the transfer button in the campus dining app, and the '
                  'points show up on your ID card right away.</p>',
  'items': [{'num': 'B5.1',
             'prompt': "Detail. What does the staff member say about the student's unused meals?",
             'options': {'A': 'They can be refunded for cash at the end of the term',
                         'B': 'They expire two weeks before final exams begin',
                         'C': "They are automatically moved to next semester's balance",
                         'D': 'They can be partly converted into coffee shop points'},
             'correct': 'D',
             'explanation': 'A funcionária explica que o aluno pode trocar até dez refeições restantes por pontos de '
                            'cafeteria (<em>you can also trade up to ten of them for coffee shop points</em>), o que '
                            'torna (D) a <strong>conversão parcial em pontos</strong>. A opção (B) confunde o prazo '
                            'de duas semanas citado pelo aluno com a regra real, que vale até o último dia de provas '
                            'finais.'},
            {'num': 'B5.2',
             'prompt': 'Inference. What will the student probably do next?',
             'options': {'A': 'Cancel his meal plan for the rest of the semester',
                         'B': 'Use the campus dining app to convert some meals',
                         'C': 'Buy a new student ID card at the library café',
                         'D': 'Switch from the block plan to the weekly plan'},
             'correct': 'B',
             'explanation': 'O estudante se anima porque usa a cafeteria da biblioteca toda manhã e pergunta como '
                            'fazer a troca, e a funcionária orienta <em>Just tap the transfer button in the campus '
                            'dining app</em>, indicando em (B) o <strong>uso do aplicativo para converter '
                            'refeições</strong>. A alternativa (C) mistura termos do áudio, pois os pontos caem no '
                            'cartão que ele já tem.'}]},
 {'id': 'mod2-bn3',
  'title': 'Exercício B6: Media Equipment Desk (meta de 2 min)',
  'level': 'A2–B1',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and an assistant at the media '
                  'equipment desk.</em></p>\n'
                  "<p><strong>Student:</strong> Hi, I'm recording an interview for my sociology class this "
                  'afternoon. Do you have a small clip-on microphone I can borrow?</p>\n'
                  '<p><strong>Assistant:</strong> Let me check the shelf... sorry, all our clip-on mics are checked '
                  'out until tomorrow. We do have a handheld digital recorder, though.</p>\n'
                  "<p><strong>Student:</strong> Hmm, we're meeting on a bench outside the student union, so I'm "
                  'worried about wind noise.</p>\n'
                  '<p><strong>Assistant:</strong> Actually, this recorder comes with a foam cover that blocks the '
                  'wind pretty well. You just set it down on the bench between you and your guest.</p>\n'
                  "<p><strong>Student:</strong> Oh, great, that'll work. How long can I keep it?</p>\n"
                  "<p><strong>Assistant:</strong> It's due back by four p.m. tomorrow. Make sure you check the "
                  'battery icon on the screen before you start recording.</p>',
  'items': [{'num': 'B6.1',
             'prompt': "Detail. Why can't the student borrow a clip-on microphone today?",
             'options': {'A': 'They are reserved for sociology professors only',
                         'B': 'They are broken and waiting for repair parts',
                         'C': 'They have all been borrowed by other people',
                         'D': 'They cannot be used outside the library building'},
             'correct': 'C',
             'explanation': 'O atendente confere a prateleira e avisa que todos os microfones de lapela estão '
                            'emprestados até o dia seguinte (<em>all our clip-on mics are checked out until '
                            'tomorrow</em>), confirmando (C) como <strong>equipamentos já retirados</strong>. A '
                            'opção (A) usa a aula de sociologia mencionada pelo aluno para criar uma restrição que '
                            'não existe no diálogo.'},
            {'num': 'B6.2',
             'prompt': 'Function. Why does the assistant mention the foam cover?',
             'options': {'A': 'To explain why the rental costs a few dollars extra',
                         'B': 'To warn the student not to drop the recorder on the ground',
                         'C': 'To show how to tell two similar models apart on the shelf',
                         'D': 'To reassure the student that the recorder will handle the wind'},
             'correct': 'D',
             'explanation': 'O assistente cita a proteção de espuma (<em>this recorder comes with a foam cover that '
                            'blocks the wind pretty well</em>) justamente para responder à preocupação do aluno e '
                            '<strong>mostrar que o aparelho reduz o vento</strong>, como diz (D). A alternativa (B) '
                            'pensa em proteção física contra queda, mas o foco ali é a qualidade do som.'}]},
 {'id': 'mod2-bn4',
  'title': 'Exercício B7: Undergraduate Research Symposium (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and the coordinator of a campus '
                  'research event.</em></p>\n'
                  '<p><strong>Student:</strong> Hi, Dr. Patel. My lab partner and I were accepted to present our '
                  "chemistry poster at next month's research symposium, but we just ran into a scheduling "
                  'issue.</p>\n'
                  '<p><strong>Coordinator:</strong> Oh? What happened?</p>\n'
                  '<p><strong>Student:</strong> Well, my partner was invited to a regional debate tournament that '
                  "same weekend, so she won't be on campus. Do we have to withdraw our poster if only one of us can "
                  'attend?</p>\n'
                  '<p><strong>Coordinator:</strong> Not at all. Plenty of co-authored posters are presented by a '
                  "single student. As long as her name stays on the printed header and the abstract, you're fine to "
                  'present solo.</p>\n'
                  "<p><strong>Student:</strong> That's a huge relief. One more thing, though. I have a Friday "
                  "afternoon lab that I can't miss. Can I request a morning presentation slot?</p>\n"
                  "<p><strong>Coordinator:</strong> Sure, we haven't finalized the room assignments yet. Send me an "
                  'email by Wednesday so I can put you in the nine-to-eleven session before the program goes to '
                  'print.</p>',
  'items': [{'num': 'B7.1',
             'prompt': 'Gist-purpose. Why did the student go to see the coordinator?',
             'options': {'A': 'To ask for extra time to finish a chemistry experiment',
                         'B': 'To find out if she can present a joint poster by herself',
                         'C': 'To add a new co-author to her research abstract',
                         'D': "To reserve a larger display board for her team's graphs"},
             'correct': 'B',
             'explanation': 'A aluna procura o coordenador porque a parceira viajará no fim de semana do evento e '
                            'quer saber se precisa cancelar o pôster ou se pode apresentar sozinha (<em>Do we have '
                            'to withdraw our poster if only one of us can attend?</em>), confirmando (B) como '
                            '<strong>dúvida sobre apresentação individual</strong>. A opção (C) fala em incluir '
                            'coautor, mas o nome da colega já estava no trabalho.'},
            {'num': 'B7.2',
             'prompt': 'Detail. Why does the coordinator ask the student to email him by Wednesday?',
             'options': {'A': 'So the chemistry department can approve her lab absence',
                         'B': 'So her partner can receive a travel grant for the tournament',
                         'C': 'So the print shop has time to enlarge her poster header',
                         'D': 'So he can give her a morning slot before the program is printed'},
             'correct': 'D',
             'explanation': 'No final da conversa, o coordenador pede o e-mail até quarta-feira para colocá-la no '
                            'turno da manhã antes da impressão do folheto (<em>so I can put you in the '
                            'nine-to-eleven session before the program goes to print</em>), o que corresponde a (D) '
                            'sobre <strong>garantir o horário matutino no programa</strong>. A alternativa (C) '
                            'mistura a palavra <em>print</em> com o cabeçalho do pôster citado antes.'}]},
 {'id': 'mod2-bn5',
  'title': 'Exercício B8: Environmental Science Office Hours (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and an environmental science '
                  'professor.</em></p>\n'
                  "<p><strong>Student:</strong> Professor Morales, do you have a minute? I'm worried about my field "
                  'report on creek water quality.</p>\n'
                  "<p><strong>Professor:</strong> Come on in, Leo. Didn't you plan to compare water samples from the "
                  'wooded bend and the downstream bridge?</p>\n'
                  "<p><strong>Student:</strong> That was the plan, yeah, but after Tuesday's heavy rain, the trail "
                  'to the wooded bend was completely flooded. Park rangers closed it for the rest of the month, so I '
                  'only have data from the bridge.</p>\n'
                  "<p><strong>Professor:</strong> Ah, I heard the creek rose quite a bit. Well, you don't need two "
                  'locations to write a strong paper. Why not pivot to a before-and-after study at the bridge site '
                  'alone?</p>\n'
                  '<p><strong>Student:</strong> Wait, how would that work? I only started collecting samples there '
                  'last week.</p>\n'
                  '<p><strong>Professor:</strong> The county water board has an automated sensor right under that '
                  'bridge. Their website posts hourly turbidity and oxygen readings going back five years, so you '
                  'can compare your post-storm samples with the baseline data from earlier this autumn.</p>\n'
                  '<p><strong>Student:</strong> Oh, I had no idea that archive was public! That actually gives me a '
                  'much clearer research question.</p>',
  'items': [{'num': 'B8.1',
             'prompt': 'Detail. What problem prevented the student from carrying out his original plan?',
             'options': {'A': 'Heavy rain flooded the path and closed one of his sampling sites',
                         'B': 'The testing equipment at the downstream bridge stopped working',
                         'C': 'The county water board restricted student access to the creek',
                         'D': 'His initial water samples were lost in the laboratory freezer'},
             'correct': 'A',
             'explanation': 'O estudante conta que a chuva forte alagou a trilha e levou os guardas-parque a '
                            "fecharem um dos pontos de coleta (<em>after Tuesday's heavy rain, the trail to the "
                            'wooded bend was completely flooded</em>), confirmando (A) como <strong>interdição da '
                            'trilha pela chuva</strong>. A opção (C) usa o nome do órgão municipal citado depois '
                            'pela professora para criar uma proibição inexistente.'},
            {'num': 'B8.2',
             'prompt': 'Detail. How does the professor suggest the student complete his report?',
             'options': {'A': 'By waiting until next month when the wooded trail reopens',
                         'B': "By borrowing water samples collected by last year's class",
                         'C': 'By combining his bridge samples with online county sensor records',
                         'D': 'By switching his topic from water quality to forest soil erosion'},
             'correct': 'C',
             'explanation': 'A professora sugere focar na ponte e cruzar as amostras pós-tempestade com os dados '
                            'públicos do sensor do condado (<em>compare your post-storm samples with the baseline '
                            'data from earlier this autumn</em>), o que valida (C) como <strong>uso complementar do '
                            'arquivo online</strong>. Se você pensou em (A), repare que a professora propõe '
                            'trabalhar com o que já existe, sem esperar a trilha reabrir.'}]},
 {'id': 'mod2-bn6',
  'title': 'Exercício B9: Study Abroad Office (meta de 3 min)',
  'level': 'B1–B2',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and a study-abroad advisor.</em></p>\n'
                  "<p><strong>Student:</strong> Hi, I'm applying for the six-week tropical ecology program in Costa "
                  'Rica this summer, and I wanted to check how the credits transfer back here.</p>\n'
                  '<p><strong>Advisor:</strong> Sure. Because that program is run by one of our partner '
                  'universities, the six credits transfer automatically as general elective hours.</p>\n'
                  '<p><strong>Student:</strong> Oh, wait. I was counting on using it to fulfill my upper-level '
                  'biology lab requirement so I can graduate on time next spring.</p>\n'
                  "<p><strong>Advisor:</strong> In that case, automatic transfer won't be enough. You'll need a "
                  'course-equivalency approval from the chair of our biology department, Dr. Lindqvist.</p>\n'
                  '<p><strong>Student:</strong> Okay, what does she usually ask to see? The short course description '
                  'on the brochure?</p>\n'
                  "<p><strong>Advisor:</strong> Actually, she's pretty thorough. A brochure blurb won't cut it. "
                  "She'll want the full weekly syllabus showing the exact number of field and lab hours, plus how "
                  'students are graded.</p>\n'
                  "<p><strong>Student:</strong> Good to know. The program deposit isn't due until next Friday, so "
                  "I'll request the detailed syllabus from the host coordinator today.</p>",
  'items': [{'num': 'B9.1',
             'prompt': 'Meaning of an expression. What does the advisor mean when he says "A brochure blurb won\'t '
                       'cut it"?',
             'options': {'A': 'A brief summary from the brochure will not be detailed enough',
                         'B': 'The printed brochure contains outdated information about the lab',
                         'C': 'The student should not clip pages out of the official catalog',
                         'D': 'The biology department no longer accepts summer field courses'},
             'correct': 'A',
             'explanation': "A expressão coloquial <em>won't cut it</em> significa que algo não basta, e o "
                            'orientador explica logo depois que a chefe do departamento exige o cronograma completo '
                            "de horas práticas (<em>She'll want the full weekly syllabus</em>), validando (A) como "
                            '<strong>insuficiência do resumo do folheto</strong>. A alternativa (C) leva o verbo '
                            '<em>cut</em> ao pé da letra, como recortar papel.'},
            {'num': 'B9.2',
             'prompt': 'Inference. What will the student probably do before paying the program deposit?',
             'options': {'A': 'Switch to a domestic summer course offered on campus',
                         'B': 'Ask the financial aid office to waive the deposit fee',
                         'C': 'Take an extra biology lab during the current semester',
                         'D': "Get the detailed syllabus and seek Dr. Lindqvist's approval"},
             'correct': 'D',
             'explanation': 'Como o depósito só vence na sexta-feira seguinte, o aluno decide pedir a ementa '
                            "detalhada imediatamente (<em>I'll request the detailed syllabus from the host "
                            'coordinator today</em>) para submeter à chefe do departamento, o que aponta para (D) '
                            'como <strong>obtenção da ementa e aprovação prévia</strong>. A opção (A) desiste do '
                            'intercâmbio sem que o aluno demonstre essa intenção.'}]},
 {'id': 'mod2-bn7',
  'title': 'Exercício B10: Architecture Studio Critique (meta de 3 min)',
  'level': 'B2–C1',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and an architecture professor after a '
                  'studio review.</em></p>\n'
                  '<p><strong>Student:</strong> Professor Vance, thanks for staying a few minutes. After the guest '
                  "panel's critique of my community center model, I'm torn about how to revise the central atrium "
                  'for the final portfolio.</p>\n'
                  "<p><strong>Professor:</strong> You shouldn't feel discouraged, Maya. The visiting architects were "
                  'genuinely impressed by how your sawtooth roof brings diffused northern light deep into the '
                  'building.</p>\n'
                  '<p><strong>Student:</strong> Right, they liked the daylighting, but they pointed out that placing '
                  'the quiet reading lounge directly off the open atrium would create an acoustic nightmare whenever '
                  'groups gather downstairs.</p>\n'
                  "<p><strong>Professor:</strong> And that's a fair critique. Concrete floors and glass balustrades "
                  "bounce sound around. But you don't have to wall off the reading lounge and lose the visual "
                  'openness that makes your design work.</p>\n'
                  '<p><strong>Student:</strong> You mean I can keep the sightlines without enclosing the second '
                  'floor in glass partitions?</p>\n'
                  '<p><strong>Professor:</strong> Exactly. Look into suspended timber baffles along the atrium '
                  'ceiling and a recessed alcove with fabric wall panels for the reading area. They absorb mid-range '
                  'chatter before it travels upward, so the space stays visually connected without functioning like '
                  'an echo chamber.</p>',
  'items': [{'num': 'B10.1',
             'prompt': 'Function. Why does the professor mention concrete floors and glass balustrades?',
             'options': {'A': 'To encourage the student to replace all glass with brick walls',
                         'B': "To explain why the panel's concern about noise was reasonable",
                         'C': 'To show that the building meets local fire safety regulations',
                         'D': 'To suggest materials that would make the model easier to build'},
             'correct': 'B',
             'explanation': "Logo após dizer <em>And that's a fair critique</em>, o professor cita o piso de "
                            'concreto e os guarda-corpos de vidro porque esses materiais refletem o som (<em>bounce '
                            'sound around</em>), justificando em (B) <strong>por que a crítica acústica fazia '
                            'sentido</strong>. Se você marcou (A), repare que ele desaconselha fechar o espaço com '
                            'paredes logo na frase seguinte.'},
            {'num': 'B10.2',
             'prompt': "Detail. How will the timber baffles and fabric panels solve the student's dilemma?",
             'options': {'A': 'They will dampen noise while preserving the open view across the atrium',
                         'B': 'They will reflect additional sunlight into the downstairs gathering area',
                         'C': 'They will divide the reading lounge into private individual study cubicles',
                         'D': 'They will support the weight of the sawtooth roof without steel columns'},
             'correct': 'A',
             'explanation': 'O professor propõe os defletores de madeira e painéis de tecido porque absorvem as '
                            'vozes mantendo o espaço integrado visualmente (<em>absorb mid-range chatter... so the '
                            'space stays visually connected</em>), validando (A) como <strong>redução de ruído sem '
                            'perder a amplitude visual</strong>. A alternativa (C) sugere fechar a área em cabines, '
                            'exatamente o que a aluna queria evitar.'}]},
 {'id': 'mod2-bn8',
  'title': 'Exercício B11: Economic History Seminar (meta de 3 min)',
  'level': 'C1',
  'objective': 'Ouça a conversa e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to a conversation between a student and an economic history '
                  'professor.</em></p>\n'
                  "<p><strong>Student:</strong> Professor Calloway, I've been going through the digitized county tax "
                  "rolls from the 1880s for my senior thesis on New England textile towns, and the numbers aren't "
                  'lining up with what we read in seminar.</p>\n'
                  "<p><strong>Professor:</strong> Let me guess. The tax assessments make mill workers' household "
                  'incomes look surprisingly stable, even during the downturn of 1884?</p>\n'
                  '<p><strong>Student:</strong> Exactly! Contemporary newspaper accounts describe widespread '
                  'layoffs, yet the municipal tax records barely register a dip. Was the press exaggerating?</p>\n'
                  '<p><strong>Professor:</strong> Not necessarily. Think about who actually appears on a '
                  'nineteenth-century property and poll-tax roll. Long-term residents who owned modest cottages or '
                  'stayed at the same address year-round were recorded, whereas transient operatives and seasonal '
                  "spinners who left town when looms shut down simply vanished from the assessor's ledger.</p>\n"
                  "<p><strong>Student:</strong> Oh, I see. So by relying solely on the tax rolls, I'm only looking "
                  'at the best-off segment of the workforce that weathered the slump.</p>\n'
                  "<p><strong>Professor:</strong> Precisely, it's a classic survivorship bias. If you want to "
                  'capture the full picture, pair those municipal rolls with the Abbott Mill weekly payroll books in '
                  "our library's special collections. Those list every piece-rate worker by week, including the ones "
                  'who disappeared mid-season.</p>',
  'items': [{'num': 'B11.1',
             'prompt': 'Detail. According to the professor, why do the county tax rolls make incomes appear stable '
                       'in 1884?',
             'options': {'A': 'Town officials inflated wage figures to attract outside factory investment',
                         'B': 'Mill owners continued paying full wages to workers during temporary shutdowns',
                         'C': 'Seasonal workers who lost their jobs left town and were omitted from the rolls',
                         'D': 'Tax assessors combined factory wages with agricultural earnings from nearby farms'},
             'correct': 'C',
             'explanation': 'A professora esclarece que os registros municipais incluíam moradores fixos, enquanto '
                            'trabalhadores temporários que partiam na crise ficavam de fora (<em>transient '
                            'operatives and seasonal spinners who left town when looms shut down simply vanished '
                            "from the assessor's ledger</em>), validando (C) como <strong>omissão dos trabalhadores "
                            'sazonais nos impostos</strong>. A alternativa (B) contradiz as demissões relatadas nos '
                            'jornais.'},
            {'num': 'B11.2',
             'prompt': 'Function. Why does the professor recommend examining the Abbott Mill payroll books?',
             'options': {'A': 'To prove that nineteenth-century newspapers fabricated stories about strikes',
                         'B': 'To provide weekly records that include short-term workers missing from tax rolls',
                         'C': 'To show how factory managers calculated property taxes for mill cottages',
                         'D': 'To replace primary archival sources with modern economic commentary'},
             'correct': 'B',
             'explanation': 'Para corrigir o viés de seleção, a professora recomenda os livros de pagamento da '
                            'fábrica porque eles registram todos os operários semana a semana, inclusive quem saía '
                            'no meio da estação (<em>Those list every piece-rate worker by week, including the ones '
                            'who disappeared mid-season</em>), confirmando (B) como <strong>fonte que inclui a mão '
                            'de obra temporária</strong>. A opção (A) inverte o argumento, já que os livros '
                            'confirmam a crise.'}]}]
MOD2_ACTION_DRILLS_B = MOD2_ACTION_DRILLS_B + MOD2_NOVOS_B
MOD2_NOVOS_C = [{'id': 'mod2-cn1',
  'title': 'Exercício C4: Biology Lab (meta de 1 min)',
  'level': 'A2–B1',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 1 minuto.',
  'passage_html': '<p><em>Narrator: Listen to an announcement at the end of a biology class.</em></p>\n'
                  '<p><strong>Instructor:</strong> Okay, everyone, before you pack up, just a quick change for '
                  "Friday's lab. We're not meeting in Room 204 this week. Instead, we'll meet directly at the campus "
                  "greenhouse, right behind the science building. Because we're only observing plant samples and "
                  "sketching them, you don't need to bring your lab coats or safety goggles this time. Just bring "
                  "your field notebook and a pencil. Oh, and please be there by ten o'clock sharp, because the "
                  'greenhouse staff will lock the side door right after we start.</p>',
  'items': [{'num': 'C4.1',
             'prompt': "Detail. What should students bring to Friday's class?",
             'options': {'A': 'A field notebook and a pencil for sketching',
                         'B': 'A white lab coat and a pair of safety goggles',
                         'C': 'A set of plant samples from the science building',
                         'D': 'A key card to unlock the greenhouse side door'},
             'correct': 'A',
             'explanation': 'O instrutor avisa que a atividade será observar e desenhar plantas, por isso pede '
                            'apenas caderno de campo e lápis: "Just bring your field notebook and a pencil." Um '
                            'ponto de atenção é (B), que junta dois itens citados no áudio, mas o professor diz '
                            'justamente que você <strong>não precisa</strong> trazê-los desta vez.'},
            {'num': 'C4.2',
             'prompt': 'Function. Why does the instructor mention the greenhouse staff?',
             'options': {'A': "To introduce the guest speakers for Friday's class",
                         'B': 'To tell students who will grade their field sketches',
                         'C': 'To explain why students need to arrive right on time',
                         'D': 'To remind students where to pick up their lab coats'},
             'correct': 'C',
             'explanation': 'O professor menciona a equipe da estufa para justificar por que você precisa chegar '
                            'pontualmente às dez horas: "please be there by ten o\'clock sharp, because the '
                            'greenhouse staff will lock the side door right after we start." A alternativa (A) é uma '
                            'armadilha comum: a equipe trabalha no local, mas o áudio não diz que ela dará uma '
                            '<strong>palestra</strong>.'}]},
 {'id': 'mod2-cn2',
  'title': 'Exercício C5: Dormitory Laundry Room (meta de 1 min)',
  'level': 'A2–B1',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 1 minuto.',
  'passage_html': '<p><em>Narrator: Listen to an announcement from a resident advisor in a student '
                  'dormitory.</em></p>\n'
                  '<p><strong>Resident Advisor:</strong> Hi, everyone. I just wanted to let you know that our '
                  'basement laundry room will be closed all weekend, starting Friday at six p.m. Facilities is '
                  "installing new card readers on the machines, so you won't need coins anymore starting Monday. If "
                  'you need to wash clothes on Saturday or Sunday, you can use the laundry room in Maple Hall next '
                  'door. Your student ID card will open their side entrance. Also, please clear out any clothes left '
                  'in the basement before Friday evening, or the crew will move them to the front desk.</p>',
  'items': [{'num': 'C5.1',
             'prompt': 'Gist-purpose. What is the main purpose of the announcement?',
             'options': {'A': 'To explain a permanent increase in dormitory laundry prices',
                         'B': 'To welcome new residents moving into Maple Hall this week',
                         'C': 'To remind students to pick up their new student ID cards',
                         'D': 'To inform residents about a temporary laundry room closure'},
             'correct': 'D',
             'explanation': 'O objetivo central do aviso é informar que a lavanderia do prédio ficará fechada no fim '
                            'de semana para uma atualização: "our basement laundry room will be closed all weekend." '
                            'A opção (C) pode atrair porque o cartão de estudante é citado, mas ele serve apenas '
                            'para abrir a porta do prédio vizinho, sem emissão de um <strong>cartão novo</strong>.'},
            {'num': 'C5.2',
             'prompt': 'Detail. What will happen to clothes left in the basement after Friday at 6 p.m.?',
             'options': {'A': 'They will be sent to the laundry room in Maple Hall',
                         'B': 'They will be taken to the front desk by the work crew',
                         'C': 'They will be locked inside the basement until Monday',
                         'D': 'They will be washed for free on the new card machines'},
             'correct': 'B',
             'explanation': 'O aviso final é direto sobre as roupas esquecidas na lavanderia: "please clear out any '
                            'clothes left in the basement before Friday evening, or the crew will move them to the '
                            'front desk." Cuidado com (A), que mistura o destino das roupas esquecidas com a '
                            '<strong>alternativa de uso</strong> em Maple Hall durante o fim de semana.'}]},
 {'id': 'mod2-cn3',
  'title': 'Exercício C6: Intramural Soccer Sign-Ups (meta de 1 min)',
  'level': 'A2–B1',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 1 minuto.',
  'passage_html': '<p><em>Narrator: Listen to an announcement at the campus recreation center.</em></p>\n'
                  "<p><strong>Coordinator:</strong> Attention, everyone! If you're planning to play in the campus "
                  'soccer league this fall, remember that registration closes this Friday at five p.m. Each team '
                  "needs at least seven players on its roster. Now, if you want to play but don't have a full group "
                  "of friends to form a team, don't worry. You can still sign up by yourself as an individual player "
                  "on the rec center website, and we'll place you on a team that needs extra people. The game "
                  'schedule comes out on Monday morning, and matches start next Wednesday evening.</p>',
  'items': [{'num': 'C6.1',
             'prompt': 'Detail. What should a student without a full team do to join the league?',
             'options': {'A': 'Wait until the game schedule comes out on Monday morning',
                         'B': 'Register as an individual player on the rec center website',
                         'C': 'Show up at the soccer field on Wednesday evening at five',
                         'D': 'Ask the coordinator to lower the seven-player requirement'},
             'correct': 'B',
             'explanation': 'Para quem não tem um grupo completo, a solução está no meio da fala: "You can still '
                            "sign up by yourself as an individual player on the rec center website, and we'll place "
                            'you on a team." A alternativa (A) traz um horário real do áudio, mas esperar até '
                            'segunda faria você <strong>perder o prazo</strong> de inscrição na sexta-feira.'},
            {'num': 'C6.2',
             'prompt': 'Detail. When will the first soccer matches take place?',
             'options': {'A': 'On Wednesday evening of next week',
                         'B': "On Friday afternoon at five o'clock",
                         'C': 'On Monday morning before classes',
                         'D': 'On Saturday afternoon at the gym'},
             'correct': 'A',
             'explanation': 'Ao final do aviso, a coordenadora separa a divulgação da tabela e o início das '
                            'partidas: "The game schedule comes out on Monday morning, and matches start next '
                            'Wednesday evening." Repare que (B) e (C) são <strong>armadilhas de datas</strong> '
                            'comuns no Listening, pois trocam o dia do jogo pelo fim das inscrições ou pela saída da '
                            'tabela.'}]},
 {'id': 'mod2-cn4',
  'title': 'Exercício C7: Geology Field Trip (meta de 2 min)',
  'level': 'B1–B2',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to an announcement in an introductory geology class.</em></p>\n'
                  "<p><strong>Professor:</strong> Before we dive into today's lecture on sediment transport, let's "
                  "go over the logistics for Saturday's field trip to the Miller River Basin. The department buses "
                  'will leave from the North Parking Lot at 7:30 a.m. sharp, and we should be back on campus by '
                  'four. The trip counts for fifteen percent of your course grade, so attendance is expected. That '
                  'said, I know a few of you work weekend shifts off campus. If you have a documented work conflict, '
                  "you need to email our teaching assistant, David, by Wednesday afternoon. He'll set you up with an "
                  "alternative assignment analyzing river-flow datasets from last year's survey, which carries the "
                  "exact same weight. Just don't wait until Friday to tell us, or we won't be able to excuse the "
                  'absence.</p>',
  'items': [{'num': 'C7.1',
             'prompt': 'Detail. What must students with a weekend work conflict do by Wednesday?',
             'options': {'A': 'Reserve a seat on the late bus leaving from the North Parking Lot',
                         'B': 'Collect sediment samples from the river basin on their own time',
                         'C': 'Contact the teaching assistant to request an alternative project',
                         'D': "Submit last year's river-flow survey before the Friday lecture"},
             'correct': 'C',
             'explanation': 'Se você trabalha no fim de semana, o professor orienta a avisar o monitor até '
                            'quarta-feira para receber a atividade substitutiva: "you need to email our teaching '
                            "assistant, David, by Wednesday afternoon. He'll set you up with an alternative "
                            'assignment." A opção (D) confunde o prazo de <strong>avisar a ausência</strong> com a '
                            'entrega da análise de dados.'},
            {'num': 'C7.2',
             'prompt': 'Inference. What can be inferred about students who report a conflict on Friday?',
             'options': {'A': 'They will have to drive their own cars to the Miller River Basin',
                         'B': 'They will receive partial credit for the river-flow dataset paper',
                         'C': 'They will be reassigned to a different geology lecture section',
                         'D': 'They will not be allowed to replace the trip with the data project'},
             'correct': 'D',
             'explanation': 'O professor encerra deixando claro que avisos na sexta-feira não serão aceitos para '
                            'abonar a falta: "Just don\'t wait until Friday to tell us, or we won\'t be able to '
                            'excuse the absence." Daí você infere que quem deixar para sexta <strong>perderá o '
                            'direito</strong> de trocar a saída de campo pelo projeto de dados, enquanto (B) inventa '
                            'um crédito parcial que o áudio não menciona.'}]},
 {'id': 'mod2-cn5',
  'title': 'Exercício C8: Campus Flu Clinic (meta de 2 min)',
  'level': 'B1–B2',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to an announcement from Student Health Services.</em></p>\n'
                  '<p><strong>Speaker:</strong> Hi, everyone. Next Tuesday and Wednesday, Student Health Services '
                  'will be hosting our annual flu shot clinic in the Student Union Ballroom, from nine a.m. to four '
                  "p.m. both days. Notice that we've split the schedule this year to cut down on long lines: between "
                  "nine and noon, anyone can walk in without an appointment, but from one to four p.m., we're only "
                  'taking students who booked a time slot online through the health portal. The vaccine is free if '
                  "you're covered by the university health plan, though you still need to bring your student ID "
                  "card. If you're on a private family insurance plan instead, please upload a photo of your "
                  "insurance card to the portal at least twenty-four hours before you come in, so our staff doesn't "
                  'have to process paperwork at the door.</p>',
  'items': [{'num': 'C8.1',
             'prompt': 'Detail. Why did Student Health Services divide the clinic schedule into two parts?',
             'options': {'A': 'To reduce waiting times at the Student Union Ballroom',
                         'B': 'To separate undergraduate students from graduate staff',
                         'C': 'To reserve morning hours for private insurance holders',
                         'D': 'To give the nursing staff a three-hour break for lunch'},
             'correct': 'A',
             'explanation': 'O motivo de dividir o atendimento entre manhã livre e tarde agendada aparece logo no '
                            'início: "we\'ve split the schedule this year to cut down on long lines." A expressão '
                            '<em>cut down on long lines</em> equivale a <strong>reduzir o tempo de fila</strong>. Já '
                            '(C) mistura a regra da manhã com a exigência do plano de saúde privado, que vem só no '
                            'final.'},
            {'num': 'C8.2',
             'prompt': 'Connecting content. What must a student with private insurance do to get vaccinated at 2 '
                       'p.m.?',
             'options': {'A': 'Walk in without an appointment and pay the fee at the door',
                         'B': 'Book a slot online and upload their insurance card in advance',
                         'C': 'Switch to the university health plan before Tuesday morning',
                         'D': 'Bring a paper copy of their family medical records at noon'},
             'correct': 'B',
             'explanation': 'Para esse caso, você junta duas condições do áudio. Às 14h é preciso agendar online, '
                            'como diz o trecho "from one to four p.m., we\'re only taking students who booked a time '
                            'slot online", e quem tem plano privado precisa enviar foto do cartão um dia antes. A '
                            'opção (A) falha porque à tarde <strong>não há encaixe</strong> sem hora marcada.'}]},
 {'id': 'mod2-cn6',
  'title': 'Exercício C9: Midterm Review Session (meta de 2 min)',
  'level': 'B1–B2',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to an announcement at the beginning of a political science '
                  'lecture.</em></p>\n'
                  '<p><strong>Professor:</strong> Good morning, everyone. Before we start, I need to make two '
                  "adjustments to this week's schedule. I'm flying to Chicago on Thursday morning to present a paper "
                  "at a conference, which means I won't be in my office for my usual Thursday afternoon hours. "
                  "Instead, I'll hold extended office hours tomorrow — that's Wednesday — from two to five p.m. on "
                  "Zoom; the link is already on the course page. As for Friday's class, we're still meeting in this "
                  'room at our regular time, because my teaching assistant, Clara, will run a midterm review '
                  "session. She'll walk you through two sample essay questions from past exams and show you how we "
                  "use the grading rubric. Keep in mind, though, that she won't be reviewing individual study "
                  'outlines during class, so save specific questions like that for my Zoom hours tomorrow.</p>',
  'items': [{'num': 'C9.1',
             'prompt': 'Detail. How can students meet with the professor this week?',
             'options': {'A': 'By visiting her office on Thursday afternoon as usual',
                         'B': "By staying in the lecture hall after Friday's review",
                         'C': 'By booking a private meeting with Clara on Wednesday',
                         'D': 'By joining her online office hours on Wednesday afternoon'},
             'correct': 'D',
             'explanation': 'Como a professora viajará na quinta, ela antecipou o atendimento para quarta à tarde, '
                            'pela internet: "Instead, I\'ll hold extended office hours tomorrow, that\'s Wednesday, '
                            'from two to five p.m. on Zoom." Um ponto de atenção é (A), que repete o <strong>horário '
                            'habitual</strong> de quinta justamente quando ela avisa que não estará lá.'},
            {'num': 'C9.2',
             'prompt': "Detail. What will the teaching assistant do during Friday's class?",
             'options': {'A': "Present the professor's conference paper on Chicago politics",
                         'B': "Give feedback on each student's individual study outline",
                         'C': 'Explain the grading rubric using past exam essay questions',
                         'D': 'Administer the first part of the political science midterm'},
             'correct': 'C',
             'explanation': 'Na aula de sexta, a monitora Clara vai analisar questões antigas e mostrar como o '
                            'critério de correção funciona: "She\'ll walk you through two sample essay questions '
                            'from past exams and show you how we use the grading rubric." Cuidado com (B), que traz '
                            'exatamente o que a professora diz que a monitora <strong>não fará</strong> em aula.'}]},
 {'id': 'mod2-cn7',
  'title': 'Exercício C10: Research Poster Symposium (meta de 2 min)',
  'level': 'B2–C1',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to an announcement for students participating in the Undergraduate '
                  'Research Symposium.</em></p>\n'
                  '<p><strong>Speaker:</strong> Thanks for coming to this brief orientation, everyone. With the '
                  'Undergraduate Research Symposium just two weeks away, I want to highlight a critical deadline '
                  'regarding your posters. The university print shop is covering the cost of printing one '
                  'large-format poster per presenter, provided you upload your final PDF to the symposium portal by '
                  'this Friday at five p.m. Now, make sure your faculty advisor signs off on the layout before you '
                  "upload it, because the print shop won't accept revised files once a job is in the queue. If you "
                  "miss Friday's cutoff, you aren't disqualified from presenting, but you'll have to have your "
                  'poster printed at a commercial shop at your own expense. Finally, on the day of the symposium, '
                  "you're only required to stand by your board during your assigned one-hour judging window; the "
                  "rest of the afternoon, you're free to view other students' work.</p>",
  'items': [{'num': 'C10.1',
             'prompt': "Function. Why does the speaker urge students to get their advisor's approval before "
                       'uploading their file?',
             'options': {'A': 'Because faculty advisors must upload the PDF files through their own accounts',
                         'B': 'Because the print shop does not allow replacement files after submission',
                         'C': "Because the symposium judges grade the advisor's comments on the layout",
                         'D': 'Because commercial print shops charge extra for unapproved poster designs'},
             'correct': 'B',
             'explanation': 'O orientador precisa aprovar a versão antes do envio porque a gráfica universitária não '
                            'aceita trocar o arquivo depois que ele entra na fila: "make sure your faculty advisor '
                            "signs off on the layout before you upload it, because the print shop won't accept "
                            'revised files once a job is in the queue." A alternativa (A) distorce o processo, pois '
                            'quem envia o arquivo no portal é <strong>você mesmo</strong>, não o orientador.'},
            {'num': 'C10.2',
             'prompt': 'Detail. What happens if a presenter submits their poster file after Friday at 5 p.m.?',
             'options': {'A': 'They are automatically removed from the symposium judging schedule',
                         'B': 'They must give a short oral presentation instead of showing a poster',
                         'C': 'They are assigned to the last one-hour judging window of the afternoon',
                         'D': 'They can still participate if they pay to print the poster elsewhere'},
             'correct': 'D',
             'explanation': 'Perder o prazo de sexta não elimina você do simpósio, mas faz você perder a impressão '
                            'gratuita e precisar pagar por fora: "If you miss Friday\'s cutoff, you aren\'t '
                            "disqualified from presenting, but you'll have to have your poster printed at a "
                            'commercial shop at your own expense." A opção (A) é uma <strong>armadilha de '
                            "extremismo</strong>, que o próprio falante descarta ao dizer <em>you aren't "
                            'disqualified</em>.'}]},
 {'id': 'mod2-cn8',
  'title': 'Exercício C11: Honors Thesis Deposit (meta de 2 min)',
  'level': 'C1',
  'objective': 'Ouça o anúncio e responda às 2 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 2 minutos.',
  'passage_html': '<p><em>Narrator: Listen to an announcement from the director of the senior honors '
                  'program.</em></p>\n'
                  '<p><strong>Director:</strong> Congratulations on reaching the final stretch of your senior honors '
                  "theses. As you prepare for next month's oral defenses, please take note of an important policy "
                  'update from the university archives. Starting this term, the library has phased out physical '
                  'bound copies altogether; your final deposit will consist solely of a PDF submitted to the '
                  'institutional repository. By default, every thesis uploaded to that repository becomes publicly '
                  'searchable worldwide as soon as degrees are conferred in June. For most of you, having your work '
                  'openly accessible is a plus. However, if your thesis incorporates unpublished data from your '
                  "advisor's lab that is slated for submission to a peer-reviewed journal, premature public release "
                  'could jeopardize that publication, since some journals consider an open thesis a prior '
                  'publication. In that case, you and your advisor must file an embargo form at the time of upload, '
                  'which restricts public access for up to two years.</p>',
  'items': [{'num': 'C11.1',
             'prompt': "Detail. How has the library's thesis submission policy changed this term?",
             'options': {'A': 'Students must now schedule their oral defense before June graduation',
                         'B': 'The institutional repository now restricts all theses for two years',
                         'C': 'Printed bound volumes have been replaced by a digital-only deposit',
                         'D': 'Faculty advisors are no longer required to sign the final upload form'},
             'correct': 'C',
             'explanation': 'A mudança deste semestre é o fim das cópias impressas encadernadas, substituídas pelo '
                            'envio apenas em PDF: "Starting this term, the library has phased out physical bound '
                            'copies altogether; your final deposit will consist solely of a PDF." O phrasal verb '
                            '<em>phase out</em> quer dizer extinguir gradualmente. Já (B) generaliza a restrição de '
                            'dois anos, que vale só para quem <strong>pede o embargo</strong>.'},
            {'num': 'C11.2',
             'prompt': 'Function. Why does the director mention peer-reviewed journals?',
             'options': {'A': 'To explain why some students may need to delay public access to their thesis',
                         'B': 'To encourage seniors to publish their theses before degrees are conferred',
                         'C': 'To clarify that articles already published in journals cannot be archived',
                         'D': 'To show that the institutional repository is ranked alongside top journals'},
             'correct': 'A',
             'explanation': 'O diretor cita os periódicos científicos para explicar em que situação vale pedir o '
                            'embargo e adiar o acesso público à tese: "premature public release could jeopardize '
                            'that publication, since some journals consider an open thesis a prior publication." A '
                            'opção (B) inverte a lógica, pois o alerta serve para <strong>proteger dados '
                            'inéditos</strong> que ainda serão enviados a uma revista.'}]}]
MOD2_ACTION_DRILLS_C = MOD2_ACTION_DRILLS_C + MOD2_NOVOS_C
MOD2_NOVOS_D = [{'id': 'mod2-dn2',
  'title': 'Exercício D4: zoologia (meta de 3 min)',
  'level': 'A2–B1',
  'objective': 'Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 3 minutos.',
  'passage_html': '<p><em>Narrator: Listen to part of a talk in an introductory zoology class.</em></p>\n'
                  "<p><strong>Professor:</strong> All right, let's continue our unit on marine mammals. Last time we "
                  'talked about whales, which spend their whole lives in deep water. Today, I want to look at a much '
                  'smaller animal that lives right along the rocky coast: the sea otter.</p>\n'
                  '<p>Unlike seals, which come onto the beach to rest, sea otters do almost everything in the water. '
                  'They hunt there, they eat there, and, believe it or not, they even sleep floating on their backs. '
                  'Now, that creates a pretty obvious problem. The ocean is always moving. If you fall asleep '
                  'floating on the surface, the waves and currents can easily push you out into the open sea, away '
                  'from your food and your group.</p>\n'
                  '<p>So how do sea otters solve this? Well, they use a clever trick. Before going to sleep, an '
                  'otter swims into a bed of giant kelp, which is a tall kind of seaweed anchored to the ocean '
                  'floor. The otter wraps a few long strands of kelp around its body like a blanket. That keeps it '
                  'in one place while it naps.</p>\n'
                  "<p>And if there's no kelp nearby, otters sometimes hold paws with another otter so they don't "
                  "drift apart. It looks cute to us, of course, but for the otters, it's really a practical survival "
                  'habit.</p>',
  'items': [{'num': 'D4.1',
             'prompt': 'Gist-content. What is the main topic of the talk?',
             'options': {'A': 'How sea otters hunt for food along rocky coastlines',
                         'B': 'How sea otters avoid drifting away while sleeping in the ocean',
                         'C': 'Why giant kelp forests are disappearing from coastal waters',
                         'D': 'Why sea otters spend more time on beaches than seals do'},
             'correct': 'B',
             'explanation': 'O foco da aula é mostrar como as lontras-marinhas <strong>dormem na água</strong> sem '
                            'serem levadas pela correnteza: "If you fall asleep floating on the surface, the waves '
                            'and currents can easily push you out... So how do sea otters solve this?" A opção (A) '
                            'pega uma palavra isolada do começo, mas a caça não é desenvolvida na explicação.'},
            {'num': 'D4.2',
             'prompt': 'Function. Why does the professor compare sea otters to seals?',
             'options': {'A': 'To show that both animals eat the same types of fish',
                         'B': 'To explain why seals are better swimmers in deep water',
                         'C': 'To argue that sea otters evolved from coastal seals',
                         'D': 'To point out that sea otters rest in the water rather than on land'},
             'correct': 'D',
             'explanation': 'A comparação serve para mostrar a você que as lontras <strong>descansam na '
                            'água</strong>, ao contrário das focas que vão para a areia: "Unlike seals, which come '
                            'onto the beach to rest, sea otters do almost everything in the water." A opção (B) '
                            'mistura as focas com as baleias citadas na frase anterior.'},
            {'num': 'D4.3',
             'prompt': 'Detail. How does giant kelp help a sleeping sea otter?',
             'options': {'A': 'It acts like an anchor because it is attached to the ocean floor',
                         'B': 'It hides the otter from sharks swimming near the surface',
                         'C': 'It provides a snack if the otter wakes up hungry at night',
                         'D': 'It keeps the water around the otter several degrees warmer'},
             'correct': 'A',
             'explanation': 'Como a alga gigante é presa ao fundo do mar, ela funciona como uma <strong>âncora '
                            'natural</strong> quando a lontra se enrola nela: "a tall kind of seaweed anchored to '
                            'the ocean floor... That keeps it in one place while it naps." Repare que (D) é uma '
                            'armadilha comum por causa da palavra <em>blanket</em>, usada só para ilustrar o gesto '
                            'de se enrolar.'},
            {'num': 'D4.4',
             'prompt': "Attitude. What is the professor's attitude toward otters holding paws?",
             'options': {'A': 'She doubts that this behavior actually happens in the wild',
                         'B': 'She worries that tourists disturb the otters to take photos of it',
                         'C': 'She views it as a useful behavior rather than just a charming habit',
                         'D': 'She thinks scientists have studied this behavior too much'},
             'correct': 'C',
             'explanation': 'A professora comenta que o gesto parece fofo, mas ressalta seu <strong>valor '
                            'prático</strong> para a sobrevivência: "It looks cute to us, of course, but for the '
                            'otters, it\'s really a practical survival habit." A alternativa (A) contradiz o tom '
                            'seguro com que ela descreve esse comportamento.'}]},
 {'id': 'mod2-dn3',
  'title': 'Exercício D5: história da arquitetura (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 4 minutos.',
  'passage_html': '<p><em>Narrator: Listen to part of a talk in an architectural history class.</em></p>\n'
                  '<p><strong>Professor:</strong> When we think about keeping buildings cool in desert climates, we '
                  'usually picture modern air-conditioning units humming away on every wall. But people have lived '
                  'comfortably in hot, dry regions for thousands of years without electricity. A great example of '
                  'how they did it is the windcatcher, or badgir, a tower structure perfected in ancient '
                  'Persia.</p>\n'
                  "<p>If you look at the skyline of an old desert city like Yazd, in modern-day Iran, you'll see "
                  'dozens of these rectangular towers rising above the flat roofs. At the top of each tower, there '
                  'are vertical openings facing the prevailing wind. Even a light breeze high above the street gets '
                  'caught by these openings and funneled straight down into the living spaces below.</p>\n'
                  "<p>Now, what happens when there's no wind at all? Well, that's where the design gets really "
                  'clever. Without a breeze, the tower works like a chimney. Engineers call this a solar chimney. '
                  'The sun heats the south side of the tower, warming the air inside it. Because warm air rises, it '
                  'flows up and out through the top of the tower. That pulls cooler air from shaded courtyards or '
                  'underground water channels into the rooms downstairs.</p>\n'
                  '<p>Today, contemporary architects are taking a fresh look at windcatchers. By combining these '
                  'traditional towers with modern sensors and dampers, new campus buildings and offices can cut '
                  'their cooling energy use dramatically. Sometimes the smartest technology is centuries old.</p>',
  'items': [{'num': 'D5.1',
             'prompt': 'Gist-content. What is the talk mainly about?',
             'options': {'A': 'How a traditional architectural feature cools buildings without electricity',
                         'B': 'Why ancient Persian cities were built near underground rivers',
                         'C': 'How modern air conditioning replaced traditional desert housing',
                         'D': 'Why tall rectangular towers were used as watchtowers in Yazd'},
             'correct': 'A',
             'explanation': 'A palestra inteira explica como os captadores de vento persas fazem o '
                            '<strong>resfriamento passivo</strong> de construções sem usar eletricidade: "people '
                            'have lived comfortably in hot, dry regions for thousands of years without electricity. '
                            'A great example of how they did it is the windcatcher." A opção (B) toma um detalhe '
                            'secundário do terceiro parágrafo como se fosse o tema principal.'},
            {'num': 'D5.2',
             'prompt': 'Detail. How does a windcatcher work on a day with no breeze?',
             'options': {'A': 'Residents pour water down the inside of the tower to cool the bricks',
                         'B': 'Large fabric fans inside the tower push warm air down to the floor',
                         'C': 'Rising warm air exits the tower and draws cooler air into the house',
                         'D': 'Heavy wooden shutters close automatically to trap cold night air inside'},
             'correct': 'C',
             'explanation': 'Sem vento, o calor do sol faz o <strong>ar quente subir</strong> e sair pelo topo, '
                            'puxando ar fresco para dentro: "Because warm air rises, it flows up and out through the '
                            'top of the tower. That pulls cooler air from shaded courtyards or underground water '
                            'channels into the rooms downstairs." Cuidado com (A), que distorce a menção aos canais '
                            'subterrâneos de água.'},
            {'num': 'D5.3',
             'prompt': 'Organization. Why does the professor mention contemporary architects at the end of the talk?',
             'options': {'A': 'To criticize modern builders for ignoring local building codes',
                         'B': 'To show that this ancient design is still relevant and adaptable today',
                         'C': 'To explain why historic towers in Yazd need urgent restoration',
                         'D': 'To argue that modern sensors are too expensive for most offices'},
             'correct': 'B',
             'explanation': 'Ao mostrar o uso das torres em prédios novos com sensores modernos, o professor prova '
                            'que a técnica antiga continua <strong>atual e aplicável</strong>: "contemporary '
                            'architects are taking a fresh look at windcatchers... new campus buildings and offices '
                            'can cut their cooling energy use dramatically." A opção (D) inventa uma crítica de '
                            'custo que não está no áudio.'},
            {'num': 'D5.4',
             'prompt': 'Meaning in context. Why does the professor say "Sometimes the smartest technology is '
                       'centuries old"?',
             'options': {'A': 'To suggest that students should study ancient history instead of engineering',
                         'B': 'To claim that ancient builders had secret tools that have been lost',
                         'C': 'To complain that modern appliances break down too easily',
                         'D': 'To emphasize that historical solutions can solve modern environmental problems'},
             'correct': 'D',
             'explanation': 'A frase final resume a ideia de que <strong>soluções históricas</strong> inteligentes '
                            'podem resolver desafios atuais de economia de energia: "new campus buildings and '
                            'offices can cut their cooling energy use dramatically. Sometimes the smartest '
                            'technology is centuries old." A opção (B) trata o elogio como se houvesse um segredo '
                            'perdido, mas o professor acabou de explicar toda a física da torre.'}]},
 {'id': 'mod2-dn4',
  'title': 'Exercício D6: psicologia cognitiva (meta de 4 min)',
  'level': 'B1–B2',
  'objective': 'Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 4 minutos.',
  'passage_html': '<p><em>Narrator: Listen to part of a talk in a cognitive psychology class.</em></p>\n'
                  "<p><strong>Professor:</strong> Have you ever noticed that when you're studying for an exam, the "
                  "one practice problem you couldn't finish keeps popping into your head at dinner, while the ten "
                  "problems you solved easily just fade away? There's actually a name for that: the Zeigarnik "
                  'effect.</p>\n'
                  '<p>It goes back to the 1920s. A psychologist named Bluma Zeigarnik was sitting in a busy Berlin '
                  'restaurant with her professor and some classmates. She noticed something odd about the waiters. A '
                  'waiter could remember a long, complicated order for a big table without writing anything down. '
                  'But the moment the food was served and the bill was paid, if you asked that same waiter what the '
                  "table had ordered, he had no idea. He'd wiped it clean from his memory.</p>\n"
                  '<p>Curious, Zeigarnik went back to her lab and gave volunteers a series of simple tasks, like '
                  "solving puzzles or stringing beads. Here's the catch: she interrupted them halfway through some "
                  'of the tasks and let them finish the others. Later, when she asked them to list all the tasks '
                  "they'd worked on, people were about twice as likely to remember the ones they hadn't "
                  'finished.</p>\n'
                  '<p>Her explanation was that starting a task creates a kind of mental tension, almost like an open '
                  'tab on your computer browser. That tension keeps the information active and easy to recall until '
                  'the job is done. Once you finish, the tab closes, and your brain lets go.</p>',
  'items': [{'num': 'D6.1',
             'prompt': 'Gist-content. What is the main idea of the talk?',
             'options': {'A': 'Waiters have better short-term memory than most university students',
                         'B': 'Interruptions during study sessions permanently damage long-term recall',
                         'C': 'Writing down tasks is less effective than memorizing them mentally',
                         'D': 'People tend to remember unfinished tasks better than completed ones'},
             'correct': 'D',
             'explanation': 'A aula gira em torno do <strong>efeito Zeigarnik</strong>, segundo o qual lembramos '
                            'melhor de tarefas inacabadas do que das já concluídas: "people were about twice as '
                            'likely to remember the ones they hadn\'t finished." A alternativa (A) foca apenas na '
                            'história dos garçons, que serve para mostrar como a psicóloga teve a ideia inicial.'},
            {'num': 'D6.2',
             'prompt': 'Detail. What did Bluma Zeigarnik observe about the waiters in the Berlin restaurant?',
             'options': {'A': 'They wrote down every order carefully to avoid making mistakes',
                         'B': 'They forgot customer orders right after the meal was paid for',
                         'C': 'They remembered regular customers better than first-time visitors',
                         'D': 'They made more mistakes when the café was quiet than when it was busy'},
             'correct': 'B',
             'explanation': 'Assim que a conta era paga e a tarefa acabava, os garçons <strong>esqueciam o '
                            'pedido</strong>: "the moment the food was served and the bill was paid, if you asked '
                            'that same waiter what the table had ordered, he had no idea." A opção (A) diz o '
                            'contrário do áudio, que afirma <em>without writing anything down</em>.'},
            {'num': 'D6.3',
             'prompt': 'Function. Why does the professor compare an unfinished task to an open browser tab?',
             'options': {'A': 'To warn students against using laptops while studying for exams',
                         'B': 'To explain how computer scientists modeled early memory software',
                         'C': 'To illustrate how the brain keeps incomplete tasks active in memory',
                         'D': 'To show that digital multitasking reduces attention span in class'},
             'correct': 'C',
             'explanation': 'A imagem da aba aberta no navegador ajuda você a visualizar a <strong>tensão '
                            'mental</strong> que mantém a tarefa ativa na memória até ser concluída: "almost like an '
                            'open tab on your computer browser. That tension keeps the information active and easy '
                            'to recall until the job is done." A opção (D) traz um tema comum sobre tecnologia, mas '
                            'que não foi discutido na aula.'},
            {'num': 'D6.4',
             'prompt': "Detail. In Zeigarnik's lab experiment, how did she test her idea?",
             'options': {'A': 'She stopped participants during some tasks and allowed them to finish others',
                         'B': 'She asked professional waiters to solve puzzles in a noisy restaurant',
                         'C': 'She timed how fast volunteers could memorize a list of restaurant menu items',
                         'D': 'She rewarded participants who remembered all of their completed tasks'},
             'correct': 'A',
             'explanation': 'No laboratório, ela <strong>interrompeu algumas tarefas</strong> na metade e deixou que '
                            'os voluntários terminassem outras: "she interrupted them halfway through some of the '
                            'tasks and let them finish the others." Repare que (B) mistura a observação inicial no '
                            'restaurante de Berlim com o experimento feito depois no laboratório.'}]},
 {'id': 'mod2-dn5',
  'title': 'Exercício D7: economia comportamental (meta de 4 min)',
  'level': 'B2–C1',
  'objective': 'Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 4 minutos.',
  'passage_html': '<p><em>Narrator: Listen to part of a talk in a behavioral economics class.</em></p>\n'
                  '<p><strong>Professor:</strong> In standard economic theory, rational decision-makers look only at '
                  "future costs and benefits. Whatever money, time, or effort you've already spent and can't recover "
                  "is called a sunk cost, and logically, it shouldn't influence what you do next. Yet in real life, "
                  'we let sunk costs drive our choices all the time.</p>\n'
                  '<p>Picture this: you buy a nonrefundable twenty-dollar ticket to an outdoor concert. The evening '
                  "of the show, a freezing rainstorm rolls in. You're miserable just thinking about going. If the "
                  "ticket had been free, you'd stay home on the couch without a second thought. But because you paid "
                  'twenty dollars, you drag yourself out into the rain so you don\'t "waste" the ticket. See the '
                  "flaw? The twenty dollars is gone either way. By going, you haven't saved your money; you've just "
                  'traded a dry evening for a wet, miserable one.</p>\n'
                  "<p>And it's not just individuals who fall into this trap. Governments and corporations do too. In "
                  'fact, economists sometimes call this the Concorde fallacy, after the supersonic passenger jet '
                  'developed jointly by Britain and France. Long before the plane entered service, both governments '
                  'realized it would never make back its massive development costs. Walking away would have saved '
                  'billions. Instead, neither side wanted to admit that the money already spent was lost, so they '
                  'kept pouring funds into the project for years.</p>\n'
                  '<p>Why is it so hard to walk away? Partly because of loss aversion: we hate admitting a loss more '
                  'than we enjoy an equivalent gain. Once we recognize that bias, though, we can ask a simpler '
                  'question: if I were starting from scratch today, would I still invest in this?</p>',
  'items': [{'num': 'D7.1',
             'prompt': 'Gist-content. What is the talk mainly about?',
             'options': {'A': 'How airline companies calculate ticket prices for international flights',
                         'B': 'Why people and organizations continue investing in losing endeavors',
                         'C': 'Why outdoor events should always offer refundable tickets to buyers',
                         'D': 'How Britain and France competed to build the fastest passenger aircraft'},
             'correct': 'B',
             'explanation': 'A palestra analisa a falácia dos <strong>custos irrecuperáveis</strong>, mostrando por '
                            'que pessoas e governos insistem em escolhas ou projetos que já deram prejuízo: '
                            '"Whatever money, time, or effort you\'ve already spent and can\'t recover is called a '
                            'sunk cost... we let sunk costs drive our choices all the time." A opção (D) foca apenas '
                            'no exemplo do avião Concorde e ainda troca cooperação, indicada em <em>developed '
                            'jointly</em>, por competição.'},
            {'num': 'D7.2',
             'prompt': 'Organization. Why does the professor discuss the concert ticket scenario?',
             'options': {'A': 'To show how an everyday decision violates rational economic logic',
                         'B': 'To argue that concert venues charge unfair prices for admission',
                         'C': 'To contrast weather forecasts with economic forecasting models',
                         'D': 'To prove that consumers care more about comfort than about money'},
             'correct': 'A',
             'explanation': 'O exemplo do ingresso mostra como uma decisão comum do dia a dia contraria a '
                            '<strong>lógica econômica</strong> racional anunciada na abertura: "See the flaw? The '
                            'twenty dollars is gone either way." A opção (D) inverte a situação, pois a pessoa abre '
                            'mão do conforto justamente por apego ao dinheiro já gasto.'},
            {'num': 'D7.3',
             'prompt': 'Detail. Why is the phenomenon also known as the Concorde fallacy?',
             'options': {'A': 'The jet was canceled before its first flight despite public support',
                         'B': 'Passengers refused to fly on the plane because tickets were too costly',
                         'C': 'Engineers hid the true cost of the aircraft from government officials',
                         'D': 'Two governments kept funding the jet even after knowing it would lose money'},
             'correct': 'D',
             'explanation': 'O nome vem do fato de Reino Unido e França terem continuado a <strong>financiar o '
                            'jato</strong> mesmo sabendo que ele nunca daria retorno: "both governments realized it '
                            'would never make back its massive development costs... so they kept pouring funds into '
                            'the project for years." A opção (A) erra porque o projeto não foi cancelado antes de '
                            'entrar em serviço.'},
            {'num': 'D7.4',
             'prompt': 'Detail. According to the professor, what should a decision-maker do when facing a sunk cost?',
             'options': {'A': 'Try to recover the initial investment by doubling the project budget',
                         'B': 'Share the financial responsibility equally with another partner',
                         'C': 'Evaluate the choice as if starting fresh, ignoring past spending',
                         'D': 'Avoid starting any long-term project that carries financial risk'},
             'correct': 'C',
             'explanation': 'No fechamento, o professor sugere que você avalie a decisão <strong>partindo do '
                            'zero</strong>, sem levar em conta o que já foi gasto: "if I were starting from scratch '
                            'today, would I still invest in this?" A opção (B) é uma armadilha porque lembra a '
                            'parceria entre dois países no caso do Concorde, que justamente não impediu o erro.'}]},
 {'id': 'mod2-dn6',
  'title': 'Exercício D8: linguística histórica (meta de 4 min)',
  'level': 'C1',
  'objective': 'Ouça a palestra e responda às 4 questões. A transcrição aparece depois que você responder a todas. '
               'Tempo-alvo: 4 minutos.',
  'passage_html': '<p><em>Narrator: Listen to part of a talk in a historical linguistics class.</em></p>\n'
                  '<p><strong>Professor:</strong> We often treat dictionary definitions as if they were carved in '
                  'stone, and people love to complain when a word starts being used in a new way. But to a linguist, '
                  "semantic shift—the gradual change in a word's meaning over time—isn't a corruption of language; "
                  "it's one of its most predictable features. Today I want to focus on two opposite directions this "
                  "shift can take: amelioration, where a word's meaning becomes more positive, and pejoration, where "
                  'it becomes more negative.</p>\n'
                  '<p>Take the ordinary English word "nice." If someone calls your essay "nice" today, it\'s a mild '
                  'compliment. But if we trace "nice" back to its Latin root, nescius, it meant "ignorant" or '
                  '"unaware." When it entered Middle English through French, it meant "foolish" or "silly." Over the '
                  'next few centuries, though, its meaning softened: from foolish to shy, then to fussy or '
                  'fastidious, then to precise and delicate, and finally to pleasant and agreeable. That upward '
                  'climb from "ignorant" to "pleasant" is a classic case of amelioration.</p>\n'
                  '<p>Now look at the reverse trajectory: pejoration. Consider the word "silly." In Old English, its '
                  'ancestor, saelig, meant "blessed" or "happy." Over time, because blessed, innocent people were '
                  'seen as harmless and defenseless, the word shifted to mean "deserving of pity," then "weak," and '
                  'eventually "foolish" or "lacking common sense." So while "nice" climbed the social ladder, '
                  '"silly" slid down it.</p>\n'
                  "<p>Notice what drives both shifts. Words don't change meaning in a vacuum; they shift because "
                  'speakers stretch them in everyday conversation—through irony, politeness, or exaggeration—until '
                  'the new implication replaces the old core meaning entirely.</p>',
  'items': [{'num': 'D8.1',
             'prompt': 'Gist-content. What is the main purpose of the lecture?',
             'options': {'A': 'To argue that modern dictionaries should preserve original Latin meanings',
                         'B': 'To explain how French grammar reshaped Middle English sentence structure',
                         'C': 'To illustrate how words can shift toward more positive or negative meanings',
                         'D': 'To show why formal academic writing avoids informal adjectives like "nice"'},
             'correct': 'C',
             'explanation': 'O objetivo da aula é explicar e exemplificar duas direções da <strong>mudança '
                            'semântica</strong>, para sentidos mais positivos ou mais negativos: "amelioration, '
                            "where a word's meaning becomes more positive, and pejoration, where it becomes more "
                            'negative." A opção (A) vai contra a visão da professora logo no primeiro parágrafo.'},
            {'num': 'D8.2',
             'prompt': 'Detail. What did the word "nice" originally mean in its Latin root?',
             'options': {'A': 'Blessed or fortunate',
                         'B': 'Precise and delicate',
                         'C': 'Pleasant and agreeable',
                         'D': 'Ignorant or unaware'},
             'correct': 'D',
             'explanation': 'Na raiz latina <em>nescius</em>, a palavra significava <strong>ignorante ou '
                            'desatento</strong>: "if we trace \'nice\' back to its Latin root, nescius, it meant '
                            '\'ignorant\' or \'unaware\'." Cuidado com (A), que traz o sentido antigo de '
                            '<em>silly</em>, enquanto (B) e (C) mostram etapas posteriores da evolução de '
                            '<em>nice</em>.'},
            {'num': 'D8.3',
             'prompt': 'Detail. How did the word "silly" change over time?',
             'options': {'A': 'It moved from meaning blessed and happy to meaning foolish',
                         'B': 'It was borrowed from French to replace an older English word',
                         'C': 'It shifted from a strong insult to a polite compliment',
                         'D': 'It kept its original Old English meaning until the twentieth century'},
             'correct': 'A',
             'explanation': 'A palavra <em>silly</em> sofreu <strong>pejoração</strong>, passando de abençoado ou '
                            'feliz no inglês antigo para tolo: "In Old English, its ancestor, saelig, meant '
                            '\'blessed\' or \'happy\'... and eventually \'foolish\' or \'lacking common sense\'." A '
                            'alternativa (C) descreve o caminho inverso, que foi o da palavra <em>nice</em>.'},
            {'num': 'D8.4',
             'prompt': 'Idiom in context. What does the professor mean by saying that words do not change meaning '
                       '"in a vacuum"?',
             'options': {'A': 'Written texts preserve older meanings longer than spoken dialects do',
                         'B': 'Shifts in meaning are driven by how people actually use words socially',
                         'C': 'Linguists cannot study dead languages without historical records',
                         'D': 'Scientific terms change meaning less often than everyday words do'},
             'correct': 'B',
             'explanation': 'Dizer que as palavras não mudam <em>in a vacuum</em> significa que a mudança não '
                            'acontece isolada, mas sim pelo <strong>uso social</strong> nas conversas do dia a dia: '
                            '"they shift because speakers stretch them in everyday conversation." A opção (D) faz '
                            'uma associação literal com a palavra <em>vacuum</em> como termo da física, sem relação '
                            'com o contexto.'}]}]
MOD2_ACTION_DRILLS_D = MOD2_ACTION_DRILLS_D + MOD2_NOVOS_D
# <<< FIM DOS EXERCÍCIOS NOVOS DO M1 E DO M2
