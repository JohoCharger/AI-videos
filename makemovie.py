from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import ImageClip, TextClip, concatenate_videoclips, ColorClip, CompositeVideoClip
from moviepy.config import change_settings
import os
import numpy as np
from moviepy.video.fx.resize import resize
from PIL import Image
import datetime
import config

def custom_resize(pic, newsize):
    pil_image = Image.fromarray(pic)
    resized_pil = pil_image.resize(newsize, Image.LANCZOS)
    return np.array(resized_pil)

# Set the path to the ImageMagick executable
os.environ['IMAGEMAGICK_BINARY'] = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'

# Or use the change_settings function
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# Image paths (replace these with your actual image paths)
image_paths1 = [
    {"filename": 'images/26-07-2024/Guardians-of-Time6dd27c.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Guardians-of-Time33ea83.jpg', "caption": "Guardians of Time"},
    {"filename": 'images/26-07-2024/Guardians-of-Time308473.jpg', "caption": "Guardians of Time"}
]
image_paths2 = [
    {"filename": 'images/26-07-2024/Guardians-of-Time6dd27c.jpg', "caption": "Guardians of Time"},
]
audio_path = "song.mp3"

# Video size
VIDEO_SIZE = (config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

def make_movie(image_paths):

    intro_image = image_paths[len(image_paths) - 1]
    black_clip = ImageClip(intro_image["filename"], duration=config.IMAGE_CLIP_DURATION)
    black_clip = black_clip.fl_image(lambda pic: custom_resize(pic, VIDEO_SIZE))
    # Create a 5-second black screen with text
    #black_clip = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0), duration=config.INTRO_CLIP_DURATION)
    text_clip = TextClip("Which duo describes you and bro", fontsize=config.FONT_SIZE, color='white', size=VIDEO_SIZE)
    text_clip = text_clip.set_duration(config.INTRO_CLIP_DURATION).set_position('center').set_start(0)
    intro_clip = CompositeVideoClip([black_clip, text_clip])

    # Create clips for each image
    image_clips = []
    for i, image in enumerate(image_paths):
        img_clip = ImageClip(image["filename"], duration=config.IMAGE_CLIP_DURATION)
        img_clip = img_clip.fl_image(lambda pic: custom_resize(pic, VIDEO_SIZE))
        text = TextClip(str(i+1) + ". " + image["caption"], fontsize=config.FONT_SIZE, color='white', size=VIDEO_SIZE)
        text = text.set_duration(config.IMAGE_CLIP_DURATION).set_position('center').set_start(0)
        clip = CompositeVideoClip([img_clip, text])
        image_clips.append(clip)


    # Concatenate all clips
    final_clip = concatenate_videoclips([intro_clip] + image_clips, method='compose')

    final_clip = final_clip.fl_image(lambda pic: custom_resize(pic, (VIDEO_SIZE[0] * 2, VIDEO_SIZE[1] * 2)))

    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip)

    # Write the result to a file
    f = open('lastID.txt', 'r')
    lastID = int(f.read()) + 1
    f.close()
    # write new id
    f = open('lastID.txt', 'w')
    f.write(str(lastID))
    f.close()

    final_clip.write_videofile("videos/finished-"  + str(lastID) + ".mp4", fps=24)

if __name__ == "__main__":
    make_movie(image_paths1)