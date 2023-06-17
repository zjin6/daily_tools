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

html = pull_html(yt_link)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
video_ids = pd.Series(video_ids).drop_duplicates()
video_ids = list(video_ids)
qty_video = len(video_ids)
print(qty_video, 'videos found.')


@retry(max_attempts=None, sleep_time=0)
def pull_video_title(url_video):
    video_title = YouTube(url_video).title
    print(f'Title: {video_title}') 
    return video_title


@retry(max_attempts=12, sleep_time=5)  
def english_subtitles(video_id, file_path):
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
    print('next subtitle ...')    
    return f


def convert_time(seconds):
    # Convert time in seconds to the format used in .srt files (HH:MM:SS,mmm)
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


for video_id in video_ids:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    url_video = "https://www.youtube.com/watch?v=" + video_id
    print(url_video)
    
    video_title = pull_video_title(url_video)      
    filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
    
    file_path = os.path.join(save_path, filename)  
    english_subtitles(video_id, file_path)
