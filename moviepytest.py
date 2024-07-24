from moviepy.editor import ImageClip, TextClip, concatenate_videoclips, ColorClip

# Image paths (replace these with your actual image paths)
image_paths = [
    'Guardians-of-the-Past2c9ccc.jpg',
    'Guardians-of-the-Past66c07c.jpg',
    'Guardians-of-the-Past716863.jpg'
]

# Video size
video_size = (288, 512)

# Create a 5-second black screen with text
black_clip = ColorClip(size=video_size, color=(0, 0, 0), duration=5)
text_clip = TextClip("Which duo describes you and bro", fontsize=24, color='white', size=video_size)
text_clip = text_clip.set_duration(5).set_position('center')
intro_clip = concatenate_videoclips([black_clip, text_clip.set_start(0)])

# Create clips for each image
image_clips = []
for i, image_path in enumerate(image_paths):
    img_clip = ImageClip("images/23-07-2024/" + image_path, duration=5).resize(video_size)
    if i != 0:
        text = TextClip("this one?", fontsize=24, color='white', size=video_size)
        text = text.set_duration(5).set_position('center')
        img_clip = concatenate_videoclips([img_clip, text.set_start(0)])
    image_clips.append(img_clip)

# Concatenate all clips
final_clip = concatenate_videoclips([intro_clip] + image_clips)

# Write the result to a file
final_clip.write_videofile("output_video.mp4", fps=24)