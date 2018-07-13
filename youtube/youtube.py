from __future__ import unicode_literals
import youtube_dl

from pathlib import Path
from os import path, listdir
from os.path import isfile, join

MEDIA_SUFFIX = "m4a"

def get_dl_dir():
    return path.join(str(Path.home()), "Downloads", "fuse-youtube-downloads")

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

# Retrieves file names from a path
def _list_dir(path):
    return [file for file in listdir(path) if isfile(join(path, file))]

def _print_unicode(source):
    if isinstance(source, list):
        for item in source:
            item = item.encode("utf-8")
            print(item)
    elif isinstance(source, str):
        source = source.encode("utf-8")
        print(source)

# Checks if a file + .m4a exists in a list
def _file_exists_in_list(file_list, file_name):
    file_name += "." + MEDIA_SUFFIX
    if file_name in file_list:
        return True
    return False
    
def _extract_meta_info(url):
    with youtube_dl.YoutubeDL() as ytdl:
        try:
            meta = ytdl.extract_info(url, download=False)
            return {
                "title": meta["title"],
            }
        except youtube_dl.DownloadError as err:
            print("_extract_meta_info: Download error")
            print(err)
        except Exception as err:
            print("_extract_meta_info: exception caught")
            print(err)
    return None

def does_music_video_exist(url):
    file_list = _list_dir(dl_dir)
    file_name = _extract_meta_info(url)["title"]
    return _file_exists_in_list(file_list, file_name)

def download_music(url):
    ret_code = None
    with youtube_dl.YoutubeDL(music_dl_opts) as ytdl:
        ret_code = ytdl.download([url])
    return ret_code