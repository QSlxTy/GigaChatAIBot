import asyncio
import os

from PIL import Image, ImageDraw, ImageFont

os.chdir('C:/Users/MSI/Desktop/GigaChatAIBot')


async def photo_maker_func(text_list, photo_list, user_id):
    max_width = 1755
    font_size = 72
    text_position = (220, 2115)
    font = ImageFont.truetype("new_font.ttf", font_size)
    image = Image.open('background_photo.png')
    end_photo_list = []
    for index, text in enumerate(text_list):
        draw = ImageDraw.Draw(image)
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox(text_position, test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)
        line_spacing = 15
        y = text_position[1]
        for line in lines:
            draw.text((text_position[0], y), line, font=font, fill=(173, 216, 230))
            bbox = draw.textbbox((text_position[0], y), line, font=font)
            y += bbox[3] - bbox[1] + line_spacing

        overlay_image = Image.open(photo_list[index])
        if overlay_image.mode != 'RGBA':
            overlay_image = overlay_image.convert('RGBA')
        overlay_image = overlay_image.resize((1850, 1850))
        overlay_position = (170, 100)
        draw = ImageDraw.Draw(image)
        border_color = (173, 216, 230)
        border_thickness = 20
        border_box = (
            overlay_position[0] - border_thickness +5,
            overlay_position[1] - border_thickness+ 5,
            overlay_position[0] + overlay_image.width + border_thickness -5,
            overlay_position[1] + overlay_image.height + border_thickness-5
        )

        corner_radius = 30
        draw.rounded_rectangle(border_box, radius=corner_radius, outline=border_color, width=border_thickness)
        image.paste(overlay_image, overlay_position, overlay_image)
        image.save(f'files/{user_id}_generated/output_image_{index}.png')
        end_photo_list.append(f'files/{user_id}_generated/output_image_{index}.png')
    return end_photo_list


if __name__ == '__main__':
    photo_path = ['files/1137048397_generated/1.jpg']
    text_list1 = [
        'Это пример текста, который будет перенесен на изображении. Он не должен выходить за пределы заданной области.'
        'Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области.'
        'Он не должен выходить за пределы заданной области.Он не должен выходить за пределы заданной области.']
    user_id1 = '1137048397'
    asyncio.run(photo_maker_func(text_list1, photo_path, user_id1))
