import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pygame
import subprocess
import RPi.GPIO as GPIO
from tkinter import PhotoImage

APP_NAME = "Bleeding Broadcaster"
ICON_FILE = "BleedingBroadcaster.png"
AUDIO_DIR = "audio"
PLAYLIST_DIR = "playlists"

# Initialize pygame mixer
pygame.mixer.init()

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # Set GPIO pin 4 as an output

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

        # Default frequency set to 1000 Hz
        self.selected_frequency = 1000

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Title and Graphic Display
        title_label = tk.Label(top_frame, text="Bleeding Broadcaster by Gam3t3ch Electronics", font=("Arial", 16, "bold"))
        title_label.pack()

        self.image = PhotoImage(file=ICON_FILE)
        image_label = tk.Label(top_frame, image=self.image)
        image_label.pack(pady=5)

        self.now_playing_label = tk.Label(top_frame, textvariable=self.now_playing, font=("Arial", 14))
        self.now_playing_label.pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Tone Generator and Sweep buttons
        ttk.Button(control_frame, text="Play Tone", command=self.play_tone).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Sweep Tone", command=self.sweep_tone).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Play", command=self.play_audio).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_audio).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_audio_and_tone).grid(row=0, column=4, padx=5)
        ttk.Checkbutton(control_frame, text="Loop Playlist", variable=self.loop).grid(row=0, column=5, padx=5)

        # Frequency Control for GPIO Pin 4
        freq_frame = tk.LabelFrame(self.root, text="Broadcast Frequency (GPIO Pin 4)", padx=10, pady=10)
        freq_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.freq_slider = tk.Scale(freq_frame, from_=20, to=80000, orient="horizontal", label="Frequency (Hz)", command=self.update_frequency)
        self.freq_slider.set(self.selected_frequency)  # Set default value to 1000 Hz
        self.freq_slider.pack(fill="both", expand=True)

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

    def update_frequency(self, val):
        self.selected_frequency = int(val)  # Update the selected frequency
        self.now_playing.set(f"Broadcasting at: {self.selected_frequency} Hz")

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

    def play_tone(self):
        # Tone generation logic placeholder (use SoX or another library here)
        self.now_playing.set(f"Now Playing: Test Tone ({self.selected_frequency} Hz)")
        # Example command to start test tone (replace with actual implementation)
        # subprocess.call(["sox", "-n", "-r", "44100", "-c", "2", "test_tone.wav", "sine", str(self.selected_frequency)])

    def sweep_tone(self):
        # Sweep tone generation logic placeholder
        self.now_playing.set("Now Playing: Sweep Tone")
        # Example command to start sweep tone (replace with actual implementation)
        # subprocess.call(["sox", "-n", "-r", "44100", "-c", "2", "sweep_tone.wav", "synth", "1", "sine", "1-1000"])

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = BroadcasterGUI(root)
    root.mainloop()
