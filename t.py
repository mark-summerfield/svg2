#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import unittest

from svg2 import Color, ColorError, Svg


class TestSvg(unittest.TestCase):

    def test_version(self):
        self.assertEqual(Svg.Version.V_1_1.name, 'V_1_1')
        self.assertEqual(Svg.Version.V_2_0.name, 'V_2_0')
        self.assertNotEqual(Svg.Version.V_2_0, Svg.Version.V_1_1)


    def test_color1(self):
        name = 'orange'
        color = Color(name)
        self.assertTrue(color.red == 0xFF and color.green == 0xA5 and
                        color.blue == 0x0 and color.alpha == 0xFF)
        self.assertEqual(name, str(color))
        self.assertEqual('#FFA500', color.rgb_html())
        self.assertEqual('#FFA500FF', color.rgba_html())
        self.assertEqual(Color('rgb(255,165,0)').rgba_html(),
                         '#FFA500FF')
        self.assertEqual(Color('rgb(100%,65%,0%)').rgb_html(),
                         '#FFA600')
        color = Color('#22CCBB')
        self.assertEqual('#22CCBB', color.rgb_html(minimize=False))
        self.assertEqual('#2CB', color.rgb_html())
        self.assertEqual('#2CB', color.name)
        self.assertEqual('#2CB', str(color))
        color = Color('#22CCBBDD')
        self.assertEqual('#22CCBBDD', color.rgba_html(minimize=False))
        self.assertEqual('#2CBD', color.rgba_html())
        self.assertEqual('#2CBD', color.name)
        self.assertEqual('#2CBD', str(color))
        bad_color = 'bad name'
        with self.assertRaises(ColorError) as err:
            Color(bad_color)
        self.assertEqual(f'invalid color: {bad_color!r}',
                         str(err.exception))
        with self.assertRaises(ColorError) as err:
            Color('rgb(0,256,0,0)')
        self.assertTrue(str(err.exception).startswith('invalid rgb value'))
        with self.assertRaises(ColorError):
            Color('rgb(0%, 101%, 0%, 1)')
        color = Color(0xFF)
        self.assertEqual(str(color), 'red')
        color = Color(0, 0xFF)
        self.assertEqual(str(color), 'lime')
        color = Color(0, 0, 0xFF)
        self.assertEqual(str(color), 'blue')
        self.assertEqual(repr(color), "Color('#00F')")
        color = Color('cyan')
        self.assertEqual(Color('aqua'), color) # synonym
        self.assertEqual(Color.CYAN, color)
        color = Color('gray')
        self.assertEqual(Color.GRAY, color)
        self.assertEqual(Color.GRAY, Color.GREY)
        self.assertEqual(Color('blue'), Color.BLUE)
        Color('rgba(0%,100%,0,0)') # mixing percent and values is fine
        with self.assertRaises(ColorError) as err:
            Color('rgb(0%,100%,0%,1.0)') # rgb has 3 values
        with self.assertRaises(ColorError) as err:
            Color('rgba(0%,100%,0%)') # rgb has 4 values
        color = Color('rgba(0%,100%,0%,1.0)')
        lime = Color.LIME
        self.assertEqual(color, lime)
        color = Color('rgb(0%,100%,0%)')
        self.assertEqual(color, lime)
        color = Color('rgb(0,255,0)')
        self.assertEqual(color, lime)
        self.assertEqual(Color('rgb(100.0%,0.0%,0.0%)'), Color.RED)
        a = Color('rgb(50%,33.33%,66.67%)')
        b = Color(255//2, 255//3, round(255 * 2/3))
        self.assertEqual(a, b)


    def test_color2(self):
        rgb = Color(0x7F, 0xA1, 0xF0)
        self.assertEqual(rgb.name, '#7FA1F0')
        self.assertEqual(str(rgb), '#7FA1F0')
        self.assertEqual(rgb.rgb_html(), '#7FA1F0')
        self.assertEqual(rgb.rgba_html(), '#7FA1F0FF')
        self.assertEqual(rgb.rgb_css(), 'rgb(127,161,240)')
        self.assertEqual(rgb.rgb_css(sep=', '), 'rgb(127, 161, 240)')
        self.assertEqual(rgb.rgb_css(sep=', ', percent=True), # decimals=2
                         'rgb(49.80%, 63.14%, 94.12%)')
        self.assertEqual(rgb.rgb_css(sep=', ', percent=True, decimals=1),
                         'rgb(49.8%, 63.1%, 94.1%)')
        self.assertEqual(rgb.rgb_css(sep=', ', percent=True, decimals=0),
                         'rgb(50%, 63%, 94%)')
        self.assertEqual(rgb, Color(rgb.name))
        self.assertEqual(rgb, Color(str(rgb)))
        self.assertEqual(rgb, Color(rgb.rgb_html()))
        self.assertEqual(rgb, Color(rgb.rgba_html()))
        self.assertEqual(rgb, Color(rgb.rgb_css()))
        self.assertEqual(rgb, Color(rgb.rgb_css(sep=', ',
                                                    percent=True)))

        rgba = Color(0x7F, 0xA1, 0xF0, 0xD0)
        self.assertEqual(rgba.name, '#7FA1F0D0')
        self.assertEqual(str(rgba), '#7FA1F0D0')
        self.assertEqual(rgba.rgba_html(), '#7FA1F0D0')
        self.assertEqual(rgba.rgba_css(sep=', '),
                         'rgba(127, 161, 240, 0.82)')
        self.assertEqual(rgba.rgba_css(sep=', ', percent=True), # decimals=2
                         'rgba(49.80%, 63.14%, 94.12%, 0.82)')
        self.assertEqual(rgba.rgba_css(sep=', ', percent=True, decimals=1),
                         'rgba(49.8%, 63.1%, 94.1%, 0.8)')
        self.assertEqual(rgba.rgba_css(sep=', ', percent=True, decimals=0),
                         'rgba(50%, 63%, 94%, 1)')
        self.assertEqual(rgba, Color(rgba.name))
        self.assertEqual(rgba, Color(str(rgba)))
        self.assertEqual(rgba, Color(rgba.rgba_html()))


    def test_color3(self):
        color = Color(0xAB, 0xCD, 0xEF)
        self.assertEqual(color.rgb, Color.Rgb(0xAb, 0xCD, 0xEF))
        color = Color(0xAB, 0xCD, 0xEF, 0x12)
        self.assertEqual(color.rgba, Color.Rgba(0xAb, 0xCD, 0xEF, 0x12))


if __name__ == '__main__':
    unittest.main()
