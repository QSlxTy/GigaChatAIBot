import asyncio
import json
import time

import aiohttp
import requests

from bot_start import logger


async def go_api_func_image(photo_url_list, prompt):
    # url, name = await s3.start_bucket(f'C:/Users/MSI/Desktop/GigaChatAIBot/files/1137048397_generated/1.jpg',
    #                                   f'test')
    # print(url)
    # url =await transform_url(url, name)
    # print(url)
    # photo_url_list.append(url)

    logger.info(f"Photo url list -> {photo_url_list}")
    if len(photo_url_list) == 1:
        photo_url = f'--cref {photo_url_list[0]}'
    elif len(photo_url_list) == 2:
        photo_url = f'--cref {photo_url_list[0]} {photo_url_list[1]}'
    elif len(photo_url_list) == 3:
        photo_url = f'--cref{photo_url_list[0]} {photo_url_list[1]} {photo_url_list[2]}'
    else:
        photo_url = f'{photo_url_list[0]} {photo_url_list[1]} {photo_url_list[2]} {photo_url_list[3]}'
    url = "https://api.goapi.ai/api/v1/task"
    logger.info(f"Prompt -> {photo_url} {prompt} art by Pixar and comic books")
    print(f"Prompt ->  {prompt} art by Pixar and comic books {photo_url}")
    payload = json.dumps({
        "model": "midjourney",
        "task_type": "imagine",
        "input": {
            "prompt": f"{photo_url} {prompt} art by Pixar and comic books",
            "aspect_ratio": "1:1",
            "process_mode": "fast",
            "skip_prompt_check": False,
            "bot_id": 0
        },
        "config": {
            "service_mode": "",
            "webhook_config": {
                "endpoint": "",
                "secret": ""
            }
        }
    })
    headers = {
        'x-api-key': '08f5a135085756176fbc89ecb97a348242fac376fcfa4e15c6fbd51fd8f2b6b5',
        'Content-Type': 'application/json'
    }
    while True:
        async with aiohttp.ClientSession() as session:
            logger.info(f"Start Image Generation")
            async with session.post(url, headers=headers, data=payload) as response:
                json_data = await response.json()
                time.sleep(5)
                url = f"https://api.goapi.ai/api/v1/task/{json_data['data']['task_id']}"
                while True:
                    async with session.get(url, headers=headers) as response:
                        json_data = await response.json()
                    logger.info(f"Image Status: {json_data['data']['status']} --> {json_data['data']['task_id']}")
                    if json_data['data']['status'] == 'pending' or json_data['data']['status'] == 'processing':
                        logger.info(f"Image Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
                        time.sleep(5)
                        continue
                    elif json_data['data']['status'] == 'completed':
                        logger.info(f"Image Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
                        print(response.json())
                        url = await go_api_func_upscale(session, json_data['data']['task_id'])
                        return url
                    else:
                        logger.info(f"Image Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['raw_message']}")
                        break


async def go_api_func_upscale(session,task_id):
    url = "https://api.goapi.ai/api/v1/task"
    payload = json.dumps({
        "model": "midjourney",
        "task_type": "upscale",
        "input": {
            "origin_task_id": task_id,
            "index": "1"
        },
        "config": {
            "service_mode": "",
            "webhook_config": {
                "endpoint": "",
                "secret": ""
            }
        }
    })
    headers = {
        'x-api-key': '08f5a135085756176fbc89ecb97a348242fac376fcfa4e15c6fbd51fd8f2b6b5',
        'Content-Type': 'application/json'
    }
    while True:
        async with session.post(url, headers=headers, data=payload) as response:
            json_data = await response.json()
        time.sleep(10)
        url = f"https://api.goapi.ai/api/v1/task/{json_data['data']['task_id']}"
        while True:
            async with session.get(url, headers=headers) as response:
                json_data = await response.json()
            if json_data['data']['status'] == 'pending' or json_data['data']['status'] == 'processing':
                logger.info(f"Upscale Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
                time.sleep(10)
                continue
            elif json_data['data']['status'] == 'completed':
                logger.info(f"Upscale Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
                print(response.json())
                return json_data['data']['output']['image_url']
            else:
                logger.info(f"Upscale Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['message']}")
                break

