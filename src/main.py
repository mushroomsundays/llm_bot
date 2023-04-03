import openai
import json
import os
import time
import numpy as np
from utils import twitter_utils as tu
import tweepy

MODEL = "gpt-3.5-turbo"

def main():
    # Replace YOUR_API_KEY with your actual API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    program_input = str(np.random.randint(0,2021))

    # Set up the prompt
    with open("prompts/historical_society.txt", "r") as f:
        prompt = f.read().replace('PROGRAM_INPUT', program_input)
    print(f"Imported prompt:\n{prompt}")
    print("Sending API request...")
    start = time.time()
    completion = openai.ChatCompletion.create(
        model=MODEL, 
        messages = [{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    end = time.time()
    print(f"API returned a response in {round(end - start, 1)} seconds.")

    # Save response as JSON
    with open("completions/most_recent.json", "w") as f:
        json.dump(completion, f)
    print("Raw completion saved to completions/most_recent.json\n")

    # Extract the completion data
    output = completion['choices'][0]['message']['content']
    metadata = {
        'id': completion['id'],
        'object': completion['object'],
        'created': completion['created'],
        'model': completion['model']
    }

    print(f"Output:\n{output}")
    #print(f"Metadata:\n{metadata}")

    # Save the prompt, output, and metadata to a file
    with open("completions/completions.json", "a") as outfile:
        data = {"prompt": prompt, "output": output, "metadata": metadata}
        json.dump(data, outfile)
        outfile.write("\n")
    print("Formatted completion appended to completion/completions.json")

    # Ask for permission to send tweet
    valid_answer = False 
    while not valid_answer:
        tweet_yn = input("Post Twitter thread? (y/n)").lower()
        if tweet_yn not in ('y', 'n'):
            print("Please input a valid answer: Y, y, N, n")
            continue
        else:
            valid_answer = True # End loop and store variable

    # Post Twitter thread if instructed to do so
    if tweet_yn == 'y':
        # Authenticate to Twitter
        try:
            auth = tu.authenticate_to_twitter_api()
        except Exception as e:
            print(f"Error authenticating to Twitter.\n{e}")
            return 0

        # Create api object
        api = tweepy.API(auth, wait_on_rate_limit=True)

        thread_content = tu.get_thread_content(output)
    
        for i,tweet in enumerate(thread_content):
            print(f"{i+1}\nTweet: {tweet}\nLength: {len(tweet)}")

        tu.send_tweet_thread(api, thread_content)

if __name__ == "__main__":
    main()





