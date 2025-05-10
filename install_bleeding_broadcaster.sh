#!/bin/bash

# Bleeding Broadcaster Installer Script
# Usage:
#   curl -sSL https://raw.githubusercontent.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster/main/install_bleeding_broadcaster.sh | bash

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
SCRIPT_NAME="bleedingbroadcaster.py"
ICON_NAME="icon.png"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
ICON_PATH="$INSTALL_DIR/$ICON_NAME"
DESKTOP_DIR="$HOME/Desktop"
DESKTOP_FILE="$DESKTOP_DIR/BleedingBroadcaster.desktop"

# ---- Ensure desktop directory exists ----
mkdir -p "$DESKTOP_DIR"

# ---- Install dependencies ----
echo "📦 Installing dependencies..."
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame

# ---- Clone or update repo ----
if [ -d "$INSTALL_DIR" ]; then
  echo "🔄 Updating Bleeding Broadcaster..."
  cd "$INSTALL_DIR" && git pull
else
  echo "⬇️ Cloning Bleeding Broadcaster..."
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

# ---- Check main script exists ----
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "❌ Error: $SCRIPT_NAME not found at $SCRIPT_PATH"
  exit 1
fi

# ---- Check icon exists or fall back ----
if [ ! -f "$ICON_PATH" ]; then
  echo "⚠️ Icon not found at $ICON_PATH, using default Python icon."
  ICON_PATH="/usr/share/pixmaps/python.xpm"
fi

# ---- Create desktop shortcut ----
echo "📁 Creating desktop shortcut at $DESKTOP_FILE..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster 
Exec=/usr/bin/python3 $SCRIPT_PATH > $HOME/Desktop/bleedingbroadcaster.log 2>&1
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "✅ Installation complete!"
echo "📌 A desktop shortcut has been created."
echo "🔁 Please restart the Bleeding Broadcaster if it's currently running."
