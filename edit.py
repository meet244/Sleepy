import tkinter as tk
from tkinter import filedialog
import json
import os


# Setup
path = f"C:\\Program Files\\Sleepi"
# Check if the directory exists
if not os.path.exists(path):
    # Create the directory if it doesn't exist
    os.makedirs(path)
    print(f"Directory '{path}' created.")
    # Create a json file to store settings
    with open(f"{path}\\settings.json", "w") as f:
        # wall_path = input("Enter the path of the folder containing wallpapers:")
        # sleep_time = input("Enter the time to sleep in minutes:")
        # wake_time = input("Enter the time to wake up in minutes:")
        # default_wall = input("Enter the path of the default wallpaper:")
        pass
    
def save_settings():
    wall_path = entry_wall_path.get()
    sleep_time = entry_sleep_time.get()
    wake_time = entry_wake_time.get()
    default_wall = entry_default_wall.get()

    settings = {
        "wall_path": wall_path,
        "sleep_time": sleep_time,
        "wake_time": wake_time,
        "default_wall": default_wall
    }

    with open(f"C:\\Program Files\\Sleepi\\settings.json", "w") as f:
        json.dump(settings, f)
        status_label.config(text="Settings updated successfully!")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_wall_path.delete(0, tk.END)
        entry_wall_path.insert(0, folder_path)

def browse_default_wall():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.avif")])
    if file_path:
        entry_default_wall.delete(0, tk.END)
        entry_default_wall.insert(0, file_path)

root = tk.Tk()
root.title("Sleepi Settings")
root.geometry("500x300")

# Labels
label_wall_path = tk.Label(root, text="Wallpaper Folder Path:")
label_sleep_time = tk.Label(root, text="Sleep Time (minutes):")
label_wake_time = tk.Label(root, text="Wake Time (minutes):")
label_default_wall = tk.Label(root, text="Default Wallpaper Path:")

label_wall_path.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
label_sleep_time.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
label_wake_time.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
label_default_wall.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

# Entry fields
entry_wall_path = tk.Entry(root, width=30)
entry_sleep_time = tk.Entry(root, width=30)
entry_wake_time = tk.Entry(root, width=30)
entry_default_wall = tk.Entry(root, width=30)

entry_wall_path.grid(row=0, column=1, padx=10, pady=5)
entry_sleep_time.grid(row=1, column=1, padx=10, pady=5)
entry_wake_time.grid(row=2, column=1, padx=10, pady=5)
entry_default_wall.grid(row=3, column=1, padx=10, pady=5)

# Browse buttons
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

browse_default_wall_button = tk.Button(root, text="Browse", command=browse_default_wall)
browse_default_wall_button.grid(row=3, column=2, padx=5, pady=5)

# Save button
save_button = tk.Button(root, text="Save Settings", command=save_settings)
save_button.grid(row=4, column=0, columnspan=2, pady=10)

# Status label
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=5, column=0, columnspan=2)

# Load existing settings if available
settings_path = "C:\\Program Files\\Sleepi\\settings.json"
if os.path.exists(settings_path):
    with open(settings_path, "r") as f:
        settings = json.load(f)
        entry_wall_path.insert(0, settings.get("wall_path", ""))
        entry_sleep_time.insert(0, settings.get("sleep_time", "5"))
        entry_wake_time.insert(0, settings.get("wake_time", "25"))
        entry_default_wall.insert(0, settings.get("default_wall", ""))

root.mainloop()
