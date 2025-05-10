#!/bin/bash

echo "=============================="
echo " Bleeding Broadcaster Updater"
echo "=============================="
echo ""

# Change to the script's directory (your project root)
cd "$(dirname "$0")" || {
    echo "Failed to enter script directory. Aborting."
    exit 1
}

# Check if it's a git repository
if [ ! -d .git ]; then
    echo "Error: This directory is not a Git repository."
    echo "Please clone the project using Git first."
    exit 1
fi

# Optional: Backup current files
backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp -r *.py *.sh "$backup_dir" 2>/dev/null

echo "Backup created at: $backup_dir"
echo ""

# Pull updates from GitHub
echo "Fetching latest updates..."
git reset --hard HEAD
git pull origin main || {
    echo "Failed to pull from GitHub."
    exit 1
}

echo ""
echo "✅ Update complete."
echo "Please restart the Bleeding Broadcaster app to apply changes."
