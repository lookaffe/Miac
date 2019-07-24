
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import os
##
##if os.path.exists("/tmp/omxplayerdbus.pi"):
##    os.remove("/tmp/omxplayerdbus.pi")
##if os.path.exists("/tmp/omxplayerdbus.pi.pid"):
##    os.remove("/tmp/omxplayerdbus.pi.pid")
##print("File Removed!")

os.system('killall omxplayer.bin')

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2

VIDEO_PATH00 = Path("/home/pi/Miac/01.mp4")
player00 = OMXPlayer(VIDEO_PATH00, args= '-b')
player00.pause()
player00.hide_video()
sleep(2)

##VIDEO_PATH1 = Path("/home/pi/Miac/03.mp4")
##VIDEO_PATH2 = Path("/home/pi/Miac/01.mp4")
VIDEO_PATHS = [Path("/home/pi/Miac/03.mp4"), Path("/home/pi/Miac/01.mp4")]

players = [0,0]

def play_video(videoNum):
##    players[videoNum].show_video()
##    players[videoNum].set_position(0.0)
##    players[videoNum].play()
    players[videoNum].load(VIDEO_PATHS[videoNum])
    
def pause_video(videoNum):
##    players[videoNum].pause()
##    players[videoNum].hide_video()
    players[videoNum].quit()
    
    
players[0] = OMXPlayer(VIDEO_PATHS[0], args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
sleep(3)
players[0].pause()
players[0].hide_video()


#player = OMXPlayer(VIDEO_PATH1,args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
#sleep(3)
#player.pause()
#sleep(2)
#player.hide_video()
players[1] = OMXPlayer(VIDEO_PATHS[1], args=['--no-osd', '--no-keys', '--win', '1000,0,1640,480'], dbus_name='org.mpris.MediaPlayer2.omxplayer2') #, '-b'
sleep(3)
players[1].pause()
players[1].hide_video()

## inizializzazione parametri per l'avvio per non far partire subito un video
adc_value = adc.read_adc(0, gain=GAIN) #valore del selettore al momento dell'accensione
pre_adc_value = adc_value

if adc_value > 16000:
    played_video = 0
elif adc_value < 16000:
    played_video = 1
    
while True:
    #    print("is open", omxc.poll())
    adc_value= adc.read_adc(0, gain=GAIN)
    if adc_value > 16000:
        playing_video = 0
    elif adc_value < 16000:
        playing_video = 1

##    if (omxc.poll()== None):
##        pre_adc_value = adc.read_adc(0, gain=GAIN)
##    else:
##        waitingVideo = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])

    if ((abs(adc_value - pre_adc_value)>1000) or (not playing_video == played_video)):
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