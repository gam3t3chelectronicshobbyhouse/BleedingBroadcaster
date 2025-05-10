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

echo "Bleeding Broadcaster has been uninstalled."
