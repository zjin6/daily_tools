from pytube import YouTube
# from pytube.cli import on_progress
from datetime import datetime
import time
# import urllib.request
import re
import os
# import pandas as pd


url_video = input("Enter video collection link : ")
mp3 = input("Download MP3? Y/N : ").upper()
save_path = r'D:\YT_temp'   #input("Enter path to save : ")
# print("\n" + url_video)
print("save to ... " + save_path)


i = 0
while i < 1:
    
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    try:
        def progress_callback(stream, chunk, bytes_remaining):
            total_size = ys.filesize
            progress_percent = ((total_size - bytes_remaining) / total_size) * 100
            time_spent = datetime.now() - start
            minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
            print(str(int(progress_percent)) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
                
        yt = YouTube(url_video, on_progress_callback = progress_callback)
        start = datetime.now()
        print('Title: ',yt.title)
        
        if mp3 =='Y' :
            ys = yt.streams.filter(only_audio=True)[4]
            print("download MP3 ... " + str(int(ys.filesize/10**6)) + ' MB')          
            out_file = ys.download(save_path)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
                
        else:
            ys = yt.streams.get_highest_resolution()
            print("download Video ... " + str(int(ys.filesize/10**6)) + ' MB')
            #print(str(int(ys.filesize/10**6)) + ' MB')
            ys.download(save_path) 
             
        print('\n' + 'download Subtitle ...')
        if 'en' in yt.captions:
            caption = yt.captions['en']
        elif 'a.en' in yt.captions:
            caption = yt.captions['a.en']
        elif 'en-GB' in yt.captions:
            caption = yt.captions['en-GB']   
            
        else:
            print('no Subtitle, jump to next ...')
            i += 1
            continue            

               
        caption_text = caption.generate_srt_captions()
        filename = re.sub(r'[<>:/\|?*"#,.\']+', '', yt.title) + '.srt'
        caption_path = save_path + '\\' + filename
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(caption_text)
              
        time_spent = datetime.now() - start
        print('time: ' + str(time_spent).split('.')[0])  
        i += 1
        
    except Exception as e:
        print("Exception --------------- : " + str(e))        
        
        if 'HTTP Error 429' in str(e):
            for wait in range(5):
                print(wait, end=' ')
                time.sleep(1)                
        
        continue











