#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


@enum.unique
class FontWeight(enum.IntEnum):
    NORMAL = 400
    BOLD = 700


class FontFace:

    def __init__(self, desc_or_family, size='1em', *,
                 weight=FontWeight.BOLD, italic=False):
        pass
        # TODO desc_or_family is either e.g., 'Times Roman 12pt bold' or
        # 'Times Roman' with size and optionally weight and italic also
        # passed (similar to Color).
