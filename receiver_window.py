from tkinter import *
from tkinter import ttk

class ReceiverWindow:
    def __init__(self, master):
        self.master = Toplevel(master)
        self.master.title("Receiver Window - SDR Control Panel")
        self.master.geometry("1000x700")

        # Main Paned Layout
        main_frame = Frame(self.master)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Spectrum / Waterfall Toggle and Display Placeholder
        display_controls = Frame(main_frame)
        display_controls.pack(fill=X, pady=(0, 10))

        self.display_mode = StringVar(value="Waterfall")
        ttk.Label(display_controls, text="Display Mode:").pack(side=LEFT)
        ttk.Combobox(display_controls, textvariable=self.display_mode, values=["Waterfall", "Spectrum"]).pack(side=LEFT, padx=5)
        ttk.Button(display_controls, text="Toggle", command=self.toggle_display_mode).pack(side=LEFT, padx=5)

        display_canvas = Canvas(main_frame, height=200, bg="black")
        display_canvas.pack(fill=X, pady=5)

        # Frequency and Demodulation Controls
        control_frame = LabelFrame(main_frame, text="Tuning and Demodulation")
        control_frame.pack(fill=X, pady=10)

        Label(control_frame, text="Frequency (Hz):").grid(row=0, column=0, sticky=W)
        self.freq_entry = Entry(control_frame, width=12)
        self.freq_entry.insert(0, "100000000")
        self.freq_entry.grid(row=0, column=1, padx=5)

        Label(control_frame, text="Demodulation:").grid(row=0, column=2, sticky=W)
        self.demod_mode = StringVar(value="FM")
        ttk.Combobox(control_frame, textvariable=self.demod_mode, values=["FM", "AM", "USB", "LSB", "CW"]).grid(row=0, column=3, padx=5)

        ttk.Button(control_frame, text="Tune", command=self.tune_frequency).grid(row=0, column=4, padx=10)

        # Gain and Squelch
        gain_squelch_frame = Frame(main_frame)
        gain_squelch_frame.pack(fill=X, pady=10)

        Label(gain_squelch_frame, text="Audio Gain:").pack(side=LEFT, padx=5)
        self.gain_slider = Scale(gain_squelch_frame, from_=0, to=100, orient=HORIZONTAL)
        self.gain_slider.set(50)
        self.gain_slider.pack(side=LEFT, padx=5)

        Label(gain_squelch_frame, text="Squelch:").pack(side=LEFT, padx=5)
        self.squelch_slider = Scale(gain_squelch_frame, from_=0, to=100, orient=HORIZONTAL)
        self.squelch_slider.set(10)
        self.squelch_slider.pack(side=LEFT, padx=5)

        # Bookmarks and Scanning
        bookmark_frame = LabelFrame(main_frame, text="Bookmarks and Scanning")
        bookmark_frame.pack(fill=X, pady=10)

        self.bookmark_listbox = Listbox(bookmark_frame, height=4)
        self.bookmark_listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        control_panel = Frame(bookmark_frame)
        control_panel.pack(side=LEFT, padx=5)

        ttk.Button(control_panel, text="Add Bookmark", command=self.add_bookmark).pack(fill=X, pady=2)
        ttk.Button(control_panel, text="Remove Selected", command=self.remove_bookmark).pack(fill=X, pady=2)

        ttk.Label(control_panel, text="Scan Range (Hz):").pack(pady=(10, 0))
        scan_frame = Frame(control_panel)
        scan_frame.pack()

        self.scan_start = Entry(scan_frame, width=10)
        self.scan_start.insert(0, "88000000")
        self.scan_start.pack(side=LEFT, padx=2)
        self.scan_stop = Entry(scan_frame, width=10)
        self.scan_stop.insert(0, "108000000")
        self.scan_stop.pack(side=LEFT, padx=2)
        ttk.Button(control_panel, text="Start Scan", command=self.start_scan).pack(fill=X, pady=5)

        # Recording Controls
        record_frame = LabelFrame(main_frame, text="Recording")
        record_frame.pack(fill=X, pady=10)

        self.is_recording = BooleanVar(value=False)
        ttk.Button(record_frame, text="Start Recording", command=self.toggle_recording).pack(side=LEFT, padx=10)

        self.status_label = Label(record_frame, text="Not Recording")
        self.status_label.pack(side=LEFT)

        # Signal Strength Meter
        signal_frame = Frame(main_frame)
        signal_frame.pack(fill=X, pady=10)

        Label(signal_frame, text="Signal Strength:").pack(side=LEFT)
        self.signal_progress = ttk.Progressbar(signal_frame, orient=HORIZONTAL, length=300, mode='determinate')
        self.signal_progress.pack(side=LEFT, padx=5)
        self.signal_progress['value'] = 25

    def toggle_display_mode(self):
        current = self.display_mode.get()
        if current == "Waterfall":
            self.display_mode.set("Spectrum")
        else:
            self.display_mode.set("Waterfall")

    def tune_frequency(self):
        freq = self.freq_entry.get()
        mode = self.demod_mode.get()
        print(f"Tuning to {freq} Hz using {mode} demodulation")

    def add_bookmark(self):
        freq = self.freq_entry.get()
        self.bookmark_listbox.insert(END, freq)

    def remove_bookmark(self):
        selected = self.bookmark_listbox.curselection()
        for idx in reversed(selected):
            self.bookmark_listbox.delete(idx)

    def start_scan(self):
        start = self.scan_start.get()
        stop = self.scan_stop.get()
        print(f"Scanning from {start} Hz to {stop} Hz")

    def toggle_recording(self):
        self.is_recording.set(not self.is_recording.get())
        status = "Recording..." if self.is_recording.get() else "Not Recording"
        self.status_label.config(text=status)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    ReceiverWindow(root)
    root.mainloop()
