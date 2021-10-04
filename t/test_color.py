#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import unittest

from svg2 import Svg


class TestColor(unittest.TestCase):

    def test_new(self):
        name = 'orange'
        color = Svg.Color(name)
        self.assertTrue(color.red == 0xFF and color.green == 0xA5 and
                        color.blue == 0x0 and color.alpha == 0x0)
        self.assertEqual(name, color.name)
        self.assertEqual('#FFA500', color.hex_rgb)
        self.assertEqual('#FFA50000', color.hex_rgba)
        self.assertEqual(Svg.Color('rgb(255,165,0)').hex_rgba, '#FFA50000')
        self.assertEqual(Svg.Color('rgb(100%,65%,0%)').hex_rgb, '#FFA600')
        bad_color = 'bad name'
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color(bad_color)
        self.assertEqual(f'invalid color: {bad_color!r}',
                         str(err.exception))
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color('rgb(0,256,0,0)')
        self.assertTrue(str(err.exception).startswith(
                        'out of range color value'))
        with self.assertRaises(Svg.ColorError):
            Svg.Color('rgb(0%,101%,0%,0%)')
        # TODO


if __name__ == '__main__':
    unittest.main()
