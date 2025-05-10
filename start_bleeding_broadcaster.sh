#!/bin/bash
echo "Launching Bleeding Broadcaster..." > /home/pi/bleeding_broadcaster.log
cd /home/pi/BleedingBroadcaster
/usr/bin/python3 bleeding_broadcaster.py >> /home/pi/bleeding_broadcaster.log 2>&1
echo ""
echo "Program exited. Check /home/pi/bleeding_broadcaster.log for errors."
read -p "Press Enter to close this window..."
