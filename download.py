import yt_dlp

# Specify the URL of the YouTube video
video_url = "https://www.youtube.com/watch?v=t_r-ST06jR4"

# Create a dictionary for options
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',      # Merge them into an mp4 file
    'outtmpl': './%(title)s.%(ext)s',      # Save with the video title and appropriate extension
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',           # Convert the final file to mp4 format
    }],
}

# Download the video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download complete!")