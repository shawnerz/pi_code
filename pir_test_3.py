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
picture_count = 0       #number of pictures taken

def snapshot(count):
    camera.awb_mode = 'sunlight'
    camera.capture('/home/pi/bird_pics/bird%s.jpg' % count)
    sleep(4)
    
while True:
    i=GPIO.input(11)
    if i==0:
        print ("No birds detected"),i
        time.sleep(1)
    elif i ==1:
        if picture_count < 100: #Arbitrarily set to 100 to keep from filling SD card.
            print ("Bird detected! Taking picture.")
            snapshot(picture_count)
            picture_count += 1 #Increments picture count

        else:
            print ("Bird detected but picture count exceeded. Not taking picture.")
        #time.sleep(5)
        
