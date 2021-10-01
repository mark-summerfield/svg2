#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


# Minimum:
#   <svg xmlns="http://www.w3.org/2000/svg">...</svg>
# This tag supports other attributes, e.g., version, width, height, viewBox,
# preserveAspectRatio, and _many_ more.
#
# XML_NAMESPACE = 'http://www.w3.org/2000/svg' # enum?

@enum.unique
class Version(enum.Enum):
    SVG_1_1 = '1.1' # 2nd edition
    SVG_2_0 = '2'
