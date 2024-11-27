import os
from PIL import Image, ImageDraw, ImageFont

os.chdir('C:/Users/MSI/Desktop/GigaChatAIBot')

def draw_text_with_wrap(image, text, position, font, max_width):
    draw = ImageDraw.Draw(image)
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox(position, test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)
    line_spacing= 20
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill=(173, 216, 230))  # Changed fill to white for better visibility
        bbox = draw.textbbox((position[0], y), line, font=font)
        y += bbox[3] - bbox[1] + line_spacing

# Example usage
image = Image.open('background_photo.png')
font_size = 72  # Adjust font size for readability
font = ImageFont.truetype("new_font.ttf", font_size)  # Use a specific font and size

text = ("В конце года я наконец-то осуществил свою мечту — нарисовал картину, которая отражала все эти яркие моменты. С каждой кисточкой я переносил на холст радость, страхи и смех, которые пережил за этот год. Когда я закончил, я посмотрел на свою работу и понял, что это не просто картина, а целая история, полная эмоций и воспоминаний. Она стала для меня напоминанием о том, как важно ценить каждый момент и делиться радостью с окружающими. Этот год стал для меня не просто временем, а настоящим путешествием в мир эмоций и открытий в мир эмоций и открытий в мир эмоций и открытий эмоций и открытий эмоций да"
        "")
max_width = 1755  # Adjusted maximum width for the text

# Set position for the text to be in the blurred area at the bottom
text_position = (220, 2115)  # Adjusted Y position to fit within the blurred area

draw_text_with_wrap(image, text, text_position, font, max_width)

# Save the image
image.save('output_image.png')