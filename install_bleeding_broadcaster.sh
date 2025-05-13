#!/bin/bash

# Bleeding Broadcaster Installer Script

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"
ICON_NAME="icon.png"
APPLICATIONS_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APPLICATIONS_DIR/bleedingbroadcaster.desktop"

# Ensure dependencies are installed
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-tk sox python3-pygame rtl-sdr

# Clone or update the repository
if [ -d "$INSTALL_DIR" ]; then
  echo "Repository already exists. Pulling latest changes..."
  cd "$INSTALL_DIR" && git pull
else
  echo "Cloning the Bleeding Broadcaster repository..."
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create applications directory if it doesn't exist
mkdir -p "$APPLICATIONS_DIR"

# Create .desktop file
echo "Creating application launcher..."
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Bleeding Broadcaster
Comment=Start Bleeding Broadcaster
Exec=/usr/bin/python3 $INSTALL_DIR/bleeding_broadcaster.py
Icon=$INSTALL_DIR/$ICON_NAME
Terminal=false
Type=Application
Categories=AudioVideo;
EOF

chmod +x "$DESKTOP_FILE"

echo "Installation complete!"
echo "You can now find 'Bleeding Broadcaster' in the Applications menu under Audio/Video or Utilities."
echo "If the application was running, please restart it."
