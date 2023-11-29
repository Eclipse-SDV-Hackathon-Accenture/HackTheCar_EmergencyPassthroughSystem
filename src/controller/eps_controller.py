"""
The 'eps_controller.py' contains the main logic of the distance calculation between the ego car to the other vehicle
based on the gps location.
This act as a 'core' function software that will integrated into an ECU.

The core logic receives the GPS location from the ego vehicle, that is transferred using eCAL middleware in the format
of NavSatFix.
For detailed information of NavSatFix data type, please refer to
https://github.com/Eclipse-SDV-Hackathon-Accenture/hack-the-car/blob/main/datatypes/ros/sensor_msgs/NavSatFix.proto
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from typing import Union, Tuple, Dict

import ecal.core.core as ecal_core
import geopy.distance
import pandas as pd
from ecal.core.publisher import StringPublisher
from ecal.core.subscriber import ProtoSubscriber
from ros.sensor_msgs.NavSatFix_pb2 import NavSatFix

# Initialize the DataFrame outside of the callback
distances = pd.DataFrame(columns=['time', 'latitude', 'longitude', 'distance'])
call_count: int = 0
start_time: datetime = datetime(2023, 11, 30, 12, 0, 0)  # November 30, 2023, at 12 PM

# Initialize the publisher object to None.
# The main purpose of this global variable is to preserved global variable, that will be overwritten with Publisher
# object from eCAL
pub: Union[None, StringPublisher] = None

config_small_car_latitude: float = 0.0
config_small_car_longitude: float = 0.0
config_distance_threshold: float = 0.0  # in meters


def callback(topic_name: str, msg: NavSatFix, time_stamp):
    """
    eCAL callback function upon receiving message from subscribed topic
    The callback is listening to the message 'ROSGlobalPosition' from the system. The topic contains the global
    position of the ego car.

    :param topic_name: The name of the received topic
    :param msg: The entire message data
    :param time_stamp: The time stamp for the data
    :return:
    """
    global distances, call_count, start_time, pub
    global config_small_car_longitude, config_small_car_latitude, config_distance_threshold

    # Calculate the current time based on call_count
    current_time = start_time + timedelta(seconds=call_count)

    coords_big_car: Tuple = (msg.latitude, msg.longitude)
    coords_small_car: Tuple = (config_small_car_latitude, config_small_car_longitude)
    dist: float = geopy.distance.geodesic(coords_big_car, coords_small_car).m

    if dist < config_distance_threshold:
        print("---------TATÜTATA-----------")

        pub.send('{"move": "on"}')
        time.sleep(0.1)
    else:
        print("Distance to Big Car: ", dist)

    # Append new data to DataFrame
    distances.loc[len(distances)] = [current_time, msg.latitude, msg.longitude, dist]

    # Increment the call count
    call_count += 1


if __name__ == "__main__":

    # Parsing arguments
    parser = argparse.ArgumentParser(
        prog='EmergencyPassthroughSystem',
        description='Core Logic Algorithm for Emergency Passthrough System',
        add_help=True)

    parser.add_argument('--config-file', '-cf', type=argparse.FileType('r', encoding='UTF-8'), required=True,
                        help="Path to config file (JSON)")
    parser.add_argument('--record-result', '-r', action='store_true', default=False,
                        help="Boolean flag to record position into .csv file at the end of the program")

    args = parser.parse_args()

    try:
        # Load configuration to a dictionary
        config: Dict = json.loads(args.config_file.read())
        # Close the file properly
        args.config_file.close()

        # Setup the configuration from the file to the global configuration
        config_small_car_latitude = config["latitude"]
        config_small_car_longitude = config["longitude"]
        config_distance_threshold = config["distance_threshold"]

        # Initialize eCAL
        ecal_core.initialize(sys.argv, "EPS Controller")

        # Create a subscriber that listens on the "ROSGlobalPosition" topic
        sub = ProtoSubscriber("ROSGlobalPosition", NavSatFix)

        # Initialize publisher that will be used to send signal to another car
        pub = StringPublisher("smallcar")

        # Set the Callback
        sub.set_callback(callback)

        # Main loop
        while ecal_core.ok():
            time.sleep(0.5)

    except KeyboardInterrupt:
        if args.record_result:
            # Save DataFrame to CSV when KeyboardInterrupt occurs
            print("\nSaving data to 'distances.csv'...")
            distances.to_csv('distances.csv', index=False)
            print("Data saved. Exiting.")

    finally:
        # Finalize eCAL API
        ecal_core.finalize()
