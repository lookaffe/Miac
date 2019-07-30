from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import RPi.GPIO as GPIO
import os
import logging

# close all previous omxplayer instances
os.system('killall omxplayer.bin')

RoAPin = 7    # pin7
RoBPin = 8    # pin8
RoSPin = 13    # pin13
globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

# this video is used for noise between videos
#STANDBY_PATH = Path("/home/pi/Miac/Video/whiteNoise.mp4")
STANDBY_PATH = Path("/home/pi/Miac/Video/white_noise.mp4")
standBy_player = OMXPlayer(STANDBY_PATH, args= ['-o', 'local', '--no-osd', '--layer', '1', '--loop','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer1') #'--win', '1000,0,1640,480'
standBy_player.set_volume(0)
#standBy_player.hide_video()

#VIDEO_PATHS = [Path("/home/pi/Miac/Video/01.mp4"), Path("/home/pi/Miac/Video/02.mp4"),Path("/home/pi/Miac/Video/03.mp4"), Path("/home/pi/Miac/Video/04.mp4")]
VIDEO_PATHS = [Path("/home/pi/Miac/Video/clip1.mp4"), Path("/home/pi/Miac/Video/clip2.mp4"),Path("/home/pi/Miac/Video/clip3.mp4"), Path("/home/pi/Miac/Video/clip4.mp4"),Path("/home/pi/Miac/Video/clip5.mp4"), Path("/home/pi/Miac/Video/clip6.mp4"),Path("/home/pi/Miac/Video/clip7.mp4"), Path("/home/pi/Miac/Video/clip8.mp4")]
NOISE_PATH = Path("/home/pi/Miac/Video/standBy.mp4") #non più lungo di 1 secondo!

numOfVideos = 8

#initialization of players and video duration
players = []
video_dur = []

something_playing = False
noise_playing = False
update_video = False
videoRange_steps = 12 # deve essere pari!

played_video = 0

def fade(videoNum, direction): # direction (1 fade in,  0 fade out)
    for x in range(255):
        if direction: 
            players[videoNum].set_alpha(x)
        else: 
            players[videoNum].set_alpha(255-x)

def set_video(videoNum):
    players[videoNum].set_volume(10)
    sleep(1)
    video_dur.append(players[videoNum].duration())
    print("dur video ",videoNum," ", video_dur[videoNum])
    players[videoNum].quit()
    
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    rotaryClear()
    global globalCounter

def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    global update_video
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            print("globalCounter = " , globalCounter)
            update_video = True
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
            print("globalCounter = " , globalCounter)
            update_video = True
        
    return globalCounter

def clear(ev=None):
    globalCounter = videoRange_steps/2
    print("globalCounter = " , globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling

def destroy():
    GPIO.cleanup()             # Release resource

setup()
##
#start the first video and hide 
players.append(OMXPlayer(VIDEO_PATHS[0], args=['-o', 'local', '--layer', '2', '--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer2')) #, '--win', '1000,0,1640,480'
set_video(0)

players.append(OMXPlayer(VIDEO_PATHS[1], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer3')) #, '-b'
set_video(1)

players.append(OMXPlayer(VIDEO_PATHS[2], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer4')) #, '-b'
set_video(2)

players.append(OMXPlayer(VIDEO_PATHS[3], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer5')) #, '-b
set_video(3)

players.append(OMXPlayer(VIDEO_PATHS[4], args=['-o', 'local', '--layer', '2', '--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer6')) #, '--win', '1000,0,1640,480'
set_video(4)

players.append(OMXPlayer(VIDEO_PATHS[5], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer7')) #, '-b'
set_video(5)

players.append(OMXPlayer(VIDEO_PATHS[6], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer8')) #, '-b'
set_video(6)

players.append(OMXPlayer(VIDEO_PATHS[7], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys','--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer9')) #, '-b'
set_video(7)

print("first played_video ",played_video)

players[0].load(VIDEO_PATHS[0])

something_playing=1
gc=0

while True:
    #update rotary value
    gc = rotaryDeal()
    try:
    
        if not something_playing:
            standBy_player.set_volume(3)
        #change video
        if (gc<0 or gc>videoRange_steps):
            prev_video = played_video
            if gc>0:
                played_video = played_video +1
                globalCounter = 0
                gc = 0
            else:
                played_video = played_video -1
                globalCounter = videoRange_steps
                gc = videoRange_steps
            
            played_video = played_video%numOfVideos
            #print("played video ", played_video, " - previous " , prev_video)
            players[played_video].load(VIDEO_PATHS[played_video])
            standBy_player.set_volume(0)
            something_playing = True 
            players[prev_video].quit()
        else:
            None

            #introduce noise
        if update_video:
            if not something_playing:
                players[played_video].load(VIDEO_PATHS[played_video])
                something_playing = True  
            standBy_player.set_volume(abs(gc-videoRange_steps/2))
            #standby_player.show_video()
            update_video = False
            
        players[played_video].set_alpha(255- 50*(abs(gc-videoRange_steps/2)))

##        if (players[played_video].position()>(video_dur[played_video] - 0.5)):
##            print("stop")
##            standBy_player.set_volume(3)
    except: #DBusException quando deve far ripartire un video finito (dbus.exceptions.DBusException: org.freedesktop.DBus.Error.NoReply: Message recipient disconnected from message bus without replying)
        something_playing = False
