from pytube import YouTube
# from pytube.cli import on_progress
from datetime import datetime
import time
import urllib.request
import re
import pandas as pd


# try to fix "Exception: IncompleteRead", seems does NOT work
# import http.client
# http.client.HTTPConnection._http_vsn = 10
# http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


yt_link = input("Enter video collection link : ")
save_path = input("Enter path to save : ")
list_link = yt_link.split("?")[1]
html = urllib.request.urlopen(yt_link)

video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
video_ids = pd.Series(video_ids).drop_duplicates()
video_ids = list(video_ids)
qty_video = len(video_ids)



i = 0
dead_link_trail = 0
incomp_list = []
while i < qty_video:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    # url_video = "https://www.youtube.com/watch?v=" + video_ids[i] + "&" + list_link + "&index=" + str(i+1)
    url_video = "https://www.youtube.com/watch?v=" + video_ids[i]
    print(url_video)

    try:
        def progress_callback(stream, chunk, bytes_remaining):
            total_size = ys.filesize
            progress_percent = int(((total_size - bytes_remaining) / total_size) * 100)
            time_spent = datetime.now() - start
            minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
            print(str(progress_percent) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
                
        yt = YouTube(url_video, on_progress_callback = progress_callback)
        start = datetime.now()
        print('Title: ',yt.title)
        ys = yt.streams.get_highest_resolution()
        print("download Video ... " + str(int(ys.filesize/10**6)) + ' MB')
        ys.download(save_path) 
        
        print('\n' + 'download Subtitle ...')
        if 'en' in yt.captions:
            caption = yt.captions['en']
        elif 'a.en' in yt.captions:
            caption = yt.captions['a.en']
        else:
            print('no Subtitle, jump to next ...')
            i += 1
            continue
            
        caption_text = caption.generate_srt_captions()
        filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', yt.title) + '.srt'
        caption_path = save_path + '\\' + filename
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(caption_text)
              
        time_spent = datetime.now() - start
        print('time: ' + str(time_spent).split('.')[0])  
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
print("\n" + current_time)
print('Incompleted videos: ---------------')
incomp_string = ''
for title, url in incomp_list:
    to_string = title + ': ' + url + '\n'
    incomp_string += to_string
    print(to_string, end='')


incomp_list_path = save_path + '\\' + 'Incompleted videos: ---------------'
with open(incomp_list_path, 'w', encoding='utf-8') as f:
    f.write(incomp_string)



    




























