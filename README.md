# HackTheCar_EmergencyPassthroughSystem

Architecture Diagram:

![hackathon_architecture](https://github.com/Eclipse-SDV-Hackathon-Accenture/HackTheCar_EmergencyPassthroughSystem/assets/7806017/c0a85f3d-268b-4035-a3ae-340ed8430583)


Overview

The Emergency Passthrough System (EPS) is a revolutionary system designed to enhance the response times of emergency vehicles in urban areas. By integrating with autonomous vehicle technology, EPS ensures that autonomous vehicles receive real-time signals from approaching emergency vehicles, enabling them to pull over safely and quickly, thus clearing the path for emergencies.
Components

EPS consists of two main components:

    EPS Controller: This component subscribes to the ROS Global Position topic to receive location data and uses eCAL for communication. It calculates the distance of each vehicle from a set location and determines whether to send a signal to autonomous vehicles to move aside.

    MQTT Bridge: This application bridges the communication between eCAL and MQTT, transmitting messages received from the EPS Controller to an MQTT broker.

Installation

    Prerequisites:
        Python 3.x
        eCAL
        geopy
        pandas
        paho-mqtt
        ROS (Robot Operating System)

    Clone the Repository:

    bash

git clone https://github.com/yourrepository/EmergencyPassthroughSystem.git

Install Dependencies:

    Install the required Python packages:

        pip install ecal geopy pandas paho-mqtt

Usage
EPS Controller

    Run the EPS Controller:

    python eps_controller.py

        This script initializes a subscriber that listens to the "ROSGlobalPosition" topic and a publisher that sends signals to small autonomous cars.

MQTT Bridge

    Configure MQTT Settings:
        Edit mqtt_bridge.py to set your MQTT broker details.

    Run the MQTT Bridge:

    python mqtt_bridge.py

        This script subscribes to the "smallcar" topic and forwards messages to the configured MQTT broker.

System Flow

    The EPS Controller receives GPS data from autonomous vehicles.
    It calculates the distance to a predefined emergency location.
    If an autonomous vehicle is within a specified range, it sends a signal to that vehicle to move aside.
    The MQTT Bridge forwards these messages to the MQTT broker for broader dissemination or integration with other systems.
