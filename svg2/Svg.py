#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from . import SvgCommonMixin, SvgWriteMixin


class Svg(SvgCommonMixin.Mixin, SvgWriteMixin.Mixin): # Class and namespace

    def __init__(self, title=None, desc=None, *, stylesheet=None):
        self.title = title
        self.desc = desc
        self.stylesheet = stylesheet
        self._namespaces = ['xmlns="http://www.w3.org/2000/svg"']
        # another common one: 'xmlns:xlink="http://www.w3.org/1999/xlink"'
        # TODO add automatically as needed or provide an API?
        self._shapes = []


    def __iadd__(self, shape):
        self._shapes.append(shape)
