from pytube import YouTube
from datetime import datetime
import time
import urllib.request
import re
import pandas as pd


yt_link = input("enter url: ")
save_path = input("path to save: ")
list_link = yt_link.split("?")[1]
html = urllib.request.urlopen(yt_link)

video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
video_ids = pd.Series(video_ids).drop_duplicates()
video_ids = list(video_ids)
qty_video = len(video_ids)


i = 0
dead_link_trail = 0 # try 'IncompleteRead' for 5 times
incomp_list = []
while i < qty_video:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    url_video = "https://www.youtube.com/watch?v=" + video_ids[i]
    print(url_video)

    try:
        def progress_callback(stream, chunk, bytes_remaining):
            total_size = ys.filesize
            progress_percent = int(((total_size - bytes_remaining) / total_size) * 100)
            time_spent = datetime.now() - start
            minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
            print(str(progress_percent) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
                
        start = datetime.now()        
        yt = YouTube(url_video, on_progress_callback = progress_callback)
        print('Title: ',yt.title)
        ys = yt.streams.get_highest_resolution()
        print("download Video ... " + str(int(ys.filesize/10**6)) + ' MB')
        ys.download(save_path) 
        
        total_time_spent = datetime.now() - start
        total_seconds = total_time_spent.total_seconds()
        download_speed = ys.filesize/10**6 / total_seconds * 60 # convert to MB/min
        print('time spent: ' + str(total_time_spent).split('.')[0])          
        print(f'overall speed: {download_speed:.1f} MB/min')

        i += 1 
        dead_link_trail = 0        
        
    except Exception as e:
        print("Exception --------------- : " + str(e))        
        
        if 'HTTP Error 429' in str(e):
            for wait in range(5):
                print(wait, end=' ')
                time.sleep(1)
        elif 'IncompleteRead' in str(e):    
            dead_link_trail += 1
        elif 'is unavailable' in str(e) or 'member' in str(e) or 'streamingData' in str(e) or dead_link_trail > 5:
            incomp_list.append((yt.title, url_video))
            dead_link_trail = 0
            i += 1   
        continue


current_time = datetime.now().strftime("%H:%M")
print("closed at " + current_time)
print('Incompleted videos: ---------------')
for title, url in incomp_list:
    print(title + ': ' + url + '\n')
