from pytube import YouTube
from datetime import datetime
import time
import urllib.request
import re
import pandas as pd
import os
from request_retry import retry


yt_link = input("yt link: ")
input_path = input("path to save: ")


@retry(max_attempts=None, sleep_time=0)
def pull_html(yt_link):
    html = urllib.request.urlopen(yt_link)
    print('html ready ...')    
    return html


keyword1 = 'playlist?list='
keyword2 = 'www.youtube.com/@'
def get_video_ids(yt_link):
    if (keyword1 in yt_link) or (keyword2 in yt_link):
        html = pull_html(yt_link)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids = list(pd.Series(video_ids).drop_duplicates())
        print(len(video_ids), 'videos found.') 
    else:
        video_ids = re.findall(r"watch\?v=(\S{11})", yt_link)
    return video_ids 
video_ids = get_video_ids(yt_link)


def get_save_path(input_path, video_ids, default_path=r'D:\YT_temp'):
    if len(input_path) == 0 and len(video_ids) == 1:
        save_path = default_path
    else:
        save_path = input_path
    return save_path
save_path = get_save_path(input_path, video_ids)


@retry(max_attempts=12, sleep_time=5) 
def get_video(url_video, save_path):

    def progress_callback(stream, chunk, bytes_remaining):
        total_size = ys.filesize
        progress_percent = int(((total_size - bytes_remaining) / total_size) * 100)
        time_spent = datetime.now() - start
        minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
        print(str(progress_percent) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
            
    start = datetime.now()        
    yt = YouTube(url_video, on_progress_callback = progress_callback)
    ys = yt.streams.get_highest_resolution()
    print("download Video ... " + str(int(ys.filesize/10**6)) + ' MB')
    ys.download(save_path) 
    
    total_time_spent = datetime.now() - start
    total_seconds = total_time_spent.total_seconds()
    download_speed = ys.filesize/10**6 / total_seconds * 60 # convert to MB/min
    print('time spent: ' + str(total_time_spent).split('.')[0])          
    print(f'overall speed: {download_speed:.1f} MB/min')


@retry(max_attempts=None, sleep_time=0)
def pull_video_title(url_video):
    video_title = YouTube(url_video).title
    print(f'Title: {video_title}') 
    return video_title


for video_id in video_ids:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    url_video = "https://www.youtube.com/watch?v=" + video_id
    print(url_video)
    
    pull_video_title(url_video)
    get_video(url_video, save_path)
