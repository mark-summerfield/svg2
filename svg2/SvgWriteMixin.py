#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import gzip
import io

from .Options import Options, Version


class Mixin:

    def save(self, filename, *, options=None):
        '''Saves the drawing as an SVG file to the given `filename`.

        The file will be compressed if `filename` ends `.svgz` or `.svg.gz`.
        The `options` defaults to `Svg.Options()`; for human readability
        use `options=Svg.Options.pretty()`.

        This method has an alias, dump().

        See also dumps() and write().
        '''
        opener = (gzip.open
                  if filename[-7:].upper().endswith(('.SVGZ', '.SVG.GZ'))
                  else open)
        with opener(filename, 'wt', encoding='utf-8') as file:
            self.write(file, options if options is not None else Options())


    dump = save # dump is more Pythonic; save is more meaningful


    def dumps(self, *, options=None):
        '''Returns the drawing as a string of SVG.

        The `options` defaults to `Svg.Options()`; for human readability
        use `options=Svg.Options.pretty()`.

        See also save(), and write().
        '''
        out = io.StringIO()
        try:
            self.write(out, options if options is not None else Options())
            return out.getvalue()
        finally:
            out.close()


    def write(self, out, options):
        '''Saves the drawing as a string of SVG to the given `out` stream.

        This is a low-level method: it is more convenient to use `save()` or
        `dumps()` (or `dump()`).

        `out` should be file-like writable; `options` should be an
        `Svg.Options` object.

        It's the caller's responsibility to close the `out` stream if
        appropriate.
        '''
        nl = options.nl
        tab = options.tab
        version = options.version
        indent = '' # usually tab * n # n is nesting level
        # Always use newlines for XML declaration and DOCTYPE (ignoring nl)
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if version is Version.V_1_1:
            out.write(
                '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
                '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        else:
            raise self.Error(f'unsupported SVG version {version.value}')
        out.write(f'<svg version="{version.value}"')
        for ns in self._namespaces:
            out.write(f' {ns}')
        # TODO write any other <svg> attributes, e.g., x, y, width, height,
        # viewBox, etc.
        out.write('>\n')
        # TODO write content
        out.write('</svg>\n')