import dbus
import requests
import os
import time

base_url = "https://source.unsplash.com/collection/"


def setWallpaperToScreens(filepath, plugin = 'org.kde.image', screen = -1):
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