import time
import json
import paho.mqtt.client as mqtt

from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar() 
car.throttle = 0.0
car.throttle_gain += 0.1

config = ''

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("smallcar")
    print("config readed - throttle:" + str(config['throttle']) + ", direction:" + config['direction'])
    
# The callback for when a PUBLISH message is received from the server.
# {"move":"off", "left":"on","right":"off"}
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(msg.topic+" "+payload)
    if payload != "":
        json.dumps(payload)
        data = json.loads(payload)
        if data['move'] == 'on':
            move_away()         
        if data['move'] == 'off':
            print("move off")
            car.throttle = 0.0

            
def move_away():
    print("move away")
    car.throttle = config['throttle']  
    
    for i in range(0,10):
        if (config['direction'] == "right"):             
            car.steering -= 0.1
        else:
            car.steering += 0.1
        time.sleep(0.5)

    car.throttle = 0.0
    car.steering = 0.0
    
    
client = mqtt.Client("", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.username_pw_set("sdv_ecal","SDV_ecal123")
client.connect("5e57e5cfb02f468ba5e49adade286f4b.s1.eu.hivemq.cloud", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

with open("smallcar.config") as f:
    config = json.load(f)
    
client.loop_forever()
   


