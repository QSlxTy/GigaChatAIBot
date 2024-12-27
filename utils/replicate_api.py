import replicate

from bot_start import logger
from src.config import BotConfig


async def replicate_func(prompt, path_list, sex):
    input_images = []
    if path_list is not None:
        for path in path_list:
            input_images.append(open(path, "rb"))
    else:
        input_images = []
    input_data = {
        "num_steps": 75,
        "style_name": "Comic book",
        "num_outputs": 1,
        "guidance_scale": 5,
        "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, "
                           "fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, "
                           "signature, watermark, username, blurry,  worst quality, greyscale, bad anatomy, "
                           "bad hands, error, text",
        "style_strength_ratio": 37
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
    elif len(input_images) == 0:
        input_data["input_image"] = BotConfig.base_img

    logger.info(input_data)
    if 'img' not in prompt:
        prompt = prompt.replace('man', ' man img', 1).replace('woman', ' woman img', 1)
    input_data["prompt"] = prompt + ' Use only Pixar style'
    logger.info(input_data)
    output = await replicate.async_run(
        BotConfig.replicate_model,
        input=input_data
    )
    return output
