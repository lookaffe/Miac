from omxplayer.player import OMXPlayer
from pathlib import Path
import time
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
ledPin = 18

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

FOLDER = '/home/pi/Music/'
DBUSNAME ='org.mpris.MediaPlayer2.omxplayer'

ARGS1= ['-o', 'local', '--no-osd', '--layer', '1', '--loop'] #'--win', '1000,0,1640,480'
ARGS2= ['-o', 'local', '--no-osd', '--layer', '2']

entries = os.listdir(FOLDER)
entries.sort()

numOfAudios = len(entries)-1

# this video is used for noise between
STANDBY_PATH = Path(FOLDER + "white_noise.mp3")
standBy_player = OMXPlayer(STANDBY_PATH, args=ARGS1, dbus_name=DBUSNAME + '1') 
standBy_player.set_volume(0)

RADIO_PATHS = []
for x in range(numOfAudios):
    RADIO_PATHS.append(Path(FOLDER + entries[x]))
NOISE_PATH = Path("/home/pi/Videos/standBy.mp4") #non più lungo di 1 secondo!

#initialization of players and video duration
players = []
audio_dur = []

something_playing = False
noise_playing = False
update_audio = False
radioRange_steps = 24# even
half_radioRange_steps = radioRange_steps/2
step_noiseVal = round(2/radioRange_steps,2)
print(step_noiseVal)

played_audio = 0

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
    globalCounter = radioRange_steps
    print("globalCounter = " , globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling

def destroy():
    GPIO.cleanup()             # Release resource

# rotary setup
setup()

# led setup
GPIO.setwarnings(False)
GPIO.setup(ledPin,GPIO.OUT)

# omxplayer setup
for x in range(numOfAudios):
    players.append(OMXPlayer(RADIO_PATHS[x], args=ARGS2, dbus_name=DBUSNAME+str(x+2))) #, '--win', '1000,0,1640,480'
    set_audio(x)
print("first played_audio ",played_audio)

# noise step values
noise_val = []
for x in range(radioRange_steps):
    noise_val.append((step_noiseVal)*abs(x-half_radioRange_steps))

noise_transition_vol = 0.0
noise_vol = 1.0
noise_time = 10
noise_playing = True

play_transition_vol = 0.0
play_vol = 0.0
something_playing=True

# steps around the middle to obtain no noise
noNoise_range = 3

# rotary steps
gc=12

# starting time of a video
video_start= 0.0

# starting time of noise
noise_start = 0.0

players[0].load(RADIO_PATHS[0])
video_start = time.time()
players[0].set_volume(play_vol)

standBy_player.set_volume(noise_vol)

while True:
    #update rotary value
    gc = rotaryDeal()
    # if nothing is playing raise the noise
    if not something_playing:
        noise_end = time.time()
        noise_dur = noise_end - noise_start
        # check noise timing, after noise_time lower the noise
        if noise_dur > noise_time:
            noise_vol = 0.2
        else:
            noise_vol = 1
            
    #introduce noise
    if update_audio:
        noise_vol = noise_val[gc%radioRange_steps]
        play_vol = 1- noise_vol
        #change video
        if (gc<0 or gc>radioRange_steps):
            prev_audio = played_audio
            if gc>0:
                played_audio = played_audio +1
                globalCounter = 0
                gc = 0
            else:
                played_audio = played_audio -1
                globalCounter = radioRange_steps
                gc = radioRange_steps
            
            played_audio = played_audio%numOfAudios
            #print("played video ", played_audio, " - previous " , prev_audio)
            #sleep(1)
            players[prev_audio].quit()
            players[played_audio].load(RADIO_PATHS[played_audio])
            video_start = time.time()
            #print("video_start ", video_start)
##                players[played_audio].set_volume(play_vol)

            #noise_vol = 0
            #standBy_player.set_volume(0)
            something_playing = True
            noise_playing = False
            
                
        if not something_playing:
            #sleep(1)
            video_start = time.time()
            players[played_audio].load(RADIO_PATHS[played_audio])
            something_playing = True
            noise_playing = False
##            players[played_audio].set_volume(play_vol)
        #standBy_player.set_volume(noise_vol)
        #standby_player.show_video()
        update_audio = False
    
    if (gc > half_radioRange_steps - noNoise_range) and (gc < half_radioRange_steps + noNoise_range) and something_playing:                   
        GPIO.output(ledPin,GPIO.HIGH)
        noise_vol = 0
    else:
        GPIO.output(ledPin,GPIO.LOW)
        
    if not (noise_transition_vol == noise_vol):
        if noise_transition_vol>noise_vol:    
            noise_transition_vol = round(noise_transition_vol-0.1, 1)
        else:
            noise_transition_vol = round(noise_transition_vol+0.1, 1)
        standBy_player.set_volume(noise_transition_vol)
        
    if not (play_transition_vol == play_vol) and something_playing:
        if play_transition_vol>play_vol:    
            play_transition_vol = round(play_transition_vol-0.1, 1)
        else:
            play_transition_vol = round(play_transition_vol+0.1, 1)
        players[played_audio].set_volume(play_transition_vol)
    
    # check video ends
    video_end = time.time()
    dur = video_end - video_start
    if (dur > audio_dur[played_audio]) and something_playing:
        something_playing = False
        noise_start = time.time()
        print("noise start")