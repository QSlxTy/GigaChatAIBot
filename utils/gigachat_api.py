import ast
import json
import os
from datetime import datetime

import gigachat

from src.config import BotConfig
from utils.prompts import generate_text_prompt, generate_photo_prompt
from utils.replicate_api import replicate_func

REPLICATE_API_TOKEN = BotConfig.replicate_token

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


async def transform_input(input_string):
    print(input_string)
    print(type(input_string))
    try:
        data = json.loads(input_string)
        print(data)
    except json.JSONDecodeError:
        raise ValueError("Некорректный формат JSON")

    # Проверяем, является ли data списком
    if isinstance(data, list):
        # Если список содержит более одного элемента
        if len(data) > 1:
            return data  # Возвращаем как есть
        else:
            return [data[0]]  # Возвращаем как список с одним элементом
    else:
        raise ValueError("Ожидался список объектов JSON")


async def gigachat_generate_text(data):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False, model="GigaChat-Pro")
    response = giga.chat(f'{generate_text_prompt} Вот входящие данные в формате JSON: {data}')
    start_index = response.choices[0].message.content.find('[')
    end_index = response.choices[0].message.content.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response.choices[0].message.content[start_index:end_index + 1]
    return ast.literal_eval(response)


async def gigachat_generate_prompt(data):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False, model="GigaChat-Pro")
    response = giga.chat(f'{generate_photo_prompt} Вот входящие данные в формате list: {data}')
    print('Ответ генерации визуализации API -', response.choices[0].message.content)
    start_index = response.choices[0].message.content.find('[')
    end_index = response.choices[0].message.content.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response.choices[0].message.content[start_index:end_index + 1]
    return ast.literal_eval(response)


async def gigachat_generate_photo(data_list, user_id):
    output_list = []
    for index, data in enumerate(data_list):
        output = await replicate_func(data, user_id)
        for index_output, item in enumerate(output):
            with open(f"files/{user_id}_generated/output_{index}.png", "wb") as file:
                file.write(item.read())
            break
        output_list.append(f"files/{user_id}_generated/output_{index}.png")
    return output_list


async def generate_main(text, path_list, user_id):
    text_response = await gigachat_generate_text(text)
    print(text_response)
    prompt_response_list = await gigachat_generate_prompt(text_response)
    print(prompt_response_list)
    photo_path_list = await gigachat_generate_photo(prompt_response_list, user_id)
    print(photo_path_list)
    return photo_path_list, text_response
