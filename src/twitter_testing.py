from utils import twitter_utils as tu

response = tu.send_tweet('Ready to learn some history? (testing2)')

id = response[0].get('id')


print(type(response))
print(type(response[0]))
print(response[0])

"""
try:
    tweet_id = response['id']
except TypeError as e:
    print(e)

try:
    tweet_id = response.id 
except Exception as e:
    print(e)
print(f"Tweet id: {tweet_id}")
"""
