__author__ = 'mlh'

import random
import math
import numpy as np


class Bug():
    """
    Bug represents a Hexbug, with mutable centroid, orientation and speed.
    It's dimensions are set at instantiation.
    Physical parameters of the bug such as mass, friction and impulse set randomly.
    """

    def __init__(self, x, y, size):
        """
        Initialize the Hexbug with physical parameters and random parameters to model the motion.
        :param x: Centroid x
        :param y: Centroid y
        :param length: Length of Hexbug
        :param width: Width of Hexbug
        """
        self.x = x
        self.y = y
        self.orientation = random.uniform(0.0, 2 * np.pi)
        self.speed = random.uniform(0, 2.0)
        self.length, self.width = size
        self.mass = random.uniform(0.0, 2.0)
        self.friction = random.uniform(0.0, 2.0)
        self.impulse = random.uniform(0.0, 10.0)

    def measurement_prob(self, x, y):
        """
        Compute the error between the passed coordinates and Bugs centroid
        :param x: The x position.
        :param y: The y position
        :return: The cartesian distance between the Bugs centroid and the coordinates passed as arguments
        """
        # todo create a probability function for x, y, orientation and speed
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def predict(self):
        #todo simulate the bug motion
        return self.x, self.y