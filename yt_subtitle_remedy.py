import os
from yt_video_audio import get_save_path, get_failur_filepath
from yt_subtitle import batch_subtitle
from yt_video_audio_remedy import fetch_video_ids



if __name__ == '__main__':   
    save_path = get_save_path(owner_playlist_title=None, base_path = r'D:\YT6', default_path=r'D:\YT_temp2')

    basename = os.path.basename(__file__)
    basename = basename.replace("_remedy", "")
    file_path = get_failur_filepath(save_path, basename)   
    video_ids = fetch_video_ids(file_path) 
    
    batch_subtitle(video_ids, save_path)
    