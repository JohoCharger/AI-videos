import requests
from openai import OpenAI
import os
from datetime import datetime
import secrets
import time
import json
import random
import selectimages
import makemovie
import config

CHATGPT_PROD_KEY = secrets.CHATGPT_PROD_KEY
LEONARDO_PROD_KEY = secrets.LEONARDO_PROD_KEY


current_date = datetime.now()
formatted_date = current_date.strftime('%d-%m-%Y')


client = OpenAI(
    # This is the default and can be omitted
    api_key=CHATGPT_PROD_KEY
)

# Define the messages in the conversation
messages = [
    {"role": "system",
     "content": config.ASSISTANT
    },
    {"role": "user", "content": config.QUERY}
]
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-4o",
)

response = chat_completion.choices[0].message.content

tokens = response.split("\n")

prompts = []
for i in range(config.NUM_PROMPTS):
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

image_list = []

for prompt in prompts:
    leonardo_json = {
        "alchemy": True,
        "height": config.IMAGE_HEIGHT,
        "modelId": config.MODEL_ID,
        "num_images": config.NUM_IMAGES,
        "prompt": prompt["prompt"],
        "width": config.IMAGE_WIDTH
    }
    testing_json = {
        "alchemy": True,
        "height": config.IMAGE_HEIGHT,
        "modelId": config.MODEL_ID,
        "num_images": config.NUM_IMAGES,
        "prompt": prompt["prompt"],
        "width": config.IMAGE_WIDTH

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

        image_list.append({
            "filename": filename,
            "caption": prompt["name"]
        })

selectimages.choose_images(image_list)
for image in selectimages.selected_images:
    print(image["filename"])
makemovie.make_movie(selectimages.selected_images)