# Conjuntos de Speaking (M3) no formato real da prova de 2026.
#
# Molde conferido nos testes práticos oficiais da ETS (docs/ets-materiais-
# oficiais.md). Os textos abaixo são originais.
#
# Listen and Repeat: 7 frases de um mesmo cenário, crescendo de tamanho. O
# aluno só ouve (o texto fica escondido) e repete uma vez.
#
# level: faixa CEFR para a qual o conjunto é indicado (usada no treino por
# nível do M0).
#
# Take an Interview: 4 perguntas do mesmo tema, em escada: fato pessoal
# simples, reação pessoal com porquê, concordar ou discordar de uma opinião,
# opinar sobre uma medida pública.

LISTEN_REPEAT_SETS = [
    {
        "id": "mod3-lr1",
        "level": "A2–B2",
        "title": "Cenário 1 · Campus library",
        "scenario": "You are learning to help at a campus library. Listen to the librarian and repeat what she says. Repeat only once.",
        "items": [
            "The library opens at eight.",
            "Books can be borrowed for two weeks.",
            "Please return them to the front desk on time.",
            "Quiet study rooms are on the second floor near the stairs.",
            "You can print documents here, but you will need your student card.",
            "If a book is not on the shelf, ask a staff member to check the system.",
            "Students who return books late may lose the right to borrow new ones for a month.",
        ],
    },
    {
        "id": "mod3-lr2",
        "level": "A2–B2",
        "title": "Cenário 2 · Coffee shop",
        "scenario": "You are starting a job at a coffee shop. Listen to your manager and repeat what he says. Repeat only once.",
        "items": [
            "Welcome to the coffee shop.",
            "We serve hot and cold drinks.",
            "Customers order at the counter on the left.",
            "Every drink can be made with regular or plant-based milk.",
            "Please write the customer's name on the cup before you start.",
            "Fresh pastries arrive each morning, and they usually sell out before noon.",
            "If someone has a food allergy, check the ingredient list and tell the manager right away.",
        ],
    },
    {
        "id": "mod3-lr3",
        "level": "B1–C1",
        "title": "Cenário 3 · Museum tour",
        "scenario": "You are training to guide visitors at a museum. Listen to the senior guide and repeat what she says. Repeat only once.",
        "items": [
            "The tour starts in this room.",
            "Please stay together as a group.",
            "Photographs are allowed, but please turn off the flash.",
            "The paintings on this wall are more than three hundred years old.",
            "Our newest exhibition, on the upper level, explores the history of flight.",
            "Visitors who would like more detail can borrow an audio guide at the entrance.",
            "The gift shop and the café, which are both next to the main exit, close thirty minutes before the museum does.",
        ],
    },
    {
        "id": "mod3-lr4",
        "level": "B1–C1",
        "title": "Cenário 4 · Chemistry lab",
        "scenario": "You are attending a safety briefing in a chemistry lab. Listen to the instructor and repeat what he says. Repeat only once.",
        "items": [
            "Safety comes first in the lab.",
            "Always wear gloves and eye protection.",
            "Long hair should be tied back before you begin.",
            "Never taste a chemical or smell it directly from the container.",
            "Label every sample clearly so that other students know what it contains.",
            "If something spills, tell the instructor immediately instead of trying to clean it yourself.",
            "Before you leave, make sure that all equipment has been washed, dried, and returned to the correct shelf.",
        ],
    },
    {
        "id": "mod3-lr5",
        "level": "B2–C2",
        "title": "Cenário 5 · Hotel front desk",
        "scenario": "You are learning to work at a hotel front desk. Listen to your supervisor and repeat what she says. Repeat only once.",
        "items": [
            "Check-in begins at three.",
            "Breakfast is served until ten o'clock.",
            "The pool and the gym are on the ground floor.",
            "Guests can leave their luggage with us after they check out.",
            "A shuttle to the airport leaves from the front entrance every half hour.",
            "If guests need a late checkout, they should let the front desk know the night before.",
            "Although the restaurant is closed on Mondays, room service remains available throughout the day and evening.",
        ],
    },
]

INTERVIEW_SETS = [
    {
        "id": "mod3-int1",
        "level": "B1–C1",
        "title": "Entrevista 1 · Study habits",
        "scenario": "You have agreed to take part in a research study about how students prepare for exams. You will have a short online interview with a researcher.",
        "items": [
            "Thank you for joining me today. I'm studying how students prepare for exams. To begin, where do you usually study: at home, in a library, or somewhere else?",
            "I see. Some students say they concentrate best alone, while others prefer to study in a group. Which works better for you, and why?",
            "Interesting. Some people believe that studying a little every day is more effective than studying for many hours right before an exam. Do you agree? Why or why not?",
            "Thank you. One last question. Some universities now keep their libraries open twenty-four hours a day. Do you think all universities should do this? Why or why not?",
        ],
    },
    {
        "id": "mod3-int2",
        "level": "B1–C1",
        "title": "Entrevista 2 · Getting around",
        "scenario": "You have agreed to take part in a survey about transportation in your area. You will have a short online interview with a researcher.",
        "items": [
            "Thanks for your time. I'm collecting opinions about transportation. First, how do you usually get around: by car, by public transportation, or on foot?",
            "OK. Some people enjoy their daily commute, and others find it stressful. How do you feel about yours, and why do you think you feel that way?",
            "I see. Some people argue that owning a car is no longer necessary for someone who lives in a big city. Do you agree? Why or why not?",
            "Good. Here is my final question. A few cities have made public transportation free for everyone. Do you think more cities should do the same? Why or why not?",
        ],
    },
    {
        "id": "mod3-int3",
        "level": "B1–C2",
        "title": "Entrevista 3 · Phones and free time",
        "scenario": "You have agreed to take part in a research study about technology and daily life. You will have a short online interview with a researcher.",
        "items": [
            "Thank you for speaking with me. My research is about technology in daily life. To start, about how many hours a day do you spend on your phone?",
            "Right. Some people feel relaxed after using social media, while others feel tired or anxious. How does it affect you, and why?",
            "Interesting. Some people say that technology has made it harder to build close friendships. Do you agree with that view? Why or why not?",
            "Thanks. One final question. Some schools have banned phones during the school day. Do you think this is a good policy? Why or why not?",
        ],
    },
    {
        "id": "mod3-int4",
        "level": "B1–C2",
        "title": "Entrevista 4 · Food and cooking",
        "scenario": "You have agreed to take part in a research study about eating habits. You will have a short online interview with a researcher.",
        "items": [
            "Thank you for being here. I'm studying people's eating habits. First of all, do you usually cook your own meals, or do you eat out?",
            "I see. Some people find cooking relaxing, and others see it as a chore. How do you feel about cooking, and why?",
            "OK. Some people believe that eating together as a family is important for children. Do you agree? Why or why not?",
            "Good points. Let me ask one last question. Some governments tax sugary drinks in order to improve public health. Do you think this is a good idea? Why or why not?",
        ],
    },
]
