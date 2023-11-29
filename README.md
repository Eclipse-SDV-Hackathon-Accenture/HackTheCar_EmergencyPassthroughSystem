# Emergency Passthrough System

The Emergency Passthrough System (EPS) is a revolutionary system designed to
enhance the response times of emergency vehicles in urban areas. By integrating
with autonomous vehicle technology, EPS ensures that autonomous vehicles receive
real-time signals from approaching emergency vehicles, enabling them to pull over
safely and quickly, thus clearing the path for emergencies.

## Table of Content

- [Emergency Passthrough System](#emergency-passthrough-system)
  - [Table of Content](#table-of-content)
  - [Components](#components)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [System Flow](#system-flow)
  - [License](#license)

## Components

For the EPS system, we designed the system with the following architecture

<p align="center">
  <img src="https://github.com/Eclipse-SDV-Hackathon-Accenture/HackTheCar_EmergencyPassthroughSystem/assets/20866800/9e353710-acb6-45b7-b0aa-7997b84407dd" alt="eps_system"/>
</p>

With this architecture we have multiple components, that are connected in the
modular way using eCAL middleware.

EPS consists of two main components:

* EPS Controller
  This component subscribes to the ROS Global Position topic to receive location
  data and uses eCAL for communication. It calculates the distance of each vehicle
  from a set location and determines whether to send a signal to autonomous vehicles
  to move aside.

* MQTT Bridge
  This application bridges the communication between eCAL and MQTT, transmitting
  messages received from the EPS Controller to an MQTT broker.

## Prerequisites

* Python >= 3.8
* [eCAL](https://eclipse-ecal.github.io/ecal/index.html)

## Installation

> [!NOTE]  
> To start the project, make sure that you installed [eCAL](https://eclipse-ecal.github.io/ecal/getting_started/setup.html).

```shell
# Clone the repository
git clone https://github.com/Eclipse-SDV-Hackathon-Accenture/HackTheCar_EmergencyPassthroughSystem 

# Change directory
cd HackTheCar_EmergencyPassthroughSystem

# Creating python virtual enviroment
python -m venv .venv

# Run the virtual environment
# Linux
source .venv/bin/activate

# Windows
source .venv\Scripts\activate

# Installing dependency
pip install .
```

## Usage

* EPS Controller

  This script initializes a subscriber that listens to the "ROSGlobalPosition"
  topic from eCAL and a publisher that sends signal after calculation to the MQTT
  Bridge compoent, that works as a Vehicle to Vehicle communication (V2V) to the
  small autonomous car.

  Run the EPS Controller:

  ```shell
  # Observing Possibilities
  python src/controller/eps_controller.py --help

  # Help information
  usage: EmergencyPassthroughSystem [-h] --config-file CONFIG_FILE [--record-result]

  Core Logic Algorithm for Emergency Passthrough System

  optional arguments:
    -h, --help            show this help message and exit
    --config-file CONFIG_FILE, -cf CONFIG_FILE
    --record-result, -r
  ```

  The script requires a mandatory argument for the path to the config file. The
  configuration file will be used to configure the distance threshold and position
  of the small car in latitude and longitude value.

  ```json
  {
    "longitude": 11.602926,
    "latitude": 48.117599,
    "distance_threshold": 10.0
  }
  ```

  The typical usage to the script is following:

  ```shell
  python eps_controller.py --config-file <path/to/config/file> -r
  ```

  

* MQTT Bridge
  Run the MQTT Bridge:
  
  ```shell
  python src/mqtt-bridge/mqtt_bridge.py
  ```

  MQTT bridge componet act as vehicle to vehicle communication software, that
  interacts with eCAL and MQTT broker, where the small autonomous car receives
  the trigger to create rescue lane.
  This software subscribes particular signal from eCAL and forwards directly to
  the provided MQTT broker.

## System Flow

The EPS Controller receives GPS data from autonomous vehicles.
It calculates the distance to a predefined emergency location.
If an autonomous vehicle is within a specified range, it sends a signal to that
vehicle to move aside. The MQTT Bridge forwards these messages to the MQTT broker
for broader dissemination or integration with other systems.

## License

Copyright (c) 2023 - present, Lace Labs at SDV Hackathon
