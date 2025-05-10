#!/bin/bash

# Bleeding Broadcaster Updater Script

INSTALL_DIR="$HOME/BleedingBroadcaster"
REPO_URL="https://github.com/gam3t3chelectronicshobbyhouse/BleedingBroadcaster"

# ---- Output colors (if terminal supports) ----
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Updating Bleeding Broadcaster...${NC}"

# ---- Check if install directory exists ----
if [ ! -d "$INSTALL_DIR" ]; then
  echo -e "${RED}❌ Error: Directory $INSTALL_DIR not found.${NC}"
  echo "Please run the install script first:"
  echo "  curl -sSL $REPO_URL/raw/main/install_bleeding_broadcaster.sh | bash"
  exit 1
fi

# ---- Pull latest changes ----
cd "$INSTALL_DIR" || exit
git pull

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ Update completed successfully.${NC}"
else
  echo -e "${RED}❌ Update failed. Please check your internet connection or GitHub repo status.${NC}"
fi

echo ""
echo -e "🔁 If Bleeding Broadcaster is currently running, please restart it to apply updates."
