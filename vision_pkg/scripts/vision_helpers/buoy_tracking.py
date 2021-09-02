#!/usr/bin/python
import cv2

class ObjectTracker:
    def __init__(self):
        self.tracker = cv2.TrackerKCF_create()

    def init(self, img, x, y, w, h):
        self.tracker.init(img, (x,y,w,h))

    def track(self, img):
        success, bbox = self.tracker.update(img)
        if success:
            return bbox
        else :
            return None