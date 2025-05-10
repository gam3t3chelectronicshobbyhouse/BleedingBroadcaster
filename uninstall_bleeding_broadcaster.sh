#!/bin/bash

# Uninstaller for Bleeding Broadcaster

INSTALL_DIR="$HOME/BleedingBroadcaster"
DESKTOP_FILE="$HOME/.local/share/applications/bleedingbroadcaster.desktop"

echo "Uninstalling Bleeding Broadcaster..."

# Remove install directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed installation directory: $INSTALL_DIR"
else
    echo "Installation directory not found."
fi

# Remove application menu entry
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "Removed application menu shortcut."
else
    echo "Application menu shortcut not found."
fi

echo "Uninstallation complete."
