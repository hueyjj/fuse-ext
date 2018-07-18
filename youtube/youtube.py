from __future__ import unicode_literals
import youtube_dl

from pathlib import Path
from os import path, listdir
from os.path import isfile, join
import logging

LOG_FILE = "youtube.log"
logging.basicConfig(filename=LOG_FILE, filemode="w", level=logging.DEBUG)
console =  logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)

MEDIA_SUFFIX = "m4a"

def get_dl_dir():
    return path.join(str(Path.home()), "Downloads", "fuse-youtube-downloads")

dl_dir = get_dl_dir()

'''
Read this. What these options actually do is try and download the m4a format of a 
youtube video, but if it doesn't find m4a then it converts it to m4a. Sometimes there are
some m4a which will still have video coded into them. The current solution is to just
run post process to extract the audio and keep the same format (m4a). 
What what we know so far, choosing a "format": !"m4a" results in downloading the entire 
video and then extracting the audio, which is not viable on a shitty connection.

And order of postprocessors matter.
'''
music_dl_opts = {
    "format": "m4a",
    "ignoreerrors": "True",
    "writethumbnail": "True",
    "outtmpl": path.join(dl_dir, "%(title)s.%(ext)s"),
    "postprocessors": [
        { "key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"},
        { "key": "EmbedThumbnail" },
    ]
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
    # Double quote are replaced by single quotes when downloading
    file_name = youtube_dl.utils.sanitize_filename(file_name)
        
    for f in file_list:
        filename, _ = path.splitext(f)
        if file_name == filename:
            return True
    with open("log.txt", "ab") as e:
        for f in file_list:
            e.write(f.encode("utf-8"))
            e.write("\n".encode())
        e.write(file_name.encode("utf-8"))
        e.write("\n".encode())
    out = "file_name=" + str(file_name.encode("utf-8")) + " does not exist"
    logger.debug(out)
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
