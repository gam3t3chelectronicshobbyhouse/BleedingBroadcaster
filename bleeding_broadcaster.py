# bleeding_broadcaster.py
# GUI for Bleeding Broadcaster by Gam3t3ch Electronics

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Globals
playlist = []
current_index = 0
loop_playlist = tk.BooleanVar()

# GUI Setup
root = tk.Tk()
root.title("Bleeding Broadcaster - by Gam3t3ch Electronics")
root.geometry("800x600")
root.iconphoto(False, tk.PhotoImage(file="BleedingBroadcaster.png"))

# Tone Generator Frame
tone_frame = ttk.LabelFrame(root, text="Test Tone Generator")
tone_frame.pack(fill="x", padx=10, pady=10)

waveform_var = tk.StringVar(value="sine")
freq_var = tk.StringVar(value="1000")
duration_var = tk.StringVar(value="5")

waveform_menu = ttk.Combobox(tone_frame, textvariable=waveform_var, values=["sine", "square", "triangle", "noise"])
wavelength_label = ttk.Label(tone_frame, text="Frequency (Hz):")
waveform_menu.grid(row=0, column=0, padx=5, pady=5)
wavelength_label.grid(row=0, column=1)
tk.Entry(tone_frame, textvariable=freq_var, width=10).grid(row=0, column=2)
tk.Label(tone_frame, text="Duration (s):").grid(row=0, column=3)
tk.Entry(tone_frame, textvariable=duration_var, width=5).grid(row=0, column=4)

# Sweep Tone Controls
sweep_frame = ttk.LabelFrame(root, text="Auto Sweep Generator")
sweep_frame.pack(fill="x", padx=10, pady=10)

sweep_start_var = tk.StringVar(value="100")
sweep_end_var = tk.StringVar(value="10000")
sweep_duration_var = tk.StringVar(value="10")

sweep_controls = [
    ("Start Freq", sweep_start_var),
    ("End Freq", sweep_end_var),
    ("Duration", sweep_duration_var)
]

for idx, (label, var) in enumerate(sweep_controls):
    ttk.Label(sweep_frame, text=label).grid(row=0, column=idx*2)
    tk.Entry(sweep_frame, textvariable=var, width=8).grid(row=0, column=idx*2+1)

# Playlist Frame
playlist_frame = ttk.LabelFrame(root, text="Broadcast Playlist")
playlist_frame.pack(fill="both", expand=True, padx=10, pady=10)

playlist_box = tk.Listbox(playlist_frame)
playlist_box.pack(fill="both", expand=True, padx=5, pady=5)

# Command Functions
def generate_tone():
    filename = "tone.wav"
    subprocess.call(['sox', '-n', '-r', '44100', '-c', '1', filename, 'synth', duration_var.get(), waveform_var.get(), freq_var.get()])
    messagebox.showinfo("Done", f"Tone generated: {filename}")

def generate_sweep():
    filename = "sweep.wav"
    freq_range = f"{sweep_start_var.get()}-{sweep_end_var.get()}"
    subprocess.call(['sox', '-n', '-r', '44100', '-c', '1', filename, 'synth', sweep_duration_var.get(), 'sine', freq_range])
    messagebox.showinfo("Done", f"Sweep generated: {filename}")

def preview_file(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def add_file():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file:
        playlist.append(file)
        playlist_box.insert(tk.END, os.path.basename(file))

def add_folder():
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.endswith('.wav') or file.endswith('.mp3'):
                full_path = os.path.join(folder, file)
                playlist.append(full_path)
                playlist_box.insert(tk.END, file)

def play_selected():
    global current_index
    try:
        current_index = playlist_box.curselection()[0]
        preview_file(playlist[current_index])
    except:
        messagebox.showwarning("Select File", "Select a file from the playlist")

def next_track():
    global current_index
    if current_index + 1 < len(playlist):
        current_index += 1
        preview_file(playlist[current_index])

def toggle_loop():
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    if loop_playlist.get():
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

def stop_playback():
    pygame.mixer.music.stop()

# Buttons
tk.Button(tone_frame, text="Generate Tone", command=generate_tone).grid(row=0, column=5, padx=5)
tk.Button(tone_frame, text="Preview", command=lambda: preview_file("tone.wav")).grid(row=0, column=6)
tk.Button(sweep_frame, text="Generate Sweep", command=generate_sweep).grid(row=0, column=6, padx=5)
tk.Button(sweep_frame, text="Preview Sweep", command=lambda: preview_file("sweep.wav")).grid(row=0, column=7)
tk.Button(root, text="Add File", command=add_file).pack(side="left", padx=5)
tk.Button(root, text="Add Folder", command=add_folder).pack(side="left", padx=5)
tk.Button(root, text="Play Selected", command=play_selected).pack(side="left", padx=5)
tk.Button(root, text="Next Track", command=next_track).pack(side="left", padx=5)
tk.Checkbutton(root, text="Loop Playlist", variable=loop_playlist, command=toggle_loop).pack(side="left", padx=5)
tk.Button(root, text="Stop", command=stop_playback).pack(side="left", padx=5)

root.mainloop()
