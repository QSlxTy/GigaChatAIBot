import ast
import json
import os

from integrations.database.models.stories import create_stories_db
from src.config import BotConfig
from utils.gpt_api import gpt_api_func_text, gpt_api_func_prompt
from utils.photo_maker import photo_maker_func
from utils.replicate_api import replicate_func

REPLICATE_API_TOKEN = BotConfig.replicate_token

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


async def generate_text(data, style):
    response, total_tokens = await gpt_api_func_text(data, style)
    start_index = response.find('[')
    end_index = response.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response[start_index:end_index + 1]
    return ast.literal_eval(response), total_tokens


async def generate_prompt(data, style):
    response,total_tokens = await gpt_api_func_prompt(data, style)
    start_index = response.find('[')
    end_index = response.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response[start_index:end_index + 1]
    return ast.literal_eval(response), total_tokens


async def replicate_generate_photo(data_list, user_id, path_list):
    output_list = []
    for index, data in enumerate(data_list):
        output = await replicate_func(data, user_id, path_list)
        for index_output, item in enumerate(output):
            with open(f"files/{user_id}_generated/output_{index}.png", "wb") as file:
                file.write(item.read())
        output_list.append(f"files/{user_id}_generated/output_{index}.png")
    return output_list


async def generate_main(text, path_list, user_id, style, session_maker):
    text_response, total_tokens = await generate_text(text, style)
    await create_stories_db(user_id, text_response, int(total_tokens), session_maker)
    prompt_response_list, total_tokens = await generate_prompt(text_response, style)
    photo_path_list = await replicate_generate_photo(prompt_response_list, user_id, path_list)
    end_photo_list = await photo_maker_func(photo_path_list, text_response, user_id)
    return photo_path_list, text_response
