#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from . import AbstractShape


class Line(AbstractShape.AbstractStroke):

    def __init__(self, x1, y1, x2, y2, *, stroke=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123').'''
        super().__init__(stroke)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


    def svg(self):
        return (f'<line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" '
                f'y2="{self.y2}"{self.stroke.svg()}/>')


    def _css(self, sep=''):
        css = self.stroke._css(sep)
        if css:
            css = f' style="{css}"'
        return (f'<line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" '
                f'y2="{self.y2}"{css}/>')


class Rect(AbstractShape.AbstractPositionStrokeFill):

    def __init__(self, x, y, *, width, height, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.width = width
        self.height = height


    def svg(self):
        return (f'<rect x="{self.x}" y="{self.y}" width="{self.width}" '
                f'height="{self.height}"{super().svg()}/>')


    def _css(self, sep=''):
        css = super()._css(sep)
        if css:
            css = f' style="{css}"'
        return (f'<rect x="{self.x}" y="{self.y}" width="{self.width}" '
                f'height="{self.height}"{css}/>')


class Circle(AbstractShape.AbstractPositionStrokeFill):

    def __init__(self, x, y, *, radius, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.radius = radius


    def svg(self):
        return (f'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}"'
                f'{super().svg()}/>')


    def _css(self, sep=''):
        css = super()._css(sep)
        if css:
            css = f' style="{css}"'
        return (f'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}"'
                f'{css}/>')


class Ellipse(Circle):

    def __init__(self, x, y, *, xradius, yradius, stroke=None, fill=None):
        '''`radius` is a synonym for `xradius`.
        The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, radius=xradius, stroke=stroke, fill=fill)
        self.yradius = yradius


    @property
    def xradius(self):
        return self.radius


    @xradius.setter
    def xradius(self, xradius):
        self.radius = xradius


    def svg(self):
        if self.xradius == self.yradius:
            return super().svg
        return (f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.xradius}" '
                f'ry="{self.yradius}"{super().svg()}/>')


    def _css(self, sep=''):
        if self.xradius == self.yradius:
            return super().svg
        return (f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.xradius}" '
                f'ry="{self.yradius}"{super()._css(sep)}/>')


class Path(AbstractShape.AbstractStrokeFill):

    def __init__(self, *, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)
        self.d = [] # sequence of drawing commands
