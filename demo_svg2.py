#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from svg2 import Color, Svg


def main():
    svg = Svg()
    print(svg)
    red = Color.RED
    print('red:', red, red.name, red.rgb_html(),
          red.rgb_html(minimize=False), red.rgb_css(),
          red.rgb_css(sep=', ', percent=True, decimals=0))
    assert red == Color('red') == Color(255) == Color('rgb(255,0,0)') \
        == Color('#F00') == Color('#FF0000') == Color('#FF0000FF') \
        == Color('#F00F') == Color('rgb(100%, 0%, 0%)')
    blueish = Color(0, 0, 0x7F, 255 * 0.8)
    print('blueish:', blueish, blueish.name, blueish.rgba_html(),
          blueish.rgba_html(minimize=False), blueish.rgba_css(),
          blueish.rgba_css(sep=', ', percent=True, decimals=1))
    assert blueish == Color('rgba(0,0,127,0.8)')


if __name__ == '__main__':
    main()
