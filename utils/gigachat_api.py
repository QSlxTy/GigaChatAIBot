import json

import gigachat

from src.config import BotConfig
from utils.prompts import generate_text_prompt


async def gigachat_api_func(prompt, text):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = await giga.chat(f'{prompt}: {text}')
    print(response)
    return response


async def gigachat_generate_text(text):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = await giga.chat(f'{generate_text_prompt} Вот входящие данные в формате JSON: {text}')
    print(response)
    return response


async def gigachat_generate_prompt(text):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = await giga.chat(f'{generate_text_prompt} Вот входящие данные в формате JSON: {text}')
    result_list = json.loads(response.replace('\n', '').replace('`', '').replace('json', ''))
    print(result_list)
    print(response)
    return response


async def gigachat_generate_photo(text):
    giga = gigachat.GigaChat(credentials=BotConfig.gigachat_key, verify_ssl_certs=False)
    response = await giga.chat(f'{generate_text_prompt} Вот входящие данные в формате JSON: {text}')
    result_list = json.loads(response)
    print(result_list)
    print(response)
    return response


async def generate_main(text):
    text_response = await gigachat_generate_text(text)
    prompt_response_list = await gigachat_generate_prompt(text_response)
