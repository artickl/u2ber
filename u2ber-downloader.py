#!/usr/bin/python3

#based on https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl
from __future__ import unicode_literals #for preventing issues with unexpected symbols
# sudo apt install python3-pip
# pip3 install --upgrade youtube-dl
# sudo apt-get install ffmpeg
import youtube_dl #for downloading video and converting it
import argparse #for initial arguments
import os #for getting file size

parser = argparse.ArgumentParser()
parser.add_argument('--url',default='http://www.youtube.com/watch?v=BaW_jenozKc',help="Link to Youtube video")
args = parser.parse_args()
outfile=""

class MyLogger(object):
    def debug(self, msg):
        #print(msg)
        if msg.startswith("[ffmpeg] Destination: "):
            global outfile
            outfile=msg[22:]

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        exit
        #print('Done downloading, now converting ...')
        #print(d)

#TODO: check if ffmpeg can be installed/be used on Google Functions
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(
        args.url,
        download=False # We just want to extract the info
    )

if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

video_url = video['webpage_url']

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# get the size of file
size = "{:.2f}".format(os.path.getsize("./"+outfile)/1024/1024)
print("File %s has been downloaded. Total size is %s Mb" % (outfile,size))