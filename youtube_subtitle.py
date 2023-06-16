from youtube_transcript_api import YouTubeTranscriptApi
import os
import urllib.request
import re
import pandas as pd
from datetime import datetime
import time
from pytube import YouTube
from request_retry import retry


yt_link = input("Enter video collection link : ")
save_path = input("Enter path to save : ")


@retry(max_attempts=None, sleep_time=0)
def pull_html(yt_link):
    html = urllib.request.urlopen(yt_link)
    print('html ready ...')    
    return html

@retry(max_attempts=None, sleep_time=0)
def pull_video_title(url_video):
    video_title = YouTube(url_video).title
    print(video_title) 
    return video_title


html = pull_html(yt_link)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
video_ids = pd.Series(video_ids).drop_duplicates()
video_ids = list(video_ids)
qty_video = len(video_ids)
print(qty_video, 'videos found.')

  
def english_subtitles(video_id, file_path):
    try:
        # Get the transcript for the YouTube video in English
        transcript_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        # Create an English .srt file
        with open(file_path, 'w', encoding='utf-8') as f:
            # Write each English subtitle entry to the .srt file
            for index, line in enumerate(transcript_en):
                start_time = line['start']
                end_time = line['start'] + line['duration']
                subtitle_text = line['text']
                subtitle_entry = f"{index + 1}\n{convert_time(start_time)} --> {convert_time(end_time)}\n{subtitle_text}\n\n"
                f.write(subtitle_entry)

        print(f"saved: {file_path}")
        return True

    except Exception as e:
        print("Exception YouTubeTranscriptApi.get_transcript --------------- " + str(e))        
        
        if 'is unavailable' in str(e) or 'member' in str(e) or 'streamingData' in str(e):
            print("no authority to access, skip ...")  
            return True
           
        elif 'IncompleteRead' in str(e):
            print('try again ... ')
            return False        
       
        elif 'HTTP Error 429' in str(e):           
            for wait in range(5):
                print(wait, end=' ')
                time.sleep(1)
            return False
        else:
            print('unknown exception to check ...')
            return False


def convert_time(seconds):
    # Convert time in seconds to the format used in .srt files (HH:MM:SS,mmm)
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def try_func(func_name, video_id, file_path, try_times=12):
    run = 0
    while run < try_times:
        print(f'run {run + 1}, ', end=' ')
        run_func = func_name(video_id, file_path)
        if run_func:
            break
        else:
            run += 1
    print('next subtitle ...')


for video_id in video_ids:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    url_video = "https://www.youtube.com/watch?v=" + video_id
    print(url_video)
    
    video_title = pull_video_title(url_video)      
    filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
    
    file_path = os.path.join(save_path, filename)  
    try_func(english_subtitles, video_id, file_path)
