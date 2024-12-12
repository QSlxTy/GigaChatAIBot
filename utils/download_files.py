import time

import requests

from bot_start import logger


async def download_func(url_list, user_id):
    path_list = []
    for count, url in enumerate(url_list):
        try:
            response = requests.get(url)
            # Проверяем, успешен ли запрос
            if response.status_code == 200:
                with open(f'files/{user_id}_generated/output_{count}.jpg', 'wb') as file:
                    file.write(response.content)
                    file.close()
                logger.info(f"Изображение успешно скачано и сохранено как files/{user_id}_generated/output_{count}.jpg")
                path_list.append(f'files/{user_id}_generated/output_{count}.jpg')
                time.sleep(1)
            else:
                logger.info(f"Ошибка при скачивании изображения: {response.status_code}")
        except Exception as e:
            logger.info(f"Произошла ошибка: {e}")

    return path_list
