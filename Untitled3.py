#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import RPi.GPIO as GPIO
import time                              

body_cascade = cv2.CascadeClassifier(r'''home/pi/Downloads/haarcascade_fullbody.xml''')
u_body_cascade=cv2.CascadeClassifier(r'''home/pi/Downloads/haarcascade_upperbody.xml''')
TRIG1 = 22
ECHO1 = 27

TRIG2 = 9
ECHO2 = 10

TRIG3 = 15
ECHO3 = 14

def initm():
    gpio.setmode(gpio.BCM)
    gpio.setup(2, gpio.OUT)
    gpio.setup(3, gpio.OUT)
    gpio.setup(4, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    
def inits():
    GPIO.setup(TRIG1,GPIO.OUT)              
    GPIO.setup(ECHO1,GPIO.IN)               

    GPIO.setup(TRIG2,GPIO.OUT)              
    GPIO.setup(ECHO2,GPIO.IN)                  

    GPIO.setup(TRIG3,GPIO.OUT)      
    GPIO.setup(ECHO3,GPIO.IN)      

def turnL(sec):
    initm()
    gpio.output(2, False)
    gpio.output(3, False)
    gpio.output(4, False) 
    gpio.output(17, True)
    time.sleep(sec)

def turnR(sec):
    initm()
    gpio.output(2, False)
    gpio.output(3, True)
    gpio.output(4, False) 
    gpio.output(17, False)
    time.sleep(sec)
    
def reverse(sec):
    initm()
    gpio.output(2, False)
    gpio.output(3, True)
    gpio.output(4, False) 
    gpio.output(17, True)
    time.sleep(sec)

GPIO.setmode(GPIO.BCM)     

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))         

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="gray", use_video_port=True):
    
    image = frame.array
    bodies = body_cascade.detectMultiScale(image, 1.3, 5)
    u_bodies = u_body_cascade.detectMultiScale(image, 1.1, 5)
    
    if bodies or u_bodies:
        break
    
    initm()
    gpio.output(2, True)
    gpio.output(3, False)
    gpio.output(4, True) 
    gpio.output(17, False)
    
    inits()
    GPIO.output(TRIG1, False)  
    GPIO.output(TRIG2, False)  
    GPIO.output(TRIG3, False)
    time.sleep(0.5)                            
    GPIO.output(TRIG1, True)
    GPIO.output(TRIG2, True)
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)   
    GPIO.output(TRIG2, False)  
    GPIO.output(TRIG3, False) 
    
    while GPIO.input(ECHO1)==0:              
        pulse_start1 = time.time()      
    while GPIO.input(ECHO1)==1:             
        pulse_end1 = time.time()                
    pulse_duration1 = pulse_end1 - pulse_start1
    
    while GPIO.input(ECHO2)==0:              
        pulse_start2 = time.time()      
    while GPIO.input(ECHO2)==1:             
        pulse_end2 = time.time()                
    pulse_duration2 = pulse_end2 - pulse_start2
    
    while GPIO.input(ECHO3)==0:              
        pulse_start3 = time.time()      
    while GPIO.input(ECHO3)==1:             
        pulse_end3 = time.time()                
    pulse_duration3 = pulse_end3 - pulse_start3
    
    distance1 = pulse_duration1 * 17150       
    distance1 = round(distance1, 2)
    
    distanceR = pulse_duration2 * 17150       
    distanceR = round(distanceR, 2)
    
    distanceL = pulse_duration3 * 17150       
    distanceL = round(distanceL, 2)
    
    if distance1 < 7:
        reverse(3)
        turnR(1)
        gpio.cleanup() 
        continue
    if distanceR < 7:
        turnL(1)
        gpio.cleanup() 
        continue
    if distanceL < 7:
        turnR(1)
        gpio.cleanup()
        continue
    gpio.cleanup()

