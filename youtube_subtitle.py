from youtube_transcript_api import YouTubeTranscriptApi
import os
import urllib.request
import re
import pandas as pd
from datetime import datetime
import time
from pytube import YouTube


yt_link = input("Enter video collection link : ")
save_path = input("Enter path to save : ")
list_link = yt_link.split("?")[1]
html = urllib.request.urlopen(yt_link)

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
        with open(file_path, 'w') as f:
            # Write each English subtitle entry to the .srt file
            for index, line in enumerate(transcript_en):
                start_time = line['start']
                end_time = line['start'] + line['duration']
                subtitle_text = line['text']
                subtitle_entry = f"{index + 1}\n{convert_time(start_time)} --> {convert_time(end_time)}\n{subtitle_text}\n\n"
                f.write(subtitle_entry)

        print(f"English subtitles saved: {file_path}")

    except Exception as e:
        print("no English subtitles")
        
        
def chinese_subtitles(video_id, file_path):
     try:
         # Get the transcript for the YouTube video in Chinese (simplified)
         transcript_zh = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans'])

         # Create a Chinese .srt file
         with open(file_path, 'w') as f:
             # Write each Chinese subtitle entry to the .srt file
             for index, line in enumerate(transcript_zh):
                 start_time = line['start']
                 end_time = line['start'] + line['duration']
                 subtitle_text = line['text']
                 subtitle_entry = f"{index + 1}\n{convert_time(start_time)} --> {convert_time(end_time)}\n{subtitle_text}\n\n"
                 f.write(subtitle_entry)

         print(f"Chinese subtitles saved: {file_path}")

     except Exception as e:
         print("no Chinese subtitles")       
        

def convert_time(seconds):
    # Convert time in seconds to the format used in .srt files (HH:MM:SS,mmm)
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


# Example usage: provide the YouTube video ID and save path
for video_id in video_ids:
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    
    url_video = "https://www.youtube.com/watch?v=" + video_id
    print(url_video)
    
    video_title = YouTube(url_video).title
    print(video_title)
    
    filename_en = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
    filename_zh = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '-zh.srt'
    file_path_en = os.path.join(save_path, filename_en)  
    file_path_zh = os.path.join(save_path, filename_zh) 
    
    english_subtitles(video_id, file_path_en)
    chinese_subtitles(video_id, file_path_zh)
