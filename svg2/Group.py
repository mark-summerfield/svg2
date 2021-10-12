#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Shape import WriteMixin


class Group(WriteMixin):

    def __init__(self, id):
        self.id = id
        self._shapes = []


    def __iadd__(self, shape):
        self._shapes.append(shape)


    def svg(self, indent, options):
        parts = [f'<g id="{self.id}">']
        indent += options.tab
        for shape in self._shapes:
            parts.append(shape.svg(indent, options))
        parts.append(f'</g>{options.nl}')
        return f'{options.nl}'.join(parts)
