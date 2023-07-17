import os
import re
from datetime import datetime
import csv
from yt_video_audio import pull_video_title
from yt_subtitle import get_language_code, english_subtitles
from request_retry import list_failed


folder_path = input("folder: ")

file_name = "failed_video_id.csv"
file_path = os.path.join(folder_path, file_name)


# Read the CSV file into a list
failed_video_id = []
with open(file_path, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        failed_video_id.extend(row)
print(failed_video_id)


for video_id in failed_video_id :
    current_time = datetime.now().strftime("%H:%M")
    print("\n" + current_time)
    url_video = "https://www.youtube.com/watch?v=" + video_id
    print(url_video)
    
    video_title = pull_video_title(url_video)      
    filename = re.sub('[<>:\/\\\|?*"#,.\']+', '', video_title) + '.srt'
    filepath = os.path.join(folder_path, filename)
     
    code_list = get_language_code(video_id)
    if code_list:
        english_subtitles(video_id, filepath, code_list[0])
    else:
            continue
    
    
# Write the list to the CSV file
with open(file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(list_failed)
print(f"\nfailure-downloadings saved to {file_path}: ")
print(list_failed)