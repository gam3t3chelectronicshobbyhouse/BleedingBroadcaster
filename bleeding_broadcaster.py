import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import pygame
import subprocess
import RPi.GPIO as GPIO
from tkinter import PhotoImage
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
        self.root.geometry("800x600")
        if os.path.exists(ICON_FILE):
            self.root.iconphoto(False, tk.PhotoImage(file=ICON_FILE))

        self.audio_files = []
        self.current_index = 0
        self.loop = tk.BooleanVar()
        self.now_playing = tk.StringVar(value="Nothing Playing")

        self.selected_mode = tk.StringVar(value="FM")
        self.unit_display = "Hz"
        self.selected_frequency_fm = 100000
        self.selected_frequency_am = 1000
        self.transmitter = None

        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(PLAYLIST_DIR, exist_ok=True)

        self.setup_transmitter()
        self.setup_ui()

    def setup_transmitter(self):
        if self.selected_mode.get() == "FM":
            self.transmitter = FMTransmitter(4, self.selected_frequency_fm)
        else:
            self.transmitter = AMTransmitter(4, self.selected_frequency_am)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

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

        mode_frame = tk.LabelFrame(self.root, text="Broadcast Mode", padx=10, pady=10)
        mode_frame.pack(padx=10, pady=5, fill="x")

        ttk.Radiobutton(mode_frame, text="FM", variable=self.selected_mode, value="FM", command=self.update_mode).pack(side="left")
        ttk.Radiobutton(mode_frame, text="AM", variable=self.selected_mode, value="AM", command=self.update_mode).pack(side="left")

        freq_frame = tk.LabelFrame(self.root, text="Frequency Control", padx=10, pady=10)
        freq_frame.pack(padx=10, pady=5, fill="x")

        self.fm_slider = tk.Scale(freq_frame, from_=88000, to=108000, orient="horizontal", label="FM Frequency (Hz)", command=self.update_frequency)
        self.fm_slider.set(self.selected_frequency_fm)
        self.fm_slider.pack(fill="x")

        self.am_slider = tk.Scale(freq_frame, from_=530, to=1700, orient="horizontal", label="AM Frequency (kHz)", command=self.update_frequency)
        self.am_slider.set(self.selected_frequency_am)
        self.am_slider.pack(fill="x")

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

        ttk.Button(bottom_frame, text="YouTube", command=lambda: self.open_link("https://www.youtube.com/gam3t3chelectronics")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Instagram", command=lambda: self.open_link("https://www.instagram.com/gam3t3chhobbyhouse/")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Donate ❤️", command=lambda: self.open_link("https://paypal.me/gam3t3ch")).pack(side="right", padx=10)
        ttk.Button(bottom_frame, text="Update", command=self.run_update_popup).pack(side="right", padx=10)

        self.update_mode()

    def update_mode(self):
        self.setup_transmitter()
        if self.selected_mode.get() == "FM":
            self.fm_slider.config(state="normal")
            self.am_slider.config(state="disabled")
            self.update_frequency(self.fm_slider.get())
        else:
            self.am_slider.config(state="normal")
            self.fm_slider.config(state="disabled")
            self.update_frequency(self.am_slider.get())

    def toggle_unit(self):
        self.unit_display = "AM/FM Bands" if self.unit_display == "Hz" else "Hz"
        self.update_frequency(self.fm_slider.get() if self.selected_mode.get() == "FM" else self.am_slider.get())

    def update_frequency(self, val):
        if self.selected_mode.get() == "FM":
            self.selected_frequency_fm = int(val)
            display_freq = f"{self.selected_frequency_fm} Hz" if self.unit_display == "Hz" else f"{self.selected_frequency_fm / 1000:.1f} MHz"
        else:
            self.selected_frequency_am = int(val)
            display_freq = f"{self.selected_frequency_am * 1000} Hz" if self.unit_display == "Hz" else f"{self.selected_frequency_am} kHz"

        self.now_playing.set(f"Broadcasting at: {display_freq}")

        if hasattr(self.transmitter, "set_frequency"):
            freq = self.selected_frequency_fm if self.selected_mode.get() == "FM" else self.selected_frequency_am * 1000
            self.transmitter.set_frequency(freq)

    def play_tone(self):
        freq = self.selected_frequency_fm if self.selected_mode.get() == "FM" else self.selected_frequency_am * 1000
        self.now_playing.set(f"Now Playing: Test Tone ({freq} Hz)")
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
        update_win.title("Updating Bleeding Broadcaster")
        update_win.geometry("600x400")

        ttk.Label(update_win, text="Checking for Updates...", font=("Arial", 14, "bold")).pack(pady=10)

        log_text = tk.Text(update_win, wrap="word", height=15, font=("Courier", 10))
        log_text.pack(fill="both", expand=True, padx=10, pady=5)

        close_button = ttk.Button(update_win, text="Close", command=update_win.destroy, state="disabled")
        close_button.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    gui = BroadcasterGUI(root)
    root.mainloop()
