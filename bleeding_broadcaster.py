import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pygame
import subprocess
import RPi.GPIO as GPIO
from tkinter import PhotoImage

# Assuming FMTransmitter and AMTransmitter are defined in fm_am_transmitter.py
from fm_am_transmitter import FMTransmitter, AMTransmitter 

APP_NAME = "Bleeding Broadcaster"
ICON_FILE = "icon.png"
BANNER_FILE = "BleedingBroadcaster.png"
AUDIO_DIR = "audio"
PLAYLIST_DIR = "playlists"

pygame.mixer.init()

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

class BroadcasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x550")
        if os.path.exists(ICON_FILE):
            self.root.iconphoto(False, tk.PhotoImage(file=ICON_FILE))

        self.audio_files = []
        self.current_index = 0
        self.loop = tk.BooleanVar()
        self.now_playing = tk.StringVar(value="Nothing Playing")

        # Default frequency in Hz for FM and AM
        self.selected_frequency = 100000  # Default FM frequency in Hz
        self.selected_mode = "FM"  # Start with FM mode
        self.unit_display = "Hz"  # Default unit display
        self.transmitter = None

        # Initializing the appropriate transmitter (FM by default)
        self.setup_transmitter()

        self.setup_ui()

        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(PLAYLIST_DIR, exist_ok=True)

    def setup_transmitter(self):
        if self.selected_mode == "FM":
            self.transmitter = FMTransmitter(4, self.selected_frequency)
        elif self.selected_mode == "AM":
            self.transmitter = AMTransmitter(4, self.selected_frequency)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Bleeding Broadcaster by Gam3t3ch Electronics", font=("Arial", 16, "bold")).pack()

        if os.path.exists(BANNER_FILE):
            self.banner_image = PhotoImage(file=BANNER_FILE).subsample(3)
            tk.Label(top_frame, image=self.banner_image).pack(pady=5)

        tk.Label(top_frame, textvariable=self.now_playing, font=("Arial", 14)).pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Play Tone", command=self.play_tone).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Sweep Tone", command=self.sweep_tone).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Play", command=self.play_audio).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_audio).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_audio_and_tone).grid(row=0, column=4, padx=5)
        ttk.Checkbutton(control_frame, text="Loop Playlist", variable=self.loop).grid(row=0, column=5, padx=5)

        # AM/FM Mode Selector
        mode_frame = tk.LabelFrame(self.root, text="Broadcast Mode", padx=10, pady=10)
        mode_frame.pack(padx=10, pady=5, fill="x")

        self.fm_rb = ttk.Radiobutton(mode_frame, text="FM", value="FM", variable=self.selected_mode,
                                      command=self.update_mode).pack(side="left")
        self.am_rb = ttk.Radiobutton(mode_frame, text="AM", value="AM", variable=self.selected_mode,
                                      command=self.update_mode).pack(side="left")

        # Frequency slider with the ability to choose units (Hz or AM/FM Bands)
        freq_frame = tk.LabelFrame(self.root, text="Broadcast Frequency", padx=10, pady=10)
        freq_frame.pack(padx=10, pady=5, fill="x")

        self.freq_slider = tk.Scale(freq_frame, from_=20, to=80000, orient="horizontal",
                                     label="Frequency (Hz)", command=self.update_frequency)
        self.freq_slider.set(self.selected_frequency)
        self.freq_slider.pack(fill="x")

        self.unit_toggle = ttk.Checkbutton(self.root, text="Display in AM/FM Bands", command=self.toggle_unit)
        self.unit_toggle.pack(pady=10)

        playlist_frame = tk.LabelFrame(self.root, text="Playlist", padx=10, pady=10)
        playlist_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.playlist_box = tk.Listbox(playlist_frame, height=8)
        self.playlist_box.pack(fill="both", expand=True)

        playlist_btn_frame = tk.Frame(self.root)
        playlist_btn_frame.pack()

        ttk.Button(playlist_btn_frame, text="Add File(s)", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(playlist_btn_frame, text="Save Playlist", command=self.save_playlist).pack(side="left", padx=5)
        ttk.Button(playlist_btn_frame, text="Load Playlist", command=self.load_playlist).pack(side="left", padx=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(bottom_frame, text="YouTube",
                   command=lambda: self.open_link("https://www.youtube.com/gam3t3chelectronics")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Instagram",
                   command=lambda: self.open_link("https://www.instagram.com/gam3t3chhobbyhouse/")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Donate ❤️",
                   command=lambda: self.open_link("https://paypal.me/gam3t3ch")).pack(side="right", padx=10)
        ttk.Button(bottom_frame, text="Update", command=self.run_update_popup).pack(side="right", padx=10)

    def update_mode(self):
        """Update mode (AM or FM) and update transmitter"""
        self.selected_frequency = 100000  # Reset to default frequency on mode change
        self.setup_transmitter()
        self.update_frequency(self.selected_frequency)

    def toggle_unit(self):
        """Toggle between Hz and AM/FM band display."""
        if self.unit_display == "Hz":
            self.unit_display = "AM/FM Bands"
        else:
            self.unit_display = "Hz"
        self.update_frequency(self.selected_frequency)

    def update_frequency(self, val):
        """Update frequency and display unit (Hz or AM/FM Bands)."""
        self.selected_frequency = int(val)
        if self.unit_display == "Hz":
            self.now_playing.set(f"Broadcasting at: {self.selected_frequency} Hz")
        else:
            # Convert frequency to AM/FM Band range (example conversion, adjust as needed)
            if self.selected_mode == "FM":
                fm_band = (self.selected_frequency - 88000) // 10  # Example conversion
                self.now_playing.set(f"FM Band: {fm_band} MHz")
            elif self.selected_mode == "AM":
                am_band = (self.selected_frequency - 530000) // 10  # Example conversion
                self.now_playing.set(f"AM Band: {am_band} kHz")
        if hasattr(self.transmitter, 'set_frequency'):
            self.transmitter.set_frequency(self.selected_frequency)

    def play_tone(self):
        self.now_playing.set(f"Now Playing: Test Tone ({self.selected_frequency} Hz)")
        if not self.transmitter.pwm_started:
            self.transmitter.start()

    def sweep_tone(self):
        self.now_playing.set("Now Playing: Sweep Tone")

    def stop_audio_and_tone(self):
        pygame.mixer.music.stop()
        self.now_playing.set("Nothing Playing")
        if self.transmitter.pwm_started:
            self.transmitter.stop()

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

    def check_audio_end(self):
        if not pygame.mixer.music.get_busy():
            if self.loop.get():
                self.current_index = (self.current_index + 1) % len(self.audio_files)
                self.play_audio()
        else:
            self.root.after(1000, self.check_audio_end)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio", "*.mp3 *.wav")])
        for file in files:
            if file not in self.audio_files:
                self.audio_files.append(file)
                self.playlist_box.insert(tk.END, os.path.basename(file))

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

    def run_update_popup(self):
        update_win = tk.Toplevel(self.root)
        update_win.title("Updating...")
        update_win.geometry("400x300")
        log_text = tk.Text(update_win, wrap="word")
        log_text.pack(expand=True, fill="both", padx=10, pady=10)

        def run_update():
            try:
                process = subprocess.Popen(["bash", "update_bleeding_broadcaster.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in process.stdout:
                    log_text.insert(tk.END, line)
                    log_text.see(tk.END)
                process.wait()
                if process.returncode == 0:
                    log_text.insert(tk.END, "\nUpdate Completed.\n")
                else:
                    log_text.insert(tk.END, f"\nUpdate Failed with code {process.returncode}.\n")
            except Exception as e:
                log_text.insert(tk.END, f"\nError: {str(e)}\n")
            ttk.Button(update_win, text="Close", command=update_win.destroy).pack(pady=5)
            tk.Label(update_win, text="Please restart the program.", font=("Arial", 10, "italic")).pack(pady=2)

        self.root.after(100, run_update)

    def open_link(self, url):
        subprocess.run(["xdg-open", url])


# Main
if __name__ == "__main__":
    root = tk.Tk()
    gui = BroadcasterGUI(root)
    root.mainloop()
