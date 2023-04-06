import tweepy
import os
import time
import json
import base64
import numpy as np
from utils import openai_utils as ai
from slack_ import Slack 

####################
# Sleep for random number of seconds between bounds
####################
def sleep_for_random_secs(min, max):
    t = np.random.randint(min, max)
    print(f"Sleeping for {t} seconds...")
    time.sleep(t)

####################
# Authenticate to Twitter API v2
####################
def authenticate_to_twitter_api():
    # Import Twitter API credentials from local env
    secrets = {
        'consumer_key': os.getenv('TWITTER_API_KEY'),
        'consumer_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }
    # authenticate to Twitter API
    auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
    auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])

    return auth

####################
# Break up tweets longer than 140 characters
####################
def find_indexes(s, target):
    """Returns index of each occurrence of char in s"""
    return [i for i,char in enumerate(s) if char == target]

def process_tweet(tweet):
    """If tweet is >60 chars, split it."""
    # TODO: do this recursively until tweets are all short enough
    tweet_length = len(tweet)
    if tweet_length <= 260:
        return tweet
    else:
        print(f"Tweet is longer than 260 ({tweet_length}) characters:\n{tweet}")
        # Find the sentence end (period) closest to halfway through the tweet
        period_indexes = find_indexes(tweet, '.')
        print(f"Period indexes: {period_indexes}")
        halfway_point = tweet_length/2
        print(f"Halfway point: {halfway_point}")
        # Get absolute value of the difference from halfway point for each period index
        diffs_dict = {np.abs(x - halfway_point): x for x in period_indexes}
        print(f"Diffs dict: {diffs_dict}")
        diffs = diffs_dict.keys()
        min_key = min(diffs)
        print(f"Min key: {min_key}. Type: {type(min_key)}")
        index_to_break_on = diffs_dict.get(min_key)
        print(f"Index to break on: {index_to_break_on}")
        t1 = tweet[:index_to_break_on+1]
        t2 = tweet[index_to_break_on:]
        print(f"First tweet:\n{t1}\n Legnth: {len(t1)}")
        print(f"Second tweet:\n{t2}\n Length: {len(t2)}")
        return [t1,t2]

def get_thread_content(content):
    # Prepare tweet thread
    # TODO: how do I do this recursively?
    thread_content = []
    for tweet in content.split('\n'):
        #thread_content = content.split('\n')
        if len(tweet) <= 260:
            thread_content.append(tweet)
        else:
            new_tweets = process_tweet(tweet)
            for t in new_tweets:
                thread_content.append(t)
    
    # Remove blanks
    thread_content = [x for x in thread_content if len(x) > 0]
    
    return thread_content

def write_png_image(img_filename):
    image_location_json = f"images/{img_filename}.json"
    with open(image_location_json, "r") as f:
        png_str = json.load(f)['data'][0].get('b64_json')
        print("JSON loaded.")
        png_bytes = base64.b64decode(png_str) # get your raw bytes
        print("JSON decoded.")
    with open(f"images/{img_filename}.png", "bw") as fid: # write as binary file
        fid.write(png_bytes)
        print("File written.")


####################
# Send Tweet Thread
####################
def send_tweet_thread(api, thread_content):
    # Post the thread
    try:
        for i,tweet in enumerate(thread_content):
            first_sentence = tweet.replace('?','.').split('.')[0]
            if i == 0: # First tweet
                tweet += f' (1/{len(thread_content)})'
                # download dall-e image with prompt = first sentence (split on . or ?)
                img_filename = ai.download_dalle_image(prompt=first_sentence, addon='landscape')
                print(f"Image downloaded. Prompt:\n{first_sentence}")
                # Attach PNG to tweet
                #img_filename = tweet.lower().replace(' ', '_').replace(',','')[:15]
                write_png_image(img_filename)
                image_location_png = f"images/{img_filename}.png"
                ret = api.media_upload(filename=image_location_png)
                response = api.update_status(media_ids=[ret.media_id_string], status=tweet)
            else:
                if tweet[:2] == '. ':
                    print("Tweet starts with period.")
                    tweet = tweet[2:] # lstrip not working for some reason?
                # Download and attach an image if third or penultimate tweet
                # Third is usually where a character is introduced
                if (i == 2) or (i == len(thread_content)-1):
                    if i == 2:
                        addon = 'portrait'
                    else:
                        addon = 'fall_of_civ'
                    # download dall-e image with prompt = first sentence (split on . or ?)
                    img_filename = ai.download_dalle_image(prompt=first_sentence, addon=addon)
                    print(f"Image downloaded. Prompt:\n{first_sentence}")
                    # Attach PNG to tweet
                    #img_filename = tweet.lower().replace(' ', '_').replace(',','')[:15]
                    write_png_image(img_filename)
                    image_location_png = f"images/{img_filename}.png"
                    tweet += f' ({i+1}/{len(thread_content)})'
                    ret = api.media_upload(filename=image_location_png)
                    response = api.update_status(
                            tweet,
                            in_reply_to_status_id=response.id, 
                            media_ids=[ret.media_id_string],
                            auto_populate_reply_metadata=True)
                else:
                    tweet += f' ({i+1}/{len(thread_content)})'
                    response = api.update_status(
                                tweet,
                                in_reply_to_status_id=response.id,
                                auto_populate_reply_metadata=True)
            print(f"Tweet #{i+1} sent!\n{tweet}")
            id = response.id
            print(f"id for tweet: {id}")
            sleep_for_random_secs(5,30)
        print("Twitter thread complete.")
    except Exception as e:
        print(f"Error sending tweet thread.\n{e}")
        return 0
