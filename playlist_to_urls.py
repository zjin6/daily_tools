from pytube import Playlist

playlist = Playlist("https://www.youtube.com/playlist?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5")


video_urls = playlist.video_urls

from pytube import YouTube

for video_url in video_urls:
    yt = YouTube(video_url)
    yt.streams.first().download()
