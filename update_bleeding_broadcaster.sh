#!/bin/bash

# Bleeding Broadcaster Updater Script

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"

echo "Updating Bleeding Broadcaster..."

# Check if the directory exists
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Error: $INSTALL_DIR does not exist."
  echo "Please install the application first using the install script."
  exit 1
fi

# Pull latest changes
cd "$INSTALL_DIR" || exit
git pull

if [ $? -eq 0 ]; then
  echo "Update completed successfully."
else
  echo "Update failed. Please check your internet connection or the repository status."
fi

echo ""
echo "If Bleeding Broadcaster is running, please restart it to apply the updates."
