#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import enum


@enum.unique
class Version(enum.Enum):
    V_1_1 = '1.1'
    V_2_0 = '2'


class Options(collections.namedtuple(
              'Options', 'use_style coord_comma sep nl tab version',
              defaults=(True, False, '', '', '', Version.V_1_1))):
    '''Options used for `Svg.save()` (`Svg.dump()`), `Svg.dumps()` and
    `Svg.write()`.
    If `use_style` is `True` (the default) where possible stroke and fill
    will be set in a `style="..."` attribute rather than as individual
    attributes (`stroke="..." fill-opacity="...").
    If `coord_comma` is `False` (the default) coordinates are separated by
    spaces. If it's `True` then a comma is placed between each coordinate of
    a coordinate pair and the coordinate pairs are separated by spaces.
    The `sep` is `''` by default and is used between style colons and after
    style semi-colons. For example with `sep=''`:
        style="stroke:blue;stroke-width:1.5;fill:red"
    whereas with `sep=' '`:
        style="stroke: blue; stroke-width: 1.5; fill: red"
    The `nl` is used for newlines and defaults to `''`, so normally the only
    newlines used follow the `<?xml...` and `<DOCTYPE...` lines. use
    `nl='\\n' for a newline after each tagged item.
    The `tab` is used as the indent at each level and defaults to `''`, so
    normally there is no indent. This only makes sense if `nl='\\n'`, in
    which case use `tab='  '` or similar.

    Use `Options()` (or just accept the default of `None` which will do the
    same) to get the most compact XML possible.

    Use `Options.pretty()` to get sensible defaults for human readability.
    '''

    @staticmethod
    def pretty(*, use_style=True, coord_comma=True, sep=' ', nl='\n',
               tab='  ', version=Version.V_1_1):
        return Options(use_style, coord_comma, sep, nl, tab, version)
