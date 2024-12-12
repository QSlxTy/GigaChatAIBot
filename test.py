import asyncio

from PIL import Image, ImageDraw, ImageFont


async def photo_maker_func(text_list, user_id):
    max_width = 1755
    font_size = 72
    text_position = (220, 2115)
    end_text = 3520
    end_photo_list = []

    for index, text in enumerate(text_list):
        font = ImageFont.truetype('new_font.ttf', font_size)
        image = Image.open('background_photo.png')
        draw = ImageDraw.Draw(image)
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textsize(test_line, font=font)
            if bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        line_spacing = 35  # Увеличьте отступ между строками
        y = text_position[1]

        for line in lines:
            bbox = draw.textbbox((text_position[0], y), line, font=font)
            print(bbox)
            text_height = 70  # Высота текста
            print(text_height)
            draw.text((text_position[0], y), line, font=font, fill=(173, 216, 230))
            y += text_height + line_spacing
            print(y)

        jpeg_path = f'files/{user_id}_generated/output_image_{index}.jpeg'
        image.convert('RGB').save(jpeg_path, 'JPEG', quality=85)
        end_photo_list.append(jpeg_path)
        image.close()

    return end_photo_list


if __name__ == "__main__":
    asyncio.run(photo_maker_func([
        'Когда я впервые увидел высокий забор, который преградил мне путь, я почувствовал, как внутри меня закипает решимость. Каждый шаг к его преодолению был полон волнения и страха, но именно в тот момент я осознал, что могу больше, чем думал. С каждым прыжком я оставлял позади не только забор, но и свои сомнения, и когда я, наконец, оказался на другой стороне, мир вокруг меня засиял новыми красками.'],
        '1137048397'))
