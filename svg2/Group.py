#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

class Group:

    def __init__(self, id):
        self.id = id
        self._items = []


    def svg(self, indent, options):
        nl = options.nl
        parts = [f'<g id="{self.id}">']
        indent += options.tab
        for item in self._items:
            parts.append(item.svg(indent, options))
        parts.append(f'</g>{nl}')
        return f'{nl}'.join(parts)
