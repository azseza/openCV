"""
Python Class using OpenCv user input utils
"""
import cv2 as open_cv
import numpy as np
import pyaml
from colors import COLOR_WHITE
from drawing_utils import draw_contours
import logging

def logger():
    logg = logging.getLogger("Coordonates Generator")
    logg.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logg.addHandler(ch)
    return logg

class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color
        self.log = logger()

        self.image = open_cv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        self.gpsCoordinates = []
        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            open_cv.imshow(self.caption, self.image)
            key = open_cv.waitKey(0)
            self.log.debug("Starting")
            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
                self.log.debug("STARTED!!")
            elif key == CoordinatesGenerator.KEY_QUIT:
                self.log.info("'q' Key was pressed quitting .. ")
                self.log.debug("ENEDED!!")
                break
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):
        idiy = 0 
        
        if event == open_cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1
            
            if self.click_count >= 4:
                self.log.debug("Done with ID %d",idiy)
                self.__handle_done()
                idiy += 1
                
            elif self.click_count > 1:
                current = self.click_count % 4
                self.log.debug("Entering point number %d", current)
                self.__handle_click_progress()

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)
# MAke changes here to the input section and YAML shit  
    def __handle_done(self):
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)

        self.click_count = 0
        self.log.info("Writing Coordinates number %d", self.ids)
        coordinates = np.array(self.coordinates)
        self.output.write("- _id : " + str(self.ids) + "\n    ImageCoordinates : \n" +
                          "        --" + str(self.coordinates[0][0]) + "\n         -" + str(self.coordinates[0][1]) + "\n" +
                          "        --" + str(self.coordinates[1][0]) + "\n         -" + str(self.coordinates[1][1]) + "\n" +
                          "        --" + str(self.coordinates[2][0]) + "\n         -" + str(self.coordinates[2][1]) + "\n" +
                          "        --" + str(self.coordinates[3][0]) + "\n         -" + str(self.coordinates[3][1]) + "\n")
        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)
        self.log.info("Writing GPS coordinates, please follow gently")
        print(15*"=")
        print("Enter Longitutde Point")
        print(15*"=")
        longitutde = float(input())
        print(15*"=")
        print("enter lattitude Point")
        print(15*"=")
        lattitude = float(input())
        self.gpsCoordinates.append((longitutde, lattitude))
        self.output.write("    Gps coordinates : \n" +
                          "        -" + str(self.gpsCoordinates[self.ids][0]) + "\n"+ 
                          "        -" + str(self.gpsCoordinates[self.ids][1]) + "\n")
        self.output.write("    Status : \n" + "        - L")
        for i in range(0, 4):
            self.coordinates.pop()
        self.log.info("Moving On .. ")
        self.ids += 1
