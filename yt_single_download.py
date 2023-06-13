from pytube import YouTube
from datetime import datetime
import time
import re
import os


url_video = input("enter url: ")
mp3 = input("download MP3? Y/N: ").upper()
save_path = r'D:\YT_temp'
print("default path ... " + save_path)


while True:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    try:
        def progress_callback(stream, chunk, bytes_remaining):
            total_size = ys.filesize
            progress_percent = ((total_size - bytes_remaining) / total_size) * 100
            time_spent = datetime.now() - start
            minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
            print(str(int(progress_percent)) + '% | ' + str(minutes_left) + 'mins ... ', end='')
                
        start = datetime.now()
        yt = YouTube(url_video, on_progress_callback = progress_callback)
        print('Title: ',yt.title)
        
        if mp3 =='Y' :
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

        break

    except Exception as e:
        print("Exception --------------- : " + str(e))        
        
        if 'HTTP Error 429' in str(e):
            for wait in range(5):
                print(wait, end=' ')
                time.sleep(1)                
        
        continue
