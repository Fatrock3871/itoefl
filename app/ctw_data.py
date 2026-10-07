# Complete the Words (Reading / M1) no formato real da prova de 2026.
#
# Molde conferido nos testes práticos oficiais da ETS (docs/ets-materiais-
# oficiais.md): parágrafo acadêmico curto, primeira frase inteira, e nas
# frases seguintes 10 palavras com o começo escrito e o final apagado, que o
# aluno digita. Não há alternativas. Os textos abaixo são originais.
#
# Marcação: [[palavra]] vira uma lacuna. O renderizador mantém a primeira
# metade da palavra (arredondada para baixo) e apaga o resto, que é a regra
# observada na prova: "might" vira "mi" + 3 letras, "that" vira "th" + 2.
#
# note: o que as lacunas daquele texto treinam, em português.

CTW_SETS = [
    {
        "id": "mod1-ctw1",
        "title": "Texto 1 · Honeybees",
        "level": "B1",
        "text": (
            "Honeybees live in large colonies that can contain tens of thousands of insects. "
            "Each [[bee]] has a [[job]] that changes [[as]] it grows [[older]]. Young workers "
            "[[clean]] the hive [[and]] feed the [[larvae]], while older [[ones]] leave the "
            "[[nest]] to collect [[food]]. A single queen lays all the eggs, sometimes more than "
            "a thousand in one day. This division of labor allows the colony to survive cold "
            "winters and long periods without flowers."
        ),
        "note": "Palavras curtas de conteúdo e duas palavras de função (as, and). "
                "Repare em \"ones\": o inglês usa esse pronome para não repetir \"workers\".",
    },
    {
        "id": "mod1-ctw2",
        "title": "Texto 2 · Volcanoes",
        "level": "B1",
        "text": (
            "Volcanoes form where melted rock from deep inside the Earth reaches the surface. "
            "This [[melted]] rock is [[called]] magma while [[it]] stays underground [[and]] lava "
            "once it [[flows]] out. Some [[eruptions]] are gentle, [[with]] slow rivers [[of]] "
            "lava, but [[others]] are violent [[explosions]] of ash and gas. Scientists watch "
            "small earthquakes and changes in the shape of a mountain to predict when an "
            "eruption may happen. Their warnings have saved thousands of lives."
        ),
        "note": "Terminações contam: called (particípio na passiva), flows (terceira pessoa), "
                "eruptions e explosions (plural). A primeira frase já entrega \"melted\".",
    },
    {
        "id": "mod1-ctw3",
        "title": "Texto 3 · The printing press",
        "level": "B1–B2",
        "text": (
            "Before the printing press, books in Europe were copied slowly by hand. A [[single]] "
            "volume could [[take]] months to [[finish]], so only [[wealthy]] people and "
            "[[religious]] institutions could [[afford]] one. When [[printers]] began using "
            "[[movable]] metal type in [[the]] fifteenth century, [[prices]] fell quickly. Ideas "
            "that had once traveled slowly could now spread across the continent within weeks. "
            "Historians often connect this change to the growth of literacy and scientific debate."
        ),
        "note": "Verbo na base depois de could e de to (take, finish, afford). "
                "Collocation: \"take months\", \"afford one\", \"prices fell\".",
    },
    {
        "id": "mod1-ctw4",
        "title": "Texto 4 · Sleep and memory",
        "level": "B2",
        "text": (
            "Sleep plays an important role in how the brain stores new information. During "
            "[[the]] day, memories [[are]] held in a [[temporary]] form that [[is]] easily lost. "
            "[[While]] we sleep, [[the]] brain replays [[recent]] experiences and [[moves]] them "
            "into [[more]] stable, long-term [[storage]]. Students who sleep after studying "
            "usually remember more than those who stay awake. For this reason, researchers "
            "advise against studying all night before an exam."
        ),
        "note": "Metade das lacunas é palavra de função (the, are, is, while, more). "
                "São as que mais derrubam quem lê só as palavras \"importantes\".",
    },
    {
        "id": "mod1-ctw5",
        "title": "Texto 5 · Urban heat",
        "level": "B2",
        "text": (
            "Cities are usually warmer than the countryside that surrounds them. Dark "
            "[[surfaces]] such as [[roads]] and rooftops [[absorb]] sunlight during [[the]] day "
            "and [[release]] the heat [[slowly]] at night. [[Tall]] buildings also [[block]] the "
            "wind [[that]] would otherwise [[carry]] warm air away. Planting trees and painting "
            "roofs in light colors can lower temperatures by several degrees. Many city "
            "governments now include such measures in their climate plans."
        ),
        "note": "Sujeito no plural pede verbo sem -s (surfaces absorb, buildings block). "
                "\"that\" abre a oração relativa que explica \"the wind\".",
    },
    {
        "id": "mod1-ctw6",
        "title": "Texto 6 · Supply and demand",
        "level": "B2–C1",
        "text": (
            "The price of a product depends largely on the relationship between supply and "
            "demand. When [[buyers]] want more [[of]] a good [[than]] producers can [[offer]], "
            "its price [[tends]] to rise. [[Higher]] prices then [[encourage]] companies to "
            "[[increase]] production, which [[eventually]] brings the [[market]] back toward "
            "balance. Governments sometimes interrupt this process by setting maximum prices. "
            "Economists warn that such limits often create shortages instead of helping consumers."
        ),
        "note": "Estrutura comparativa (more of ... than) e verbos acadêmicos com seus "
                "complementos: \"tends to rise\", \"encourage companies to increase\".",
    },
    {
        "id": "mod1-ctw7",
        "title": "Texto 7 · Coral reefs",
        "level": "C1",
        "text": (
            "Coral reefs cover less than one percent of the ocean floor, yet they support about "
            "a quarter of all marine species. The [[structures]] are built [[by]] tiny animals "
            "[[whose]] hard skeletons [[accumulate]] over thousands [[of]] years. These "
            "[[animals]] depend on [[microscopic]] algae that [[live]] inside their [[tissues]] "
            "and provide [[much]] of their energy. When water becomes too warm, the corals expel "
            "the algae and turn white. Unless temperatures fall again, the weakened reef may "
            "not recover."
        ),
        "note": "Passiva com agente (are built by), relativo possessivo (whose) e vocabulário "
                "científico longo, em que ortografia decide o ponto.",
    },
    {
        "id": "mod1-ctw8",
        "title": "Texto 8 · Confirmation bias",
        "level": "C1+",
        "text": (
            "People rarely evaluate evidence as objectively as they believe they do. "
            "Psychologists [[have]] shown that [[individuals]] tend to [[notice]] information "
            "that [[confirms]] what they [[already]] think, while [[overlooking]] facts that "
            "[[challenge]] it. This [[tendency]], known as [[confirmation]] bias, affects "
            "[[experts]] as well as beginners. It can distort medical diagnoses, financial "
            "decisions, and even scientific research. Awareness of the bias helps, although it "
            "does not eliminate its influence."
        ),
        "note": "Famílias de palavras no mesmo texto (confirms, confirmation; tend, tendency) "
                "e a forma em -ing depois de while (overlooking).",
    },
]
