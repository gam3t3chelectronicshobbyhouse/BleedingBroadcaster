import os
import tkinter as tk
from tkinter import filedialog, messagebox

class RadioBroadcaster:
    def __init__(self, master):
        self.master = master
        master.title("Bleeding Broadcaster")

        # Title Banner
        self.title_label = tk.Label(master, text="Bleeding Broadcaster", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(5, 10))

        # Modulation Type
        self.mod_label = tk.Label(master, text="Modulation:")
        self.mod_label.grid(row=1, column=0, sticky="e")

        self.modulation = tk.StringVar(value="am")
        tk.Radiobutton(master, text="AM", variable=self.modulation, value="am").grid(row=1, column=1)
        tk.Radiobutton(master, text="FM", variable=self.modulation, value="fm").grid(row=1, column=2)

        # Frequency Input
        self.freq_label = tk.Label(master, text="Frequency (kHz for AM, MHz for FM):")
        self.freq_label.grid(row=2, column=0, sticky="e")

        self.freq_entry = tk.Entry(master)
        self.freq_entry.grid(row=2, column=1, columnspan=2, sticky="we")

        # Audio File Selection
        self.audio_label = tk.Label(master, text="Audio File:")
        self.audio_label.grid(row=3, column=0, sticky="e")

        self.audio_path = tk.StringVar()
        self.audio_entry = tk.Entry(master, textvariable=self.audio_path, width=40)
        self.audio_entry.grid(row=3, column=1)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=3, column=2)

        # Tone Generator Section
        self.tone_label = tk.Label(master, text="Test Tone Generator (SoX):", font=("Helvetica", 10, "bold"))
        self.tone_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        self.tone_buttons = [
            ("440Hz Sine", lambda: self.generate_tone("sine", 440)),
            ("Sweep 20Hz-20kHz", lambda: self.generate_tone("sweep")),
            ("Pink Noise", lambda: self.generate_tone("pinknoise")),
            ("White Noise", lambda: self.generate_tone("whitenoise")),
        ]
        for idx, (label, command) in enumerate(self.tone_buttons):
            tk.Button(master, text=label, command=command).grid(row=5, column=idx % 3, pady=2)

        # Control Buttons
        self.start_button = tk.Button(master, text="Start Transmission", command=self.start_transmission, bg="green", fg="white")
        self.start_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_transmission, bg="red", fg="white")
        self.stop_button.grid(row=6, column=2, pady=10)

        # Output Status
        self.status = tk.Text(master, height=10, width=60)
        self.status.grid(row=7, column=0, columnspan=3)
        self.log("Ready.")

        # Footer
        self.footer = tk.Label(master, text="by Gam3t3ch Electronics", font=("Helvetica", 8))
        self.footer.grid(row=8, column=0, columnspan=3, pady=(5, 5))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.audio_path.set(file_path)

    def log(self, message):
        self.status.insert(tk.END, f"{message}\n")
        self.status.see(tk.END)

    def start_transmission(self):
        mod = self.modulation.get()
        freq = self.freq_entry.get()
        file = self.audio_path.get()

        if not freq or not file:
            messagebox.showerror("Missing Data", "Please enter a frequency and select or generate a WAV file.")
            return

        cmd = ""
        if mod == "fm":
            cmd = f"sudo ./rpitx/bin/piFM -f {freq} '{file}'"
        else:
            cmd = f"sudo ./rpitx/bin/piAM -f {freq} '{file}'"

        self.log(f"Starting {mod.upper()} transmission at {freq} with file: {file}")
        self.log("Press STOP to end transmission.")
        os.system(f"pkill piFM; pkill piAM; {cmd} &")

    def stop_transmission(self):
        os.system("pkill piFM; pkill piAM")
        self.log("Transmission stopped.")

    def generate_tone(self, tone_type, freq=440):
        filename = f"/tmp/{tone_type}.wav"
        if tone_type == "sine":
            cmd = f"sox -n -r 44100 -c 1 {filename} synth 5 sine {freq}"
        elif tone_type == "sweep":
            cmd = f"sox -n -r 44100 -c 1 {filename} synth 10 sine 20-20000"
        elif tone_type == "pinknoise":
            cmd = f"sox -n -r 44100 -c 1 {filename} synth 5 pinknoise"
        elif tone_type == "whitenoise":
            cmd = f"sox -n -r 44100 -c 1 {filename} synth 5 whitenoise"
        else:
            return

        os.system(cmd)
        self.audio_path.set(filename)
        self.log(f"Generated {tone_type} to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RadioBroadcaster(root)
    root.mainloop()
