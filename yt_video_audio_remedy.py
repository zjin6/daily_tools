import os
from datetime import datetime
import csv
from yt_video_audio import pull_video_title, get_video_audio
from request_retry import list_failed


folder_path = input("folder: ")
is_mp3 = input("download MP3? Y/N: ").upper()

file_name = "failed_url_video.csv"
file_path = os.path.join(folder_path, file_name)


# Read the CSV file into a list
failed_url_video = []
with open(file_path, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        failed_url_video.extend(row)
print(failed_url_video)


for url_video in failed_url_video :
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    print(url_video)
    
    pull_video_title(url_video)
    get_video_audio(url_video, folder_path, is_mp3)
    
    
# Write the list to the CSV file
with open(file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(list_failed)
print(f"\nfailure-downloadings saved to {file_path}: ")
print(list_failed)