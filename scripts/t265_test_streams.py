#####################################################
##          librealsense T265 streams test         ##
#####################################################
# Set the path for IDLE
import sys
sys.path.append("/usr/local/lib/")
# Fix this error: https://stackoverflow.com/questions/43019951/after-install-ros-kinetic-cannot-import-opencv
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
   sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') 

# This assumes .so file is found on the same directory
import pyrealsense2 as rs

# Prettier prints for reverse-engineering
from pprint import pprint
import numpy as np
import cv2


# Get realsense pipeline handle
pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()

# Prints a list of available streams, not all are supported by each device
print('Available streams:')
pprint(dir(rs.stream))

# Enable streams you are interested in
cfg.enable_stream(rs.stream.pose) # Positional data (translation, rotation, velocity etc)
cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

# Start the configured pipeline
pipe.start(cfg)

try:
    while True:
        frames = pipe.wait_for_frames()

        # Left fisheye camera frame
        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        # Right fisheye camera frame
        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())

        print('Left frame', left_data.shape)
        print('Right frame', right_data.shape)

        # Stack both images horizontally
        # cv2.imshow('T265 Streams', np.hstack((left_data, right_data)))

        # Positional data frame
        pose = frames.get_pose_frame()
        if pose:
            pose_data = pose.get_pose_data()
            print('\nFrame number: ', pose.frame_number)
            print('Position: ', pose_data.translation)
            print('Velocity: ', pose_data.velocity)
            print('Acceleration: ', pose_data.acceleration)
            print('Rotation: ', pose_data.rotation)
finally:
    pipe.stop()
