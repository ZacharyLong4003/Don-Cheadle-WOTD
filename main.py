import tweepy
import drawer
import datetime

# Define the credentials
api_key = "API KEY"
api_secret = "API SECRET"
bearer_token = r"Bearer Token"
access_token = "Access Token"
access_token_secret = "Access Token"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Get the current date
current_date = datetime.datetime.now().strftime("%m/%d")

# Text to include in the tweet
tweet_text = f"{current_date}"

# Draw the word on the image
drawer.draw_text_on_image()

# Path to the image
image_path = "FILEPATH/output.jpg"

# Upload the image
upload = api.media_upload(image_path)

# Extract the media ID
media_id = upload.media_id_string

# Post tweet with image
client.create_tweet(text=tweet_text, media_ids=[media_id])
