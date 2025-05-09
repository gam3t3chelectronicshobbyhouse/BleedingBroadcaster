#!/bin/bash

set -e

echo "Updating system..."
sudo apt update && sudo apt install -y python3 python3-tk sox git build-essential

echo "Cloning rpitx..."
cd ~
if [ ! -d "rpitx" ]; then
  git clone https://github.com/F5OEO/rpitx.git
  cd rpitx
  ./install.sh
else
  echo "rpitx already installed."
fi

echo "Downloading Bleeding Broadcaster GUI..."
cd ~
mkdir -p ~/BleedingBroadcaster
cd ~/BleedingBroadcaster

# Download GUI Python script
wget -O bleeding_broadcaster.py https://raw.githubusercontent.com/Gam3t3ch/BleedingBroadcaster/main/bleeding_broadcaster.py

# Download icon (replace with your actual hosted PNG URL if you have one)
wget -O icon.png https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Raspberry_Pi_Logo.svg/240px-Raspberry_Pi_Logo.svg.png

echo "Creating desktop shortcut..."
cat <<EOF > ~/Desktop/BleedingBroadcaster.desktop
[Desktop Entry]
Name=Bleeding Broadcaster
Comment=RF Broadcaster with AM/FM & Tone Generator
Exec=python3 ~/BleedingBroadcaster/bleeding_broadcaster.py
Icon=~/BleedingBroadcaster/icon.png
Terminal=false
Type=Application
Categories=Audio;HamRadio;Electronics;
EOF

chmod +x ~/Desktop/BleedingBroadcaster.desktop

echo "Installation complete!"
echo "Launch the app from your Desktop or with:"
echo "  python3 ~/BleedingBroadcaster/bleeding_broadcaster.py"
