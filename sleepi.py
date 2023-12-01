import time
import pyautogui as pg
import os
import random
import ctypes
import json

# Setup
# remove directory if exists
try:
    os.rmdir(f"C:\\Program Files\\Sleepi")
except:
    pass
path = f"C:\\Program Files\\Sleepi"
# Check if the directory exists
if not os.path.exists(path):
    # open editing window
    pass
else:
    print(f"Directory '{path}' already exists.")

# fetch settings from json file
with open(f"{path}\\settings.json", "r") as f:
    settings = json.load(f)

wall_path = settings["wall_path"]
sleep_time = settings["sleep_time"]
wake_time = settings["wake_time"]
default_wall = settings["default_wall"]

pg.FAILSAFE = False

def setWalpaper(default=False):

    SPI_SETDESKWALLPAPER = 20
    loc = ""
    if default:
        loc = default_wall
    else:
        # select any image from the folder except default.jpg
        while(default_wall in loc or loc==""):
            # Get all files in the directory
            files = os.listdir(wall_path)

            # Select a random image
            selected_image = random.choice(files)
            print(selected_image)
            loc = os.path.join(wall_path, selected_image)

    print(loc)
    wallpaper_path = loc
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 0)

def down():
    # make screen down by pressing win + d
    pg.keyDown('win')
    pg.press('d')
    pg.keyUp('win')
    time.sleep(0.5)

while True:
    # start a timer of x minutes
    timer = time.time() + wake_time * 60
    # timer = time.time() + 3
    nodo = 0
    paused = False
    cm = pg.position()
    
    while time.time() < timer:
        # checks if user is working or not
        if(pg.position()==cm):
            nodo+=2
            if paused:
                # if timer is less than x mins
                if(timer-time.time()<wake_time*60):
                    # add more 2 sec + 2 sec cooldown
                    timer += 2*2
            else:
                # if no movements for 3 minutes
                if(nodo>=180):
                    paused = True
                    # add more 3 mins + 3 min cooldown if timer is less than x mins
                    if(timer-time.time()<wake_time*60):
                        timer += 2*3*60
                    nodo = 0
        else:
            paused = False
            nodo = 0
            cm = pg.position()
        time.sleep(2)

    setWalpaper()
    down()

    mouse = pg.position()
    prev = pg.screenshot()
    
    print("Sleeping for 5 minutes")

    # Sleeping for y minutes
    sleeper = time.time() + sleep_time * 60
    while time.time() < sleeper:
        # checks if current screen is same as previous by comparing 2 images
        if(mouse != pg.position()):
            pg.moveTo(mouse.x, mouse.y)
            time.sleep(0.5)
        if(prev != pg.screenshot()):
            down()
        time.sleep(1)
    
    setWalpaper(True)
    down()
