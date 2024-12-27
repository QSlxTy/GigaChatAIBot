import ast
import os

from bot_start import logger
from integrations.database.models.stories import create_stories_db
from src.config import BotConfig
from utils.download_files import download_func
from utils.go_api import go_api_func_image
from utils.gpt_api import gpt_api_func_text, gpt_api_func_prompt
from utils.photo_maker import photo_maker_func

REPLICATE_API_TOKEN = BotConfig.replicate_token

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


async def generate_text(data, style, sex):
    response, total_tokens = await gpt_api_func_text(data, style, sex)
    start_index = response.find('[')
    end_index = response.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response[start_index:end_index + 1]
    return ast.literal_eval(response), total_tokens


async def generate_prompt(data, style, sex):
    response, total_tokens = await gpt_api_func_prompt(data, style, sex)
    start_index = response.find('[')
    end_index = response.rfind(']')
    if start_index != -1 and end_index != -1:
        response = response[start_index:end_index + 1]
    return ast.literal_eval(response), total_tokens


async def replicate_generate_photo(url_list, data_list, user_id, path_list):
    output_list = []
    for data in data_list:
        output = await go_api_func_image(url_list, data)
        output_list.append(output)

    return output_list


async def generate_main(text, path_list, url_list, user_id, style, sex, session_maker):
    logger.info(f'Start GPT Generate history --> {user_id}')
    text_response, total_tokens = await generate_text(text, style, sex)
    logger.info(f'End generation history --> {text_response}\n'
                f'Start GPT Generate prompt --> {user_id}')
    await create_stories_db(user_id, text_response, int(total_tokens), session_maker)
    prompt_response_list, total_tokens = await generate_prompt(text_response, style, sex)
    logger.info(f'End generate prompt --> {prompt_response_list}\n'
                f'Start Replicate Generate photo --> {user_id}')
    photo_path_list = await replicate_generate_photo(url_list, prompt_response_list, user_id, path_list)
    logger.info(f'End generate photo --> {photo_path_list}\n'
                f'Start Photo Maker --> {user_id}')
    photo_path_list = await download_func(photo_path_list, user_id)
    end_photo_list = await photo_maker_func(text_response, photo_path_list, user_id)
    logger.info(f'End generate history --> {user_id}\n'
                f'{end_photo_list}')
    return end_photo_list
