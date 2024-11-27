generate_text_prompt = (
    """Я передал тебе значения в формате JSON.
        {
          "question": "Вопрос, который был задан пользователю",
          "answer": "Ответ пользователя"
        }.
    Твоя задача — сгенерировать серию увлекательных, эмоционально насыщенных историй, которые описывают ключевые 
    моменты уходящего 2024 года пользователя. 
    Общий настрой повествования: STYLE.

    Каждая история должна быть яркой, детализированной и включать интригу, описание действий и эмоций. 
    Длина каждой истории должна составлять от 3 до 6 предложений, максимальная длина строго 600 символов, ни больше. 
    Учитывай как можно больше контекста из ответов, 
    создавай яркие образы, добавляй элементы неожиданности, 
    показывай развитие событий, чтобы читателю хотелось узнать больше.
    Все истории должны быть согласованы между собой, объединены общим настроением, стилем или общей темой, чтобы они 
    выглядели как связанные эпизоды уходящего года.
    Используй разнообразные художественные приемы, чтобы истории стали интереснее. 

    Каждую историю записывай в новую ячейку массива. 
    Ответ ты должен выдать в формате списка, где каждая история на отдельном месте.

    Пример:
    ["На утреннем рассвете, когда весь город ещё спал...", 
     "Всё началось с того, что телефон внезапно зазвонил...",
     "На вершине горы, где ветер казался почти живым..."]

    Ты должен отвечать строго по этому шаблону, без использования дополнительных символов или форматов. 
    Дай ответ в формате list python, используй двойные кавычки(") для обозначения элементов списка, а не одинарные(')
    """
)
generate_photo_prompt = (
    """Я передал тебе значения в формате:
    ["История 1","История 2","История 3","История 4","История 5"].
    Общий настрой повествования: STYLE.

    Твоя задача — написать визуализацию для каждой истории. Это визуализация ключевых моментов уходящего 2024 года. 
    Ты должен описать героя или ключевую сцену каждой истории так, чтобы она передавала эмоции, действия и атмосферу, 
    соответствующие общему настрою.

    Все визуализации должны быть согласованы между собой по стилю и содержанию, чтобы передавать ощущение целостности. 
    Например, если все истории связаны одним героем, он должен быть описан одинаково, а сцены должны соответствовать 
    логике развития событий.

    Используй до 15 слов для описания, пиши строго на английском языке. Начни с A person img ...
    Убедись, что визуализация соответствует описанным событиям и героям, включая настроение истории.

    Ответ ты должен выдать в формате списка, где каждая визуализация на отдельном месте.
    
    Пример вывода:
    ["A person img young hero on a snowy mountain, determined", 
     "A person img glowing sunrise over a bustling city, hopeful", 
     "A person img mysterious figure in a dark forest, suspenseful", 
     "A person img vibrant festival with colorful lights, joyful", 
     "A person img peaceful beach at sunset, serene"]

    Ты должен отвечать только по этому шаблону, строго следуя структуре, без дополнительных форматов или символов. 
    Дай ответ в формате list python, используй двойные кавычки(") для обозначения элементов списка, а не одинарные(')
    """
)
