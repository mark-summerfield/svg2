#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Color import Color
from .Common import Version
from .Fill import Fill
from .Stroke import Stroke


class Line:

    def __init__(self, x1, y1, x2, y2, *, stroke=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stroke = stroke # Stroke


class _Stroke_Fill:

    def __init__(self, stroke=None, fill=None):
        self._stroke = stroke # Stroke
        self._fill = fill # Fill


    @property
    def stroke(self):
        return self._stroke


    @stroke.setter
    def stroke(self, stroke):
        if isinstance(stroke, str):
            stroke = Stroke(Color(stroke))
        elif isinstance(stroke, Color):
            stroke = Stroke(stroke)
        self._stroke = stroke


    @property
    def fill(self):
        return self._fill


    @fill.setter
    def fill(self, fill):
        if isinstance(fill, str):
            fill = Fill(Color(fill))
        elif isinstance(fill, Color):
            fill = Fill(fill)
        self._fill = fill


    def _svg(self, version=Version.V_1_1, indent=None):
        stroke = self._stroke.svg(version, indent) if self._stroke else ''
        fill = self._fill.svg(version, indent) if self._fill else ''
        return stroke + fill


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


    def svg(self, version=Version.V_1_1, indent=None):
        end = '\n' if indent is not None else ''
        return (f'<rect x="{self.x}" y="{self.y}" width="{self.width}" '
                f'height="{self.height}"{self._svg()}/>{end}')


class Circle(_Position_Stroke_Fill):

    def __init__(self, x, y, *, radius, stroke=None, fill=None):
        super().__init__(x, y, stroke, fill)
        self.radius = radius


    def svg(self, version=Version.V_1_1, indent=None):
        end = '\n' if indent is not None else ''
        return (f'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}"'
                f'{self._svg()}/>{end}')


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


    def svg(self, version=Version.V_1_1, indent=None):
        if self.xradius == self.yradius:
            return super().svg(version, indent)
        end = '\n' if indent is not None else ''
        return (f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.xradius}" '
                f'ry="{self.yradius}"{self._svg()}/>{end}')


class Path(_Stroke_Fill):

    def __init__(self, *, stroke=None, fill=None):
        super().__init__(stroke, fill)
        self.d = [] # sequence of drawing commands
