#!/bin/bash
#Make sure no Xephyr instances are running
pkill Xephyr
# Open Xephyr for the current X display
export DISPLAY=:0
Xephyr -screen 1280x720 -br -ac -noreset :1 &
# Run main.py for the Xephyr window
export DISPLAY=:1
python main.py