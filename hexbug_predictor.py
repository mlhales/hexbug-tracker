__author__ = 'mike'


import math
import cv2
import numpy as np
from bounds import *


class HexbugPredictor():
    """
    HexbugPredictor predicts future hexbug location using a particle filter and simple model for
    motion and collision.
    """
    def __init__(self, centroid, bounds, bug_size, source = None):
        self.centroid = centroid
        self.bounds = bounds
        self.bug_size = bug_size
        self.source = source

    def predict(self):
        if self.source:
            cap = cv2.VideoCapture(self.source)

        for pt in self.centroid:
            if cap:
                frame = cap.read()
                cv2.imshow("Prediction", frame)

        if cap:
            cv2.destroyAllWindows()
            cap.release()



