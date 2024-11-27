import asyncio
import os

import aiofiles
from PIL import Image, ImageDraw, ImageFont


async def photo_maker_func(photo_path, text_list, user_id):
    os.chdir('C:/Users/MSI/Desktop/GigaChatAIBot')
    for index, path in enumerate(photo_path):
        background = Image.open('background_photo.png')
        background = background.resize((2160, 3840))

        # Открываем фото
        photo = Image.open(path)
        photo.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        # Определяем размеры и отступы
        bg_width, bg_height = background.size
        photo_width, photo_height = photo.size
        padding = 20  # Отступы
        # Вычисляем позицию для размещения фото
        x = (bg_width - photo_width) // 2
        y = padding
        # Вставляем фото на фон
        background.paste(photo, (x, y))
        # Создаем объект для рисования
        draw = ImageDraw.Draw(background)
        # 3. Задаем координаты области для текста (левый верхний угол и правый нижний угол)
        # 3. Задаем координаты области (левый верхний угол и правый нижний угол)
        top_left = (50, 50)  # координаты левого верхнего угла
        bottom_right = (300, 150)  # координаты правого нижнего угла
        # 5. Задаем текст и шрифт
        font = ImageFont.load_default()  # используем стандартный шрифт

        # 6. Задаем координаты для текста (левый верхний угол области)
        text_position = (top_left[0] + 10, top_left[1] + 10)  # немного отступаем от границ

        # 7. Рисуем текст на изображении
        draw.text(text_position, text_list[index], fill="black", font=font)

        # Сохраняем итоговое изображение
        background.save(f'files/{user_id}_generated/end_{index}.png', format='PNG')


if __name__ == '__main__':
    photo_path = ['files/1137048397_generated/1.jpg']
    text_list = ['"Это пример текста, который будет перенесен на изображении. Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области."']
    user_id = '1137048397'
    asyncio.run(photo_maker_func(photo_path, text_list, user_id))
