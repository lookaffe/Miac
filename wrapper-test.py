#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH = Path("/home/pi/MIAC/01.mkv")
player = OMXPlayer(VIDEO_PATH)
sleep(1)
player.quit()

player.load(VIDEO_PATH)
sleep(2)
player.pause()
sleep(2)
player.hide_video()
sleep(2)
player.show_video()
player.quit()