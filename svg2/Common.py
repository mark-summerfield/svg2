#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import enum


@enum.unique
class Version(enum.Enum):
    V_1_1 = '1.1'
    V_2_0 = '2'
