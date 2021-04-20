"""
Helper file for the hand counter/gesture app 
"""
from typing import Tuple
import numpy as np
import cv2 as cv
import freenect
#Reading the frame 

def read_frame0()->Tuple[bool, np.ndarray]:
    """Helper function to read frames from Kinect
    depth sensor.
    Convertes the 11 bit frame to an uint8
    to visualize the frame : cv.imshow("depth", read_frame()[1])

    Returns:
        Tuple[bool, np.ndarray]: true, np.uint8 if capture is good 
                                 false, np.empty if capture is not good
    """
    depth, timestamp = freenect.sync_get_depth()
    if depth is None:
        return False, np.empty(depth, dtype=np.int8)
    np.clip(depth, 0, 2**10-1, depth)
    depth >>= 2
    return (True, depth.astype(np.uint8))

def read_the_imagez():
    """Helper Function to read frames from kinect 
    depth sensor.

    Returns:
        Tuple[bool, np.ndarray]: true, np.uint8 if capture is good 
                                 false, np.empty if capture is not good
    """
    device = cv.cv.CV_CAP_OPENI
    capture = cv.VideoCapture(device)
    if not capture.grab():
        return False, None
    return capture.retrieve(cv.CAP_OPENNI_DEPTH_MAP)

#Recongnizing the gestures 

def recognize(frame: np.uint8)->Tuple[int, np.ndarray]:
    