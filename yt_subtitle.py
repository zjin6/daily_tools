from youtube_transcript_api import YouTubeTranscriptApi
import os
import urllib.request
import re
import pandas as pd
from datetime import datetime
import time
from pytube import YouTube
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


english_code_set = ['en', 'en-US', 'a.en']
@retry(max_attempts=12, sleep_time=5) 
def get_language_code(video_id):
    code_list = []
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("Available Language Code: ", end='')
    for transcript in transcripts: # to list all codes
        language_code = transcript.language_code
        print(language_code, end=' ')
        if language_code in english_code_set:
            code_list.append(language_code)
    return code_list


@retry(max_attempts=12, sleep_time=5)  
def english_subtitles(video_id, file_path, language_code):
    # Get the transcript for the YouTube video in English
    transcript_en = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])

    # Create an English .srt file
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write each English subtitle entry to the .srt file
        for index, line in enumerate(transcript_en):
            start_time = line['start']
            end_time = line['start'] + line['duration']
            subtitle_text = line['text']
            subtitle_entry = f"{index + 1}\n{convert_time(start_time)} --> {convert_time(end_time)}\n{subtitle_text}\n\n"
            f.write(subtitle_entry)

    print(f"\nsaved: {file_path}")
    print('next subtitle ...')    
    return f


def convert_time(seconds):
    # Convert time in seconds to the format used in .srt files (HH:MM:SS,mmm)
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


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
    
    video_title = pull_video_title(url_video)      
    filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
     
    file_path = os.path.join(save_path, filename)
    code_list = get_language_code(video_id)
    if code_list:
        english_subtitles(video_id, file_path, code_list[0])
    else:
        continue
    
