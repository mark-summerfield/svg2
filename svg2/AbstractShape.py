#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Color import Color
from .Fill import Fill
from .Stroke import Stroke


class AbstractStroke:

    def __init__(self, stroke=None):
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
