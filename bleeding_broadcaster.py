import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pygame
import subprocess

APP_NAME = "Bleeding Broadcaster"
ICON_FILE = "BleedingBroadcaster.png"
AUDIO_DIR = "audio"
PLAYLIST_DIR = "playlists"

# Initialize pygame mixer
pygame.mixer.init()

class BroadcasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x500")
        if os.path.exists(ICON_FILE):
            self.root.iconphoto(False, tk.PhotoImage(file=ICON_FILE))

        self.audio_files = []
        self.current_index = 0
        self.loop = tk.BooleanVar()
        self.now_playing = tk.StringVar(value="Nothing Playing")

        self.setup_ui()

        # Create folders if not present
        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(PLAYLIST_DIR, exist_ok=True)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.now_playing_label = tk.Label(top_frame, textvariable=self.now_playing, font=("Arial", 14))
        self.now_playing_label.pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Play", command=self.play_audio).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_audio).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_audio_and_tone).grid(row=0, column=2, padx=5)
        ttk.Checkbutton(control_frame, text="Loop Playlist", variable=self.loop).grid(row=0, column=3, padx=5)

        playlist_frame = tk.LabelFrame(self.root, text="Playlist", padx=10, pady=10)
        playlist_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.playlist_box = tk.Listbox(playlist_frame, height=10)
        self.playlist_box.pack(fill="both", expand=True)

        playlist_btn_frame = tk.Frame(self.root)
        playlist_btn_frame.pack()

        ttk.Button(playlist_btn_frame, text="Add File(s)", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(playlist_btn_frame, text="Save Playlist", command=self.save_playlist).pack(side="left", padx=5)
        ttk.Button(playlist_btn_frame, text="Load Playlist", command=self.load_playlist).pack(side="left", padx=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        # Social + Donate Buttons
        ttk.Button(bottom_frame, text="YouTube", command=lambda: self.open_link("https://www.youtube.com/gam3t3chelectronics")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Instagram", command=lambda: self.open_link("https://www.instagram.com/gam3t3chhobbyhouse/")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Donate ❤️", command=lambda: self.open_link("https://paypal.me/gam3t3ch")).pack(side="right", padx=10)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio", "*.mp3 *.wav")])
        for file in files:
            if file not in self.audio_files:
                self.audio_files.append(file)
                self.playlist_box.insert(tk.END, os.path.basename(file))

    def play_audio(self):
        if not self.audio_files:
            messagebox.showwarning("No Files", "Add audio files to the playlist.")
            return
        if self.playlist_box.curselection():
            self.current_index = self.playlist_box.curselection()[0]
        pygame.mixer.music.load(self.audio_files[self.current_index])
        pygame.mixer.music.play()
        self.now_playing.set(f"Now Playing: {os.path.basename(self.audio_files[self.current_index])}")
        self.root.after(1000, self.check_audio_end)

    def pause_audio(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_audio_and_tone(self):
        pygame.mixer.music.stop()
        self.now_playing.set("Nothing Playing")
        # Stop any subprocess test tones or sweeps here
        # Example: subprocess.call(["pkill", "sox"])

    def check_audio_end(self):
        if not pygame.mixer.music.get_busy():
            if self.loop.get():
                self.current_index = (self.current_index + 1) % len(self.audio_files)
                self.play_audio()
        else:
            self.root.after(1000, self.check_audio_end)

    def save_playlist(self):
        file = filedialog.asksaveasfilename(initialdir=PLAYLIST_DIR, defaultextension=".txt",
                                            filetypes=[("Playlist", "*.txt")])
        if file:
            with open(file, 'w') as f:
                for item in self.audio_files:
                    f.write(item + "\n")

    def load_playlist(self):
        file = filedialog.askopenfilename(initialdir=PLAYLIST_DIR, filetypes=[("Playlist", "*.txt")])
        if file:
            self.audio_files = []
            self.playlist_box.delete(0, tk.END)
            with open(file, 'r') as f:
                for line in f:
                    path = line.strip()
                    if os.path.isfile(path):
                        self.audio_files.append(path)
                        self.playlist_box.insert(tk.END, os.path.basename(path))

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = BroadcasterGUI(root)
    root.mainloop()
