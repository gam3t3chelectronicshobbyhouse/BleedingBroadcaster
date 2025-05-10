#!/bin/bash

# Uninstaller script for Bleeding Broadcaster
INSTALL_DIR="$HOME/BleedingBroadcaster"
DESKTOP_FILE="$HOME/Desktop/BleedingBroadcaster.desktop"

echo "Removing Bleeding Broadcaster files..."

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
  rm -rf "$INSTALL_DIR"
  echo "Deleted: $INSTALL_DIR"
fi

# Remove desktop shortcut
if [ -f "$DESKTOP_FILE" ]; then
  rm "$DESKTOP_FILE"
  echo "Deleted: $DESKTOP_FILE"
fi

# Optional: Remove dependencies (prompt user)
echo "Would you like to remove the installed dependencies as well? (y/n)"
read -r REMOVE_DEPS
if [[ "$REMOVE_DEPS" == "y" || "$REMOVE_DEPS" == "Y" ]]; then
  sudo apt-get remove --purge -y git python3-pip python3-tk sox python3-pygame
  sudo apt-get autoremove -y
  echo "Dependencies removed."
else
  echo "Dependencies retained."
fi

echo "Bleeding Broadcaster has been uninstalled."
