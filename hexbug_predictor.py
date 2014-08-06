__author__ = 'mlh'


import math
import cv2
import numpy as np
from bounds import *
from filter import *


class HexbugPredictor():
    """
    HexbugPredictor predicts future hexbug location using a particle filter and simple model for
    motion and collision.
    """

    def __init__(self, centroid, bounds, bug_size, source=None):
        """
        Initialize the object with passed parameters and a ParticleFilter of Bugs.
        """
        self.centroid = centroid
        self.bounds = bounds
        self.bug_size = bug_size
        self.source = source
        if source:
            self.cap = cv2.VideoCapture(source)
        self.filter = ParticleFilter(Bug, 10000)

    def __del__(self):
        if self.cap:
            self.cap.release()

    def train(self):
        """
        Iterate over the centroid data, updating the particle filter each time to determine the best
        location, orientation and world properties.
        """
        for pt in self.centroid:
            if self.cap:
                captured, frame = self.cap.read()
                if captured:
                    cv2.circle(frame, (pt[0], pt[1]), 2, (0, 0, 255), 1)
                    cv2.imshow("Training", frame)
                    cv2.waitKey(1)
            self.filter.sense(pt[0], pt[1])

    def predict(self, steps):
        """
        Choose the best particle from the particle filter, and iteratively step it to generate the
        desired number of predictions.
        :param steps: Number of predictions to return
        :return: List of predictions
        """
        best = self.filter.best()
        predictions = []
        for i in range(steps):
            predictions.append(best.predict())
        return predictions




