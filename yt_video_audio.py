from pytube import YouTube
from datetime import datetime
import urllib.request
import re
import pandas as pd
import os
import csv
from request_retry import retry, list_failed



@retry(max_attempts=None, sleep_time=0)
def pull_html(yt_link):
    html = urllib.request.urlopen(yt_link)
    print('html ready ...')    
    return html


def get_video_ids(yt_link):
    keyword1 = 'playlist?list='
    keyword2 = 'www.youtube.com/@'
    
    if (keyword1 in yt_link) or (keyword2 in yt_link):
        html = pull_html(yt_link)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids = list(pd.Series(video_ids).drop_duplicates())
        print(len(video_ids), 'videos found.') 
    else:
        video_ids = re.findall(r"watch\?v=(\S{11})", yt_link)
    return video_ids 


def get_save_path(input_path, default_path=r'D:\YT_temp2'):
    if len(input_path) == 0:
        save_path = default_path
    else:
        save_path = input_path
    return save_path


@retry(max_attempts=12, sleep_time=5) 
def get_video_audio(video_id, save_path, is_mp3):
    url_video = "https://www.youtube.com/watch?v=" + video_id
    def progress_callback(stream, chunk, bytes_remaining):
        total_size = ys.filesize
        progress_percent = ((total_size - bytes_remaining) / total_size) * 100
        time_spent = datetime.now() - start
        minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
        print(str(int(progress_percent)) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
            
    start = datetime.now()        
    yt = YouTube(url_video, on_progress_callback = progress_callback)
    
    if is_mp3 =='Y' :
        ys = yt.streams.filter(only_audio=True)[4]
        print("download MP3 ... " + str(int(ys.filesize/10**6)) + ' MB')          
        out_file = ys.download(save_path)
        # rename to .mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    else:
        ys = yt.streams.get_highest_resolution()
        print("download Video ... " + str(int(ys.filesize/10**6)) + ' MB')
        ys.download(save_path) 
    
    total_time_spent = datetime.now() - start
    total_seconds = total_time_spent.total_seconds()
    download_speed = ys.filesize/10**6 / total_seconds * 60 # convert to MB/min
    print('time spent: ' + str(total_time_spent).split('.')[0])          
    print(f'overall speed: {download_speed:.1f} MB/min')


@retry(max_attempts=None, sleep_time=0)
def pull_video_title(video_id):
    url_video = "https://www.youtube.com/watch?v=" + video_id
    video_title = YouTube(url_video).title
    print(f'Title: {video_title}') 
    return video_title


def get_failur_filepath(save_path, basename):   
    filename_without_ext = os.path.splitext(basename)[0]
    file_name = filename_without_ext + "_failed.csv"
    file_path = os.path.join(save_path, file_name)
    return file_path


def save_failur_downloadings(file_path, list_failed):   
    # Write the list to the CSV file
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_failed)
    print(f"\nfailure-downloadings saved to {file_path}: ")
    print(list_failed)
    return csvfile


def batch_video_audio(video_ids, save_path):   
    is_mp3 = input("download MP3? Y/N: ").upper()   
    
    for video_id in video_ids:
        current_time = datetime.now().strftime("%H:%M")
        print("\n" + current_time)
        print(video_id)
        
        pull_video_title(video_id)
        get_video_audio(video_id, save_path, is_mp3)
       
    basename = os.path.basename(__file__)
    file_path = get_failur_filepath(save_path, basename)
    save_failur_downloadings(file_path, list_failed)    


if __name__ == '__main__':   
    yt_link = input("yt link: ")
    input_path = input("path to save: ")    
    
    video_ids = get_video_ids(yt_link)  
    save_path = get_save_path(input_path)    
    batch_video_audio(video_ids, save_path)
    
