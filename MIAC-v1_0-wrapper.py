from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import os

# close all previous omxplayer instances
os.system('killall omxplayer.bin')

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2

# this video is used only to mantain a black screen
VIDEO_PATH00 = Path("/home/pi/Miac/01.mp4")
player00 = OMXPlayer(VIDEO_PATH00)#, args= '-b')
player00.pause()
player00.hide_video()
sleep(1)

VIDEO_PATHS = [Path("/home/pi/Miac/03.mp4"), Path("/home/pi/Miac/01.mp4")]
NOISE_PATH = Path("/home/pi/Miac/staticNoise.mp4")

#initialization of players
players = [0,0]

something_playing = False

def play_video(videoNum):
##    players[videoNum].show_video()
##    players[videoNum].set_position(0.0)
##    players[videoNum].play()
    players[videoNum].load(VIDEO_PATHS[videoNum])
    
def pause_video(videoNum):
##    players[videoNum].pause()
##    players[videoNum].hide_video()
    players[videoNum].quit()
    
#start the first video and hide 
players[0] = OMXPlayer(VIDEO_PATHS[0], args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
sleep(3)
players[0].quit()
##players[0].pause()
##players[0].hide_video()


#player = OMXPlayer(VIDEO_PATH1,args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
#sleep(3)
#player.pause()
#sleep(2)
#player.hide_video()
players[1] = OMXPlayer(VIDEO_PATHS[1], args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer2') #, '-b'
sleep(3)
players[0].quit()
##players[1].pause()
##players[1].hide_video()

## inizializzazione parametri per l'avvio per non far partire subito un video
adc_value = adc.read_adc(0, gain=GAIN) #valore del selettore al momento dell'accensione
pre_adc_value = adc_value

if adc_value > 16000:
    played_video = 0
elif adc_value < 16000:
    played_video = 1
    
while True:
    #update adc value
    adc_value= adc.read_adc(0, gain=GAIN)
    if adc_value > 16000:
        playing_video = 0
    elif adc_value < 16000:
        playing_video = 1
    
    #if a video is playing update the pre_adc_value
    try:
        if (players[playing_video].can_play()):
            if ((abs(adc_value - adc.read_adc(0, gain=GAIN))>200) ):
                noiseplay = OMXPlayer(NOISE_PATH, args=['-o', 'local', '--vol', ' -4500', '--alpha', '55', '--no-osd', '--no-keys', '--win', '1000,0,1640,480'])
            pre_adc_value = adc.read_adc(0, gain=GAIN)
            something_playing = True
            
        else:
            something_playing = False
##        waitingVideo = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])
    except:
        something_playing = False
        
    # se il video non sta andando e si muove il cursore di 1000 o si passa all'altro video
    if (((not something_playing) and (abs(adc_value - pre_adc_value)>500)) or (not playing_video == played_video)):
        print("adc_value",adc_value - pre_adc_value)
        if adc_value > 16000:
            played_video = 0
            pause_video(1)
            play_video(0)
        elif adc_value < 16000:
            played_video = 1
            pause_video(0)
            play_video(1)
        pre_adc_value = adc_value