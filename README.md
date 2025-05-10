Bleeding Broadcaster is an AM/FM signal broadcaster for the Raspberry Pi, designed specifically for audio diagnostics. Use it to test how signals bleed into active speakers and other audio systems. The software includes signal generation tools, a playlist system, and integration with tools like TinySA and oscilloscopes.

🌟 Features

📡 AM/FM Broadcasting (via GPIO on Raspberry Pi)

🔊 Test Tone Generator (powered by SoX)

🔁 Auto-Sweep Modes for frequency testing

🎶 Audio Playlist Broadcasting (WAV/MP3)

🔁 Playlist looping support

💾 Load individual files or entire folders

🔎 Built-in update checker + one-click updates

📥 One-line installer script

🧹 One-line uninstaller

🖥️ Desktop shortcut with custom icon

🛠️ Works great on Raspberry Pi 3, 4, and 5

🧰 Requirements

Raspberry Pi 3 or newer (Pi 4 or 5 recommended)

Raspbian OS (32 or 64-bit)

Internet connection for installation/update

Basic GPIO hookup (for broadcasting antenna)

📦 Installation

```bash
curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash
```

❌ Uninstallation

```bash
curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/uninstall_bleeding_broadcaster.sh | bash
```

📈 Connection Guide

GPIO 4 (Pin 7): This acts as your antenna line.

Connect a 75–100cm long wire to GPIO4 to act as your antenna.

Optional: Add a 75-ohm resistor in series with the wire.

⚠️ This software is for diagnostic and testing purposes only and should only be used within legal radio frequency ranges and power levels in your country.

📂 Folder Structure

bleeding_broadcaster_gui.py – The main application GUI

update_bleeding_broadcaster.sh – GitHub update script

install_bleeding_broadcaster.sh – One-line installer

uninstall_bleeding_broadcaster.sh – One-line uninstaller

BleedingBroadcaster.png – App icon

🛠️ Upcoming Features

Custom PCB with scope and TinySA breakout BNCs

Logging & analysis of signal bleed-through

Signal strength tuning & hardware calibration UI

💡 Need Help?

Visit our GitHub issues page or reach out through our project portal at:
https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster

👨‍🔧 Created by

Gam3t3ch Electronics Hobby House

