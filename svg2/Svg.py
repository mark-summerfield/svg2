#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .common import Standard


class Svg: # Class and namespace

    Standard = Standard

    def __init__(self):
        self._items = []


    def save(self, filename, *, standard=Standard.SVG_1_1_2E):
        with open(filename, 'wt', encoding='utf-8') as file:
            self.write(file, standard=standard)


    def write(self, writable, *, standard=Standard.SVG_1_1_2E):
        raise NotImplementedError
