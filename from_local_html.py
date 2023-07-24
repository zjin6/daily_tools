import re



def read_htmlfile(file_path):
    with open(file_path, "rb") as f:
        html = f.read().decode("utf-8")
    # print(html[:200])
    return html


def fetch_vmess(html):
    vmess_pattern = r'vmess://[a-zA-Z0-9+/=]+'
    vmess_codes = re.findall(vmess_pattern, html)
    print(str(len(vmess_codes)) + ' vmess codes ' + '-' * 40)
    for i, code in enumerate(vmess_codes):
        print(i+1, code)    
    return vmess_codes


def fetch_title(html):
    playlist_titles = re.findall(r'yt-simple-endpoint style-scope ytd-grid-playlist-renderer.*?>(.*?)</a>', html)
    print(str(len(playlist_titles)) + ' playlists ' + '-' * 40)
    for i, title in enumerate(playlist_titles):
        print(i+1, title)    
    return playlist_titles    
    

if __name__ == '__main__':
    file_path = input("path to .html: ")
    html = read_htmlfile(file_path)
    # fetch_vmess(html)
    fetch_title(html)
    
    
    
    
import pafy 
    

url = "https://www.youtube.com / playlist?list = PLqM7alHXFySGqCvcwfqqMrteqWukz9ZoE"

playlist = pafy.get_playlist(url)
author = playlist["author"]
title = playlist["title"]