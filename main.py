import requests
from openai import OpenAI
import os
from datetime import datetime
import secrets
import time
import json
import random

CHATGPT_PROD_KEY = secrets.CHATGPT_PROD_KEY
LEONARDO_PROD_KEY = secrets.LEONARDO_PROD_KEY

NUM_PROMPTS = 2
NUM_IMAGES = 3

current_date = datetime.now()
formatted_date = current_date.strftime('%d-%m-%Y')


client = OpenAI(
    # This is the default and can be omitted
    api_key=CHATGPT_PROD_KEY
)
query = "Mysterious, ancient."
assistant = "Your job is to give the user " + str(NUM_PROMPTS) +" example prompts for a text-to-image generation AI. The user wants the images to contain only two men and lots of detail and contrast. The user will give you a few adjectives or themes for you to generate the prompts from. The prompts don't need to start with \"Generate an image...\" or anything like that. He will also want a caption for the photo which should describe the two men and be no more than 2 words long, and he will want this format in your response: \n[CAPTION]\n[PROPMPT]"

# Define the messages in the conversation
messages = [
    {"role": "system",
     "content": assistant
    },
    {"role": "user", "content": query}
]
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-4o-mini",
)

# Print the assistant's reply
response = chat_completion.choices[0].message.content

tokens = response.split("\n")

prompts = []
for i in range(NUM_PROMPTS):
  name = tokens[i * 3].strip("[] \t\n")
  prompt = tokens[i*3+1]
  prompts.append({
    "name": name,
    "prompt": prompt
  })
api_key = secrets.LEONARDO_PROD_KEY
leonardo_authorization = "Bearer %s" % api_key

leonardo_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": leonardo_authorization
}

leonardo_url = "https://cloud.leonardo.ai/api/rest/v1/generations"

for prompt in prompts:
    leonardo_json = {
        "alchemy": True,
        "height": 1024,
        "modelId": "e71a1c2f-4f80-4800-934f-2c68979d8cc8",
        "num_images": NUM_IMAGES,
        "presetStyle": "ANIME",
        "prompt": prompt["prompt"],
        "width": 576
    }
    testing_json = {
        "alchemy": False,
        "height": 512,
        "modelId": "e71a1c2f-4f80-4800-934f-2c68979d8cc8",
        "num_images": NUM_IMAGES,
        "presetStyle": "ANIME",
        "prompt": prompt["prompt"],
        "width": 512

    }

    response = requests.post(leonardo_url, json=leonardo_json, headers=leonardo_headers)

    generation_id = response.json()['sdGenerationJob']['generationId']
    print("GenerationID " + str(generation_id))
    print("GenerationCost " + str(response.json()['sdGenerationJob']['apiCreditCost']))

    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

    time.sleep(30)

    response = requests.get(url, headers=leonardo_headers)

    imageList = response.json()['generations_by_pk']['generated_images']
    if len(imageList) == 0:
        print('images not ready, generation_id = ' + str(generation_id))
        exit(1)

    dirname = 'images/' + formatted_date
    if not os.path.exists(dirname): os.makedirs(dirname)

    for image in imageList:
        filename = 'images/' + formatted_date + '/' + prompt["name"].replace(' ', '-') + hex(random.randint(1000000,9999999))[2:] + '.jpg'
        f = open(filename, 'wb')
        f.write(requests.get(image["url"]).content)
        f.close()

print(prompts)