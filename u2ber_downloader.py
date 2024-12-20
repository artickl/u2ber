#!/usr/bin/python3

#based on https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl
from __future__ import unicode_literals #for preventing issues with unexpected symbols
import youtube_dl #pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
import argparse #for initial arguments
import os #for getting file size

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

def u2ber_download(url, folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                'key': 'EmbedThumbnail',
            },
        ],
        'outtmpl': '%(title)s-%(id)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'verbose': True,
    }

    ydl_opts['outtmpl'] = folder+"/"+ydl_opts['outtmpl']
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            url,
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

    return outfile, size


def main(args):
    outfile, size = u2ber_download(args.url, args.folder)
    print("File %s has been downloaded. Total size is %s Mb" % (outfile,size))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',default='http://www.youtube.com/watch?v=BaW_jenozKc',help="Link to Youtube video")
    parser.add_argument('--folder',default='download',help="Folder where file should be stored")
    args = parser.parse_args()
    outfile=""

    main(args)