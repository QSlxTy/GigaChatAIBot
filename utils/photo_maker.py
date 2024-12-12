from PIL import Image, ImageDraw, ImageFont

from bot_start import logger


async def photo_maker_func(text_list, photo_list, user_id):
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
            bbox = draw.textbbox(text_position, test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        line_spacing = 35
        y = text_position[1]
        total_text_height = 0

        for line in lines:
            bbox = draw.textbbox((text_position[0], y), line, font=font)
            text_height = bbox[3] - bbox[1]
            total_text_height += text_height + line_spacing

        if total_text_height > (end_text - text_position[1]):
            lines = lines[:(end_text - text_position[1]) // (font_size + line_spacing)]

        y = text_position[1]
        for line in lines:
            bbox = draw.textbbox((text_position[0], y), line, font=font)
            text_height = bbox[3] - bbox[1]
            draw.text((text_position[0], y), line, font=font, fill=(173, 216, 230))
            y += text_height + line_spacing
        try:
            overlay_image = Image.open(photo_list[index])

            if overlay_image.mode != 'RGBA':
                overlay_image = overlay_image.convert('RGBA')
            overlay_image = overlay_image.resize((1850, 1850))
            overlay_position = (170, 100)
            draw = ImageDraw.Draw(image)
            border_color = (173, 216, 230)
            border_thickness = 20
            border_box = (
                overlay_position[0] - border_thickness + 5,
                overlay_position[1] - border_thickness + 5,
                overlay_position[0] + overlay_image.width + border_thickness - 5,
                overlay_position[1] + overlay_image.height + border_thickness - 5
            )

            corner_radius = 30
            draw.rounded_rectangle(border_box, radius=corner_radius, outline=border_color, width=border_thickness)
            image.paste(overlay_image, overlay_position, overlay_image)
            jpeg_path = f'files/{user_id}_generated/output_image_{index}.jpeg'
            image.convert('RGB').save(jpeg_path, 'JPEG', quality=85)  # Установите желаемое качество
            end_photo_list.append(jpeg_path)
            image.close()
        except Exception as _ex:
            logger.error(f'Photomaker error --> {_ex}')
            image.close()

    return end_photo_list
