import RPi.GPIO as GPIO
import os
import sys
from subprocess import Popen
import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2

noise = ("/home/pi/MIAC/00.mp4")
movies = ("/home/pi/MIAC/03.mp4", "/home/pi/MIAC/01.mp4")

#omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])  #video di partenza
omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])
# waitingVideo = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])
# inizializzazione parametri per l'avvio per non far partire subito un video
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
        play_video = 0
    elif adc_value < 16000:
        play_video = 1

    if (omxc.poll()== None):
        pre_adc_value = adc.read_adc(0, gain=GAIN)
    #else:
        #waitingVideo = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])

    if ((abs(adc_value - pre_adc_value)>1000) or (not play_video == played_video)):
        print("adc_value",adc_value - pre_adc_value)
        if (omxc.poll()== None):
            os.system('killall omxplayer.bin')
        if adc_value > 16000:
            played_video = 0
            omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , movies[0]])
        elif adc_value < 16000:
            played_video = 1
            omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , movies[1]])
        pre_adc_value = adc_value
