import os
import random
import re

import PIL.Image
import PIL.ImageEnhance
import PIL.ImageFont
import PIL.ImageDraw


def select_sample(data):
    sample_divider = '===================='
    samples = data.split(sample_divider)
    sample = random.choice(samples)
    lines = sample.splitlines()
    select_this = random.randint(0, len(lines) - 11)
    return lines[select_this:select_this + 11]


def find_longest_line(font, lines):
    max_width = 0
    for line in lines:
        text_width = font.getmask(line).getbbox()[2]
        if text_width > max_width:
            max_width = text_width
    return max_width


def draw_lines(lines):
    margin = 60
    font = PIL.ImageFont.truetype("Aller/tahoma.ttf", size=23)
    longest_line = find_longest_line(font, lines)

    image_width = min(longest_line + margin, 1600)
    image_height = 345

    bgs = os.listdir('backgrounds')
    random_bg = random.choice(bgs)
    background = PIL.Image.open(os.path.join('backgrounds', random_bg))

    cropped_bg = background.crop((0, background.height - image_height, image_width, background.height))

    enhancer = PIL.ImageEnhance.Brightness(cropped_bg)
    cropped_bg = enhancer.enhance(0.2)

    draw = PIL.ImageDraw.Draw(cropped_bg)
    for line_no, line in enumerate(lines):
        username_part = ':'.join(line.split(':')[:2])
        text_part = ':'.join(line.split(':')[2:])
        draw.text((8, line_no * 28), username_part + ":", (255, 240, 154), font=font)
        username_width = font.getmask(username_part).getbbox()[2]
        draw.text((8 + username_width, line_no * 28), text_part, (255, 255, 255), font=font)

    draw.text((8, 11 * 28), ">", (255, 255, 255), font=font)
    draw.text((8 + 15, 11 * 28), "|", (230, 230, 230), font=font)

    return cropped_bg


def validate_lines(lines):
    for line in lines:
        try:
            x = line.split(':')[:2]
        except:
            return False

        if len(line) < 1:
            return False

    return True


def filter_words(lines):
    filters = {r'eren_ekebas': "haygiya"}
    new_lines = []
    for line in lines:
        new_line = line
        for old_word, new_word in filters.items():
            new_line = re.sub(old_word, new_word, new_line, flags=re.IGNORECASE)
        new_lines.append(new_line)
    return new_lines


def select_lines_from_sample(sample):
    lines = sample.splitlines()
    select_this = random.randint(0, len(lines) - 11)
    return lines[select_this:select_this + 11]


def validate_sample(sample):
    return len(sample.splitlines()) >= 11


if __name__ == '__main__':
    with open('gpt2_gentext.txt', encoding='utf-8') as f:
        data = f.read()

    samples = data.split("====================")
    os.makedirs('sample_images', exist_ok=True)
    for i, sample in enumerate(samples):
        if not validate_sample(sample):
            continue
        selected_lines = select_lines_from_sample(sample)
        while not validate_lines(selected_lines):
            selected_lines = select_lines_from_sample(sample)

        new_lines = filter_words(selected_lines)
        img = draw_lines(new_lines)
        img.save(os.path.join('sample_images', f'sample{i}.png'))
