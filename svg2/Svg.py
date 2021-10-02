#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import gzip
import io

from .common import Version


class Svg: # Class and namespace

    Version = Version

    def __init__(self):
        self._items = []


    def save(self, filename, *, version=Version.SVG_1_1):
        '''Save the drawing as an SVG file.
        The file will be compressed if the filename ends .svgz or .svg.gz.
        This method has an alias, 'dump()'.
        See also dumps() and write().
        '''
        opener = (gzip.open if filename.upper().endswith(('.SVGZ', '.GZ'))
                  else open)
        with opener(filename, 'wt', encoding='utf-8') as file:
            self.write(file, version=version)


    dump = save # dump is more Pythonic; save is more meaningful


    def dumps(self, *, version=Version.SVG_1_1):
        '''Return the drawing as an SVG string.
        See also save() and write().'''
        stream = io.StringIO()
        self.write(stream, version=version)
        svg = stream.getvalue()
        stream.close()
        return svg


    def write(self, stream, *, version):
        '''Save the drawing as an SVG to the given stream.
        It's the caller's responsibility to close the stream if appropriate.
        See also save() and dumps().'''
        raise NotImplementedError
