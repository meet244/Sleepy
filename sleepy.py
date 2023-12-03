"""
 ____  _                       
/ ___|| | ___  ___ _ __  _   _ 
\___ \| |/ _ \/ _ \ '_ \| | | |
 ___) | |  __/  __/ |_) | |_| |
|____/|_|\___|\___| .__/ \__, |
                  |_|    |___/ 

By: MEET PATEL(@meet244 - Github)
"""

import time
import pyautogui as pg
import os
import random
import ctypes
import json
import customtkinter as ctk
import sys

# Setup
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


settings = resource_path("data\\settings.json")

# Check if the directory exists
if not os.path.exists(settings):
    # open editing window
    print(f"Settings file {settings} not found. Please run again.")

    def save_settings():
        wall_path = entry_wall_path.get()
        sleep_time = entry_sleep_time.get()
        wake_time = entry_wake_time.get()
        default_wall = entry_default_wall.get()

        # check if all filled
        if not wall_path or not sleep_time or not wake_time or not default_wall:
            status_label.configure(text="Please fill all the fields!")
            return
        
        settings_data = {
            "wall_path": wall_path,
            "sleep_time": sleep_time,
            "wake_time": wake_time,
            "default_wall": default_wall
        }

        os.makedirs(os.path.dirname(settings), exist_ok=True)  # Create the directory if it doesn't exist

        with open(settings, "w") as f:
            json.dump(settings_data, f)
            status_label.configure(text="Settings updated successfully!")
        root.destroy()

    def browse_folder():
        folder_path = ctk.filedialog.askdirectory()
        if folder_path:
            entry_wall_path.delete(0, ctk.END)
            entry_wall_path.insert(0, folder_path)

    def browse_default_wall():
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.avif")])
        if file_path:
            entry_default_wall.delete(0, ctk.END)
            entry_default_wall.insert(0, file_path)

    root = ctk.CTk()
    root.title("Sleepy Settings - OneTime Setup")
    root.geometry("450x230")
    root.resizable(False, False)
    root.iconbitmap(resource_path("assets\\icon.ico"))

    # Labels
    label_wall_path = ctk.CTkLabel(root, text="Wallpaper Folder Path:")
    label_sleep_time = ctk.CTkLabel(root, text="Sleep Time (minutes):")
    label_wake_time = ctk.CTkLabel(root, text="Wake Time (minutes):")
    label_default_wall = ctk.CTkLabel(root, text="Default Wallpaper Path:")

    label_wall_path.grid(row=0, column=0, padx=10, pady=5, sticky=ctk.W)
    label_sleep_time.grid(row=1, column=0, padx=10, pady=5, sticky=ctk.W)
    label_wake_time.grid(row=2, column=0, padx=10, pady=5, sticky=ctk.W)
    label_default_wall.grid(row=3, column=0, padx=10, pady=5, sticky=ctk.W)

    # Entry fields
    entry_wall_path = ctk.CTkEntry(root, width=200)
    entry_sleep_time = ctk.CTkEntry(root, width=200)
    entry_wake_time = ctk.CTkEntry(root, width=200)
    entry_default_wall = ctk.CTkEntry(root, width=200)

    entry_sleep_time.insert(0, "5")
    entry_wake_time.insert(0, "25")

    entry_wall_path.grid(row=0, column=1, padx=10, pady=5)
    entry_sleep_time.grid(row=1, column=1, padx=10, pady=5)
    entry_wake_time.grid(row=2, column=1, padx=10, pady=5)
    entry_default_wall.grid(row=3, column=1, padx=10, pady=5)

    # Browse buttons
    browse_button = ctk.CTkButton(root, text="Browse", command=browse_folder, width=50)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    browse_default_wall_button = ctk.CTkButton(root, text="Browse", command=browse_default_wall, width=50)
    browse_default_wall_button.grid(row=3, column=2, padx=5, pady=5)

    # Save button
    save_button = ctk.CTkButton(root, text="Save Settings", command=save_settings)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Status label
    status_label = ctk.CTkLabel(root, text="")
    status_label.grid(row=5, column=0, columnspan=2)

    # Load existing settings if available
    if os.path.exists(settings):
        with open(settings, "r") as f:
            settings_data = json.load(f)
            entry_wall_path.insert(0, settings_data.get("wall_path", ""))
            entry_sleep_time.insert(0, settings_data.get("sleep_time", "5"))
            entry_wake_time.insert(0, settings_data.get("wake_time", "25"))
            entry_default_wall.insert(0, settings_data.get("default_wall", ""))

    root.mainloop()
else:print(f"Directory '{settings}' already exists.")

# fetch settings from json file
try:
    with open(settings, "r") as f:
        settings_data = json.load(f)
except:
    print("Error reading settings file. Please run again.")

try:
    wall_path = settings_data["wall_path"]
    sleep_time = int(settings_data["sleep_time"])
    wake_time = int(settings_data["wake_time"])
    default_wall = settings_data["default_wall"]

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

    setWalpaper(True)

    while True:
        # start a timer of x minutes
        timer = time.time() + wake_time * 60
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
except Exception as e:
    print(e)