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
        "objective": "Escolha a resposta mais natural e pragmaticamente adequada a cada fala. Tempo-alvo: 12 segundos por item.",
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
        "objective": "Leia o diálogo (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 3 minutos.",
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
        "objective": "Leia o diálogo (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 3 minutos.",
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
        "objective": "Leia o diálogo (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 3 minutos.",
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
        "objective": "Leia o anúncio (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 2 minutos.",
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
        "objective": "Leia o anúncio (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 2 minutos.",
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
        "objective": "Leia o anúncio (ou peça para alguém ler em voz alta) e responda às 2 questões. Tempo-alvo: 2 minutos.",
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
        "objective": "Leia a palestra (ou peça para alguém ler em voz alta) e responda às 4 questões. Tempo-alvo: 4 minutos.",
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
        "objective": "Leia a palestra (ou peça para alguém ler em voz alta) e responda às 4 questões. Tempo-alvo: 4 minutos.",
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
        "objective": "Leia a palestra (ou peça para alguém ler em voz alta) e responda às 4 questões. Tempo-alvo: 4 minutos.",
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
