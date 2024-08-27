from youtube_transcript_api import YouTubeTranscriptApi
import os, re
# from pytube import YouTube
from datetime import datetime
from request_retry import retry, list_failed
from yt_video_audio import get_video_ids, get_owner_playlist_title, get_save_path, pull_video_title, get_failur_filepath, save_failur_downloadings



@retry(max_attempts=12, sleep_time=5) 
def get_language_code(video_id):
    english_code_set = ['en', 'en-US','en-GB', 'a.en']
    en_code_list = []
    chinese_code_set = ['zh', 'zh-TW', 'zh-CN']
    zh_code_list = []    
    
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("Available Language Code: ", end='')
    for transcript in transcripts: # to list all codes
        language_code = transcript.language_code
        print(language_code, end=' ')
        if language_code in english_code_set:
            en_code_list.append(language_code)
        if language_code in chinese_code_set:
            zh_code_list.append(language_code)            
            
    return en_code_list, zh_code_list # return both English and Chinese language codes


@retry(max_attempts=12, sleep_time=5)  
def download_subtitle(video_id, filepath, language_code):
    # Get the transcript for the YouTube video
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])

    # Create an English .srt file
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write each English subtitle entry to the .srt file
        for index, line in enumerate(transcript):
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


def batch_subtitle(video_ids, save_path):
    subtile_size = len(video_ids)
    
    for i, video_id in enumerate(video_ids):
        current_time = datetime.now().strftime("%H:%M")
        print("\n" + current_time)
        print(f'{i+1}/{subtile_size}: {video_id}')
        
        video_title = pull_video_title(video_id)      
        en_filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'         
        en_filepath = os.path.join(save_path, en_filename)
        zh_filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '_zh.srt'         
        zh_filepath = os.path.join(save_path, zh_filename)        
        
        
        # url_video = "https://www.youtube.com/watch?v=" + video_id
        # yt = YouTube(url_video)
        # ys = yt.streams.filter(only_audio=True).first()
        # file_name = ys.default_filename  # Get the default file name
        # out_file = os.path.join(save_path, file_name)  # Construct the full path
        # base, ext = os.path.splitext(out_file)
        # filepath = base + '.srt'       
        

        code_lists = get_language_code(video_id) # get both list for en and zh language codes
        if code_lists:
            en_code_list, zh_code_list = code_lists 
            if en_code_list:
                download_subtitle(video_id, en_filepath, en_code_list[0])
            if zh_code_list:
                download_subtitle(video_id, zh_filepath, zh_code_list[0])            
           
   
    basename = os.path.basename(__file__)
    file_path = get_failur_filepath(save_path, basename)
    save_failur_downloadings(file_path, list_failed)    


if __name__ == '__main__':    
    yt_link = input("yt link: ")
    owner_playlist_title =  get_owner_playlist_title(yt_link)
    save_path = get_save_path(owner_playlist_title=owner_playlist_title, base_path = r'D:\YT5', default_path=r'D:\YT_temp2')
    
    video_ids = get_video_ids(yt_link)
    batch_subtitle(video_ids, save_path)
































