#!/bin/bash

# Bleeding Broadcaster Installer Script
# Usage: curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_NAME="icon.png"
DESKTOP_FILE="$HOME/Desktop/BleedingBroadcaster.desktop"

# Ensure dependencies
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
  cd "$INSTALL_DIR" && git pull
else
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster 
Exec=/usr/bin/python3 /home/pi/BleedingBroadcaster/bleedingbroadcaster.py > /home/pi/Desktop/bleedingbroadcaster.log 2>&1
Icon=icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"
# Launch application
python3 "$INSTALL_DIR/bleeding_broadcaster.py"
