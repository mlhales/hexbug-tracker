__author__ = 'mlh'


import math
import cv2
import numpy as np
from bounds import *
from filter import *
from hexbug import *


def round_point(point):
    return [int(round(point[0])), int(round(point[1]))]


def round_to_tuple(point):
    pt = round_point(point)
    return pt[0], pt[1]

class HexbugPredictor():
    """
    HexbugPredictor predicts future hexbug location using a particle filter and simple model for
    motion and collision.
    """

    def __init__(self, world_properties, source=None):
        """
        Initialize the object with passed parameters and a ParticleFilter of Bugs.
        """
        self.measurements = world_properties["centroid"]
        size = world_properties["size"]
        self.source = source
        if source:
            self.cap = cv2.VideoCapture(source)
        self.bug = Hexbug(self.measurements[0], size)

    def __del__(self):
        if self.cap:
            self.cap.release()

    def train(self):
        """
        Iterate over the centroid data, updating the particle filter each time to determine the best
        location, orientation and world properties.
        """
        ctr = 0
        for pt in self.measurements:
            if self.cap:
                captured, frame = self.cap.read()
                if captured:
                    cv2.circle(frame, (pt[0], pt[1]), 2, (0, 0, 255), 1)

            if pt[0] > 0 and pt[1] > 0:
                self.bug.sense(pt)
            else:
                self.bug.sense(self.bug.predict())

            if ctr > 1:
                clone = self.bug.clone()
                l = clone.centroid
                for i in range(63):
                    p = clone.predict()
                    clone.sense(p)
                    cv2.line(frame, round_to_tuple(l), round_to_tuple(p), (0, 0, 255), 1)
                    l = p

            l = self.measurements[ctr]
            for i in range(ctr + 1, min(ctr + 63, len(self.measurements) - 1)):
                p = self.measurements[i]
                if p[0] > 0 and p[1] > 0:
                    cv2.line(frame, round_to_tuple(l), round_to_tuple(p), (255, 0, 0), 1)
                    l = p
            cv2.imshow("Training", frame)
            cv2.waitKey(1)
            ctr += 1


    def predict(self, steps):
        """
        Choose the best particle from the particle filter, and iteratively step it to generate the
        desired number of predictions.
        :param steps: Number of predictions to return
        :return: List of predictions
        """
        predictions = []
        clone = self.bug.clone()
        for i in range(steps):
            p = clone.predict()
            predictions.append(round_point(p))
            clone.sense(p)
        return predictions





