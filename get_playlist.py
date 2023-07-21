from bs4 import BeautifulSoup
import requests
from request_retry import retry


@retry(max_attempts=None, sleep_time=0)
def get_playlist_url(channel_url):   
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.content, "html.parser")
    playlist_links = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-playlist-renderer"})
    
    # Extract the URLs of the playlists from the links
    playlist_urls = []
    for playlist_link in playlist_links:
        playlist_url = "https://www.youtube.com" + playlist_link["href"]
        playlist_urls.append(playlist_url)
    
    print("playlist_urls: ")
    print(playlist_urls)
    return playlist_urls


@retry(max_attempts=None, sleep_time=0)
def get_playlist(channel_url):   
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.content, "html.parser")
    playlist_containers = soup.find_all("ytd-grid-playlist-renderer", {"class": "style-scope ytd-grid-renderer"})
    
    # Extract the URLs and titles of the playlists from the containers
    playlists = {}
    for playlist_container in playlist_containers:
        playlist_link = playlist_container.find("a", {"class": "yt-simple-endpoint style-scope ytd-playlist-renderer"})
        playlist_url = "https://www.youtube.com" + playlist_link["href"]
        playlist_title = playlist_link["title"]
        playlists[playlist_title] = playlist_url
    
    print("playlist titles : urls ... ")
    print(playlists)
    return playlists


if __name__ == '__main__':

    # "https://www.youtube.com/channel/CHANNEL_ID/playlists"
    channel_url = input("channel url: ")
    get_playlist_url(channel_url)
    get_playlist(channel_url)






