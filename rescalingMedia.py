"""Python code snippet to rescale and reshape media files
"""
import cv2 as cv

# img = cv.imread('images/crazy.png')
# cv.imshow('ke', img)

def rescale_frame(frame, scale=0.75):
    """simple func to rescale a frame ,
    Will work for live videos, normal videos and images 

    Args:
        frame cv.img: frame as inout figure to rescale
        scale (float, optional): rescaling amp. Defaults to 0.75.
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def change_resolution(width, height):
    """ will only work on live videos 
    change the resolution

    Args:
        width (int) 
        height (int)): 
    """
    capture.set(3, width)
    capture.set(4, height)

#showing off ..

capture = cv.VideoCapture('vidz/tsunade.mp4')

while True:
    isTrue, frame = capture.read()
    
    frame_resized = rescale_frame(frame)
    
    cv.imshow('Video', frame)
    cv.imshow('littleVideo', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('x'):
        break

capture.release()
cv.destroyAllWindows()