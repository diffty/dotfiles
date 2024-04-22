#!/bin/bash

# Terminate already running bar instances
# If all your bars have ipc enabled, you can use 
polybar-msg cmd quit
# Otherwise you can use the nuclear option:
# killall -q polybar

# Launch bar1 and bar2
echo "---" | tee -a /tmp/polybar1.log /tmp/polybar2.log


MONITOR="DP-1" polybar dfbar-screen-main 2>&1 | tee -a /tmp/polybar1.log & disown
MONITOR="HDMI-0" polybar dfbar-screen-secondary 2>&1 | tee -a /tmp/polybar2.log & disown

echo "Bars launched..."
