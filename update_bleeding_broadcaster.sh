#!/bin/bash

# Directory where the application files are stored
APP_DIR="/home/BleedingBroadcaster"  # Replace with your actual app directory
GIT_REPO="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"  # Replace with your actual GitHub repository

# Function to check if git is installed
check_git() {
    if ! command -v git &>/dev/null; then
        echo "Git not found, please install Git first."
        exit 1
    fi
}

# Function to pull the latest changes from the repository
git_pull() {
    echo "Fetching the latest updates from the repository..."
    cd "$APP_DIR" || exit 1
    git fetch --all
    git reset --hard origin/main  # Assuming 'main' is your branch
}

# Function to handle downloading and replacing files
download_files() {
    echo "Downloading new files from the GitHub repository..."
    git_pull

    # Assuming all files are in the repo and will be overwritten
    echo "Replacing old files with the new ones..."
    git checkout .
}

# Function to restart the application if required
restart_application() {
    echo "Update complete! Restarting the application..."
    sudo systemctl restart bleeding_broadcaster  # Example: Adjust for your system's init system or method
}

# Function to handle errors and clean exit
handle_error() {
    echo "An error occurred during the update process. Please check the logs and try again."
    exit 1
}

# Main update script
main() {
    check_git
    echo "Starting update process..."
    download_files || handle_error
    restart_application
}

main
