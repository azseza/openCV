import cv2 as open_cv
import numpy as np
import logging
from database.models import Parkings

COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)   
COLOR_GREEN = (0, 255, 0)  
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)


def logger(id):
    """Logger of motion detection"""
    log = logging.getLogger('Motion detector Number %d',id)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
            '%(asctime) - %(name) - %(message)s'
    )
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log



class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, id_coordinates, start_frame=1):
        self.log = logger(id_coordinates)
        self.video = video
        self.bigId = id_coordinates
        self.coordinates_data = Parkings.objects.get(id=id_coordinates)
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):
        capture = open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)

        coordinates_data = self.coordinates_data
        log.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data["ParkingLot"]:
            coordinates = self._coordinates(p)
            log.debug("coordinates: %s", coordinates)

            rect = open_cv.boundingRect(coordinates)
            log.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            log.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint16),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)
            log.debug("mask: %s", self.mask)

        statuses = self.coordinates_data["ParkingLot"]["LotStatus"]
        times = [None] * len(coordinates_data)

        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()
            log.debug("new_frame: %s", new_frame)

            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0

            for index, c in enumerate(coordinates_data):
                
                status = self.__apply(grayed, index, c)

                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index] = None
                    continue

                if times[index] is not None and self.status_changed(statuses, index, status):
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                        statuses[index] = status
                        times[index] = None
                    continue

                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index] = position_in_seconds

            for index, p in enumerate(coordinates_data["ParkingLot"]):
                coordinates = self._coordinates(p)
                color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
            self.coordinates_data["ParkingLot"]["LotStatus"] = statuses
            Parkings.objects.get(id=self.bigId).update(**self.coordinates_data)
            open_cv.imshow(str(self.video), new_frame)
            k = open_cv.waitKey(1)
            if k == ord("q"):
                break
        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        log.debug("points: %s", coordinates)

        rect = self.bounds[index]
        log.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        log.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        stat = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        if stat:
            status = 'L'
        else:
            status = 'O'
        log.debug("status: %s", status)

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
