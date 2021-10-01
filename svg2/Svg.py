#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import io

from .common import Version


class Svg: # Class and namespace

    Version = Version

    def __init__(self):
        self._items = []


    def save(self, filename, *, version=Version.SVG_1_1):
        with open(filename, 'wt', encoding='utf-8') as file:
            self._write(file, version=version)


    def writestr(self, *, version=Version.SVG_1_1):
        stream = io.StringIO()
        self._write(stream, version=version)
        svg = stream.getvalue()
        stream.close()
        return svg


    def _write(self, stream, *, version):
        raise NotImplementedError
