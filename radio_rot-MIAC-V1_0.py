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

FOLDER = '/home/pi/Videos/'
DBUSNAME ='org.mpris.MediaPlayer2.omxplayer'

ARGS1= ['-o', 'local', '--no-osd', '--layer', '1', '--loop' , '--win', '1000,0,1640,480'] #'--win', '1000,0,1640,480'
ARGS2= ['-o', 'local', '--no-osd', '--layer', '2', '--win', '1000,0,1640,480']

entries = os.listdir(FOLDER)
entries.sort()

numOfAudios = len(entries)-1

# this video is used for noise between
STANDBY_PATH = Path(FOLDER + "white_noise.mp4")
standBy_player = OMXPlayer(STANDBY_PATH, args=ARGS1, dbus_name=DBUSNAME + '1') 
standBy_player.set_volume(0)

RADIO_PATHS = []
for x in range(numOfAudios):
    RADIO_PATHS.append(Path(FOLDER + entries[x]))
NOISE_PATH = Path("/home/pi/Videos/standBy.mp4") #non più lungo di 1 secondo!

numOfAudios = 8

#initialization of players and video duration
players = []
audio_dur = []

something_playing = False
noise_playing = False
update_audio = False
radioRange_steps = 12 # deve essere pari!

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

def set_audio(videoNum):
    players[videoNum].set_volume(1)
    sleep(1)
    audio_dur.append(players[videoNum].duration())
    print("dur video ",videoNum," ", audio_dur[videoNum])
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
    global update_audio
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            print("globalCounter = " , globalCounter)
            update_audio = True
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
            print("globalCounter = " , globalCounter)
            update_audio = True
        
    return globalCounter

def clear(ev=None):
    globalCounter = radioRange_steps/2
    print("globalCounter = " , globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling

def destroy():
    GPIO.cleanup()             # Release resource

setup()

for x in range(numOfAudios):
    players.append(OMXPlayer(RADIO_PATHS[x], args=ARGS2, dbus_name=DBUSNAME+str(x+2))) #, '--win', '1000,0,1640,480'
    set_audio(x)
print("first played_audio ",played_audio)

players[0].load(RADIO_PATHS[0])

something_playing=1
gc=0

while True:
    #update rotary value
    gc = rotaryDeal()
    try:
    
        if not something_playing:
            standBy_player.set_volume(1)
        #change video
        if (gc<0 or gc>radioRange_steps):
            prev_video = played_audio
            if gc>0:
                played_audio = played_audio +1
                globalCounter = 0
                gc = 0
            else:
                played_audio = played_audio -1
                globalCounter = radioRange_steps
                gc = radioRange_steps
            
            played_audio = played_audio%numOfAudios
            #print("played video ", played_audio, " - previous " , prev_video)
            players[played_audio].load(RADIO_PATHS[played_audio])
            standBy_player.set_volume(0)
            something_playing = True 
            players[prev_video].quit()
        else:
            None

            #introduce noise
        if update_audio:
            if not something_playing:
                players[played_audio].load(RADIO_PATHS[played_audio])
                something_playing = True
##            players[played_audio].set_volume(1.1 - (1/(radioRange_steps/2))*abs(gc-radioRange_steps/2))
##            standBy_player.set_volume((1/(radioRange_steps/2))*abs(gc-radioRange_steps/2))
            noise_vol = (1/(radioRange_steps/2))*abs(gc-radioRange_steps/2)
            play_vol = 1-noise_vol
            if play_vol<0.2:
                play_vol=0.2
            players[played_audio].set_volume(play_vol)
            standBy_player.set_volume(noise_vol)
            #standby_player.show_video()
            update_audio = False
            print((1/(radioRange_steps/2))*abs(gc-radioRange_steps/2))
            players[played_audio].set_alpha(255- (255/(radioRange_steps/2))*(abs(gc-radioRange_steps/2)))

##        if (players[played_audio].position()>(audio_dur[played_audio] - 0.5)):
##            print("stop")
##            standBy_player.set_volume(3)
    except: #DBusException quando deve far ripartire un video finito (dbus.exceptions.DBusException: org.freedesktop.DBus.Error.NoReply: Message recipient disconnected from message bus without replying)
        something_playing = False
