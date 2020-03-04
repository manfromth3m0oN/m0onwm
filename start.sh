pkill Xephyr
export DISPLAY=:0
Xephyr -screen 1280x720 -br -ac -noreset :1 &
export DISPLAY=:1
python main.py
