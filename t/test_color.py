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
                        color.blue == 0x0 and color.alpha == 0xFF)
        self.assertEqual(name, color.name)
        self.assertEqual('#FFA500', color.rgb_html())
        self.assertEqual('#FFA500FF', color.rgba_html())
        self.assertEqual(Svg.Color('rgb(255,165,0)').rgba_html(),
                         '#FFA500FF')
        self.assertEqual(Svg.Color('rgb(100%,65%,0%)').rgb_html(),
                         '#FFA600')
        color = Svg.Color('#22CCBB')
        self.assertEqual('#22CCBB', color.rgb_html(minimize=False))
        self.assertEqual('#2CB', color.rgb_html())
        self.assertEqual('#2CBF', color.name)
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
            Svg.Color('rgb(0%, 101%, 0%, 0%)')
        color = Svg.Color(0xFF)
        self.assertEqual(color.name, 'red')
        color = Svg.Color(0, 0xFF)
        self.assertEqual(color.name, 'lime')
        color = Svg.Color(0, 0, 0xFF)
        self.assertEqual(color.name, 'blue')
        color = Svg.Color('cyan')
        self.assertEqual(Svg.Color('aqua'), color) # synonym
        self.assertEqual(Svg.Color.CYAN, color)
        color = Svg.Color('gray')
        self.assertEqual(Svg.Color.GRAY, color)
        self.assertEqual(Svg.Color.GRAY, Svg.Color.GREY)
        self.assertEqual(Svg.Color('blue'), Svg.Color.BLUE)
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color('rgb(0%,100%,0,0)') # mixing percent and values
        color = Svg.Color('rgb(0%,100%,0%,100%)')
        lime = Svg.Color.LIME
        self.assertEqual(color, lime)
        color = Svg.Color('rgb(0%,100%,0%)')
        self.assertEqual(color, lime)
        color = Svg.Color('rgb(0,255,0)')
        self.assertEqual(color, lime)
        # TODO


if __name__ == '__main__':
    unittest.main()
