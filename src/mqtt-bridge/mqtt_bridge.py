"""
Application to bridge communication between eCAL and MQTT

"""

import sys

import ecal.core.core as ecal_core
import paho.mqtt.client as mqtt
from ecal.core.publisher import StringPublisher
from ecal.core.subscriber import StringSubscriber

mqttClient = mqtt.Client("", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

def on_connect(mqttClient, userdata, flags, rc):
    """
    Callback method 
    """

    print("Connected with result code " + str(rc))
    mqttClient.subscribe("#")


def on_message(mqttClient, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
    pub = StringPublisher("MQTT_Message")
    pub.send(str(msg.payload))


def callback(topic_name, msg, time):
    print(topic_name + " " + msg)
    mqttClient.publish(topic_name, msg)
    mqttClient.publish


if __name__ == "__main__":
    ecal_core.initialize(sys.argv, "MQTT Bridge")

    sub = StringSubscriber("hello_mqtt")

    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.username_pw_set("", "")
    mqttClient.tls_set()
    mqttClient.connect("5e57e5cfb02f468ba5e49adade286f4b.s1.eu.hivemq.cloud", 8883, 60)

    # Set the Callback
    sub.set_callback(callback)

    mqttClient.loop_forever()

    # finalize eCAL API
    ecal_core.finalize()
