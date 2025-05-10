#!/bin/bash

# Bleeding Broadcaster Installer Script
# Usage: curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_NAME="icon.png"
DESKTOP_FILE="$HOME/Desktop/BleedingBroadcaster.desktop"

# Ensure dependencies are installed
echo "Updating system and installing dependencies..."
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame

# Clone or update the repository
if [ -d "$INSTALL_DIR" ]; then
  echo "Repository already exists. Pulling latest changes..."
  cd "$INSTALL_DIR" && git pull
else
  echo "Cloning the Bleeding Broadcaster repository..."
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster
Exec=lxterminal -e /usr/bin/python3  $INSTALL_DIR/bleedingbroadcaster.py
Icon=$INSTALL_DIR/$ICON_NAME
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"
chmod +x "$INSTALL_DIR/bleedingbroadcaster.py"

echo "Installation complete! The Bleeding Broadcaster shortcut is now on your desktop."
echo "Please restart the program if it's already running."

# End of script
