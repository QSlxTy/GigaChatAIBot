import ast
import json
import os

from integrations.database.models.stories import create_stories_db
from src.config import BotConfig
from utils.gpt_api import gpt_api_func
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


async def generate_text(data, style):
    response = await gpt_api_func(data, style)
    start_index = response.choices[0].message.content.find('[')
    end_index = response.choices[0].message.content.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response.choices[0].message.content[start_index:end_index + 1]
    return ast.literal_eval(response), response.usage.total_tokens


async def generate_prompt(data, style):
    response = await gpt_api_func(data, style)
    print('Ответ генерации визуализации API -', response.choices[0].message.content)
    start_index = response.choices[0].message.content.find('[')
    end_index = response.choices[0].message.content.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response.choices[0].message.content[start_index:end_index + 1]
    return ast.literal_eval(response), response.usage.total_tokens


async def replicate_generate_photo(data_list, user_id, path_list):
    output_list = []
    for index, data in enumerate(data_list):
        output = await replicate_func(data, user_id, path_list)
        for index_output, item in enumerate(output):
            with open(f"files/{user_id}_generated/output_{index}.png", "wb") as file:
                file.write(item.read())
                file.close()
            break
        output_list.append(f"files/{user_id}_generated/output_{index}.png")
    return output_list


async def generate_main(text, path_list, user_id, style, session_maker):
    text_response, total_tokens = await generate_text(text, style)
    print(text_response)
    await create_stories_db(user_id, text_response, int(total_tokens), session_maker)
    prompt_response_list, total_tokens = await generate_prompt(text_response, style)
    print(prompt_response_list)
    photo_path_list = await replicate_generate_photo(prompt_response_list, user_id, path_list)
    print(photo_path_list)
    return photo_path_list, text_response
