import requests
import json
import time
import secrets

actuallyRun = False

api_key = secrets.LEONARDO_PROD_KEY
leonardo_authorization = "Bearer %s" % api_key

leonardo_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": leonardo_authorization
}

leonardo_url = "https://cloud.leonardo.ai/api/rest/v1/generations"

leonardo_json = {
  "alchemy": True,
  "height": 1024,
  "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
  "num_images": 3,
  "presetStyle": "ANIME",
  "prompt": "A majestic cat in the snow",
  "width": 576
}

testing_json = {
  "alchemy": False,
  "height": 512,
  "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",
  "num_images": 4,
  "presetStyle": "ANIME",
  "prompt": "A majestic cat in the snow",
  "width": 512

}

#{"generations_by_pk":{"generated_images":[{"url":"https://cdn.leonardo.ai/users/7a448808-2afe-479d-aacf-780f99651d3e/generations/5d5f1319-d0b9-4219-a7d5-d1e84bdc38d4/Default_A_majestic_cat_in_the_snow_0.jpg","nsfw":false,"id":"d1d34d3c-af3b-4d78-8f22-6ba253950d1f","likeCount":0,"motionMP4URL":null,"generated_image_variation_generics":[]}, {"url":"https://cdn.leonardo.ai/users/7a448808-2afe-479d-aacf-780f99651d3e/generations/5d5f1319-d0b9-4219-a7d5-d1e84bdc38d4/Default_A_majestic_cat_in_the_snow_1.jpg","nsfw":false,"id":"4ebbd835-0e20-4f0f-af7c-15ab063fbf2f","likeCount":0,"motionMP4URL":null,"generated_image_variation_generics":[]}],"modelId":"b24e16ff-06e3-43eb-8d33-4416c2d75876","motion":null,"motionModel":null,"motionStrength":null,"prompt":"A majestic cat in the snow","negativePrompt":"","imageHeight":512,"imageToVideo":null,"imageWidth":512,"inferenceSteps":15,"seed":5958383965,"public":false,"scheduler":"EULER_DISCRETE","sdVersion":"SDXL_LIGHTNING","status":"COMPLETE","presetStyle":"ANIME","initStrength":null,"guidanceScale":7,"id":"5d5f1319-d0b9-4219-a7d5-d1e84bdc38d4","createdAt":"2024-07-23T16:56:21.208","promptMagic":false,"promptMagicVersion":null,"promptMagicStrength":null,"photoReal":false,"photoRealStrength":null,"fantasyAvatar":null,"generation_elements":[]}}

generation_id = 0

response = requests.post(leonardo_url, json=testing_json, headers=leonardo_headers)

generation_id = response.json()['sdGenerationJob']['generationId']
print("GenerationCost" + generation_id)
print(response.json()['sdGenerationJob']['apiCreditCost'])

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(30)

response = requests.get(url, headers=leonardo_headers)

imageList = response.json()['generations_by_pk']['generated_images']
if len(imageList) == 0:
  print('images not ready, generation_id = ' + str(generation_id))
  exit(1)

print(response.text)