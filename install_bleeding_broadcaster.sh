#!/bin/bash

# Bleeding Broadcaster Installer Script (Plain Version)

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_PATH="$INSTALL_DIR/icon.png"
DESKTOP_FILE="$HOME/Desktop/BleedingBroadcaster.desktop"
WRAPPER_SCRIPT="$INSTALL_DIR/start_bleeding_broadcaster.sh"

echo "Updating system and installing dependencies..."
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame

echo "Cloning or updating the Bleeding Broadcaster repository..."
if [ -d "$INSTALL_DIR" ]; then
  cd "$INSTALL_DIR" && git pull
else
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

echo "Creating launcher script..."
cat <<EOF > "$WRAPPER_SCRIPT"
#!/bin/bash
echo "Launching Bleeding Broadcaster..." > /home/pi/bleeding_broadcaster.log
cd "$INSTALL_DIR"
/usr/bin/python3 bleeding_broadcaster.py >> /home/pi/bleeding_broadcaster.log 2>&1
echo ""
echo "Program exited. Check /home/pi/bleeding_broadcaster.log for details."
read -p "Press Enter to close this window..."
EOF

chmod +x "$WRAPPER_SCRIPT"

echo "Creating desktop shortcut..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster
Exec=lxterminal -e $WRAPPER_SCRIPT
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "Installation complete."
echo "You can now launch Bleeding Broadcaster from the desktop shortcut."
echo "If it was already running, please restart it."
