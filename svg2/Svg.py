#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import gzip
import io

from .Color import Color, ColorError
from .Common import Version


class Svg: # Class and namespace

    Color = Color
    ColorError = ColorError
    Version = Version

    def __init__(self):
        self._items = []


    def save(self, filename, *, version=Version.SVG_1_1, indent=None):
        '''Save the drawing as an SVG file.

        The file will be compressed if the `filename` ends `.svgz` or
        `.svg.gz`.

        The `version` is the SVG version to output and may be either
        `Version.SVG_1_1` (the default) or `Version.SVG_2_0`.

        If `indent` is None (the default) then the SVG will have the minimum
        possible whitespace with no newlines or indentation. If `indent` is
        0, it will have a newline after each close tag or end of tag but no
        indentation. If `indent` is >= 1, it will have newlines after each
        close tag or end of tag and within each tag the specified indent (as
        a count of spaces).

        This method has an alias, dump().

        See also dumps() and write().
        '''
        opener = (gzip.open
                  if filename[-7:].upper().endswith(('.SVGZ', '.SVG.GZ'))
                  else open)
        with opener(filename, 'wt', encoding='utf-8') as file:
            self.write(file, version=version, indent=indent)


    dump = save # dump is more Pythonic; save is more meaningful


    def dumps(self, *, version=Version.SVG_1_1, indent=None):
        '''Return the drawing as an SVG string.

        See also save() (for an explanation of the arguments), and
        write().'''
        stream = io.StringIO()
        self.write(stream, version=version, indent=indent)
        svg = stream.getvalue()
        stream.close()
        return svg


    def write(self, stream, *, version, indent):
        '''Save the drawing as an SVG to the given stream.

        This is a low-level method: it is more convenient to use save() or
        dumps().

        It's the caller's responsibility to close the stream if appropriate.
        '''
        raise NotImplementedError
