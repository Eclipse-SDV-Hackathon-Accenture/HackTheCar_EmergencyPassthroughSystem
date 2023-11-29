import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar()

def move_away(config):
    print("move away")
    car.throttle = config['throttle']

    for i in range(0,20):
        if (config['direction'] == "right"):
            if (i > 5):
                print("move to normal")
                if(car.steering < 0):
                    car.steering += 0.1
            else:
                print("move right")
                car.steering -= 0.1
        else:
            if (i > 5):
                print("move to normal")
                if(car.steering > 0):
                    car.steering -= 0.1
            else:
                print("move left")
                car.steering += 0.1
        time.sleep(0.5)

    car.throttle = 0.0
    car.steering = 0.0

with open("smallcar.config") as f:
    config = json.load(f)
    move_away(config);
