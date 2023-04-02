import tweepy
import os

def authenticate_to_twitter_api(secrets):
    # authenticate to Twitter API
    auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
    auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])

####################
# Send Tweet
####################
def send_tweet(content):
    # Send tweet
    # set up your Twitter API credentials
    secrets = {
        'consumer_key': os.getenv('TWITTER_API_KEY'),
        'consumer_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }
    # Authenticate to Twitter
    try:
        auth = authenticate_to_twitter_api(secrets)
    except Exception as e:
        print(f"Error authenticating to Twitter.\n{e}")
        return 0
    # Create API object
    try:
        api = tweepy.API(auth, wait_on_rate_limit=True)
    except Exception as e:
        print(f"Error creating Twitter API object.\n{e}")
        return 0
    # Send tweet
    try:
        api.update_status(content)
        print("Tweet sent!")
    except Exception as e:
        print(f"Error sending tweet.\n{e}")
        return 0



    return auth








