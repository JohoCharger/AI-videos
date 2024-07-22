import requests
from openai import OpenAI
import os
from datetime import datetime
import secrets

CHATGPT_PROD_KEY = secrets.CHATGPT_PROD_KEY
LEONARDO_PROD_KEY = secrets.LEONARDO_PROD_KEY

NUM_EXAMPLES = 3

client = OpenAI(
    # This is the default and can be omitted
    api_key=CHATGPT_PROD_KEY
)
query = "Dark, mysterious."
assistant = "Your job is to give the user " + str(NUM_EXAMPLES) +" example prompts for a text-to-image generation AI. The user wants the images to contain only two men and lots of detail and contrast. The user will give you a few adjectives or themes for you to generate the prompts from. The prompts don't need to start with \"Generate an image...\" or anything like that. He will also want a caption for the photo which should describe the two men and be no more than 2 words long, and he will want this format in your response: \n[CAPTION]\n[PROPMPT]"

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
for i in range(NUM_EXAMPLES):
  name = tokens[i * NUM_EXAMPLES].strip("[] \t\n")
  prompt = tokens[i*NUM_EXAMPLES+1]
  prompts.append({
    "name": name,
    "prompt": prompt
  })

print(prompts)