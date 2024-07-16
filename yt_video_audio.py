from pytube import YouTube, Playlist
from datetime import datetime
import urllib.request
import re
import pandas as pd
import os, subprocess
import csv
from request_retry import retry, list_failed



@retry(max_attempts=None, sleep_time=0)
def pull_html(yt_link):
    html = urllib.request.urlopen(yt_link)
    print('html ready ...')    
    return html


def get_video_ids(yt_link):
    keyword1 = 'playlist?list='
    keyword2 = 'www.youtube.com/@'
    
    if keyword1 in yt_link:
        playlist = Playlist(yt_link)
        re_context = str(playlist.video_urls)
    elif keyword2 in yt_link:
        html = pull_html(yt_link)
        re_context = html.read().decode()
    else:
        re_context = yt_link

    video_ids = re.findall(r"watch\?v=(\S{11})", re_context)
    video_ids = list(pd.Series(video_ids).drop_duplicates())
    print(len(video_ids), 'videos found.') 
    return video_ids 


def get_owner_playlist_title(yt_link):
    playlist = Playlist(yt_link)
    try:
        playlist_title = playlist.title
        owner = playlist.owner
        print("Owner:", owner)
        print("Playlist Title:", playlist_title)
        return owner, playlist_title
    except Exception as e:
        print('No playlist_title available: Exception- ' + str(e))
        return None


def get_save_path(owner_playlist_title=None, base_path = r'D:\YT6', default_path=r'D:\YT_temp2'):
    if owner_playlist_title == None:
        input_path = input("path to save: ")
        if len(input_path) == 0:
            save_path = default_path
        else:
            save_path = input_path
    else:
        owner, playlist_title  = owner_playlist_title
        folder_name_initial = f"{owner} - {playlist_title}"
        folder_name = re.sub('[<>:\/\\\|?*"#,.\']+', '', folder_name_initial)
        folder_path = os.path.join(base_path, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created at {base_path}")
        else:
            print(f"Folder '{folder_name}' already exists at {base_path}")           
        save_path = folder_path
            
    return save_path


@retry(max_attempts=24, sleep_time=5) 
def get_audio(video_id, save_path):
    url_video = "https://www.youtube.com/watch?v=" + video_id
    def progress_callback(stream, chunk, bytes_remaining):
        total_size = ys.filesize
        progress_percent = ((total_size - bytes_remaining) / total_size) * 100
        time_spent = datetime.now() - start
        minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
        print(str(int(progress_percent)) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
            
    start = datetime.now()        
    yt = YouTube(url_video, on_progress_callback = progress_callback)
    
    audio_streams = yt.streams.filter(only_audio=True, mime_type="audio/mp4")
    audio_stream = sorted(audio_streams, key=lambda s: int(s.abr[:-4]), reverse=True)[0]
    ys = audio_stream            
    filesize = audio_stream.filesize
    print(f"audio = {int(filesize / 10**6)} MB, abr: {audio_stream.abr}")
     
    out_file = audio_stream.download(save_path)
    base, ext = os.path.splitext(out_file) # rename to _au.mp3
    audio_file = base + '_au.mp4'
    os.rename(out_file, audio_file)   
   
    total_time_spent = datetime.now() - start
    total_seconds = total_time_spent.total_seconds()
    download_speed = filesize/10**6 / total_seconds * 60 # convert to MB/min
    print('time spent: ' + str(total_time_spent).split('.')[0])          
    print(f'overall speed: {download_speed:.1f} MB/min')
    
    return audio_file
 
    
@retry(max_attempts=24, sleep_time=5) 
def get_video(video_id, save_path):
    url_video = "https://www.youtube.com/watch?v=" + video_id
    def progress_callback(stream, chunk, bytes_remaining):
        total_size = ys.filesize
        progress_percent = ((total_size - bytes_remaining) / total_size) * 100
        time_spent = datetime.now() - start
        minutes_left = round(time_spent.total_seconds() / progress_percent * (100 - progress_percent) /60, 1)
        print(str(int(progress_percent)) + '% | ' + str(minutes_left) + 'mins ... ', end='')        
            
    start = datetime.now()        
    yt = YouTube(url_video, on_progress_callback = progress_callback)
           
    resolutions = ["1080p", "720p", "480p", "360p"]
    for res in resolutions:
        video_stream = yt.streams.filter(res=res, mime_type="video/mp4").first()
        if video_stream:
            break             
    ys = video_stream
    filesize = video_stream.filesize        
    print(f"video = {int(filesize / 10**6)} MB, res: {res}")
           
    out_file = video_stream.download(save_path)       
    base, ext = os.path.splitext(out_file) # rename to _vi.mp4
    video_file = base + '_vi.mp4'
    os.rename(out_file, video_file)
    
    merge_file = base + '.mp4'   
   
    total_time_spent = datetime.now() - start
    total_seconds = total_time_spent.total_seconds()
    download_speed = filesize/10**6 / total_seconds * 60 # convert to MB/min
    print('time spent: ' + str(total_time_spent).split('.')[0])          
    print(f'overall speed: {download_speed:.1f} MB/min') 
    
    return merge_file, video_file   
   

def merge_video_audio(merge_path, video_path, audio_path, del_raw=True):
    command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c copy "{merge_path}"'
    print('\n' + command, end=' ...... ')
    subprocess.call(command, shell=True)
    print('merging done.')
    
    # Optionally remove the separate audio and video files
    if del_raw:
        os.remove(audio_path)
        os.remove(video_path)
        print('deleted raw video and audio files')


@retry(max_attempts=None, sleep_time=0)
def pull_video_title(video_id):
    url_video = "https://www.youtube.com/watch?v=" + video_id
    video_title = YouTube(url_video).title
    print(f'Title: {video_title}') 
    return video_title


def get_failur_filepath(save_path, basename):   
    filename_without_ext = os.path.splitext(basename)[0]
    file_name = filename_without_ext + "_failed.csv"
    file_path = os.path.join(save_path, file_name)
    return file_path


def save_failur_downloadings(file_path, list_failed):   
    # Write the list to the CSV file
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_failed)
    print(f"\nfailure-downloadings saved to {file_path}: ")
    print(list_failed)
    return csvfile


def batch_video_audio(video_ids, save_path):   
    is_mp3 = input("download MP3? Y/N: ").upper()
    video_size = len(video_ids)
    
    for i, video_id in enumerate(video_ids):
        current_time = datetime.now().strftime("%H:%M")
        print("\n" + current_time)
        print(f'{i+1}/{video_size}: {video_id}')
        
        pull_video_title(video_id)
        audio_path = get_audio(video_id, save_path)
        
        if  is_mp3 != "Y":       
            try:
                merge_path, video_path =  get_video(video_id, save_path)
                merge_video_audio(merge_path, video_path, audio_path, del_raw=True) 
            except Exception as e:
                print(e)
               
    basename = os.path.basename(__file__)
    file_path = get_failur_filepath(save_path, basename)
    save_failur_downloadings(file_path, list_failed)    


if __name__ == '__main__':   
    yt_link = input("yt link: ")
    owner_playlist_title =  get_owner_playlist_title(yt_link)
    save_path = get_save_path(owner_playlist_title=owner_playlist_title, base_path = r'D:\YT5', default_path=r'D:\YT_temp2')
    
    video_ids = get_video_ids(yt_link)  
    batch_video_audio(video_ids, save_path)
    
























