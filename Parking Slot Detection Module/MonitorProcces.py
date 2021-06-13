"""
Parking monitor Status
"""
from . import motion_detector
from database.models import Parkings


class MonitorProcess:
    def __init__(self, video_feed, idParking):
        self.idParking = idParking
        self.video_fead = video_feed
    def start(self):
        mon = MotionDetector(self.video_feed, slef.idParking, 1)
        mon.detect_motion()
        
