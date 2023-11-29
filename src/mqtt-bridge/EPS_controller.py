import pandas as pd
import geopy.distance
import time
import sys
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
from ros.sensor_msgs.NavSatFix_pb2 import NavSatFix
from datetime import datetime, timedelta

# Initialize the DataFrame outside of the callback
distances = pd.DataFrame(columns=['time', 'latitude', 'longitude', 'distance'])
call_count = 0
start_time = datetime(2023, 11, 30, 12, 0, 0)  # November 30, 2023, at 12 PM

# Callback for receiving messages
def callback(topic_name, msg, time_stamp):
    global distances, call_count, start_time

    # Calculate the current time based on call_count
    current_time = start_time + timedelta(seconds=call_count)

    coords_bc = (msg.latitude, msg.longitude)
    coords_sc = (48.1175793, 11.6028788)
    dist = geopy.distance.geodesic(coords_bc, coords_sc).m

    if dist < 10:
        print("---------TATÜTATA-----------")
    else: 
        print("Distance to Big Car: ", dist)

    # Append new data to DataFrame
    distances.loc[len(distances)] = [current_time, msg.latitude, msg.longitude, dist]

    # Increment the call count
    call_count += 1

if __name__ == "__main__":
    try:
        # Initialize eCAL
        ecal_core.initialize(sys.argv, "test")

        # Create a subscriber that listens on the "ROSGlobalPosition" topic
        sub = ProtoSubscriber("ROSGlobalPosition", NavSatFix)

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
