#!/bin/bash

# Bleeding Broadcaster Installer Script
# Usage: curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_NAME="BleedingBroadcaster.png"
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

# Create desktop shortcut
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=Bleeding Broadcaster
Comment=Broadcast AM/FM audio for testing
Exec=python3 $INSTALL_DIR/bleeding_broadcaster.py
Icon=$INSTALL_DIR/$ICON_NAME
Terminal=false
Type=Application
Categories=Audio;Utility;
EOF

chmod +x "$DESKTOP_FILE"

# Launch application
python3 "$INSTALL_DIR/bleeding_broadcaster_gui.py"
