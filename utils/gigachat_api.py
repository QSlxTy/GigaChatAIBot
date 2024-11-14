import ast
import asyncio
import base64
import json
import os

import gigachat
import replicate

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
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = giga.chat(f'{generate_text_prompt} Вот входящие данные в формате JSON: {data}')
    print(response.choices[0].message.content)
    return response.choices[0].message.content


async def gigachat_generate_prompt(data):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = giga.chat(f'{generate_photo_prompt} Вот входящие данные в формате list: {data}')
    print(response.choices[0].message.content)
    start_index = response.choices[0].message.content.find('[')
    end_index = response.choices[0].message.content.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response.choices[0].message.content[start_index:end_index + 1]
    return ast.literal_eval(response)


async def gigachat_generate_photo(data_list, user_id):
    input_images = []
    for file in os.listdir(f'files/{user_id}/'):
        with open(f'files/{user_id}/{file}', 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            input_images.append(f"data:application/octet-stream;base64,{data}")
    output_list = []
    for data in data_list:
        output_list.append(await replicate_func(input_images, data))
    return output_list


async def generate_main(text, user_id, path):
    text_response = await gigachat_generate_text(text)
    prompt_response_list = await gigachat_generate_prompt(text_response)
    photo_list = await gigachat_generate_photo(prompt_response_list, user_id)
    print(photo_list)
