"""Python script that helps detetct and count the number of fingers displayed in 
a video.
"""
import cv2 as cv
import numpy as np
import handCounterHelper import read_the_imagez, recognize
#initialzing the video capture
def draw_helpers(image_drawing: np.ndarray)->None:
    """A function that instructs the user where to put 
    his hand in the center of the screen.

    Args:
        image_drawing (np.ndarray): input image flow to draw into 
    """
    height, width = image_drawing.shape[:2]
    color = (0,102,255)
    cv.circle(image_drawing, (width // 2, height // 2), 3, color, 2)
    cv.rectangle(image_drawing, (width // 2, height // 3), 
                (width * 2 // 3, height * 2 // 3), 3, color, 2)

#Main program of the app
if __name__ == "__main__":
    #Iterating through frames
    for _, frame in iter(read_the_imagez, (False, None)):
        #counting fingers and annotating them 
        num_fingers, img_draw = recognize(frame)
        #Drawing helpers in the output image
        draw_helpers(img_draw)
        #Putting text in the output image
        cv.putText(img_draw, str(num_fingers), (30,30), 
                    cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        #Showing all the stuff 
        cv.imshow("frame", img_draw)
        #quiting in Esc Key
        if cv.waitKey(10) == 27:
            break
