#from picamera import PiCamera
#from time import sleep

#camera = PiCamera()

#camera.start_preview()
#sleep(10)
#camera.stop_preview()


from picamera.array import PiRGBArray
from picamera import PiCamera
from pprint import pprint
import time
import sys
import cv2
import RPi.GPIO as GPIO 
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) 
GPIO.setup(15, GPIO.OUT)


c = 261
d = 294
r = 1
p = GPIO.PWM(15, 100)


def Blink(numTimes, speed):
    for i in range(0,numTimes):
        print('Alarm Running')
        GPIO.output(7, True) 
        GPIO.output(15, True) 
        time.sleep(speed) ## Wait
        p.start(100)             # start the PWM on 100  percent duty cycle  
        p.ChangeDutyCycle(90)   # change the duty cycle to 90%  
        p.ChangeFrequency(c)  # change the frequency to 261 Hz (floats also work)  
        time.sleep(speed) ## Wait
        p.ChangeFrequency(d)  # change the frequency to 294 Hz (floats also work)  
        time.sleep(speed) ## Wait
        p.stop()                # stop the PWM output  
        print('Alarm Running')

iterations = 1
speed = 0.5


# initialize the camera and grab a reference to the raw camera capture
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.2.0/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.2.0/data/haarcascades/haarcascade_eye.xml')

SleepStatus = 0
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(320,240))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	img = frame.array
	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30,30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        SleepStatus = 0
        for (x,y,w,h) in faces:

            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)#
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                SleepStatus = 1
            if SleepStatus == 1:
                print('Driver Awake')
                SleepStatus = 0
            else:
                print('Driver Sleeping... Alarm Started')
                SleepStatus = 0
                Blink(int(iterations),float(speed))
                print('Alarm Stopping..')
                
                    
        cv2.imshow('img',img)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
