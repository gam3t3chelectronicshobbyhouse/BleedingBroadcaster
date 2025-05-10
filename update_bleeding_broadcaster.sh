#!/bin/bash

# Update script for Bleeding Broadcaster
INSTALL_DIR="$HOME/BleedingBroadcaster"

if [ -d "$INSTALL_DIR/.git" ]; then
  cd "$INSTALL_DIR"
  echo "Checking for updates..."
  git pull
  echo "Bleeding Broadcaster updated. Please restart the application if it's running."
else
  echo "Git repo not found in $INSTALL_DIR. Please reinstall using the installer script."
fi
