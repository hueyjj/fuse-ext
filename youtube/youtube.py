from __future__ import unicode_literals
import youtube_dl

from pathlib import Path
from os import path

def get_dl_dir():
    return path.join(str(Path.home()), "Downloads")

dl_dir = get_dl_dir()

music_dl_opts = {
    "format": "m4a",
    "ignoreerrors": "True",
    "writethumbnail": "True",
    "outtmpl": path.join(dl_dir, "%(title)s.%(ext)s"),
    "postprocessors": [{
        "key": "EmbedThumbnail"
    }]
}

def download_music(url):
    ret_code = None
    with youtube_dl.YoutubeDL(music_dl_opts) as ytdl:
        ret_code = ytdl.download([url])
    return ret_code