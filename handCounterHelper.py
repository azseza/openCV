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
    """Python function to recognize how many fingers are 
    in the picture

    Args:
        frame (np.uint8): Input gray scaled image

    Returns:
        Tuple[int, np.ndarray]: number of fingers, countour of the hand
    """
    segment = segment_arm(frame)
    contour, defects = find_hull_effects(segment)
    image_draw = cv.cvtColor(segment, cv.COLOR_GRAY2RGB)
    num_fingers, image_draw = detect_num_fingers(contour, defects, image_draw)
    return num_fingers, image_draw



def segment_arm(frame: np.uint8, absolute_depth: int = 14) -> np.ndarray:
    """Function that segments an image and returns a black and white image
    smoothed image of the hand to count

    Args:
        frame (np.uint8): [description]
        absolute_depth (int, optional): [description]. Defaults to 14.

    Returns:
        np.ndarray: [description]
    """
    height, width = frame.shape[:2]
    #Finding the center region of imgheight frame 
    center_half = 10 # half-width of 21 is 21/2-1
    center = frame[height // 2 - center_half:height // 2 + center_half, 
                   width // 2 - center_half:width // 2 +center_half]
    #putting the filter border
    median = np.median(center)
    #applying the first filter in grayscale(unknown region nor hand nor non-hand)
    frame = np.where(abs(frame-median) <= absolute_depth, 128, 0).astype(np.uint8)
    #morphological closing and smoothing
    kernel = np.ones((3, 3), np.uint8)
    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel).astype(np.ndarray)
    #applying white filter to the hand (part we are sure about it's the hand) 
    smaal_kernel = 3 
    frame[height // 2 - smaal_kernel:height // 2 + smaal_kernel,
         width // 2 - smaal_kernel:width // 2 + smaal_kernel] = 128
    #Applapplying the mask 
    mask = np.zeros((height + 2, width + 2), np.uint8)    
    flood = frame.copy()
    cv.floodFilld(flood, mask, (width // 2, height // 2), 255, flags=4 | (255<<8))
    ret, flooded = cv.threshold(flood, 129, 255, cv.THRESH_BINARY)
    return flooded

#Finding the hand countours 
def find_hull_effects(segment: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    coutours, hirarchy = cv.findContours(segment, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #choosing the biggest countours
    max_contour = max(coutours, key=cv.contourArea)
    #Minimizing edges of the biggest contour
    e = 0.01 * cv.arcLength(max_contour, True)
    max_contour = cv.approxPolyDP(max_contour, e, True)
    