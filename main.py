# Zachary Long 6/4/2024
#WOTD Twitter bot V 0.0.5

import tweepy
import drawer
import nltk
from datetime import datetime, date
import requests
import random
import config
import holidays

word_api_key=config.word_api_key
auth = tweepy.OAuth1UserHandler(config.api_key, config.api_secret, config.access_token, config.access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(config.bearer_token, config.api_key, config.api_secret, config.access_token, config.access_token_secret)

default_don="images/the_don.png"

# Choose between Wordnik word of the day and common words library
use_wordnik_word = False  # Set to True to use Wordnik word of the day, False for common words library

# Get the current date
current_date = datetime.now().strftime("%m/%d")

# Text to include in the tweet
tweet_text = f"{current_date}"

#Get the word of the day 

def fetch_word_of_the_day(word_api_key):
    url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={word_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("word", None)
    else:
        print("Failed to fetch word of the day.")
        return None

def get_holiday_word():
    today = date.today()
    us_holidays = holidays.US(years=today.year)

    holiday_words = {
        "New Year's Day": ["celebrate", "party", "fireworks", "resolution"],
        "Valentine's Day": ["love", "romance", "heart", "cupid","Please Heather come back I didnt mean what I said"],
        "Easter": ["eggs", "bunny", "chocolate", "spring"],
        "Halloween": ["spooky", "pumpkin", "candy", "ghost"],
        "Christmas Day": ["gift", "merry", "jolly", "tree"],
        "Independence Day": ["freedom", "patriotism", "flag", "fireworks"],
        "Thanksgiving": ["gratitude", "feast", "family", "turkey"],
        "Labor Day": ["work", "rest", "celebration", "parade"]
    }

    for holiday in holiday_words.keys():
        if today in us_holidays and us_holidays[today] == holiday:
            return holiday, random.choice(holiday_words[holiday])
    return None, None

def get_holiday_image_path(holiday):
    holiday_images = {
        "New Year's Day": "images/new_years_day.png",
        "Valentine's Day": "images/valentines_day.png",
        "Easter": "images/easter.png",
        "Halloween": "images/halloween.png",
        "Christmas Day": "images/christmas.png",
        "Independence Day": "images/independence_day.png",
        "Thanksgiving": "images/thanksgiving.png",
        "Labor Day": "images/labor_day.png"
    }
    return holiday_images.get(holiday, default_don)

# Fetch word of the day from the API
word = fetch_word_of_the_day(word_api_key)

# Priority to holiday word if available, otherwise use word of the day
holiday, holiday_word = get_holiday_word()

def fetch_random_oxford_word():
    with open("oxford_5000.txt", "r") as file:
        oxford_words = file.read().splitlines()
    return random.choice(oxford_words)

#Do the word
if holiday_word:
    word=holiday_word
    print("Holiday word drawn:", word)
elif word and use_wordnik_word:
    print("Word of the day drawn from Wordnik:", word)
else:
    word = fetch_random_oxford_word()
    print("Random word drawn from Oxford 5000 word list:", word)

image_path = get_holiday_image_path(holiday) if holiday else default_don

drawer.draw_text_on_image(word, image_path)

if (word[len(word)-2]=='e' or word[len(word)-2]=='o') and word[len(word)-1]=='r':
        tweet_text=tweet_text + " " + word + " her? I hardly know her (I am very sorry)"

print(tweet_text)

# Path to the image
image_path = "C:/Users/zane1/Desktop/Don Cheadle Bot/output.jpg"

# Upload the image
upload = api.media_upload(image_path)

# Extract the media ID
media_id = upload.media_id_string

# Post tweet with image

client.create_tweet(text=tweet_text, media_ids=[media_id])
