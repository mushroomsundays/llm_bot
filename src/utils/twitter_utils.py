import tweepy
import os
import time
import numpy as np

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
    """If tweet is > 280 chars, split it."""
    # TODO: do this recursively until tweets are all short enough
    tweet_length = len(tweet)
    if tweet_length <= 280:
        return tweet
    else:
        print(f"Tweet is longer than 250 ({tweet_length}) characters:\n{tweet}")
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
        if len(tweet) <= 280:
            thread_content.append(tweet)
        else:
            new_tweets = process_tweet(tweet)
            for t in new_tweets:
                thread_content.append(t)
    
    # Remove blanks
    thread_content = [x for x in thread_content if len(x) > 0]
    
    return thread_content

####################
# Send Tweet Thread
####################
def send_tweet_thread(api, thread_content):
    # Post the thread
    try:
        for i,tweet in enumerate(thread_content):
            if i == 0: # First tweet
                tweet += f' (1/{len(thread_content)})'
                response = api.update_status(tweet)
            else:
                if tweet[:2] == '. ':
                    print("Tweet starts with period.")
                    tweet = tweet[2:] # lstrip not working for some reason?
                tweet += f' ({i+1}/{len(thread_content)})'
                #print(f"Tweet to send:\n{tweet}")
                #print(f"Length: {len(tweet)}")
                response = api.update_status(
                            tweet,
                            in_reply_to_status_id=response.id, 
                            auto_populate_reply_metadata=True)
                #response = client.create_tweet(text=content) # also doesn't work
            print(f"Tweet #{i+1} sent!\n{tweet}")
            #print(f"Response: {response}")
            #id = response[0].get('id')
            id = response.id
            print(f"id for tweet: {id}")
            sleep_for_random_secs(5,30)
        print("Twitter thread complete.")
    except Exception as e:
        print(f"Error sending tweet thread.\n{e}")
        return 0
