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

# this audio is used only to mantain a black screen
##AUDIO_PATH00 = Path("/home/pi/Miac/Audio/01.mp3")
##player00 = OMXPlayer(AUDIO_PATH00, args= '-b')
##player00.pause()
##player00.hide_audio()
##sleep(1)

AUDIO_PATHS = [Path("/home/pi/Miac/Audio/01.mp3"), Path("/home/pi/Miac/Audio/02.mp3"),Path("/home/pi/Miac/Audio/03.mp3"), Path("/home/pi/Miac/Audio/04.mp3")]
NOISE_PATH = Path("/home/pi/Miac/Audio/staticNoise.mp3") #non più lungo di 1 secondo!

#initialization of players
players = [0,0,0,0]

something_playing = False

def play_audio(audioNum):
##    players[audioNum].show_audio()
##    players[audioNum].set_position(0.0)
##    players[audioNum].play()
    players[audioNum].load(AUDIO_PATHS[audioNum])
    
def pause_audio(audioNum):
##    players[audioNum].pause()
##    players[audioNum].hide_audio()
    players[audioNum].quit()
    
#start the first audio and hide 
players[0] = OMXPlayer(AUDIO_PATHS[0], args=['-o',  'both'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
sleep(2)
players[0].quit()

players[1] = OMXPlayer(AUDIO_PATHS[1], args=['-o',  'both'], dbus_name='org.mpris.MediaPlayer2.omxplayer2') #, '-b'
sleep(2)
players[1].quit()

players[2] = OMXPlayer(AUDIO_PATHS[2], args=['-o',  'both'], dbus_name='org.mpris.MediaPlayer2.omxplayer3') #, '-b'
sleep(2)
players[2].quit()

players[3] = OMXPlayer(AUDIO_PATHS[3], args=['-o',  'both'], dbus_name='org.mpris.MediaPlayer2.omxplayer4') #, '-b'
sleep(2)
players[3].quit()

## inizializzazione parametri per l'avvio per non far partire subito un audio
adc_value = adc.read_adc(0, gain=GAIN) #valore del selettore al momento dell'accensione
pre_adc_value = adc_value

if adc_value > 0:
    played_audio = 0
    if adc_value > 6000:
        played_audio = 1
        if adc_value > 12000:
            played_audio = 2
            if adc_value > 18000:
                played_audio = 3
print("first played_audio ",played_audio)
                
while True:
    #update adc value
    adc_value= adc.read_adc(0, gain=GAIN)
    if adc_value > 0:
        playing_audio = 0
        if adc_value > 8000:
            playing_audio = 1
            if adc_value > 16000:
                playing_audio = 2
                if adc_value > 24000:
                    playing_audio = 3
    
    #if a audio is playing update the pre_adc_value
    try:
        if (players[playing_audio].can_play()):
            if ((abs(adc_value - adc.read_adc(0, gain=GAIN))>200) ):
                noiseplay = OMXPlayer(NOISE_PATH, args=['-o',  'both'])
                #sistemare la ripetizione del noise sovrapposta
            pre_adc_value = adc.read_adc(0, gain=GAIN)
            something_playing = True
        else:
            something_playing = False
    except:
        something_playing = False
    
##    print("played_audio ",played_audio, " | playing_audio ", playing_audio, " | something_playing ", something_playing)
                
    # se il audio non sta andando e si muove il cursore di 500 o si passa all'altro audio
    if (((not something_playing) and (abs(adc_value - pre_adc_value)>500)) or (not playing_audio == played_audio)):
        print("adc_value",adc_value)
        players[played_audio].quit()
        #noiseplay.quit()
        play_audio(playing_audio)
        pre_adc_value = adc_value
        played_audio = playing_audio