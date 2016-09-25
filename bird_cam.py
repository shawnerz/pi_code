#***************************************************************#
# This code is to use a Raspberry Pi as a Wildlife Camera.     	#
# A Passive Infrared (PIR) sensor and Pi Camera is to be       	#
# connected to the Pi. The PIR sensor is supposed to be		#
# connected to GP17 (a.k.a. GPIO11). When tripped, the camera	#
# is instructed to take a picture.				#
#								#
# If you're running recent firmware, add the following to       #
# /boot/config.txt to turn off camera LED                       #
#                                                               #
# disable_camera_led=1                                          #
#                                                               #
# SRC 25 Sep 2016
#***************************************************************#
import RPi.GPIO as GPIO
import time
import sensor
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

camera = PiCamera()     #Camera initialization
#camera.rotation = 180	#Uncomment to rotate if camera or Pi is upside-down
picture_count = 0	#picture counter
max_picture_count = 400 #Keeps from filling the SD card with pictures

def snapshot(count):
    camera.awb_mode = 'auto'
    camera.capture('/home/pi/bird_pics/bird%s.jpg' % count)
    sleep(4)
    
while True:
    i=GPIO.input(11)
    if i==0:
	#print ("No birds detected"),i #optional debug code
        time.sleep(1)
    elif i ==1:
        if picture_count < max_picture_count:
            #print ("Bird detected! Taking picture.") #optional debug code
            snapshot(picture_count)
            picture_count += 1 #Increments picture counter

        else:
            exit(0) # Picture count exceeded; exiting
        
