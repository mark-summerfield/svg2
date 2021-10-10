#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum

from .Color import Color


@enum.unique
class LineCap(enum.Enum):
    BUTT = 'butt'
    ROUND = 'round'
    SQUARE = 'square'

    @classmethod
    def default(Class):
        return Class.BUTT


@enum.unique
class LineJoin(enum.Enum):
    ARCS = 'arcs'
    BEVEL = 'bevel'
    MITER = 'miter'
    MITERCLIP = 'miter-clip'
    ROUND = 'round'

    @classmethod
    def default(Class):
        return Class.MITER


class Stroke:

    LineCap = LineCap
    LineJoin = LineJoin

    def __init__(self, color=Color.BLACK, width=1, *, opacity=1,
                 linecap=LineCap.default(), linejoin=LineJoin.default(),
                 dasharray=None):
        self.color = color if isinstance(color, Color) else Color(color)
        self.width = width # Length
        self.opacity = opacity # 0.0-1.0
        self.linejoin = linejoin # LineJoin
        self.linecap = linecap # LineCap
        self.dasharray = dasharray # sequence of ints


    def svg(self):
        parts = []
        if self.color != Color.BLACK:
            parts = [f'stroke="{self.color}"']
        if self.width != 1:
            parts.append(f'stroke-width="{self.width}"')
        if self.opacity != 1:
            parts.append(f'stroke-opacity="{self.opacity}"')
        if self.linecap is not LineCap.default():
            parts.append(f'stroke-linecap="{self.linecap.value}"')
        if self.linejoin is not LineJoin.default():
            parts.append(f'stroke-linejoin="{self.linejoin.value}"')
        if self.dasharray:
            dashes = ' '.join(self.dasharray)
            parts.append(f'stroke-dasharray="{dashes}"')
        if parts:
            return ' ' + ' '.join(parts)
        return ''


    def _css(self, sep=''):
        parts = []
        if self.color != Color.BLACK:
            parts = [f'stroke:{sep}{self.color}']
        if self.width != 1:
            parts.append(f'stroke-width:{sep}{self.width}')
        if self.opacity != 1:
            parts.append(f'stroke-opacity:{sep}{self.opacity}')
        if self.linecap is not LineCap.default():
            parts.append(f'stroke-linecap:{sep}{self.linecap.value}')
        if self.linejoin is not LineJoin.default():
            parts.append(f'stroke-linejoin:{sep}{self.linejoin.value}')
        if self.dasharray:
            dashes = ' '.join(self.dasharray)
            parts.append(f'stroke-dasharray:{sep}{dashes}')
        if parts:
            return f';{sep}'.join(parts)
        return ''
