from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import RPi.GPIO as GPIO
import os
import logging

# close all previous omxplayer instances
os.system('killall omxplayer.bin')

# rotary pins declaration
RoAPin = 7    # pin7
RoBPin = 8    # pin8
RoSPin = 13    # pin13
globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

FOLDER = '/home/pi/Videos/'
DBUSNAME ='org.mpris.MediaPlayer2.omxplayer'

# args for omxplayer
ARGS1= ['-o', 'local', '--no-osd', '--layer', '1', '--loop', '--win', '1000,0,1640,480']
ARGS2= ['-o', 'local', '--no-osd', '--layer', '2','--win', '1000,0,1640,480']

entries = os.listdir(FOLDER)
entries.sort()

numOfVideos = len(entries)-1

# this video is used for noise between
STANDBY_PATH = Path(FOLDER + "white_noise.mp4")
standBy_player = OMXPlayer(STANDBY_PATH, args=ARGS1, dbus_name=DBUSNAME + '1') #'--win', '1000,0,1640,480'
standBy_player.set_volume(0)

VIDEO_PATHS = []
for x in range(numOfVideos):
    VIDEO_PATHS.append(Path(FOLDER + entries[x]))
NOISE_PATH = Path("/home/pi/Videos/standBy.mp4") #non più lungo di 1 secondo!

#initialization of players and video duration
players = []
video_dur = []

something_playing = False
noise_playing = False
update_video = False

fade_speed = 10

played_video = 0

def fade(videoNum, direction): # direction (1 fade in,  0 fade out)
    if direction:
        for x in range(0, 255, fade_speed):
            vol = 1 - (x/255)
            players[videoNum].set_alpha(x)
            players[videoNum].set_volume(1-vol)
            standBy_player.set_volume(vol)
    else:
        for x in range(0, 255, fade_speed):
            vol = 1 - (x/255)
            players[videoNum].set_alpha(255-x)
            players[videoNum].set_volume(vol)
            standBy_player.set_volume(1-vol)

# for video initialization
def set_video(videoNum):
    players[videoNum].set_volume(1)
    sleep(1)
    video_dur.append(players[videoNum].duration())
    print("dur video ",videoNum," ", video_dur[videoNum])
    players[videoNum].quit()

# rotary setup
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    rotaryClear()
    global globalCounter

#rotary update
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

# load and play all videos to check it
for x in range(numOfVideos):
    players.append(OMXPlayer(VIDEO_PATHS[x], args=ARGS2, dbus_name=DBUSNAME+str(x+2)))
    set_video(x)

print("first played_video ",played_video)

players[0].load(VIDEO_PATHS[0])

something_playing=1
gc=0

while True:
    #update rotary value
    gc = rotaryDeal()
    try:
        #change video
        if update_video:
            previous_video = played_video
            played_video = played_video + gc
            played_video = played_video%numOfVideos
            
            if not something_playing:
                previous_video = previous_video -gc
                played_video = played_video -gc
                players[played_video].load(VIDEO_PATHS[played_video])
                fade(played_video, 1)
            else:
                fade(previous_video, 0)
                players[previous_video].quit()
                players[played_video].load(VIDEO_PATHS[played_video])
                fade(played_video, 1)
            print("played video ", played_video, " - previous " , previous_video)
            something_playing = True
            globalCounter = 0
            gc = 0

            update_video = False
        else:
            if not something_playing:
                standBy_player.set_volume(1)
        players[played_video].can_control()
    except: #DBusException quando deve far ripartire un video finito (dbus.exceptions.DBusException: org.freedesktop.DBus.Error.NoReply: Message recipient disconnected from message bus without replying)
        something_playing = False
