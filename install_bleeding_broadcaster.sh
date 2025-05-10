#!/bin/bash

# Bleeding Broadcaster Installer Script
# Usage: curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_PATH="$INSTALL_DIR/icon.png"
DESKTOP_FILE="$HOME/Desktop/BleedingBroadcaster.desktop"
PYTHON_EXEC="/usr/bin/python3"
MAIN_SCRIPT="$INSTALL_DIR/bleedingbroadcaster.py"

echo "Installing Bleeding Broadcaster..."

# Ensure required packages
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
  echo "Updating existing installation..."
  cd "$INSTALL_DIR" || exit
  git pull
else
  echo "Cloning Bleeding Broadcaster..."
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create desktop shortcut
echo "Creating desktop shortcut..."

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster
Exec=lxterminal -e $PYTHON_EXEC $MAIN_SCRIPT
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

# Ensure icon is readable
if [ -f "$ICON_PATH" ]; then
  xdg-icon-resource install --novendor --size 64 "$ICON_PATH" "bleeding-broadcaster"
fi

echo "Installation complete."
echo "You can now launch Bleeding Broadcaster from your Desktop."
echo "If the program was already open, please restart it to use the latest version."
