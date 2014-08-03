__author__ = 'mike'

import random
import math
import numpy as np


class Bug():
    """
    Bug represents a Hexbug, with mutable centroid, orientation and speed.
    It's dimensions are set at instantiation.
    Physical parameters of the bug such as mass, friction and impulse set randomly.
    """
    def __init__(self, x, y, orientation, speed, length, width):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed
        self.length = length
        self.width = width
        self.mass = random.uniform(0.0, 2.0)
        self.friction = random.uniform(0.0, 2.0)
        self.impulse = random.uniform(0.0, 10.0)

    def move(self, bounds):
        """
        Move the Bug by changing its mutable state (x, y, orientation and speed) based on
        the intrinsic parameters. First calculate the straight line motion. If straight line
        motion would intercept the bounds, model a collision.
        :param bounds: A Bounds object representing the known world.
        :return: None
        """

    def error(self, x, y):
        """
        Compute the error between the passed coordinates and Bugs centroid
        :param x: The x position.
        :param y: The y position
        :return: The cartesian distance between the Bugs centroid and the coordinates passed as arguments
        """
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def predict_once(self):
        return self.x, self.y

    def predict_many(self, iterations):
        predictions = []
        for ea in range(iterations):
            predictions.append(self.predict_once())
        return predictions