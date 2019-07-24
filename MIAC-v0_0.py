import RPi.GPIO as GPIO
import os
from subprocess import Popen, PIPE
import Adafruit_ADS1x15

def function():
    global omxc
    global noiseVideo

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

noise = ("/home/pi/MIAC/staticNoise.mp4")
movies = ("/home/pi/MIAC/Video/BIANCOROSSOVERDONE_1taglio.mp4", "/home/pi/MIAC/Video/SIGNORE_E_SIGNORI_1taglio.mp4")


# inizializzazione parametri per l'avvio per non far partire subito un video
adc_value = adc.read_adc(0, gain=GAIN) #valore del selettore al momento dell'accensione
pre_adc_value = adc_value

if adc_value > 16000:
    played_video = 0
elif adc_value < 16000:
    played_video = 1
    
#omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise])  #video di partenza
omxc = Popen(['omxplayer', '-o', 'local','--win' , '1000,0,1640,480' , movies[played_video]])
noiseVideo = Popen(['omxplayer', '--alpha', '255','--win' , '1000,0,1640,480' , noise])

while True:
#    print("is open", omxc.poll())
    adc_value= adc.read_adc(0, gain=GAIN)
    if adc_value > 16000:
        play_video = 0
    elif adc_value < 16000:
        play_video = 1

    if (omxc.poll()== None):
#        adcnow = adc.read_adc(0, gain=GAIN)
#        print('preADC ', pre_adc_value,' - adc ', adcnow)
        if ((abs(adc_value - adc.read_adc(0, gain=GAIN))>50) and (not noiseVideo.poll()==None)):
            noiseVideo = Popen(['omxplayer','-o', 'local', '--vol', ' -4500', '--alpha', '55','--win' , '1000,0,1640,480' , noise], stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        pre_adc_value = adc.read_adc(0, gain=GAIN)

    if ((abs(adc_value - pre_adc_value)>1000) or (not play_video == played_video)):
        print("adc_value",adc_value - pre_adc_value)
        if (omxc.poll()== None):
            #omxc.stdin.write("q")
            os.system('killall omxplayer.bin')
        if adc_value > 16000:
            played_video = 0
            omxc = Popen(['omxplayer',  '-o', 'local','--win' , '1000,0,1640,480' , movies[0]],stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        elif adc_value < 16000:
            played_video = 1
            omxc = Popen(['omxplayer',  '-o', 'local','--win' , '1000,0,1640,480' , movies[1]],stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        pre_adc_value = adc_value
    
    
    acd_value_end = adc.read_adc(0, gain=GAIN)
