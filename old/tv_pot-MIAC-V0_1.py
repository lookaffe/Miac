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
VIDEO_PATH00 = Path("/home/pi/Miac/Video/staticNoise.mp4")#"/home/pi/Miac/Video/01.mp4")
player00 = OMXPlayer(VIDEO_PATH00, args= ['--layer', '2', '-loop', '-b'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
##player00.pause()
##player00.hide_video()
sleep(1)

VIDEO_PATHS = [Path("/home/pi/Miac/Video/01.mp4"), Path("/home/pi/Miac/Video/02.mp4"),Path("/home/pi/Miac/Video/03.mp4"), Path("/home/pi/Miac/Video/04.mp4")]
NOISE_PATH = Path("/home/pi/Miac/Video/staticNoise.mp4") #non più lungo di 1 secondo!

#initialization of players
players = [0,0,0,0]

something_playing = False
noise_playing = False

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
players[0] = OMXPlayer(VIDEO_PATHS[0], args=['-o', 'local', '--layer', '2', '--no-osd', '--no-keys'], dbus_name='org.mpris.MediaPlayer2.omxplayer2') #, '--win', '1000,0,1640,480'
sleep(2)
players[0].quit()

players[1] = OMXPlayer(VIDEO_PATHS[1], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys'], dbus_name='org.mpris.MediaPlayer2.omxplayer3') #, '-b'
sleep(2)
players[1].quit()

players[2] = OMXPlayer(VIDEO_PATHS[2], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys'], dbus_name='org.mpris.MediaPlayer2.omxplayer4') #, '-b'
sleep(2)
players[2].quit()

players[3] = OMXPlayer(VIDEO_PATHS[3], args=['-o', 'local', '--layer', '2','--no-osd', '--no-keys'], dbus_name='org.mpris.MediaPlayer2.omxplayer5') #, '-b'
sleep(2)
players[3].quit()

## inizializzazione parametri per l'avvio per non far partire subito un video
adc_value = adc.read_adc(0, gain=GAIN) #valore del selettore al momento dell'accensione
pre_adc_value = adc_value

if adc_value > 0:
    played_video = 0
    if adc_value > 6000:
        played_video = 1
        if adc_value > 12000:
            played_video = 2
            if adc_value > 18000:
                played_video = 3
print("first played_video ",played_video)
                
while True:
    #update adc value
    adc_value= adc.read_adc(0, gain=GAIN)
    if adc_value > 0:
        playing_video = 0
        if adc_value > 8000:
            playing_video = 1
            if adc_value > 16000:
                playing_video = 2
                if adc_value > 24000:
                    playing_video = 3
    
    #if a video is playing update the pre_adc_value
    try:
        if (players[playing_video].can_play()):
            
##            if ((abs(adc_value - adc.read_adc(0, gain=GAIN))>200) and (not noise_playing)):
##                noiseplay = OMXPlayer(NOISE_PATH, args=['-o', 'local', '--layer', '2','--vol', ' -4500', '--alpha', '55', '--no-osd', '--no-keys'], dbus_name='org.mpris.MediaPlayer2.omxplayer9')
##                noise_playing = True
                #sistemare la ripetizione del noise sovrapposta
            pre_adc_value = adc.read_adc(0, gain=GAIN)
            something_playing = True
        else:
            something_playing = False
    except:
        noise_playing = False
        something_playing = False
    
##    print("played_video ",played_video, " | playing_video ", playing_video, " | something_playing ", something_playing)
                
    # se il video non sta andando e si muove il cursore di 500 o si passa all'altro video
    if (((not something_playing) and (abs(adc_value - pre_adc_value)>500)) or (not playing_video == played_video)):
        print("adc_value",adc_value)
        players[played_video].quit()
        #noiseplay.quit()
        play_video(playing_video)
        pre_adc_value = adc_value
        played_video = playing_video