#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import unittest

from svg2 import Svg


class TestColor(unittest.TestCase):

    def test1(self):
        name = 'orange'
        color = Svg.Color(name)
        self.assertTrue(color.red == 0xFF and color.green == 0xA5 and
                        color.blue == 0x0 and color.alpha == 0xFF)
        self.assertEqual(name, str(color))
        self.assertEqual('#FFA500', color.rgb_html())
        self.assertEqual('#FFA500FF', color.rgba_html())
        self.assertEqual(Svg.Color('rgb(255,165,0)').rgba_html(),
                         '#FFA500FF')
        self.assertEqual(Svg.Color('rgb(100%,65%,0%)').rgb_html(),
                         '#FFA600')
        color = Svg.Color('#22CCBB')
        self.assertEqual('#22CCBB', color.rgb_html(minimize=False))
        self.assertEqual('#2CB', color.rgb_html())
        self.assertEqual('#2CB', color.name)
        self.assertEqual('#2CB', str(color))
        color = Svg.Color('#22CCBBDD')
        self.assertEqual('#22CCBBDD', color.rgba_html(minimize=False))
        self.assertEqual('#2CBD', color.rgba_html())
        self.assertEqual('#2CBD', color.name)
        self.assertEqual('#2CBD', str(color))
        bad_color = 'bad name'
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color(bad_color)
        self.assertEqual(f'invalid color: {bad_color!r}',
                         str(err.exception))
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color('rgb(0,256,0,0)')
        self.assertTrue(str(err.exception).startswith('invalid rgb value'))
        with self.assertRaises(Svg.ColorError):
            Svg.Color('rgb(0%, 101%, 0%, 1)')
        color = Svg.Color(0xFF)
        self.assertEqual(str(color), 'red')
        color = Svg.Color(0, 0xFF)
        self.assertEqual(str(color), 'lime')
        color = Svg.Color(0, 0, 0xFF)
        self.assertEqual(str(color), 'blue')
        self.assertEqual(repr(color), "Color('#00F')")
        color = Svg.Color('cyan')
        self.assertEqual(Svg.Color('aqua'), color) # synonym
        self.assertEqual(Svg.Color.CYAN, color)
        color = Svg.Color('gray')
        self.assertEqual(Svg.Color.GRAY, color)
        self.assertEqual(Svg.Color.GRAY, Svg.Color.GREY)
        self.assertEqual(Svg.Color('blue'), Svg.Color.BLUE)
        Svg.Color('rgba(0%,100%,0,0)') # mixing percent and values is fine
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color('rgb(0%,100%,0%,1.0)') # rgb has 3 values
        with self.assertRaises(Svg.ColorError) as err:
            Svg.Color('rgba(0%,100%,0%)') # rgb has 4 values
        color = Svg.Color('rgba(0%,100%,0%,1.0)')
        lime = Svg.Color.LIME
        self.assertEqual(color, lime)
        color = Svg.Color('rgb(0%,100%,0%)')
        self.assertEqual(color, lime)
        color = Svg.Color('rgb(0,255,0)')
        self.assertEqual(color, lime)
        self.assertEqual(Svg.Color('rgb(100.0%,0.0%,0.0%)'), Svg.Color.RED)
        a = Svg.Color('rgb(50%,33.33%,66.67%)')
        b = Svg.Color(255//2, 255//3, round(255 * 2/3))
        self.assertEqual(a, b)
        # TODO


if __name__ == '__main__':
    unittest.main()
