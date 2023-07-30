import re
import time
from datetime import timedelta
import keyboard
import pandas as pd
import colorama
from colorama import Fore, Style
colorama.init()



def parse_srt_file(filename):
    with open(filename, 'r') as file:
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


def batch_subtitle_explanation(subtitles, playtime, printed_subtitles, explained_words, alltensplur_dict):
    for subtitle in subtitles:
        if (subtitle[2] != ' ') and (subtitle[0] <= playtime <= subtitle[1]) and (subtitle not in printed_subtitles):
            print(Style.RESET_ALL)
            left_space = 60 - len(subtitle[2]) # assume total print lenth=60, adjustable
            print('\n'  + '-' * 60 + format_timedelta(playtime))
            print(subtitle[2] + ' ' + '-' * left_space + ' ' + format_timedelta(playtime) + '\n') # + Fore.RESET, Style.BRIGHT + 
            print_explanation(subtitle, explained_words, alltensplur_dict)
            printed_subtitles.append(subtitle)


def print_explanation(subtitle, explained_words, alltensplur_dict):
    words = subtitle[2].split()
    for word in words:
        if (len(word) > 4) and (word not in explained_words):
            try:
                explanations = alltensplur_dict[word].split('\\n')
                for i, explanation in enumerate(explanations):
                    if i == 0:
                        head = word + ' : '
                    else:
                        head = " " * (len(word) + 3)
                    print(Fore.GREEN + f' {head}{explanation}') # + Style.BRIGHT + Fore.GREEN 
                print()
                explained_words.append(word)
            except Exception:
                continue    


def batch_explanation(subtitles, playtime, printed_subtitles, explained_words, alltensplur_dict):
    for subtitle in subtitles:
        if (subtitle[2] != ' ') and (subtitle[0] <= playtime <= subtitle[1]) and (subtitle not in printed_subtitles):
            print_explanation(subtitle, explained_words, alltensplur_dict)
            printed_subtitles.append(subtitle)


def file_todic(filepath=r"C:\Users\zjin6\Downloads\ecdict_cet6_tensplur.xlsx"):
    df = pd.read_excel(filepath)
    alltensplur_dict = {}

    for index, row in df.iterrows():
        key = row['tensplur']
        value = row['definition']
        alltensplur_dict[key] = value
    
    # print(alltensplur_dict)
    return alltensplur_dict


def run_fromfile(filepath, alltensplur_dict):
    subtitles = parse_srt_file(filepath)
    printed_subtitles = []
    explained_words = []
    # last_printed_playtime = timedelta(seconds=0)
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
            batch_explanation(subtitles, playtime, printed_subtitles, explained_words, alltensplur_dict)
    
            # Check if all subtitles have been printed
            if playtime.seconds >= subtitles[-1][0].seconds:
                break
    
            # Print playtime every 15 seconds
            # if playtime - last_printed_playtime >= timedelta(seconds=15):
            #     print('\n'+'-'*50, format_timedelta(playtime))
            #     last_printed_playtime = playtime
    
        # Adjust sleep duration as needed
        time.sleep(0.1)


if __name__ == '__main__':
    print('loading dictionary ...')
    alltensplur_dict = file_todic(filepath=r"C:\Users\zjin6\Downloads\ecdict_cet6_tensplur.xlsx")
    
    filepath = input("path to the .srt file: ")
    run_fromfile(filepath, alltensplur_dict)


