import requests
import os
import time

base_url = "https://source.unsplash.com/collection/"

def getRandomPhotoFromColletion(collectionId, resolution="1920x1080"):
    url = base_url + str(collectionId) + '/' + str(resolution)
    wallpaper = requests.get(url)
    filepath = os.environ['HOME']+'/.local/share/wallpapers/photo_' + str(int(time.time())) + '.jpg'

    with open(filepath, 'wb') as f:
        f.write(wallpaper.content)
    
    return filepath
