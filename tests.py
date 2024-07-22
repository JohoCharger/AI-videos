import os
from datetime import datetime

response = """[Shadowed Allies]  
A dimly lit alleyway shrouded in mist, where two men stand back-to-back, cloaked in dark trench coats. Their faces are partially obscured by shadows, revealing only their intense eyes that pierce through the gloom. A hint of neon light flickers in the background, casting a sharp contrast against their silhouettes, while splatters of rain create vivid reflections on the cobblestone pavement.

[Hidden Secrets]  
In an ancient, moss-covered forest under a moonlit sky, two men dressed in rugged, tattered clothing crouch beside an old, weathered stone altar. The air is thick with tension, shadows dancing around them as wisps of fog curl at their feet. Detailed foliage frames the scene, and a faint light emanates from a mysterious artifact they hold, illuminating their determined expressions against the dark backdrop.

[Hidden Secrets]  
In an ancient, moss-covered forest under a moonlit sky, two men dressed in rugged, tattered clothing crouch beside an old, weathered stone altar. The air is thick with tension, shadows dancing around them as wisps of fog curl at their feet. Detailed foliage frames the scene, and a faint light emanates from a mysterious artifact they hold, illuminating their determined expressions against the dark backdrop.
"""

prompts = []

tokens = response.split("\n")
for i in range(3):
  name = tokens[i * 3].strip("[] \t\n")
  prompt = tokens[i*3+1]
  prompts.append({
    "name": name,
    "prompt": prompt
  })

current_date = datetime.now()
formatted_date = current_date.strftime('%d-%m-%Y')
filename = "prompts/" + formatted_date

content = current_date.strftime('%H-%M-%S -- RESPONSE \n') + response

if os.path.exists(filename):
  with open(filename, 'a') as file:
    file.write(content + '\n')
else:
  with open(filename, 'w') as file:
    file.write(content + '\n')