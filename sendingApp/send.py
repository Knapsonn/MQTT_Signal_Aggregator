import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random 
import time

def on_connect(client,userdata,flags,rc):
    if rc ==0:
        print("Connection succesfull!")
    else:
        print("Connection error!" + str(rc))

#Parameters for MQTT Broker
mqtt_broker = "mqtt"
mqtt_port = 1883

#Configuration of mqtt broker
client = mqtt.Client("Sender")

client.on_connect = on_connect

client.connect(mqtt_broker, mqtt_port,60)

while True: 

    rand_float = random.uniform(0.01,999.99)
    rand_float = round(rand_float,2)
    now = datetime.now()

    payload = {
        "time": str(now),
        "value": rand_float,
        "unit" : "V"
    }

    json_payload = json.dumps(payload)

    time.sleep(1)
    client.publish("measurements",json_payload,0)


