#!/bin/bash

# Bleeding Broadcaster Installer for Raspberry Pi
# Targeted for Raspberry Pi 3, 4, and 5

APP_NAME="Bleeding Broadcaster"
ICON_NAME="BleedingBroadcaster.png"
SCRIPT_NAME="bleeding_broadcaster.py"
DESKTOP_ENTRY="BleedingBroadcaster.desktop"
INSTALL_DIR="$HOME/BleedingBroadcaster"

# Create install directory
mkdir -p "$INSTALL_DIR"

# Copy the Python script and icon
cp "$SCRIPT_NAME" "$INSTALL_DIR/"
cp "$ICON_NAME" "$INSTALL_DIR/"

# Update package list and install dependencies
sudo apt update
sudo apt install -y sox libsox-fmt-all python3 python3-pip python3-tk
pip3 install pygame

# Create desktop entry
cat <<EOF > "$HOME/Desktop/$DESKTOP_ENTRY"
[Desktop Entry]
Name=$APP_NAME
Comment=Broadcast AM/FM audio and test tones for speaker diagnostics
Exec=python3 $INSTALL_DIR/$SCRIPT_NAME
Icon=$INSTALL_DIR/$ICON_NAME
Terminal=false
Type=Application
Categories=Audio;Utility;
EOF

chmod +x "$HOME/Desktop/$DESKTOP_ENTRY"
echo "\n $APP_NAME installed successfully! Launch it from your desktop."
