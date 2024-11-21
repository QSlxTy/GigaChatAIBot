import aiohttp
from openai import OpenAI

from src.config import BotConfig
from utils.prompts import generate_text_prompt, generate_photo_prompt


async def gpt_api_func_text(prompt, style):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {BotConfig.gpt_token}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": f'{generate_text_prompt.replace("STYLE", style)}: {prompt}'},
                    ],
                    "temperature": 0
                }
        ) as response:
            print(await response.text())
            response = await response.json()
            return response['choices'][0]['message']['content'], response['usage']['total_tokens']


async def gpt_api_func_prompt(prompt, style):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {BotConfig.gpt_token}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": f'{generate_photo_prompt.replace("STYLE", style)}: {prompt}'},
                    ],
                    "temperature": 0
                }
        ) as response:
            print(await response.text())
            response = await response.json()
            return response['choices'][0]['message']['content'], response['usage']['total_tokens']

