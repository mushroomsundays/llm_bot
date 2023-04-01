import json

with open('completions/most_recent.json') as json_file:
    data = json.load(json_file)
print(data)
print(data.keys())

response = data['choices'][0]['message']['content']

print(response)