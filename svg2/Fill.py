#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum

from .Color import Color


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
        self.color = (color if isinstance(color, Color) or color == 'none'
                      else Color(color))
        self.opacity = opacity # 0.0-1.0
        self.fillrule = fillrule # FillRule


    def svg(self, options):
        parts = []
        if options.use_style:
            sep = options.sep
            if self.color != Color.BLACK:
                parts.append(f'fill:{sep}{self.color}')
            if self.opacity != 1:
                parts.append(f'fill-opacity:{sep}{self.opacity}')
            if self.fillrule is not FillRule.default():
                parts.append(f'fill-rule={sep}{self.fillrule.value}')
            if parts:
                return f';{sep}'.join(parts)
        else:
            if self.color != Color.BLACK:
                parts.append(f'fill="{self.color}"')
            if self.opacity != 1:
                parts.append(f'fill-opacity="{self.opacity}"')
            if self.fillrule is not FillRule.default():
                parts.append(f'fill-rule="{self.fillrule.value}"')
            if parts:
                return ' '.join(parts)
        return ''
