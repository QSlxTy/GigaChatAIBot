import asyncio
import json
import time

import requests

from bot_start import logger
from test import transform_url
from utils.s3 import s3


async def go_api_func_image(photo_url_list, prompt):
    url, name = await s3.start_bucket(f'C:/Users/MSI/Desktop/GigaChatAIBot/files/1137048397_generated/1.jpg',
                                      f'test')
    print(url)
    url =await transform_url(url, name)
    print(url)
    photo_url_list.append(url)

    logger.info(f"Photo url list -> {photo_url_list}")
    if len(photo_url_list) == 1:
        photo_url = f'{photo_url_list[0]}'
    elif len(photo_url_list) == 2:
        photo_url = f'{photo_url_list[0]} {photo_url_list[1]}'
    elif len(photo_url_list) == 3:
        photo_url = f'{photo_url_list[0]} {photo_url_list[1]} {photo_url_list[2]}'
    else:
        photo_url = f'{photo_url_list[0]} {photo_url_list[1]} {photo_url_list[2]} {photo_url_list[3]}'
    url = "https://api.goapi.ai/api/v1/task"
    logger.info(f"Prompt -> {photo_url} {prompt} art by Pixar")
    print(f"Prompt -> {photo_url} {prompt} art by Pixar")
    payload = json.dumps({
        "model": "midjourney",
        "task_type": "imagine",
        "input": {
            "prompt": f"{photo_url} {prompt} art by Pixar",
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
        'x-api-key': '13a91570cbcc0f7cd9af31f3f4be73afb4a1fb9d3ad17a3f0cb1f829cab1d40b',
        'Content-Type': 'application/json'
    }
    logger.info(f"Start Image Generation")
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    time.sleep(5)
    url = f"https://api.goapi.ai/api/v1/task/{json_data['data']['task_id']}"
    while True:
        response = requests.get(url, headers=headers)
        json_data = response.json()
        logger.info(f"Image Status: {json_data['data']['status']} --> {json_data['data']['task_id']}")
        print(f"Image Status: {json_data['data']['status']} --> {json_data['data']['task_id']}")
        print(json_data)
        if json_data['data']['status'] == 'pending' or json_data['data']['status'] == 'processing':
            logger.info(f"Image Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            print(f"Image Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            time.sleep(5)
            continue
        elif json_data['data']['status'] == 'completed':
            logger.info(f"Image Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            print(f"Image Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            json_data = response.json()
            print(json_data)
            url = await go_api_func_upscale(json_data['data']['task_id'])
            return url
        else:
            logger.info(f"Image Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['message']}")
            print(f"Image Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['message']}")
            break


async def go_api_func_upscale(task_id):
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
        'x-api-key': '13a91570cbcc0f7cd9af31f3f4be73afb4a1fb9d3ad17a3f0cb1f829cab1d40b',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    time.sleep(10)
    url = f"https://api.goapi.ai/api/v1/task/{json_data['data']['task_id']}"
    while True:
        response = requests.get(url, headers=headers)
        json_data = response.json()
        if json_data['data']['status'] == 'pending' or json_data['data']['status'] == 'processing':
            logger.info(f"Upscale Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            print(f"Upscale Waiting: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            time.sleep(10)
            continue
        elif json_data['data']['status'] == 'completed':
            logger.info(f"Upscale Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            print(f"Upscale Completed: {json_data['data']['status']} --> {json_data['data']['task_id']}")
            json_data = response.json()
            print(json_data)
            return json_data['data']['output']['image_url']
        else:
            logger.info(f"Upscale Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['message']}")
            print(f"Upscale Error: {json_data['data']['status']} --> {json_data['data']['task_id']} --> {json_data['data']['error']['message']}")
            break

if __name__ == '__main__':
    asyncio.run(go_api_func_image([],'a man in the jungle'))