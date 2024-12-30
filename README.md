# AI Video creator

### TikTok video generator made for fun!

## Description 🗒️

- Simple program that combines ChatGPT, Leonardo.ai image generation and automated video editing.
- The program generates a video consisting of a series of images featuring cool looking AI generated images.
- The images featured in the video consist of two people in different scenarios, although the program can be easily 
  configured to generate anything by changing the ChatGPT prompt.

## What Does the program Do? 🤔

1. The program starts by prompting the user for a theme.
2. Using this prompt, the program requests ChatGPT, to generate a few different prompts for a text-to-image AI 
   application based on the users wishes.
3. The program then sends these prompts to Leonardo.ai, which generates the images, three versions of each prompt.
4. After the images are generated and fetched, a tkinter window is opened, allowing the user to select the best 
   image generated by each prompt.
5. The program uses `pymovie` to create a video using these images along with some automated editing.
6. The video is then saved to the `videos` directory. Images are also stored in the `images` directory.

## Notes 📝
- Running this program is not free, as it uses ChatGPT and Leonardo.ai.
- In the root directory create a `secrets.py` file with two string constants:
  - **LEONARDO_PROD_KEY** (your leonardo.ai api key)
  - **CHATGPT_PROD_KEY** (your chatgpt api key)
- When requesting images from Leonardo.ai the program pauses for 30 seconds, allowing the images to be generated. It 
  will then send only one request to Leonardo.ai to fetch the generated images. If the images are not yet generated, 
  the program will exit. This should never happen, as there is quite a lot of buffer time.
- This program was made for fun, and should not be taken too seriously.