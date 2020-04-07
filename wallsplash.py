#!/usr/bin/env python3
import dbus
import requests
import os
import time
import random
# More info at: https://source.unsplash.com/

base_url = "https://source.unsplash.com/collection/"

def setWallpaperToScreens(filepath, screen = -1, plugin = 'org.kde.image'):
    jscript = """
    var allDesktops = desktops();
    var screen = %i

    if (screen > -1){
        d = allDesktops[screen];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        d.writeConfig("Image", "file://%s")
    }
    else {
        for (i = 0; i < allDesktops.length; i++) {
            d = allDesktops[i];
            d.wallpaperPlugin = "%s";
            d.currentConfigGroup = Array("Wallpaper", "%s", "General");
            d.writeConfig("Image", "file://%s")
        }
    }
    """
    
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % (screen, plugin, plugin, filepath, plugin, plugin, filepath))

def getRandomPhotoFromColletion(collectionId, resolution="1920x1080"):
    url = base_url + str(collectionId) + '/' + str(resolution)
    wallpaper = requests.get(url)
    filepath = os.environ['HOME']+'/.local/share/wallpapers/photo_' + str(int(time.time())) + '.jpg'
    try:
        with open(filepath, 'wb') as f:
            f.write(wallpaper.content)
    except:
        os.remove(filepath)
        return "Error!! Couldn't write to filepath!"
    
    return filepath

def deleteOldWallpapers(days=1):
    for file in os.listdir(): 
        if int(time.time()) - os.stat(file)[-2] > 60*60*24*days: 
            os.remove(file)
        
if __name__ == "__main__":
    deleteOldWallpapers(days=1)
    collections = [
        8807226, 
        1976082, 
        786921,
        784236, 
        8925813,
        488437,
        535285,
        142563,
        1111575,
        ]
    
    for screen in range(0, 2):
        collection = random.choice(collections)
        filepath = getRandomPhotoFromColletion(collection)
        setWallpaperToScreens(filepath, screen)
        time.sleep(2)
        
    