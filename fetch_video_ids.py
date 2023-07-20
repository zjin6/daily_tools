import pyperclip
import pyautogui
from pytube import YouTube
from yt_video_audio import save_failur_downloadings



print('please bring Chrome browser to desk front now ... 5 seconds to wait ...')
pyautogui.sleep(5)


def copy_url():
    print('\npyautogui starts to copy url ...')
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
        print(i, url[:50])  # do whatever you want with the URL
    
    return urls
    

def url_2_id(video_urls):
    print('\npytube starts to convert url 2 id ... below exceptions ...')
    video_ids = []
    
    for i, url in enumerate(video_urls):
        try: # if not youtube video url
            yt = YouTube(url)
            video_id = yt.video_id
            video_ids.append(video_id)  
        except Exception as e:
            print(i+1, str(e)[:50])
    
    print("\nfetched ids:")
    print(video_ids)
    return video_ids
   

if __name__ == '__main__':  
    file_path1 = r"D:\YT2\yt_video_audio_failed.csv"
    file_path2 = r"D:\YT2\yt_subtitle_failed.csv"

    video_urls = copy_url()
    video_ids = url_2_id(video_urls)
    save_failur_downloadings(file_path1, video_urls)
    save_failur_downloadings(file_path2, video_urls)














