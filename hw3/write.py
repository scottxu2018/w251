import paho.mqtt.client as mqtt
import cv2
import numpy as np
from datetime import datetime

broker="10.187.64.5"
port=1883
mqtt_local = mqtt.Client("write")

def on_connect(client, userdata, flags, rc):
  print("Connected with local "+str(rc))
  client.subscribe("face")

def on_message(client, userdata, message):
  print("receive msg")
  #print(message.payload)
  #outfile = "/hw3/storage/face.txt"
  #f= open(outfile,"w+")
  #print("writing")
  #f.write("This is a msg")
  #f.close()
  #np_arr = np.fromstring(message, np.uint8)
  outfile = '/hw3/storage/face_%s.jpg' % str(datetime.now())
  print(outfile)
  image = np.asarray(bytearray(message.payload), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 # cv2.imshow('img_decode',image)
 # cv2.waitKey() 
 # nparr = np.fromstring((message.payload, np.uint8))
 # img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
  cv2.imwrite(outfile, image)
  print("writing")  

mqtt_local.connect(broker, port)
#mqtt_local.connect(cloud,port)
#mqtt_local.publish("image",payload = "test")
mqtt_local.on_connect = on_connect
mqtt_local.on_message = on_message
mqtt_local.loop_forever()

