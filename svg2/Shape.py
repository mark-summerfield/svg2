#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from xml.sax.saxutils import escape as esc

from . import AbstractShape
from .SvgError import SvgError

# TODO change css_style(options.sep) to css_style(options)


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
        svg = _svg(options.use_style, self.stroke.svg(options),
                   self.css_style(options.sep))
        return (f'{indent}<line x1="{self.x1}" y1="{self.y1}" '
                f'x2="{self.x2}" y2="{self.y2}"{self.css_classes}{svg}/>'
                f'{options.nl}')


class Rect(AbstractShape.AbstractPositionStrokeFill, WriteMixin):

    def __init__(self, x, y, *, width, height, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.width = width
        self.height = height


    def svg(self, indent, options):
        svg = _svg(options.use_style, super().svg(options),
                   self.css_style(options.sep))
        return (f'{indent}<rect x="{self.x}" y="{self.y}" '
                f'width="{self.width}" height="{self.height}"'
                f'{self.css_classes}{svg}/>{options.nl}')


class Circle(AbstractShape.AbstractPositionStrokeFill, WriteMixin):

    def __init__(self, x, y, *, radius, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(x, y, stroke, fill)
        self.radius = radius


    def svg(self, indent, options):
        svg = _svg(options.use_style, super().svg(options),
                   self.css_style(options.sep))
        return (f'{indent}<circle cx="{self.x}" cy="{self.y}" '
                f'r="{self.radius}"{self.css_classes}{svg}/>{options.nl}')


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
        svg = _svg(options.use_style, super().svg(options),
                   self.css_style(options.sep))
        return (f'{indent}<ellipse cx="{self.x}" cy="{self.y}" '
                f'rx="{self.xradius}" ry="{self.yradius}"{self.css_classes}'
                f'{svg}/>{options.nl}')


class Polygon(AbstractShape.AbstractStrokeFill, WriteMixin):

    def __init__(self, *, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)

    # TODO


class Polyline(AbstractShape.AbstractStrokeFill, WriteMixin):

    def __init__(self, points=None, *, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)
        self._points = []
        if points:
            self.set(points)


    def add(self, x, y):
        self._points += [x, y]


    def set(self, points):
        '''`points` must be a list or tuple of numbers.'''
        if len(points) % 2:
            raise SvgError('an even number of coordinates is required, '
                           f'{len(points):,} were passed')
        self._points = points


    def clear(self):
        self._points.clear()


    def svg(self, indent, options):
        if not self._points:
            return ''
        svg = _svg(options.use_style, super().svg(options),
                   self.css_style(options.sep))
        if options.coord_comma:
            points = ' '.join(f'{x},{y}' for x, y in zip(
                              self._points[::2], self._points[1::2]))
        else:
            points = ' '.join(str(n) for n in self._points)
        return (f'{indent}<polyline points="{points}"{self.css_classes}'
                f'{svg}/>{options.nl}')


class Path(AbstractShape.AbstractStrokeFill, WriteMixin):

    def __init__(self, *, stroke=None, fill=None):
        '''The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)
        self._d = [] # sequence of drawing commands

    # TODO


class Text(AbstractShape.AbstractPositionStrokeFill, WriteMixin):

    def __init__(self, text, *, font=None, stroke=None, fill=None):
        '''The font ###########
        The stroke can be a Stroke, Color, or color string (e.g., 'red',
        '#ABC123'). The fill can be a Fill, Color, or color string.'''
        super().__init__(stroke, fill)
        self.text = text
        self.font = font


    def svg(self, indent, options):
        stroke = self.stroke.svg(options)
        fill = self.fill.svg(options)
        if stroke and fill:
            sep = f';{options.sep}' if options.use_style else ' '
            svg = stroke + sep + fill
        else:
            svg = stroke + fill
        # TODO add font either as style or inline and add to svg
        return (f'{indent}<text x="{self.x}" y="{self.y}"{self.css_classes}'
                f'{svg}>{esc(self.text)}</text>{options.nl}')


def _svg(use_style, svg, css_style):
    if use_style:
        if svg and css_style:
            svg = svg + '; ' + css_style
        else:
            svg = svg + css_style
        return f' style="{svg}"' if svg else ''
    return svg if svg.startswith((' ', ';')) else f' {svg}'
