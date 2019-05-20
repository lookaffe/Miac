import dbus
import subprocess
from subprocess import Popen
import time

movies = ("/home/pi/MIAC/03.mp4", "/home/pi/MIAC/01.mp4")
command1 = 'omxplayer --win 1000,0,1640,480 --dbus_name "org.mpris.MediaPlayer2.omxplayer1" --loop --no-osd /home/pi/MIAC/03.mp4'

Popen([command1], shell=True)

time.sleep(1)
subprocess.call(['dbuscontrol.sh org.mpris.MediaPlayer2.omxplayer1 stop'], shell=True)
        