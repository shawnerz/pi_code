#***************************************************************#
# This code is to use a Raspberry Pi as a Bird Camera.     	#
# Since birds are primarly active from about 6 AM to 6 PM, the  #
# camera is only enabled during that time. Change start_hour	#
# and end_hour for your local needs.				#
# If you're going to use this as a wildlife or trail camera and #
# plan to take nightime pictures with an IR illuminator, then	#
# remove or comment out the hour check 'if' statement.          #
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
# SRC 24 Oct 2016						#
#***************************************************************#
import RPi.GPIO as GPIO
import time, datetime
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

camera = PiCamera()     #Camera initialization
#camera.rotation = 180	#Uncomment to rotate if camera or Pi is upside-down
picture_count = 0	#picture counter
max_picture_count = 400 #Keeps from filling the SD card with pictures
start_hour = 6          #Hour to start taking pictures
end_hour = 19           #Hour to stop taking pictures
current_hour = 0        #Initial hour value

def snapshot(count):
    camera.awb_mode = 'auto'
    camera.capture('/home/pi/bird_pics/bird%s.jpg' % count)
    sleep(4)
    
while True:
    i=GPIO.input(11)
    current_hour = datetime.datetime.now().time().hour
    if current_hour >= start_hour and current_hour < end_hour:
        
        if i == 0:
	#print ("No birds detected"),i #optional debug code
            time.sleep(1)
        elif i == 1:
            if picture_count < max_picture_count:
                #print ("Bird detected! Taking picture.") #optional debug code
                snapshot(picture_count)
                picture_count += 1 #Increments picture counter

            else:
                exit(0) # Picture count exceeded; exiting program
        
    else:
        sleep(60)	# This is executed if it's not time to take to take 
			# pictures.
