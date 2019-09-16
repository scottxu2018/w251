import paho.mqtt.client as mqtt
#import os

broker="192.168.1.5"
port=1883
mqtt_local = mqtt.Client("forwarder")

cloud = "52.117.209.19"

mqtt_cloud = mqtt.Client("remote")
#while(1):
def on_connect(client, userdata, flags, rc):
  print("Connected with local "+str(rc))
  client.subscribe("face")

def on_connect_remote(client, userdata, flags, rc):
  print("Connected with cloud " +str(rc))

def on_message(client, userdata, message):
  print("receive msg")
   #print("connected with cloud")
  mqtt_cloud.publish("face", payload =message.payload) 
  print("publish")
  #client.disconnect()
  #msg_queue.append(message.payload)
  #print(len(msg_queue))

msg_queue =[]
try:
  mqtt_local.connect(broker, port)
  mqtt_cloud.connect(cloud,port)
except:
  print("Failed to connect")

mqtt_local.on_connect = on_connect
#mqtt_cloud.on_connect = on_connect_remote
mqtt_local.on_message = on_message
#print("finish get msg")
#for x in range(len(msg_queue)):
#  print("publish")
#  mqtt_cloud.publish("face", msg_queue.pop())

mqtt_local.loop_forever()
#mqtt_cloud.loop_forever()
