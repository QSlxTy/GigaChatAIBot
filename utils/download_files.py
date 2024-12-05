import requests


async def download_func(url_list, user_id):
    path_list = []
    for url in url_list:
        try:
            response = requests.get(url)

            # Проверяем, успешен ли запрос
            if response.status_code == 200:
                with open(f'files/{user_id}_generated/{url.split("/")[-1]}', 'wb') as file:
                    file.write(response.content)
                print(f"Изображение успешно скачано и сохранено как f'files/{user_id}_generated/{url.split('/')[-1]}")
                path_list.append(f'files/{user_id}_generated/{url.split("/")[-1]}')
            else:
                print(f"Ошибка при скачивании изображения: {response.status_code}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    return path_list