#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

class Line:

    def __init__(self, x1, y1, x2, y2, *, stroke=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stroke = stroke # Stroke


class _Stroke_Fill:

    def __init__(self, stroke=None, fill=None):
        self.stroke = stroke # Stroke
        self.fill = fill # Fill


class _Position_Stroke_Fill(_Stroke_Fill):

    def __init__(self, x, y, stroke=None, fill=None):
        super().__init__(stroke, fill)
        self.x = x
        self.y = y


class Rect(_Position_Stroke_Fill):

    def __init__(self, x, y, *, width, height, stroke=None, fill=None):
        super().__init__(x, y, stroke, fill)
        self.width = width
        self.height = height


class Circle(_Position_Stroke_Fill):

    def __init__(self, x, y, *, radius, stroke=None, fill=None):
        super().__init__(x, y, stroke, fill)
        self.radius = radius


class Ellipse(Circle):

    def __init__(self, x, y, *, xradius, yradius, stroke=None, fill=None):
        '''.radius is a synonym for .xradius.'''
        super().__init__(x, y, radius=xradius, stroke=stroke, fill=fill)
        self.yradius = yradius


    @property
    def xradius(self):
        return self.radius


    @xradius.setter
    def xradius(self, xradius):
        self.radius = xradius


class Path(_Stroke_Fill):

    def __init__(self, *, stroke=None, fill=None):
        super().__init__(stroke, fill)
        self.d = [] # sequence of drawing commands
