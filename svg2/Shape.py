#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from . import AbstractShape


class WriteMixin:

    def write(self, out, indent, options):
        out.write(self.svg(indent, options))


class Line(AbstractShape.AbstractStroke, WriteMixin):

    def __init__(self, x1, y1, x2, y2, *, stroke=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123').'''
        super().__init__(stroke)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


    def svg(self, indent, options):
        style = _stylize(options.use_style, self.stroke.svg(options))
        return (f'{indent}<line x1="{self.x1}" y1="{self.y1}" '
                f'x2="{self.x2}" y2="{self.y2}"{style}/>{options.nl}')


class Rect(AbstractShape.AbstractPositionStrokeFill, WriteMixin):

    def __init__(self, x, y, *, width, height, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.width = width
        self.height = height


    def svg(self, indent, options):
        style = _stylize(options.use_style, super().svg(options))
        return (f'{indent}<rect x="{self.x}" y="{self.y}" '
                f'width="{self.width}" height="{self.height}"{style}/>'
                f'{options.nl}')


class Circle(AbstractShape.AbstractPositionStrokeFill):

    def __init__(self, x, y, *, radius, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.radius = radius


    def svg(self, indent, options):
        style = _stylize(options.use_style, super().svg(options))
        return (f'{indent}<circle cx="{self.x}" cy="{self.y}" '
                f'r="{self.radius}"{style}/>{options.nl}')


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


    def svg(self, indent, options):
        if self.xradius == self.yradius:
            return super().svg(indent, options)
        style = _stylize(options.use_style, super().svg(options))
        return (f'{indent}<ellipse cx="{self.x}" cy="{self.y}" '
                f'rx="{self.xradius}" ry="{self.yradius}"'
                f'{style}/>{options.nl}')


class Polygon(AbstractShape.AbstractStrokeFill):

    def __init__(self, *, stroke=None, fill=None):
        pass # TODO


class Polyline(AbstractShape.AbstractStrokeFill):

    def __init__(self, *, stroke=None, fill=None):
        pass # TODO


class Path(AbstractShape.AbstractStrokeFill):

    def __init__(self, *, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)
        self._d = [] # sequence of drawing commands

    # TODO


def _stylize(use_style, style):
    if use_style:
        return f' style="{style}"' if style else ''
    return style if style.startswith((' ', ';')) else f' {style}'
