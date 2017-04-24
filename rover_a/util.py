#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy


class bresenham:
    """ determines the points of an n-dimensional raster that should be selected in order to form a close approximation
    to a straight line between two points. src: https://gist.github.com/flags/1132363
    """
    def __init__(self, start, end):
        self.start = list(start)
        self.end = list(end)
        self.path = []
        self.reverse = False

        self.steep = numpy.abs(self.end[1] - self.start[1]) > numpy.abs(self.end[0] - self.start[0])

        if self.steep:
            self.start = self.swap(self.start[0], self.start[1])
            self.end = self.swap(self.end[0], self.end[1])

        if self.start[0] > self.end[0]:
            self.reverse = True
            _x0 = int(self.start[0])
            _x1 = int(self.end[0])
            self.start[0] = _x1
            self.end[0] = _x0

            _y0 = int(self.start[1])
            _y1 = int(self.end[1])
            self.start[1] = _y1
            self.end[1] = _y0

        dx = self.end[0] - self.start[0]
        dy = numpy.abs(self.end[1] - self.start[1])
        error = 0
        derr = dy / float(dx)

        ystep = 0
        y = self.start[1]

        if self.start[1] < self.end[1]:
            ystep = 1
        else:
            ystep = -1

        for x in range(int(self.start[0]), int(self.end[0]) + 1):
            if self.steep:
                self.path.append((y, x))
            else:
                self.path.append((x, y))

            error += derr

            if error >= 0.5:
                y += ystep
                error -= 1.0

        if self.reverse:
            self.path.reverse()

    def swap(self, n1, n2):
        return [n2, n1]

# Trigonometry
def cart2pol(x, y):
    rho = numpy.sqrt(x ** 2 + y ** 2)
    phi = numpy.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * numpy.cos(phi)
    y = rho * numpy.sin(phi)
    return (x, y)
