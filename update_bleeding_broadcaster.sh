#!/bin/bash

# Update script for Bleeding Broadcaster
INSTALL_DIR="$HOME/BleedingBroadcaster"

if [ -d "$INSTALL_DIR/.git" ]; then
  echo "Checking for updates..."
  cd "$INSTALL_DIR"
  echo "Please close Bleeding Broadcaster before applying updates."
  read -p "Press [Enter] to continue with update or Ctrl+C to cancel..."
  git pull
  echo "Bleeding Broadcaster has been updated. Please restart the application manually if it's open."
else
  echo " Git repo not found in $INSTALL_DIR. Please reinstall using the installer script."
fi
