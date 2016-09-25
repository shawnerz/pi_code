import RPi.GPIO as GPIO
import time
import sensor
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)


#***************************************************************#
# If you're running recent firmware, add the following to     	#
# /boot/config.txt to turn off camera LED                	#
#								#
# disable_camera_led=1						#
#								#
#***************************************************************#

camera = PiCamera()     #Camera initialization

#camera.rotation = 180	#Uncomment to rotate if camera or Pi is upside-down
picture_count = 0	#picture counter


def snapshot(count):
    camera.awb_mode = 'sunlight'
    camera.capture('/home/pi/bird_pics/bird%s.jpg' % count)
    sleep(4)
    
while True:
    i=GPIO.input(11)
    if i==0:
	#print ("No birds detected"),i optional debug code
        time.sleep(1)
    elif i ==1:
        if picture_count < 400: #Arbitrarily set to 400 to keep from filling SD card.
            #print ("Bird detected! Taking picture.") optional debug code
            snapshot(picture_count)
            picture_count += 1 #Increments picture counter

        else:
            exit(0) # Picture count exceeded; exiting
        
