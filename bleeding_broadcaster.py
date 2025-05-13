import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import threading
import subprocess
import RPi.GPIO as GPIO
from wideband_transmitter import WidebandTransmitter
from receiver_window import open_receiver_window

APP_NAME = "Bleeding Broadcaster"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_FILE = os.path.join(SCRIPT_DIR, "icon.png")
BANNER_FILE = os.path.join(SCRIPT_DIR, "BleedingBroadcaster.png")
AUDIO_DIR = os.path.join(SCRIPT_DIR, "audio")
PLAYLIST_DIR = os.path.join(SCRIPT_DIR, "playlists")

pygame.mixer.init()
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

class BroadcasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.state("zoomed")  # Maximized on launch
        if os.path.exists(ICON_FILE):
            self.root.iconphoto(False, tk.PhotoImage(file=ICON_FILE))

        self.audio_files = []
        self.current_index = 0
        self.loop = tk.BooleanVar()
        self.now_playing = tk.StringVar(value="Nothing Playing")
        self.frequency = tk.IntVar(value=100000)
        self.transmitter = WidebandTransmitter(4, self.frequency.get())

        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(PLAYLIST_DIR, exist_ok=True)

        self.setup_ui()
        self.update_frequency_display(None)

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Bleeding Broadcaster by Gam3t3ch Electronics", font=("Arial", 16, "bold")).pack()

        if os.path.exists(BANNER_FILE):
            self.banner_image = tk.PhotoImage(file=BANNER_FILE).subsample(3)
            tk.Label(top_frame, image=self.banner_image).pack(pady=5)

        tk.Label(top_frame, textvariable=self.now_playing, font=("Arial", 14)).pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Play Tone", command=self.play_tone).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Sweep Tone", command=self.sweep_tone).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Play", command=self.play_audio).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_audio).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_audio_and_tone).grid(row=0, column=4, padx=5)

        loop_frame = tk.Frame(self.root)
        loop_frame.pack(pady=5)
        ttk.Checkbutton(loop_frame, text="Loop Playlist", variable=self.loop).pack()

        # Frequency input and slider
        freq_frame = tk.LabelFrame(self.root, text="Frequency Selector")
        freq_frame.pack(padx=10, pady=10, fill="x")

        input_frame = tk.Frame(freq_frame)
        input_frame.pack(fill="x", pady=5)

        tk.Label(input_frame, text="Frequency (Hz):").pack(side="left")
        self.freq_entry = ttk.Entry(input_frame, width=10)
        self.freq_entry.pack(side="left", padx=5)
        self.freq_entry.bind("<Return>", self.set_frequency_from_entry)

        self.slider = tk.Scale(freq_frame, from_=0, to=108000, orient="horizontal",
                               showvalue=False, variable=self.frequency,
                               command=self.update_frequency_display, length=800)
        self.slider.pack(padx=10, fill="x")

        self.slider.bind("<Configure>", lambda e: self.draw_frequency_bands(freq_frame))

        playlist_frame = tk.LabelFrame(self.root, text="Playlist")
        playlist_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.playlist_box = tk.Listbox(playlist_frame, height=8)
        self.playlist_box.pack(fill="both", expand=True)

        playlist_controls = tk.Frame(self.root)
        playlist_controls.pack()

        ttk.Button(playlist_controls, text="Add Files", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(playlist_controls, text="Save Playlist", command=self.save_playlist).pack(side="left", padx=5)
        ttk.Button(playlist_controls, text="Load Playlist", command=self.load_playlist).pack(side="left", padx=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(bottom_frame, text="Launch Receiver", command=open_receiver_window).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Update", command=self.run_update_popup).pack(side="right", padx=10)
        ttk.Button(bottom_frame, text="Donate ❤️", command=lambda: self.open_link("https://paypal.me/gam3t3ch")).pack(side="right", padx=10)
        ttk.Button(bottom_frame, text="Instagram", command=lambda: self.open_link("https://www.instagram.com/gam3t3chhobbyhouse/")).pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="YouTube", command=lambda: self.open_link("https://www.youtube.com/gam3t3chelectronics")).pack(side="left", padx=10)

    def draw_frequency_bands(self, parent):
        for widget in parent.pack_slaves():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        canvas = tk.Canvas(parent, height=50, bg="white")
        canvas.pack(fill="x", padx=10)
        width = canvas.winfo_width() or 800
        bands = [
            (0, 3000, "CB Band", "lightblue"),
            (530, 1700, "AM Band", "orange"),
            (88000, 108000, "FM Band", "lightgreen"),
        ]
        for low, high, label, color in bands:
            x1 = int((low / 108000) * width)
            x2 = int((high / 108000) * width)
            canvas.create_rectangle(x1, 10, x2, 40, fill=color, outline="")
            canvas.create_text((x1 + x2) // 2, 25, text=label, font=("Arial", 10, "bold"))

    def update_frequency_display(self, _):
        freq = self.frequency.get()
        self.now_playing.set(f"Broadcasting at: {freq} Hz")
        if hasattr(self.transmitter, 'set_frequency'):
            self.transmitter.set_frequency(freq)
        self.freq_entry.delete(0, tk.END)
        self.freq_entry.insert(0, str(freq))

    def set_frequency_from_entry(self, event):
        try:
            val = int(self.freq_entry.get())
            val = max(0, min(108000, val))
            self.frequency.set(val)
            self.update_frequency_display(None)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid frequency.")

    def play_tone(self):
        self.now_playing.set(f"Now Playing: Test Tone ({self.frequency.get()} Hz)")
        if not self.transmitter.pwm_started:
            self.transmitter.start()

    def sweep_tone(self):
        self.now_playing.set("Now Playing: Sweep Tone")
        # Implement sweep logic if desired

    def stop_audio_and_tone(self):
        pygame.mixer.music.stop()
        self.now_playing.set("Nothing Playing")
        if self.transmitter.pwm_started:
            self.transmitter.stop()

    def play_audio(self):
        if not self.audio_files:
            messagebox.showwarning("No Files", "Please add audio files to the playlist.")
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
        file = filedialog.asksaveasfilename(initialdir=PLAYLIST_DIR, defaultextension=".txt", filetypes=[("Playlist", "*.txt")])
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
        update_win.geometry("450x300")
        log_text = tk.Text(update_win, wrap="word")
        log_text.pack(expand=True, fill="both", padx=10, pady=10)

        def run_update():
            try:
                update_script = os.path.join(SCRIPT_DIR, "update_bleeding_broadcaster.sh")
                process = subprocess.Popen(["bash", update_script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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

        threading.Thread(target=run_update, daemon=True).start()

    def open_link(self, url):
        subprocess.run(["xdg-open", url])

if __name__ == "__main__":
    root = tk.Tk()
    app = BroadcasterGUI(root)
    root.mainloop()
