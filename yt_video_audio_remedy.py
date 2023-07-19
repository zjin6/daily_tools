import os
import csv
from yt_video_audio import get_save_path, get_failur_filepath, batch_video_audio



def fetch_video_ids(file_path):
    # Read the CSV file into a list
    video_ids = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_ids.extend(row)
    print(video_ids)
    return video_ids


if __name__ == '__main__':   
    input_path = input("path to save: ") 
    save_path = get_save_path(input_path)

    basename = os.path.basename(__file__)
    basename = basename.replace("_remedy", "")
    file_path = get_failur_filepath(save_path, basename)   
    video_ids = fetch_video_ids(file_path) 
    
    batch_video_audio(video_ids, save_path)
    