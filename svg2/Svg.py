#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

class _SVG: # base class for all that's common to SVG 1.1 and 2

    def __init__(self):
        self._items = []


class Svg1(_SVG):

    def __init__(self):
        super().__init__()


    @property
    def standard(self):
        return '1.1 2nd edition'


class Svg2(_SVG):

    def __init__(self):
        super().__init__()


    @property
    def standard(self):
        return '2.0'
