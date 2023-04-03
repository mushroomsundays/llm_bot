import json
import io
import os
import base64
import openai
import time
import tweepy
from PIL import Image
from utils import openai_utils as ai
from utils import twitter_utils as tw

openai.api_key = os.getenv('OPENAI_API_KEY')

PROMPT = "Sui Dynasty, beautiful landscape, digital art"

#ai.download_dalle_image(PROMPT)
#print("Image downloaded")

#file = io.BytesIO(base64.b64decode(base64_data))


#****Instructions for tweeting a photo stored on file system****


# Example image manipulation
image_location = "images/Sui D-1680471312.json"
with open(image_location, 'r') as f:
    png_str = json.load(f)['data'][0].get('b64_json')
    print("JSON loaded.")
    png_bytes = base64.b64decode(png_str) # get your raw bytes
    print("JSON decoded.")

with open('images/test.png', 'bw') as fid: # write as binary file
    fid.write(png_bytes)
    print("File written.")
#img = Image.open()
#print("Image created.")

"""
time.sleep(5)

# Save image in-memory
b = io.BytesIO()
img.save(b, "PNG")
print("Image object saved.")
b.seek(0)
"""


auth = tw.authenticate_to_twitter_api()
api = tweepy.API(auth, wait_on_rate_limit=True)

#api.update_with_media(info[randomChoice]['image'], 
#                      status=info[randomChoice]['text'])

#api.update_with_media(filename="images/Sui D-1680471312.json", status="Image")

# Upload media to Twitter APIv1.1
#ret = api.media_upload(file=b)
ret = api.media_upload(filename="images/test.png")

# Attach media to tweet
api.update_status(media_ids=[ret.media_id_string], status="Image post test")
print("Image posted")

