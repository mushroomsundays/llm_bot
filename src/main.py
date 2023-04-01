import openai
import json
import os
import time

def parse_response():
    with open('response.json') as json_file:
        data = json.load(json_file)

    response = data['choices'][0]['message']['content']

    print(response)
    return response

def main():
    # Replace YOUR_API_KEY with your actual API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Set up the prompt
    with open("prompts/prompt.txt", "r") as f:
        prompt = f.read()
    print(f"Imported prompt:\n{prompt}")
    print("Sending API request...")
    start = time.time()
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages = [{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    end = time.time()
    print(f"API returned a response in {round(end - start, 1)} seconds.")

    # Save response as JSON
    with open("completions/most_recent.json", "w") as f:
        json.dump(completion, f)
    print("Raw completion saved to completions/most_recent.json")

    # Extract the completion data
    output = completion['choices'][0]['message']['content']
    metadata = {
        'id': completion['id'],
        'object': completion['object'],
        'created': completion['created'],
        'model': completion['model']
    }

    print(f"Output:\n{output}")
    print(f"Metadata:\n{metadata}")

    # Save the prompt, output, and metadata to a file
    with open("completions/completions.json", "a") as outfile:
        data = {"prompt": prompt, "output": output, "metadata": metadata}
        json.dump(data, outfile)
        outfile.write("\n")
    print("Formatted completion appended to completion/completions.json")

if __name__ == "__main__":
    main()





