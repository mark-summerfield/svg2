#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


@enum.unique
class Version(enum.Enum):
    SVG_1_1 = '1.1' # 2nd edition
    SVG_2_0 = '2'
