#!/usr/bin/python

import subprocess
import time

v1 = "/home/pi/MIAC/Video/BIANCOROSSOVERDONE_1taglio.mp4"
v2 = "/home/pi/MIAC/Video/SIGNORE_E_SIGNORI_1taglio.mp4"
name2 = "org.mpris.MediaPlayer2.omxplayer2"
name3 = "org.mpris.MediaPlayer2.omxplayer2"

pauseWord = 'p'
quitWord = 'q'

#Cache the first video by loading and then sending a pauseWord command
p1 = subprocess.Popen(["omxplayer", '-b','-o', 'local', '--win' , '1000,0,1640,480', v1, "--no-osd"], stdin=subprocess.PIPE)
time.sleep(1.3)
p1.stdin.write(pauseWord.encode())

#Test loop 2 videos 10000 times
count = 0
#while (count < 1):
#
##From this point in python we are in a loop, all code in a loop has to be indented.
##Play video 1 by sending the pauseWord command again which unpauseWords the video.
#    print(count)
#    p1.stdin.write(pauseWord.encode())
#
##Whilst the first video plays, we are now going to load the second video and pauseWord it
#    p2 = subprocess.Popen(["omxplayer",'--win' , '1000,0,1640,480', v2, "--no-osd"], stdin=subprocess.PIPE)
#    time.sleep(0.3)
#    p2.stdin.write(pauseWord.encode())
#
##We're going to play the first video for 3 seconds
#    time.sleep(3)
#
##Now we're going to quit the first video and then unpauseWord the second
#    p1.stdin.write(quitWord.encode())
#    p2.stdin.write(pauseWord.encode())
#
##As we have quit the first video, we need to load it again and pauseWord.
##We cant send a rewind command, doesnt work correctly in OMXPlayer 
#    p1 = subprocess.Popen(["omxplayer",'--win' , '1000,0,1640,480', v1, "--no-osd", "--dbus_name", name3], stdin=subprocess.PIPE)
#    time.sleep(0.3)
#    p1.stdin.write(pauseWord.encode())
#
##We're gonna play the second video for 5 seconds and quit.
#    time.sleep(5) 
#    p2.stdin.write(pauseWord.encode())
#
##Increment the count by 1
#    count = count + 1