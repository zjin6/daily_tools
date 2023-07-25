    
    
    
import pafy 
    

url = "https://www.youtube.com / playlist?list = PLqM7alHXFySGqCvcwfqqMrteqWukz9ZoE"

playlist = pafy.get_playlist(url)
author = playlist["author"]
title = playlist["title"]