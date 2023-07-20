import pyperclip
import pyautogui
import re
from yt_video_audio import save_failur_downloadings



print('please bring Chrome browser to desk front now ... 5 seconds to wait ...')
pyautogui.sleep(5)


def copy_url():
    print('\ncopy url ...')
    urls = []
    i = 0
    
    while True:
        i += 1
        pyautogui.sleep(1)  
        pyautogui.hotkey('ctrl', 'tab')
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        url = pyperclip.paste()
            
        if url in urls: break
        urls.append(url)
        print(i, url[:50]) # limit length of printing to see one line only
    
    return urls
    

def url_2_id(video_urls):
    print('\nconvert to id ... below not youtube video links ...')
    video_ids = []
    
    for i, url in enumerate(video_urls):
        try:
            video_id = re.search(r'(?<=https://www\.youtube\.com/watch\?v=)[^&]+', url).group(0)
            video_ids.append(video_id)
        except Exception as e:
            print(i+1, url[:50])
    
    print("\nfetched ids:")
    print(video_ids)
    return video_ids
   

if __name__ == '__main__':  
    file_path1 = r"D:\YT_temp2\yt_video_audio_failed.csv"
    file_path2 = r"D:\YT_temp2\yt_subtitle_failed.csv"

    video_urls = copy_url()
    video_ids = url_2_id(video_urls)
    save_failur_downloadings(file_path1, video_ids)
    save_failur_downloadings(file_path2, video_ids)
