import re
import time
from datetime import timedelta
import keyboard
import pandas as pd


def parse_srt_file(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n'
    matches = re.findall(pattern, content, re.DOTALL)

    subtitles = []
    for match in matches:
        start_time = timedelta(hours=int(match[1][:2]), minutes=int(match[1][3:5]), seconds=int(match[1][6:8]), milliseconds=int(match[1][9:]))
        end_time = timedelta(hours=int(match[2][:2]), minutes=int(match[2][3:5]), seconds=int(match[2][6:8]), milliseconds=int(match[2][9:]))
        text = match[3]
        subtitles.append((start_time, end_time, text))

    return subtitles

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    else:
        return "{:02d}:{:02d}".format(minutes, seconds)

def translate_subtitle(subtitle, translations):
    translated_subtitle = []
    for word in subtitle.split():
        if (len(word) > 5) and (word in translations):
            if len(translations[word]) > 6:
                translated_subtitle.append(f'{word}:{translations[word][:6]} ')
            else:
                translated_subtitle.append(f'{word}:{translations[word][:]} ')
        else:
            translated_subtitle.append(' ')
    return ' '.join(translated_subtitle)

def print_subtitle(subtitles, playtime, printed_subtitles, translations):
    for subtitle in subtitles:
        if subtitle[0] <= playtime <= subtitle[1] and subtitle not in printed_subtitles:
            original_subtitle = subtitle[2]
            translated_subtitle = translate_subtitle(original_subtitle, translations)
            print(translated_subtitle)
            print(original_subtitle)
            printed_subtitles.append(subtitle)

# Read translations from Excel
translations_df = pd.read_excel(r"C:\Users\zjin6\Downloads\toefl9400.xlsx", usecols="B,D")
translations = dict(translations_df.values)

# Example usage
filename = input("Enter the path of the .srt file: ")
subtitles = parse_srt_file(filename)

printed_subtitles = []
last_printed_playtime = timedelta(seconds=0)
paused = False
pause_start_time = None
elapsed_pause_time = 0

start_time = time.time()
while True:
    if keyboard.is_pressed(" "):
        if not paused:
            paused = True
            pause_start_time = time.time()
        else:
            paused = False
            elapsed_pause_time += time.time() - pause_start_time
        time.sleep(0.2)  # Wait for key release to avoid multiple toggles

    if not paused:
        current_time = time.time()
        elapsed_time = current_time - start_time - elapsed_pause_time
        playtime = timedelta(seconds=elapsed_time)
        print_subtitle(subtitles, playtime, printed_subtitles, translations)

        # Check if all subtitles have been printed
        if playtime.seconds >= subtitles[-1][0].seconds:
            break

        # Print playtime every 15 seconds
        if playtime - last_printed_playtime >= timedelta(seconds=15):
            print('\n'+'-'*50, format_timedelta(playtime))
            last_printed_playtime = playtime

    # Adjust sleep duration as needed
    time.sleep(0.1)









