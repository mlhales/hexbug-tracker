__author__ = 'mlh'


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