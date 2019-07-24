import RPi.GPIO as GPIO
import time
from random import randint
from subprocess import Popen, PIPE
import os
import sys
import Adafruit_ADS1x15
import logging

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
logger = logging.getLogger(__name__)

class Player:
    def __init__(self, movie):
        self.movie = movie
        self.process = None

    def start(self):
        self.stop()
        self.process = Popen(['omxplayer','--win' , '1000,0,1640,480', self.movie], stdin=PIPE,
        stdout=open(os.devnull, 'r+b', 0), close_fds=True, bufsize=0)
        self.process.stdin.write("b") # start playing

    def stop(self):
        p = self.process
        if p is not None:
            try:
                p.stdin.write("q") # send quit command
                p.terminate()
                p.wait() # -> move into background thread if necessary
            except EnvironmentError as e:
                logger.error("can't stop %s: %s", self.movie, e)

noise = ("/home/pi/MIAC/00.mp4")
movies = ("/home/pi/MIAC/03.mp4", "/home/pi/MIAC/01.mp4")

first_player = Player(movie=movies[0])
second_player = Player(movie=movies[1])

second_player.start()
second_player.stop()


first_player.start()
print ("start the first/standard clip")

adc_value, pre_adc_value = 0, 0

while True:
    adc_value= adc.read_adc(0, gain=GAIN)
    if((first_player.process.poll() is not None) and (second_player.process.poll() is not None)):
            print ("restart flickering video")
            first_player.stop()
            second_player.stop()
            first_player.start()
    if(adc_value>16000): # change in state detected
        print ("state has changed")
        print ("scaring video played")
        if(second_player.process.poll() is not None):
            first_player.stop()
            second_player.start()
    state = i

    
#while True:
#       
#    if ((abs(adc_value - pre_adc_value)>1000)):
#        print('adc_value ',abs(adc_value - pre_adc_value))
#        pre_adc_value = adc_value
#        input_states[0] = not input_states[0]
#        input_states[1] = not input_states[1]
#        if adc_value > 16000:
#            input_states[0] = False
#            input_states[1] = True
#            player = playMov(0)
#        elif adc_value < 16000:
#            input_states[1] = False
#            input_states[0] = True
#            player = playMov(1)
##        #else: quit_video = False
##        for x in range(len(last_states)):
##            #If video1Pin is shorted to ground
##            if input_states[x] != last_states[x]:
##                if (player and not input_states[x]):
##                    os.system('killall omxplayer.bin')
##                    omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , movies[x]]) #'omxplayer', '--win 0,0,640,480', movie1])
##                    player = True
##                elif not input_states[x]:
##                    omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , movies[x]]) #'omxplayer', '--win 0,0,640,480', movie1])
##                    player = True
###            if not player:
###                omxc = Popen(['omxplayer', '--win' , '1000,0,1640,480' , noise]) 
##            #quit_video to close omxplayer manually - used during debug
##            if quit_video == False:
##                os.system('killall omxplayer.bin')
##                player = False
##
##            
##            #Set last_input states
##            last_states[x] = input_states[x]
#        print('player', player)
