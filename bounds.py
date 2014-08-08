__author__ = 'mlh'

import math


def distance_between(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += math.pi * 2
    return ((a + math.pi) % (math.pi * 2)) - math.pi


def get_orientation(previous_point, current_point):
    """Returns the angle, in radians, between the target and hunter positions"""
    previous_x, previous_y = previous_point
    current_x, current_y = current_point
    heading = math.atan2(current_y - previous_y, current_x - previous_x)
    heading = angle_trunc(heading)
    return heading


def angle_between(x, y):
    return math.atan2(math.sin(x - y), math.cos(x - y))


class Bounds():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0

    def expand_box(self, box):
        for point in box:
            self.expand_point(point[0], point[1])

    def expand_point(self, x, y):
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