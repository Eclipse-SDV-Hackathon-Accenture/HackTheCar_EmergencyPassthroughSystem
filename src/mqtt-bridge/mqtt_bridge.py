"""
Application to bridge communication between eCAL and MQTT
This is an intermediate solution to forward the communication information from eCAL middleware to MQTT

"""

import argparse
import json
import sys
from typing import Dict

import ecal.core.core as ecal_core
import paho.mqtt.client as mqtt
from ecal.core.publisher import StringPublisher
from ecal.core.subscriber import StringSubscriber

mqttClient = mqtt.Client("", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)


def on_connect(mqttClient, userdata, flags, returnCode):
    """
    Callback method on connect for MQTT connection

    :param mqttClient:
    :param userdata:
    :param flags:
    :param returnCode:
    :return:
    """

    print("Connected with result code " + str(returnCode))
    mqttClient.subscribe("#")


def on_message(mqttClient, userdata, msg):
    """
    MQTT Callback method on message receive

    :param mqttClient:
    :param userdata:
    :param msg:
    :return:
    """
    print(msg.topic + " " + str(msg.payload))

    pub = StringPublisher("MQTT_Message")
    pub.send(str(msg.payload))


def callback(topic_name, msg, time):
    """
    Callback function for eCAL topic

    :param topic_name:
    :param msg:
    :param time:
    :return:
    """
    print(topic_name + " " + msg)
    mqttClient.publish(topic_name, msg)


if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser(
        prog='MQTT-eCAL Bridge',
        description='Bridge application between eCAL and MQTT',
        add_help=True)

    parser.add_argument('--config-file', '-cf', type=argparse.FileType('r', encoding='UTF-8'), required=True,
                        help="Path to config file (JSON)")

    args = parser.parse_args()

    try:
        # Load configuration to a dictionary
        config: Dict = json.loads(args.config_file.read())
        # Close the file properly
        args.config_file.close()

        ecal_core.initialize(sys.argv, "MQTT Bridge")

        # Initialize Subscriber to a topic from eCAL
        sub = StringSubscriber("smallcar")

        # Initializ MQTT client
        mqttClient.on_connect = on_connect
        mqttClient.on_message = on_message
        mqttClient.username_pw_set(config["mqtt_user"], config["mqtt_password"])
        mqttClient.tls_set()
        mqttClient.connect(config["mqtt_host"], config["mqtt_port"], 60)

        # Set the Callback for eCAL
        sub.set_callback(callback)

        mqttClient.loop_forever()

    except KeyboardInterrupt:
        print("Existing System...")

    finally:
        # finalize eCAL API
        print("Finalize eCAL Core...")
        ecal_core.finalize()
