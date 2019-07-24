import dbus
import os
import subprocess
from subprocess import Popen
import time

movies = ("/home/pi/MIAC/03.mp4", "/home/pi/MIAC/01.mp4")
command1 = 'omxplayer --win 1000,0,1640,480 --dbus_name "org.mpris.MediaPlayer2.omxplayer1" --loop --no-osd /home/pi/MIAC/03.mp4'

Popen([command1], shell=True)

time.sleep(3)
os.system('dbuscontrol.sh stop')
        