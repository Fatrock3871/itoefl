# Itens de Build a Sentence (Writing / M4) para o widget interativo.
# Somente itens de reordenacao pura: todos os fragmentos entram na resposta,
# sem mudanca de morfologia. Os itens que exigem trocar tempo verbal ou ordem
# de adjetivos ficam como texto no modulo (Drills 1 e 4).
#
# fragments: ordem embaralhada apresentada ao aluno
# answer:    lista de fragmentos na ordem correta (== frase montada)
# sentence:  a frase final legivel (para o feedback)
# note:      nota gramatical curta

BUILD_SENTENCE_ITEMS = [
    {
        "id": "bs1",
        "fragments": ["always", "the library", "on Fridays", "visits", "she"],
        "answer": ["she", "always", "visits", "the library", "on Fridays"],
        "sentence": "She always visits the library on Fridays.",
        "note": "Advérbio de frequência entre o sujeito e o verbo principal.",
    },
    {
        "id": "bs2",
        "fragments": ["never", "seen", "I", "have", "such a beautiful sunset"],
        "answer": ["I", "have", "never", "seen", "such a beautiful sunset"],
        "sentence": "I have never seen such a beautiful sunset.",
        "note": "Presente perfeito com \"never\" entre o auxiliar \"have\" e o particípio.",
    },
    {
        "id": "bs3",
        "fragments": ["the book", "who", "recommended", "the teacher", "was", "very helpful"],
        "answer": ["the teacher", "who", "recommended", "the book", "was", "very helpful"],
        "sentence": "The teacher who recommended the book was very helpful.",
        "note": "Oração relativa restritiva com \"who\" logo após o sujeito \"the teacher\".",
    },
    {
        "id": "bs4",
        "fragments": ["not only", "he", "late", "but also", "arrived", "forgot", "his notes"],
        "answer": ["he", "not only", "arrived", "late", "but also", "forgot", "his notes"],
        "sentence": "He not only arrived late but also forgot his notes.",
        "note": "Estrutura correlativa \"not only... but also\" com paralelismo verbal (arrived / forgot).",
    },
    {
        "id": "bs5",
        "fragments": ["by", "will", "the project", "next Friday", "finished", "be"],
        "answer": ["the project", "will", "be", "finished", "by", "next Friday"],
        "sentence": "The project will be finished by next Friday.",
        "note": "Futuro passivo: \"will be + particípio\" + prazo com \"by\".",
    },
    {
        "id": "bs6",
        "fragments": ["she", "said", "(that)", "the meeting", "postponed", "had been"],
        "answer": ["she", "said", "(that)", "the meeting", "had been", "postponed"],
        "sentence": "She said (that) the meeting had been postponed.",
        "note": "Discurso indireto: backshift para past perfect a partir de um relato no passado.",
    },
    {
        "id": "bs7",
        "fragments": ["had", "I", "known", "would", "I", "earlier,", "have left"],
        "answer": ["had", "I", "known", "earlier,", "I", "would", "have left"],
        "sentence": "Had I known earlier, I would have left.",
        "note": "Terceiro condicional com inversão (sem \"if\"): \"Had + sujeito + particípio...\".",
    },
    {
        "id": "bs8",
        "fragments": ["the", "students", "who", "studied", "passed", "hardest", "the exam"],
        "answer": ["the", "students", "who", "studied", "hardest", "passed", "the exam"],
        "sentence": "The students who studied hardest passed the exam.",
        "note": "Relativa restritiva + advérbio superlativo \"hardest\" após o verbo \"studied\".",
    },
    {
        "id": "bs9",
        "fragments": ["so", "the", "exam", "that", "difficult", "half", "the class", "failed", "was"],
        "answer": ["the", "exam", "was", "so", "difficult", "that", "half", "the class", "failed"],
        "sentence": "The exam was so difficult that half the class failed.",
        "note": "Estrutura \"so + adjetivo + that + consequência\".",
    },
    {
        "id": "bs10",
        "fragments": ["were", "I", "in", "your", "position,", "I", "would", "reconsider", "the offer"],
        "answer": ["were", "I", "in", "your", "position,", "I", "would", "reconsider", "the offer"],
        "sentence": "Were I in your position, I would reconsider the offer.",
        "note": "Segundo condicional invertido (formal): \"Were I...\" substitui \"If I were...\".",
    },
]
