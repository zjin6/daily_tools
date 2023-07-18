from youtube_transcript_api import YouTubeTranscriptApi
import os
import re
from datetime import datetime
import csv
from request_retry import retry, list_failed
from yt_video_audio import get_video_ids, get_save_path, pull_video_title, get_failur_filepath, save_failur_downloadings



@retry(max_attempts=12, sleep_time=5) 
def get_language_code(video_id):
    english_code_set = ['en', 'en-US', 'a.en']
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
def english_subtitles(video_id, filepath, language_code):
    # Get the transcript for the YouTube video in English
    transcript_en = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])

    # Create an English .srt file
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write each English subtitle entry to the .srt file
        for index, line in enumerate(transcript_en):
            start_time = line['start']
            end_time = line['start'] + line['duration']
            subtitle_text = line['text']
            subtitle_entry = f"{index + 1}\n{convert_time(start_time)} --> {convert_time(end_time)}\n{subtitle_text}\n\n"
            f.write(subtitle_entry)

    print(f"\nsaved: {filepath}")
    print('next subtitle ...')    
    return f


def convert_time(seconds):
    # Convert time in seconds to the format used in .srt files (HH:MM:SS,mmm)
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


if __name__ == '__main__':
    
    yt_link = input("yt link: ")
    input_path = input("path to save: ")
    
    video_ids = get_video_ids(yt_link)
    save_path = get_save_path(input_path)
    
    for video_id in video_ids:
        current_time = datetime.now().strftime("%H:%M")
        print("\n" + current_time)
        
        url_video = "https://www.youtube.com/watch?v=" + video_id
        print(url_video)
        
        video_title = pull_video_title(url_video)      
        filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
         
        filepath = os.path.join(save_path, filename)
        code_list = get_language_code(video_id)
        if code_list:
            english_subtitles(video_id, filepath, code_list[0])
        else:
            continue
    
    basename = os.path.basename(__file__)
    file_path = get_failur_filepath(save_path, basename)
    save_failur_downloadings(file_path, list_failed)
