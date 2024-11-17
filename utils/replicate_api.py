import base64
import os

import replicate

from src.config import BotConfig


async def replicate_func(prompt, user_id, path_list):
    input_images = []
    if path_list is not None:
        for path in path_list:
            with open(path, "rb") as file:
                input_images.append(file)
        else:
            input_images = []
    input_data = {
        "num_steps": 75,
        "style_name": "Disney Charactor",
        "num_outputs": 1,
        "guidance_scale": 5,
        "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, "
                           "fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, "
                           "signature, watermark, username, blurry,  worst quality, greyscale, bad anatomy, "
                           "bad hands, error, text",
        "style_strength_ratio": 20
    }

    if len(input_images) == 1:
        input_data["input_image"] = input_images[0]
    elif len(input_images) == 2:
        input_data["input_image"] = input_images[0]
        input_data["input_image2"] = input_images[1]
    elif len(input_images) == 3:
        input_data["input_image"] = input_images[0]
        input_data["input_image2"] = input_images[1]
        input_data["input_image3"] = input_images[2]
    elif len(input_images) == 4:
        input_data["input_image"] = input_images[0]
        input_data["input_image2"] = input_images[1]
        input_data["input_image3"] = input_images[2]
        input_data["input_image4"] = input_images[3]
    input_data["prompt"] = "A person img " + prompt + " art by Pixar"
    print(input_data)
    output = await replicate.async_run(
        BotConfig.replicate_model,
        input=input_data
    )
    for file in input_images:
        file.close()
    return output
