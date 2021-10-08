#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import gzip
import io

from .Fill import Fill
from .Options import Options, Version
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

    class SvgError(Exception):
        pass


    def __init__(self):
        self._namespaces = ['xmlns="http://www.w3.org/2000/svg"']
        # another common one: 'xmlns:xlink="http://www.w3.org/1999/xlink"'
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


    def write(self, out, options):
        '''Save the drawing as an SVG to the given out stream.

        This is a low-level method: it is more convenient to use save() or
        dumps().

        It's the caller's responsibility to close the out stream if
        appropriate.
        '''
        options = options if options is not None else Options()
        nl = options.nl
        tab = options.tab
        version = options.version
        indent = '' # usually tab * n # n is nesting level
        # Always use newlines for XML declaration and DOCTYPE
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if version is Version.V_1_1:
            out.write(
                '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
                '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        else:
            raise Svg.SvgError(f'unsupported SVG version {version.value}')
        out.write(f'<svg version="{version.value}"')
        for ns in self._namespaces:
            out.write(f' {ns}')
        out.write('>\n')
        # TODO write content
        out.write('</svg>\n')
