__author__ = 'mlh'

from bounds import *
import random
import math
import numpy as np


class Hexbug():
    """
    Hexbug represents a Hexbug, with mutable centroid, orientation and speed.
    It's dimensions are set at instantiation.
    Physical parameters of the bug such as mass, friction and impulse set randomly.
    """

    def __init__(self, centroid, size, bounds):
        """
        Initialize the Hexbug with physical parameters and random parameters to model the motion.
        :param x: Centroid x
        :param y: Centroid y
        :param size: Length and Width of Hexbug
        """
        self.centroid = centroid
        self.filter = centroid
        self.speed = None
        self.theta = None
        self.filter_theta = None
        self.dtheta = None
        self.ddtheta = None
        self.size = size
        self.bounds = bounds

    def clone(self):
        bug = Hexbug(self.centroid, self.size, self.bounds)
        bug.speed = self.speed
        bug.theta = self.theta
        bug.filter_theta = self.filter_theta
        bug.dtheta = self.dtheta
        bug.ddtheta = self.ddtheta
        return bug

    def sense(self, c):
        if c != self.centroid:
            nfc = [(0.1 * c[0]) + (0.9 * self.filter[0]), (0.1 * c[1]) + (0.9 * self.filter[1])]
            self.speed = math.sqrt((self.filter[0] - nfc[0]) ** 2 + (self.filter[1] - nfc[1]) ** 2)
            nt = get_orientation(self.centroid, c)
            nft = get_orientation(self.filter, c)
            if self.filter_theta:
                dt = angle_trunc(nft - self.filter_theta)
                if self.dtheta:
                    self.ddtheta = angle_trunc(dt - self.dtheta)
                else:
                    self.ddtheta = 0
                self.dtheta = dt
            else:
                self.ddtheta = 0.0
                self.dtheta = 0.0
            self.theta = nt
            self.filter_theta = nft
            self.filter = nfc
            self.centroid = c

    def predict(self):
        if self.speed and self.filter_theta:
            theta = self.theta + (0.5 * self.dtheta)
            x = self.centroid[0] + (math.cos(theta) * 9.5)
            y = self.centroid[1] + (math.sin(theta) * 9.5)

            if self.collision_predicted(x, y):
                clone = self.clone()
                # recursively turn the bug right until it is facing away from the boundary wall
                clone.theta = self.theta + (math.pi / 4.0)
                clone.filter_theta = self.filter_theta + (math.pi / 4.0)
                clone.dtheta = self.dtheta * 0.25
                return clone.predict()
        else:
            x = self.centroid[0]
            y = self.centroid[1]
        return [x, y]

    def collision_predicted(self, x, y):
        """
        Determines if a collision with the bounds is predicted.
        :param x:
        :param y:
        :return: Boolean
        """
        exceeds, _, _ = self.bounds.exceeds(x, y)
        return exceeds
