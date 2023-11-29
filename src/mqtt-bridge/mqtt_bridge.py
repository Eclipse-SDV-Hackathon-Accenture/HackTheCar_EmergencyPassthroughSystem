"""
Application to bridge communication between eCAL and MQTT

"""

import sys

import ecal.core.core as ecal_core
import paho.mqtt.client as mqtt
from ecal.core.publisher import StringPublisher
from ecal.core.subscriber import StringSubscriber

client = mqtt.Client("", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

def on_connect(client, userdata, flags, rc):
    """
    Callback method 
    """

    print("Connected with result code " + str(rc))

    client.subscribe("#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    pub = StringPublisher("MQTT_Message")

    pub.send(str(msg.payload))


def callback(topic_name, msg, time):
    print(msg)
    client.publish(topic_name, msg)
    client.publish


if __name__ == "__main__":
    ecal_core.initialize(sys.argv, "MQTT Bridge")

    sub = StringSubscriber("hello_mqtt")

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("", "")
    client.tls_set()
    client.connect("5e57e5cfb02f468ba5e49adade286f4b.s1.eu.hivemq.cloud", 8883, 60)

    # Set the Callback
    sub.set_callback(callback)

    client.loop_forever()

    # finalize eCAL API
    ecal_core.finalize()
