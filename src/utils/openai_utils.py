import openai
import json
import os
import numpy as np
import time

def download_dalle_image(prompt, addon=None):
    """Prompts Dall-e and downloads the image as JSON.
    Returns img_filename which does not include the filetype (e.g. .json)"""

    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Append addon to prompt
    if addon == 'landscape':
        prompt += ', beautiful landscape, digital art'
    if addon == 'portrait':
        prompt += ', human portrait, digital art'
    if addon == 'fall_of_civ':
        # Throwing in a random number string so that this image isn't the same every time
        salt = str(np.random.randint(1000000,1999999))
        prompt += f', crumbling architecture, setting sun, digital art {salt}'

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        response_format="b64_json",
    )

    # TODO: end function here and return response. Create separate function to dump and convert to png
    timestamp = time.time()
    img_filename = prompt.lower().replace(' ', '_').replace(',','')[:15] + f'_{timestamp}'
    file_name = f"images/{img_filename}.json"

    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    return img_filename