import requests
import random
from PIL import Image, ImageDraw, ImageFont
import nltk
from datetime import datetime, date



def fetch_word_of_the_day(api_key):
    url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("word", None)
    else:
        print("Failed to fetch word of the day.")
        return None

def get_holiday_word():
    today = date.today()  # Get the current date
    holiday_words = {
        "New Year's Day": ["celebrate", "party", "fireworks", "resolution"],
        "Valentine's Day": ["love", "romance", "heart", "cupid"],
        "Easter": ["eggs", "bunny", "chocolate", "spring"],
        "Halloween": ["spooky", "pumpkin", "candy", "ghost"],
        "Christmas": ["gift", "merry", "jolly", "tree"],
        "Independence Day": ["freedom", "patriotism", "flag", "fireworks"],
        "Thanksgiving": ["gratitude", "feast", "family", "turkey"],
        "Memorial Day": ["remember", "honor", "sacrifice", "hero"],
        "Labor Day": ["work", "rest", "celebration", "parade"]
    }
    holiday_dates = {
        "New Year's Day": date(today.year, 1, 1),
        "Valentine's Day": date(today.year, 2, 14),
        "Easter": date(today.year, 3, 31),
        "Halloween": date(today.year, 10, 31),
        "Christmas": (date(today.year, 12, 18), date(today.year, 12, 25)),
        "Independence Day": date(today.year, 7, 4),
        "Thanksgiving": (date(today.year, 11, 1), date(today.year, 11, 30)),
        "Memorial Day": date(today.year, 5, 1),  # Single day
        "Labor Day": date(today.year, 9, 1)  # Single day
    }
    for holiday, date_range in holiday_dates.items():
        if isinstance(date_range, tuple):  # Check if it's a date range
            start_date, end_date = date_range
            if start_date <= today <= end_date:
                return random.choice(holiday_words[holiday])
        elif date_range == today:  # Check if it's a single date
            return random.choice(holiday_words[holiday])
    return None

def draw_text_on_image(text, image_path="FILES PATH FOR IMAGE",
                       font_size=60, fixed_font_size=60, font_color="white", outline_color="black",
                       output_path="output.jpg", outline_width=2):
    try:
        image = Image.open(image_path)
    except OSError:
        raise OSError(f"Could not open image file: {image_path}")

    try:
        font = ImageFont.truetype("impact.ttf", font_size)
        fixed_font = ImageFont.truetype("impact.ttf", fixed_font_size)
    except OSError:
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
            fixed_font = ImageFont.truetype("arialbd.ttf", fixed_font_size)
        except OSError:
            raise OSError("Could not load font. Please install a bold font or provide the path to 'impact.ttf'.")

    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    fixed_text_lines = ["Don Cheadle Word", "of the Day"]
    fixed_text_height = 0
    for line in fixed_text_lines:
        fixed_text_width, line_height = draw.textsize(line, font=fixed_font)
        fixed_text_height += line_height
    fixed_text_height += len(fixed_text_lines) - 1
    fixed_y_pos = 10

    y_offset = fixed_y_pos
    for line in fixed_text_lines:
        fixed_text_width, fixed_text_height = draw.textsize(line, font=fixed_font)
        fixed_x_pos = (image_width - fixed_text_width) // 2
        draw.text((fixed_x_pos - outline_width, y_offset), line, fill=outline_color, font=fixed_font)
        draw.text((fixed_x_pos + outline_width, y_offset), line, fill=outline_color, font=fixed_font)
        draw.text((fixed_x_pos, y_offset - outline_width), line, fill=outline_color, font=fixed_font)
        draw.text((fixed_x_pos, y_offset + outline_width), line, fill=outline_color, font=fixed_font)
        draw.text((fixed_x_pos, y_offset), line, fill=font_color, font=fixed_font)
        y_offset += fixed_text_height + 1

    text_width, text_height = draw.textsize(text, font=font)
    x_pos = (image_width - text_width) // 2
    y_pos = image_height - text_height - 10

    draw.text((x_pos - outline_width, y_pos), text, fill=outline_color, font=font)
    draw.text((x_pos + outline_width, y_pos), text, fill=outline_color, font=font)
    draw.text((x_pos, y_pos - outline_width), text, fill=outline_color, font=font)
    draw.text((x_pos, y_pos + outline_width), text, fill=outline_color, font=font)
    draw.text((x_pos, y_pos), text, fill=font_color, font=font)

    try:
        image.save(output_path)
    except OSError:
        raise OSError(f"Could not save image to: {output_path}")

    print(f"Text with outline added to image. Saved as: {output_path}")

# Set your API key here
api_key = "API KEY"

# Fetch word of the day from the API
word = fetch_word_of_the_day(api_key)

# Choose between Wordnik word of the day and common words library
use_wordnik_word = False  # Set to True to use Wordnik word of the day, False for common words library

# Priority to holiday word if available, otherwise use word of the day
holiday_word = get_holiday_word()
if holiday_word:
    draw_text_on_image(holiday_word)
    print("Holiday word drawn:", holiday_word)
elif word and use_wordnik_word:
    draw_text_on_image(word)
    print("Word of the day drawn from Wordnik:", word)
else:
    common_words = nltk.corpus.words.words('en')
    random_word = random.choice(common_words)
    draw_text_on_image(random_word)
    print("Random word drawn from common words library:", random_word)
