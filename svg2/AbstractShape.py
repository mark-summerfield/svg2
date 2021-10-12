#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Color import Color
from .Fill import Fill
from .Stroke import Stroke


class AbstractShape:

    def __init__(self):
        self._css_classes = []
        self._css_style = {}


    def add_css_style(self, name, value):
        self._css_style[name] = value


    def css_style(self, sep): # TODO accept options and do sep better
        if not self._css_style:
            return ''
        parts = []
        for name, value in self._css_style.items():
            parts.append(f'{name}: {value}')
        return f';{sep}'.join(parts)


    def add_css_class(self, css_class):
        if css_class not in self._css_classes:
            self._css_classes.append(css_class)
            return True
        return False


    @property
    def css_classes(self):
        if self._css_classes:
            classes = ' '.join(self._css_classes)
            return f' class="{classes}"'
        return ''


class AbstractStroke(AbstractShape):

    def __init__(self, stroke=None):
        super().__init__()
        self.stroke = stroke


    @property
    def stroke(self):
        return self._stroke


    @stroke.setter
    def stroke(self, stroke):
        '''Can set with a Stroke, Color, or color string.'''
        if stroke is None:
            stroke = Stroke()
        elif isinstance(stroke, str):
            stroke = Stroke(Color(stroke))
        elif isinstance(stroke, Color):
            stroke = Stroke(stroke)
        self._stroke = stroke


    def svg(self, options):
        return self.stroke.svg(options)


class AbstractStrokeFill(AbstractStroke):

    def __init__(self, stroke=None, fill=None):
        super().__init__(stroke)
        self.fill = fill # Fill


    @property
    def fill(self):
        return self._fill


    @fill.setter
    def fill(self, fill):
        '''Can set with a Fill, Color, or color string.
        Use 'none' for transparent.
        '''
        if fill is None:
            fill = Fill()
        elif isinstance(fill, str):
            fill = Fill(Color(fill))
        elif isinstance(fill, Color):
            fill = Fill(fill)
        self._fill = fill


    def svg(self, options):
        stroke = self.stroke.svg(options)
        fill = self.fill.svg(options)
        if stroke and fill:
            sep = f';{options.sep}' if options.use_style else ' '
            return stroke + sep + fill
        return stroke + fill # one or both are ''


class AbstractPositionStrokeFill(AbstractStrokeFill):

    def __init__(self, x, y, stroke=None, fill=None):
        super().__init__(stroke, fill)
        self.x = x
        self.y = y
