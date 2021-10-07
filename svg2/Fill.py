#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


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

    def __init__(self, color=None, *, opacity=1,
                 fillrule=FillRule.default()):
        self.color = color # Color
        self.opacity = opacity # 0.0-1.0
        self._fillrule = fillrule # FillRule


    @property
    def fill(self):
        return str(self.color) if self.color else 'none'


    @property
    def fillrule(self):
        return self._fillrule.value


    @property
    def svg(self):
        parts = []
        if self.color:
            parts.append(f'fill="{self.fill}"')
        if self.opacity != 1:
            parts.append(f'fill-opacity="{self.opacity}"')
        if self._fillrule is not FillRule.default():
            parts.append(f'fill-rule="{self._fillrule.value}"')
        if parts:
            return ' '.join(parts)
        return ''
