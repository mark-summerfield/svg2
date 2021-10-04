#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import unittest

from svg2 import Svg


class TestColor(unittest.TestCase):

    def test_new(self):
        color = Svg.Color.new('orange')
        self.assertTrue(color.red == 0xFF and color.green == 0xA5 and
                        color.blue == 0x0 and color.alpha == 0x0)
        # TODO


if __name__ == '__main__':
    unittest.main()
