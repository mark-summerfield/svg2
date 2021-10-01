#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


@enum.unique
class Standard(enum.Enum):
    SVG_1_1_2E = 1
    SVG_2_0 = 2
