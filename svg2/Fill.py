#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum

from .Color import Color
from .Common import Version


@enum.unique
class FillRule(enum.Enum):
    NONZERO = 'nonzero'
    EVENODD = 'evenodd'

    @classmethod
    def default(Class):
        return Class.NONZERO


class Fill:

    NONZERO = FillRule.NONZERO
    EVENODD = FillRule.EVENODD

    def __init__(self, color='none', *, opacity=1,
                 fillrule=FillRule.default()):
        self.color = Color(color) if color != 'none' else color
        self.opacity = opacity # 0.0-1.0
        self._fillrule = fillrule # FillRule


    @property
    def fillrule(self):
        return self._fillrule.value


    @fillrule.setter
    def fillrule(self, fillrule):
        self._fillrule = fillrule


    def svg(self, version=Version.V_1_1, indent=None):
        parts = []
        if self.color != Color.BLACK:
            parts.append(f'fill="{self.color}"')
        if self.opacity != 1:
            parts.append(f'fill-opacity="{self.opacity}"')
        if self._fillrule is not FillRule.default():
            parts.append(f'fill-rule="{self._fillrule.value}"')
        if parts:
            return ' ' + ' '.join(parts)
        return ''
