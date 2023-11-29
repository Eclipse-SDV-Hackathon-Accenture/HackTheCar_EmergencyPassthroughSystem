import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar()

print("Init done ...")
print(car.throttle_gain)
print(car.throttle)
print("go")

car.throttle = 0.2
car.throttle_gain += 0.1

print(car.throttle_gain)
print(car.throttle)
time.sleep(1)

car.throttle = 0.0

print("stop")
print(car.throttle_gain)
print(car.throttle)
time.sleep(1)
print("go")

car.throttle = 0.2

print(car.throttle_gain)
print(car.throttle)
time.sleep(1)


##for i in range(0,10):
##    car.steering += 0.1
##    car.throttle_gain += 0.1
##    time.sleep(0.1)

##for i in range(0,10):
##    car.steering -= 0.1
##    time.sleep(0.1)

##print(car.throttle_gain)
##print(car.throttle)
car.throttle = 0.0



