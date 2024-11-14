generate_text_prompt = (
    """Я передал тебе значения в формате JSON.
        {
          "question": "Вопрос который был задан пользователю,
          "answer": "Ответ польхователя"
        }.
    Твоя задача сгенерировать текстовую историю, состоящую из 5 абзацев, которые последовательно описывают ключевые моменты года пользователя.
    Ответ ты должен выдать в формате списка в котором каждый абзац на отдельном месте
    Пример:
    [
        "Абзац 1";
        "Абзац 2";
        "Абзац 3";
        "Абзац 4";
        "Абзац 5"
    ]
    Ты должен отвечать только по этому шаблону, не используй никаких джругих форматов, или специальных символов. Дай ответ в формате list python
    """
)
generate_photo_prompt = (
    """Я передал тебе значения в формате 
    [
        "Абзац 1";
        "Абзац 2";
        "Абзац 3";
        "Абзац 4";
        "Абзац 5"
    ]
    Твоя задача учитывая информацию, написать визуализацию для каждого абзаца, твоя задача описать героя этой истории. 
    Есть правила формирования промта для визуализации: не больше 10 слов, на английском языке и начинай с конструкции "A person img ...". 
    Ответ ты должен выдать в формате списка в котором каждая вихуализация на отдельном месте.
    [
        "Визуализация 1";
        "Визуализация 2";
        "Визуализация 3";
        "Визуализация 4";
        "Визуализация 5"
    ]
    Ты должен отвечать только по этому шаблону, не используй никаких других форматов, или специальных символов. Дай ответ в формате list python
    """
)
