#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import gzip
import io

from .Options import Options, Version
from .Fill import Fill
from .Shape import Circle, Ellipse, Line, Path, Rect
from .Stroke import Stroke


class Svg: # Class and namespace

    Circle = Circle
    Ellipse = Ellipse
    Fill = Fill
    Line = Line
    Options = Options
    Path = Path
    Rect = Rect
    Stroke = Stroke
    Version = Version

    def __init__(self):
        self._items = []


    def save(self, filename, *, options=None):
        '''Save the drawing as an SVG file.

        The file will be compressed if the `filename` ends `.svgz` or
        `.svg.gz`.

        This method has an alias, dump().

        See also dumps() and write().
        '''
        opener = (gzip.open
                  if filename[-7:].upper().endswith(('.SVGZ', '.SVG.GZ'))
                  else open)
        with opener(filename, 'wt', encoding='utf-8') as file:
            self.write(file, options)


    dump = save # dump is more Pythonic; save is more meaningful


    def dumps(self, *, options=None):
        '''Return the drawing as an SVG string.

        See also save() (for an explanation of the arguments), and
        write().'''
        stream = io.StringIO()
        self.write(stream, options)
        svg = stream.getvalue()
        stream.close()
        return svg


    def write(self, stream, *, options):
        '''Save the drawing as an SVG to the given stream.

        This is a low-level method: it is more convenient to use save() or
        dumps().

        It's the caller's responsibility to close the stream if appropriate.
        '''
        options = options if options is not None else Options()
        raise NotImplementedError
