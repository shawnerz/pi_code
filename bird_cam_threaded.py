#***************************************************************#
# This code is to use a Raspberry Pi as a Bird Camera.     		#
# Since birds are primarly active from about 6 AM to 6 PM, the  #
# camera is only enabled during that time. If you're going to   #
# use this as a wildlife or trail camera and plan to take       #
# nightime pictures with an IR illuminator, then remove or      #
# comment out the hour check 'if' statement.                    #
# A Passive Infrared (PIR) sensor and Pi Camera is to be       	#
# connected to the Pi. The PIR sensor is supposed to be			#
# connected to GP17 (a.k.a. GPIO11). When tripped, the camera	#
# is instructed to take a picture.								#
#																#
# If you're running recent firmware, add the following to       #
# /boot/config.txt to turn off camera LED                       #
#                                                               #
# disable_camera_led=1                                          #
#                                                               #
# SRC 4 Oct 2016												#
# DKN 11 Oct added thread to see if it alleviates drag on system#
#***************************************************************#

import RPi.GPIO as GPIO
import time, datetime, sensor
from threading import Thread
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

camera = PiCamera()     #Camera initialization
#camera.rotation = 180	#Uncomment to rotate if camera or Pi is upside-down
picture_count = 0	#picture counter
max_picture_count = 400	#Keeps from filling the SD card with pictures
start_hour = 6          #Hour to start taking pictures
end_hour = 18           #Hour to stop taking pictures
current_hour = 0        #Initial hour value
global flag		#Flag to let thread and main know when max count has been reached
flag = True		#Only way to set a var as global. Tell it it's global wherever you use it

def snapshot(count):
    camera.awb_mode = 'auto'
    camera.capture('/home/pi/bird_pics/bird%s.jpg' % count)
    #print "called snapshot %d" % count
    time.sleep(4)

def doWork(picture_count, max_picture_count, start_hour, end_hour):
	global flag	
	while flag:
		i=GPIO.input(11)		
		current_hour = datetime.datetime.now().time().hour
		if current_hour >= start_hour and current_hour < end_hour:
			if i == 0:
				#print ("No birds detected"),i #optional debug code
				time.sleep(1)
			elif i == 1:
				if picture_count < max_picture_count:
					#print ("Bird detected! Taking picture.") 	#optional debug code
					snapshot(picture_count)
					picture_count += 1 #Increments picture counter
					print "incremented picture_count %d" % picture_count
		time.sleep(60)
		if (picture_count >= max_picture_count):
			flag=False
			print "Max picture count reached."
	
	
##  The "main" part of the program.  Using daemon=True allows the thread to be interrupted with ^c when you want to kill it
t = Thread(target=doWork, args=(picture_count,max_picture_count,start_hour, end_hour,))
t.daemon = True
t.start()

# allow the thread to run until you kill it or until max picture count is reached.
while True:
   time.sleep(10)
   if flag == False:
	print "Ending bird_cam program "
	break


