__author__ = 'mlh'

from utility import *
from bounds import *
import random
import math
import numpy as np


class Bug(ComparableMixin):
    """
    Bug represents a Hexbug, with mutable centroid, orientation and speed.
    It's dimensions are set at instantiation.
    Physical parameters of the bug such as mass, friction and impulse set randomly.
    """
    speed_mu = 0
    speed_var = 1000
    speed_max = 11
    turn_mu = 0
    turn_var = 1000
    turn_max = math.pi

    def __init__(self, x, y, size):
        """
        Initialize the Hexbug with physical parameters and random parameters to model the motion.
        :param x: Centroid x
        :param y: Centroid y
        :param size: Length and Width of Hexbug
        """
        self.x = x
        self.y = y
        self.orientation = random.uniform(0.0, 2 * np.pi)
        self.turn = angle_trunc(random.gauss(Bug.turn_mu, Bug.turn_var))
        self.speed = random.gauss(Bug.speed_mu, Bug.speed_var)
        self.length, self.width = size
        self.weight = 0

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    def clone(self):
        clone = Bug(self.x, self.y, (self.length, self.width))
        clone.set(self.orientation, self.turn, self.speed)
        return clone

    def _cmpkey(self):
        return self.weight

    def set(self, orientation, turn, speed):
        self.orientation = orientation
        self.turn = turn
        self.speed = speed

    def centroid(self):
        return [self.x, self.y]

    def measurement_prob(self, x, y):
        """
        Compute the probability that the measurement represents this bugs location
        :param x: The x position.
        :param y: The y position
        :return: The probability, based on cartesian distance between the Bugs centroid
        and the coordinates passed as arguments
        """
        next_bug = self.random_move()
        sigma = Bug.speed_var
        particle_error = math.sqrt((self.x - next_bug.x) ** 2 + (self.y - next_bug.y) ** 2)
        measurement_error = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        self.weight = math.exp(- ((particle_error - measurement_error) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(
            2.0 * math.pi * (sigma ** 2))
        return self.weight, next_bug

    def random_move(self):
        """
        Randomly move the bug by adding gaussian error to its speed and turn, then stepping it.
        :return: A new Bug instance.
        """
        turn = max(-Bug.turn_max, min(Bug.turn_max, self.turn + random.gauss(0.0, Bug.turn_var)))
        orientation = self.orientation + random.gauss(0.0, Bug.turn_var)
        orientation %= 2 * math.pi
        speed = max(0, min(Bug.speed_max, self.speed + random.gauss(0.0, Bug.speed_mu)))
        x = np.int0(self.x + (math.cos(orientation) * speed))
        y = np.int0(self.y + (math.sin(orientation) * speed))
        bug = Bug(x, y, (self.length, self.width))
        bug.set(orientation, turn, speed)
        return bug

    def predict_move(self):
        """
        Move the bug by stepping it according to its current speed and turn.
        :return: A new Bug instance.
        """
        orientation = self.orientation  # + self.turn
        # orientation %= 2 * math.pi
        x = np.int0(self.x + (math.cos(orientation) * self.speed))
        y = np.int0(self.y + (math.sin(orientation) * self.speed))
        bug = Bug(x, y, (self.length, self.width))
        bug.set(orientation, self.turn, self.speed)
        return bug