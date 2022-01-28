# check remaining storage (how?)
# if less than 5 GB, abort
# get the current datestamp and use for names
# record a 10-15 second video 
# snap 2 still images, one after the other
# don't use preview

import picamera
from datetime import datetime
from time import sleep

name = datetime.now().strftime("%Y%m%d_%H%M%S")

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.start_recording('/home/pi/flight_imaging/' + name + '.h264')
camera.wait_recording(15)
camera.stop_recording()
sleep(2)
# camera = picamera.PiCamera()
camera.resolution = (1024, 768)
sleep(2)
camera.capture('/home/pi/flight_imaging/' + name + '_1.jpg')
sleep(2)
camera.capture('/home/pi/flight_imaging/' + name + '_2.jpg')
