import numpy as np
import cv2
import os
import paho.mqtt.client as mqtt

broker="192.168.1.5"
#broker = "52.117.209.19"
port=1883
mqttc = mqtt.Client("detector") 
#print("hello")
cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FOURCC,cv2.CV_FOURCC('M', 'J', 'P', 'G'))
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
#face_cascade.load('haarcascade_frontalface_default.xml')
while(cv2.waitKey(10) != 27):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("frame")
    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0 :
	print("1")
	mqttc.connect(broker,port)
	mqttc.publish("face", payload = np.array(cv2.imencode('.jpg', gray)[1]).tostring())
