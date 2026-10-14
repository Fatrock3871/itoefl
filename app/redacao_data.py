"""Os 10 temas do envio de redação para correção (decisões do dono, 2026-10-13).

Tudo o que o aluno lê na tarefa está em inglês, como na prova: a situação e os
3 pontos do e-mail (com destinatário e assunto já preenchidos); a pergunta do
professor, com 2 ou 3 frases de contexto, e as falas de dois colegas, de 40 a
60 palavras cada. O título e o objetivo de cada tema ficam em português e o
aluno os vê antes de começar.

Textos originais: nada copiado nem adaptado de perto de material da ETS. Só o
formato segue o dos testes práticos de 2026 (docs/ets-materiais-oficiais.md).

Os ids (E1 a E5, D1 a D5) e a tarefa de cada um têm de bater com
REDACAO_REGRAS.temas em supabase/functions/_shared/redacao.js, que é o que o
servidor aceita. O smoke test confere.
"""

# Os números das regras repetidos aqui só para o texto da tela "antes de
# começar". Quem decide de verdade é o redacao.js (servidor e site); o smoke
# test reprova se divergirem.
INTERVALO_DIAS = 4
PRAZO_DIAS_UTEIS = 3
MINUTOS = {"email": 7, "discussion": 10}
MIN_PALAVRAS_DISCUSSAO = 100

EMAIL_TOPICS = [
    {
        "id": "E1",
        "titulo": "Livro danificado",
        "objetivo": "Registro formal, pedido de desculpas sem exagero e uma proposta concreta.",
        "to": "Ms. Laura Bennett, Circulation Desk, Hartwell University Library",
        "subject": "Damaged library book",
        "situation": (
            "Last week you borrowed a book from the university library for a research paper. "
            "Yesterday you accidentally spilled coffee on it, and several pages are now stained "
            "and stuck together. The book is due back in three days."
        ),
        "points": [
            "Explain what happened to the book.",
            "Offer a way to solve the problem.",
            "Ask whether there is a deadline or a fine you should know about.",
        ],
    },
    {
        "id": "E2",
        "titulo": "Colega que não colabora",
        "objetivo": "Tom diplomático, fatos antes de opinião e um pedido claro.",
        "to": "Professor Daniel Okafor",
        "subject": "Question about our group project",
        "situation": (
            "You are in a group of four students preparing a project for your sociology course. "
            "The presentation is in ten days. Two weeks ago the group agreed on a date to share "
            "each person's section, but one member still has not sent his part."
        ),
        "points": [
            "Describe the situation in a fair and neutral way.",
            "Explain what the group has already tried.",
            "Ask the professor for advice.",
        ],
    },
    {
        "id": "E3",
        "titulo": "Estágio com data em conflito",
        "objetivo": "Cortesia profissional, modais (would, could) e negociação.",
        "to": "Ms. Rachel Lim, Internship Coordinator, Brightline Engineering",
        "subject": "Summer internship start date",
        "situation": (
            "You have been accepted for a summer internship at an engineering company. "
            "The internship is scheduled to begin on June 2, but your final exams at the "
            "university continue until June 6."
        ),
        "points": [
            "Thank the coordinator for the offer.",
            "Explain the scheduling conflict.",
            "Propose a new start date.",
        ],
    },
    {
        "id": "E4",
        "titulo": "Barulho na moradia estudantil",
        "objetivo": "Reclamação objetiva, causa e efeito e uma sugestão viável.",
        "to": "Residential Life Office",
        "subject": "Construction noise near Maple Hall",
        "situation": (
            "You live in Maple Hall, a student residence on campus. Construction work on a new "
            "building next to the residence starts every morning at 6 a.m. and continues for most "
            "of the day. Your final exams begin in two weeks."
        ),
        "points": [
            "Describe the problem.",
            "Explain how it is affecting your studies.",
            "Suggest a possible solution.",
        ],
    },
    {
        "id": "E5",
        "titulo": "Evento cultural",
        "objetivo": "Persuasão breve, pedido com justificativa e perguntas indiretas.",
        "to": "Mr. Thomas Reyes, Director of Student Activities",
        "subject": "Proposal for a cultural exchange night",
        "situation": (
            "You would like to organize an evening on campus where international and local "
            "students share food, music, and traditions from their countries. Several students "
            "have already offered to help you."
        ),
        "points": [
            "Introduce your idea.",
            "Ask for a space or funding for the event.",
            "Ask what steps you need to follow to get the event approved.",
        ],
    },
]

DISCUSSION_TOPICS = [
    {
        "id": "D1",
        "titulo": "Educação financeira",
        "objetivo": "Posição clara, uma razão com exemplo e resposta direta a um colega.",
        "course": "Economics",
        "professor": "Dr. Meyer",
        "question": (
            "Some universities have started adding practical life skills to the courses every "
            "student must take. Personal finance is a common example: budgeting, credit, loans, "
            "and saving. Should universities require every student to take a course in personal "
            "finance? Why or why not?"
        ),
        "students": [
            ("Ana", "I think it should be required. A lot of students graduate with credit card debt "
                    "or loans they never really understood when they signed for them. One semester "
                    "learning about interest rates and budgeting could save people years of financial "
                    "stress. It is just as useful as any other general education course."),
            ("Marcus", "I see the point, but most programs are already packed with requirements, and "
                       "many students struggle to graduate on time. Adding another mandatory course "
                       "would make that worse. Free optional workshops on budgeting or student loans "
                       "would reach the students who need them without forcing everyone to give up a "
                       "class they actually want."),
        ],
    },
    {
        "id": "D2",
        "titulo": "Trabalho remoto",
        "objetivo": "Considerar um contra-argumento e responder a ele.",
        "course": "Sociology",
        "professor": "Dr. Chen",
        "question": (
            "Since the pandemic, millions of people have continued to work from home at least part "
            "of the week, and researchers still disagree about what this shift means in the long "
            "run. Is remote work better or worse for society as a whole?"
        ),
        "students": [
            ("Priya", "Better, in my opinion. When people work from home, there are fewer cars on the "
                      "road during rush hour, which means less traffic and less air pollution in big "
                      "cities. People also save the hours they used to spend commuting, and they can "
                      "use that time for their families or for rest."),
            ("Daniel", "I think it is worse, especially for young workers. In my first job, I learned "
                       "most of what I know by watching experienced colleagues handle problems and by "
                       "asking quick questions at their desks. On a video call, that kind of informal "
                       "learning almost never happens, so new employees develop more slowly."),
        ],
    },
    {
        "id": "D3",
        "titulo": "Lixo plástico",
        "objetivo": "Comparar duas soluções e escolher com critério.",
        "course": "Environmental science",
        "professor": "Dr. Alvarez",
        "question": (
            "Cities around the world are looking for ways to keep plastic out of landfills and "
            "oceans. Some ban single-use items such as bags and straws, while others pay people "
            "to return bottles and containers. What is the most effective way for cities to reduce "
            "plastic waste: banning single-use plastics or rewarding recycling?"
        ),
        "students": [
            ("Lucía", "Banning is the only approach that really works. Rewards depend on people "
                      "remembering to collect bottles and take them somewhere, and most people simply "
                      "won't make the effort. When a store is not allowed to hand out plastic bags, "
                      "everyone adapts within a few weeks, and the habit changes for good."),
            ("Tom", "I disagree. Bans often create resistance, and in some places they have even led to "
                    "an illegal market for banned products. Rewarding recycling gives people a reason "
                    "to cooperate instead of a rule to fight against. In my hometown, a small refund for "
                    "each bottle got almost everyone returning their containers."),
        ],
    },
    {
        "id": "D4",
        "titulo": "Exploração espacial",
        "objetivo": "Argumento com exemplo concreto e linguagem cautelosa (may, tend to).",
        "course": "Public policy",
        "professor": "Dr. Novak",
        "question": (
            "This week we are discussing how governments set priorities for public spending. Space "
            "programs cost billions of dollars every year, while many countries still face serious "
            "problems in health care, education, and poverty. Should governments spend public money "
            "on space exploration while problems on Earth remain unsolved?"
        ),
        "students": [
            ("Kenji", "Yes, they should. Space research has produced many technologies we now use every "
                      "day, such as water filters, better medical imaging, and the satellites that make "
                      "weather forecasts possible. Cutting these programs would mean losing future "
                      "discoveries that could help solve the very problems people on Earth are facing."),
            ("Fatima", "I don't agree. When people in the same country cannot get basic health care or a "
                       "decent school, spending billions on rockets is hard to justify. The money would "
                       "have a much more direct effect if it went to hospitals and teachers. Space can "
                       "wait until the basic needs are met."),
        ],
    },
    {
        "id": "D5",
        "titulo": "Notícias nas redes sociais",
        "objetivo": "Nuance (concordar em parte) e vocabulário acadêmico do M6.",
        "course": "Media studies",
        "professor": "Dr. Hughes",
        "question": (
            "Surveys show that many people under 25 now get most of their news from social media "
            "rather than from newspapers or television. This change affects what young people know "
            "about the world and how they form opinions. Do social media platforms help or hurt the "
            "way young people learn about the news?"
        ),
        "students": [
            ("Leo", "They help. News reaches you within minutes, and you can see how journalists, experts, "
                    "and ordinary people in different countries are reacting to the same event. Before "
                    "social media, most young people only saw one newspaper or one TV channel, so their "
                    "view of the world was actually much narrower."),
            ("Sara", "I think they hurt more than they help. The algorithm learns what you already like and "
                     "keeps showing you posts that confirm it. After a while, you stop seeing other points "
                     "of view at all, and you start to believe that everyone thinks the way you do."),
        ],
    },
]

TOPICS = EMAIL_TOPICS + DISCUSSION_TOPICS
