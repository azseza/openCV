"""
Python script showing of how to I/O images/videos with openCV
"""

#importing the libraries 
import cv2 as cv

#reading an image 
#image = cv.imread('images/trump.png')

#and then 
#cv.imshow('trump', image)

#Reading a video 

capture = cv.VideoCapture('vidz/tsunade.mp4')

while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('x'):
        break
capture.release()
cv.destroyAllWindows()