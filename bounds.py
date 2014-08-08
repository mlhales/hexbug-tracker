__author__ = 'mlh'

import math


def distance_between(point1, point2):
    """
    Determine the euclidean distance between two points.
    :param point1:
    :param point2:
    :return: The distance.
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += math.pi * 2
    return ((a + math.pi) % (math.pi * 2)) - math.pi


def get_orientation(previous_point, current_point):
    """Returns the angle, in radians, between two points"""
    previous_x, previous_y = previous_point
    current_x, current_y = current_point
    heading = math.atan2(current_y - previous_y, current_x - previous_x)
    heading = angle_trunc(heading)
    return heading


def angle_between(x, y):
    """
    Returns the signed angle between two points (between -pi and pi)
    :param x:
    :param y:
    :return: Angle in radians
    """
    return math.atan2(math.sin(x - y), math.cos(x - y))


class Bounds():
    """
    Bounds represents the rectangular world in which the Hexbug moves.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0

    def expand_box(self, box):
        """
        Expand the bounds for each point of the box.
        :param box: Four points than define a rectangle
        """
        for point in box:
            self.expand_point(point[0], point[1])

    def expand_point(self, x, y):
        """
        If the point exceeds the bounds, expand the bounds to include it.
        """
        if x < self.x:
            self.w += self.x - x
            self.x = x
        if y < self.y:
            self.h += self.y - y
            self.y = y
        if x > (self.x + self.w):
            self.w = x - self.x
        if y > (self.y + self.h):
            self.h = y - self.y

    def exceeds(self, x, y):
        """
        Return whether the passed point is outside of the bounds
        :param x:
        :param y:
        :return: Boolean
        """
        response = False
        xi = x
        yi = y
        if x < self.x:
            xi = self.x
            response = True
        if y < self.y:
            yi = self.y
            response = True
        if x > self.x + self.w:
            xi = self.x + self.w
            response = True
        if y > self.y + self.h:
            yi = self.y + self.h
            response = True
        return response, xi, yi