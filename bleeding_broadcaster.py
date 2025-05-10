import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import pygame
import threading
import requests
import time

git_repo_url = "https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
install_dir = os.path.expanduser("~/BleedingBroadcaster")

class BleedingBroadcasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bleeding Broadcaster by Gam3t3ch Electronics")
        self.root.geometry("800x600")
        self.playlist = []
        self.current_index = 0
        self.loop_playlist = tk.BooleanVar(value=False)

        pygame.mixer.init()

        self.setup_ui()

    def setup_ui(self):
        self.icon = tk.PhotoImage(file=os.path.join(install_dir, "BleedingBroadcaster.png"))
        self.root.iconphoto(False, self.icon)

        tk.Label(self.root, text="Audio Playlist").pack()
        self.listbox = tk.Listbox(self.root, width=100, height=10)
        self.listbox.pack(pady=10)

        controls = tk.Frame(self.root)
        controls.pack()

        tk.Button(controls, text="Add File", command=self.add_file).pack(side=tk.LEFT)
        tk.Button(controls, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT)
        tk.Button(controls, text="Play", command=self.play_current).pack(side=tk.LEFT)
        tk.Button(controls, text="Next", command=self.play_next).pack(side=tk.LEFT)
        tk.Checkbutton(controls, text="Loop Playlist", variable=self.loop_playlist).pack(side=tk.LEFT)

        tk.Button(self.root, text="Generate Test Tone", command=self.generate_test_tone).pack(pady=10)
        tk.Button(self.root, text="Start Auto Sweep", command=self.auto_sweep).pack(pady=10)

        tk.Button(self.root, text="Check for Updates", command=self.check_for_updates).pack(pady=10)

    def add_file(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.mp3")])
        for f in files:
            self.playlist.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            for file in os.listdir(folder):
                if file.lower().endswith((".wav", ".mp3")):
                    path = os.path.join(folder, file)
                    self.playlist.append(path)
                    self.listbox.insert(tk.END, file)

    def play_current(self):
        if self.playlist:
            try:
                pygame.mixer.music.load(self.playlist[self.current_index])
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.USEREVENT)
                self.root.after(1000, self.check_music_end)
            except Exception as e:
                messagebox.showerror("Playback Error", str(e))

    def play_next(self):
        self.current_index += 1
        if self.current_index >= len(self.playlist):
            if self.loop_playlist.get():
                self.current_index = 0
            else:
                return
        self.play_current()

    def check_music_end(self):
        if not pygame.mixer.music.get_busy():
            self.play_next()
        else:
            self.root.after(1000, self.check_music_end)

    def generate_test_tone(self):
        subprocess.Popen(["play", "-n", "synth", "5", "sine", "1000"])

    def auto_sweep(self):
        subprocess.Popen(["play", "-n", "synth", "10", "sine", "300-3000"])

    def check_for_updates(self):
        def _run_update():
            current_hash = subprocess.getoutput(f"cd {install_dir} && git rev-parse HEAD")
            remote_hash = subprocess.getoutput(f"cd {install_dir} && git fetch origin && git rev-parse origin/main")

            if current_hash != remote_hash:
                answer = messagebox.askyesno("Update Available", "A new update is available.\n\nApply update now?")
                if answer:
                    subprocess.call(["bash", os.path.join(install_dir, "update_bleeding_broadcaster.sh")])
                    msg = messagebox.askyesno("Updated", "Update complete. Restart application now?")
                    if msg:
                        self.root.destroy()
                        os.execv(__file__, ["python3"] + sys.argv)
            else:
                messagebox.showinfo("No Update", "You already have the latest version.")

        threading.Thread(target=_run_update).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BleedingBroadcasterApp(root)
    root.mainloop()
