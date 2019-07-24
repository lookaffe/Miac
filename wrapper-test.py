#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH00 = Path("/home/pi/Miac/01.mp4")
player00 = OMXPlayer(VIDEO_PATH00, args= '-b')
player00.pause()
player00.hide_video()
sleep(2)

VIDEO_PATH = Path("/home/pi/Miac/03.mp4")
player = OMXPlayer(VIDEO_PATH)
sleep(1)
player.quit()

player.load(VIDEO_PATH)
sleep(2)

player.pause()
print (player.stopEvent)
sleep(2)
player.hide_video()
sleep(2)
player.show_video()
player.quit()

sleep(3)
player00.quit()
