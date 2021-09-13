#based on https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl
from __future__ import unicode_literals
# sudo apt install python3-pip
# pip3 install --upgrade youtube-dl
# sudo apt-get install ffmpeg
import youtube_dl

ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(
        'http://www.youtube.com/watch?v=BaW_jenozKc',
        download=False # We just want to extract the info
    )

if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

video_url = video['webpage_url']

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])