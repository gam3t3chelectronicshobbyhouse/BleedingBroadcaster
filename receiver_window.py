
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReceiverWindow:
    def __init__(self, master=None):
        self.window = tk.Toplevel(master)
        self.window.title("RTL-SDR Receiver")
        self.window.geometry("800x600")

        # Frequency input
        freq_frame = ttk.Frame(self.window)
        freq_frame.pack(pady=10)
        ttk.Label(freq_frame, text="Frequency (MHz):").pack(side=tk.LEFT)
        self.freq_entry = ttk.Entry(freq_frame, width=10)
        self.freq_entry.pack(side=tk.LEFT, padx=5)
        self.freq_entry.insert(0, "100.1")  # Default frequency

        # Control buttons
        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=10)
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_receiving)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_receiving, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title("Spectrum")
        self.ax.set_xlabel("Frequency (MHz)")
        self.ax.set_ylabel("Relative power (dB)")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # SDR and threading
        self.sdr = None
        self.running = False
        self.thread = None

        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_receiving(self):
        try:
            freq_mhz = float(self.freq_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid frequency in MHz.")
            return

        self.sdr = RtlSdr()
        self.sdr.sample_rate = 2.4e6  # Hz
        self.sdr.center_freq = freq_mhz * 1e6  # Hz
        self.sdr.gain = 'auto'

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.thread.start()

    def stop_receiving(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.sdr:
            self.sdr.close()
            self.sdr = None

    def receive_loop(self):
        while self.running:
            try:
                samples = self.sdr.read_samples(256*1024)
                self.ax.cla()
                self.ax.psd(samples, NFFT=1024, Fs=self.sdr.sample_rate / 1e6, Fc=self.sdr.center_freq / 1e6)
                self.ax.set_xlabel("Frequency (MHz)")
                self.ax.set_ylabel("Relative power (dB)")
                self.ax.set_title("Spectrum")
                self.canvas.draw()
            except Exception as e:
                print(f"Error: {e}")
                self.stop_receiving()
                break

    def on_close(self):
        self.stop_receiving()
        self.window.destroy()
