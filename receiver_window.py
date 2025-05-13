import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class ReceiverWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("RTL-SDR Receiver")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.freq_var = tk.StringVar(value="100000000")  # Default: 100 MHz
        self.mode_var = tk.StringVar(value="fm")

        self.receiver_process = None

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Frequency (Hz):").grid(row=0, column=0, sticky="e", pady=5)
        self.freq_entry = ttk.Entry(frame, textvariable=self.freq_var, width=20)
        self.freq_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Mode:").grid(row=1, column=0, sticky="e", pady=5)
        mode_menu = ttk.Combobox(frame, textvariable=self.mode_var, values=["fm", "am", "usb", "lsb"], state="readonly")
        mode_menu.grid(row=1, column=1, pady=5)

        self.start_button = ttk.Button(frame, text="Start Receiver", command=self.start_receiver)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.stop_button = ttk.Button(frame, text="Stop Receiver", command=self.stop_receiver, state="disabled")
        self.stop_button.grid(row=3, column=0, columnspan=2, pady=5)

    def start_receiver(self):
        freq = self.freq_var.get()
        mode = self.mode_var.get()

        try:
            int(freq)
        except ValueError:
            messagebox.showerror("Invalid Frequency", "Please enter a valid numeric frequency in Hz.")
            return

        if self.receiver_process:
            self.stop_receiver()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        thread = threading.Thread(target=self.run_receiver_process, args=(freq, mode), daemon=True)
        thread.start()

    def run_receiver_process(self, freq, mode):
        mode_flags = {
            "fm": ["-M", "fm", "-s", "200k", "-A", "fast", "-l", "0"],
            "am": ["-M", "am", "-s", "10k", "-l", "0"],
            "usb": ["-M", "usb", "-s", "10k", "-l", "0"],
            "lsb": ["-M", "lsb", "-s", "10k", "-l", "0"]
        }

        cmd = ["rtl_fm", "-f", freq] + mode_flags.get(mode, []) + ["-"]
        try:
            self.receiver_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            self.aplay_process = subprocess.Popen(["aplay", "-r", "22050", "-f", "S16_LE"], stdin=self.receiver_process.stdout)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start receiver:\n{e}")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def stop_receiver(self):
        if self.receiver_process:
            self.receiver_process.terminate()
            self.receiver_process = None
        if hasattr(self, 'aplay_process') and self.aplay_process:
            self.aplay_process.terminate()
            self.aplay_process = None

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def on_close(self):
        self.stop_receiver()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
