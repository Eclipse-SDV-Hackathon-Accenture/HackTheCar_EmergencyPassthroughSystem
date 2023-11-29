import sys
import time
from datetime import datetime, timedelta

import ecal.core.core as ecal_core
import geopy.distance
import pandas as pd
from ecal.core.subscriber import ProtoSubscriber
from ecal.core.publisher import StringPublisher

from ros.sensor_msgs.NavSatFix_pb2 import NavSatFix

# Initialize the DataFrame outside of the callback
distances = pd.DataFrame(columns=['time', 'latitude', 'longitude', 'distance'])
call_count = 0
start_time = datetime(2023, 11, 30, 12, 0, 0)  # November 30, 2023, at 12 PM

pub = None

# Callback for receiving messages
def callback(topic_name, msg, time_stamp):
    global distances, call_count, start_time

    global pub

    # Calculate the current time based on call_count
    current_time = start_time + timedelta(seconds=call_count)

    coords_bc = (msg.latitude, msg.longitude)
    coords_sc = (48.117599, 11.602926)
    dist = geopy.distance.geodesic(coords_bc, coords_sc).m

    if dist < 10:
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
    try:
        # Initialize eCAL
        ecal_core.initialize(sys.argv, "EPS Controller")

        # Create a subscriber that listens on the "ROSGlobalPosition" topic
        sub = ProtoSubscriber("ROSGlobalPosition", NavSatFix)

        pub = StringPublisher("smallcar")

        # Set the Callback
        sub.set_callback(callback)

        # Main loop
        while ecal_core.ok():
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Save DataFrame to CSV when KeyboardInterrupt occurs
        print("\nSaving data to 'distances.csv'...")
        distances.to_csv('distances.csv', index=False)
        print("Data saved. Exiting.")
    
    finally:
        # Finalize eCAL API
        ecal_core.finalize()
