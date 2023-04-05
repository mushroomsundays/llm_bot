import requests
import os 
from slack import WebClient
from slack.errors import SlackApiError

class Slack:
    def __init__(self, webhook_url, bot_user_oauth_token):
        self.webhook_url = webhook_url
        self.bot_user_oauth_token = bot_user_oauth_token
    
    def post_message(self, message, channel, image_path=None):
        if image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found at path: {image_path}")
            
            # Send the message with an image attached
            client = WebClient(self.webhook_url)
            with open(image_path, 'rb') as f:
                image = f.read()
                response = client.files_upload(
                    token=self.bot_user_oauth_token,
                    channels=channel,
                    content=image,
                    initial_comment=message
                )
                print(response)
        else:
            # If no image, just send the message
            result = client.chat_postMessage(
                channel=channel,
                text=message
            )
            print(result)

def main():
    # Create a new Slack object with your webhook URL and bot OAuth token
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    bot_user_oauth_token = os.getenv('SLACK_BOT_USER_OAUTH_TOKEN')
    slack = Slack(webhook_url, bot_user_oauth_token)

    # post the content of your thread to Slack
    channel = '#history'
    message = 'image test'
    image_path = 'images/test.png'
    slack.post_message(message, channel, image_path)
    #slack.post_message(content)

if __name__ == "__main__":
    main()