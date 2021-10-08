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
        'Options', 'nl indent sep decimals version',
        defaults=('', '', ',', 0, Version.V_1_1))):

    @staticmethod
    def pretty(*, nl='\n', indent='  ', sep=', ', decimals=2,
               version=Version.V_1_1):
        return Options(nl, indent, sep, decimals, version)
