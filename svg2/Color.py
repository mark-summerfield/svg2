#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import re

from .Common import Error


class Color(collections.namedtuple('Color', 'red green blue alpha',
                                   defaults=(0, 0, 0, 0))):
    '''A Color is represented by the four components each 0-255 in range.'''

    __slots__ = ()

    SEP = ','
    '''Change to ', ' for pretty-printing.'''

    @staticmethod
    def new(color):
        '''Returns a Color from a color name (e.g., 'blue'), hex string
        (e.g., '#F00', '#00FF73'), or style (e.g., rgb(255, 0, 0),
        rgb(100%, 0%, 0%)), or raises an Error.'''
        color_rx = re.compile(
            r'#(?P<hex>[\da-fA-F]{3,8})|'
            r'rgb\s*\((?P<rgb>\d{1,3}%?,\s*\d{1,3}%?,\s*\d{1,3}%?\s*'
            r'(?:,\s*\d{1,3}%?)?\s*)\)')
        match = color_rx.fullmatch(color)
        if match is None:
            t = _color_for_name(color)
            if t is not None:
                return Color(*t)
        else:
            h = match.group('hex')
            if h:
                if len(h) == 3:
                    h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}'
                elif len(h) == 4:
                    h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}{h[3]}{h[3]}'
                if len(h) == 6:
                    return Color(int(h[:2], 16), int(h[2:4], 16),
                                 int(h[4:6], 16))
                return Color(int(h[:2], 16), int(h[2:4], 16),
                             int(h[4:6], 16), int(h[6:8], 16))
            else:
                rgb = match.group('rgb')
                percent = '%' in rgb
                rgb = [float(x.strip(' %')) for x in rgb.split(',', 3)]
                if percent:
                    for i in range(len(rgb)):
                        rgb[i] *= _PERCENT_FACTOR
                return Color(*rgb)
        raise Error(f'invalid color: {color!r}')


    @property
    def name(self):
        name = name_for_color.get(self)
        if name is None:
            return self.hex_rgba
        return name


    @property
    def rgb_ints(self):
        return (f'rgb({self.red}{Color.SEP}{self.green}{Color.SEP}'
                f'{self.blue})')


    @property
    def rgba_ints(self):
        return (f'rgb({self.red}{Color.SEP}{self.green}{Color.SEP}'
                f'{self.blue}{Color.SEP}{self.alpha})')


    @property
    def rgb_percents(self):
        return (f'rgb({self.red/255:.0%}{Color.SEP}{self.green/255:.0%}'
                f'{Color.SEP}{self.blue/255:.0%})')


    @property
    def rgba_percents(self):
        return (f'rgb({self.red/255:.0%}{Color.SEP}{self.green/255:.0%}'
                f'{Color.SEP}{self.blue/255:.0%}{Color.SEP}'
                f'{self.alpha/255:.0%})')


    @property
    def hex_rgb(self):
        return f'#{self.red:02X}{self.green:02X}{self.blue:02X}'


    @property
    def hex_rgba(self):
        return (f'#{self.red:02X}{self.green:02X}{self.blue:02X}'
                f'{self.alpha:02X}')


def _color_for_name(name):
    if _color_for_name.d is None:
        _color_for_name.d = {v: k for k, v in name_for_color.items()}
    return _color_for_name.d.get(name.strip().replace(' ', '').lower(),
                                 None)
_color_for_name.d = None # noqa: E305


_PERCENT_FACTOR = 255 / 100

name_for_color = {
    (0x00, 0x00, 0x00, 0x0): 'black',
    (0xC0, 0xC0, 0xC0, 0x0): 'silver',
    (0x80, 0x80, 0x80, 0x0): 'grey',
    (0xFF, 0xFF, 0xFF, 0x0): 'white',
    (0x80, 0x00, 0x00, 0x0): 'maroon',
    (0xFF, 0x00, 0x00, 0x0): 'red',
    (0x80, 0x00, 0x80, 0x0): 'purple',
    (0xFF, 0x00, 0xFF, 0x0): 'magenta',
    (0x00, 0x80, 0x00, 0x0): 'green',
    (0x00, 0xFF, 0x00, 0x0): 'lime',
    (0x80, 0x80, 0x00, 0x0): 'olive',
    (0xFF, 0xFF, 0x00, 0x0): 'yellow',
    (0x00, 0x00, 0x80, 0x0): 'navy',
    (0x00, 0x00, 0xFF, 0x0): 'blue',
    (0x00, 0x80, 0x80, 0x0): 'teal',
    (0x00, 0xFF, 0xFF, 0x0): 'cyan',
    (0xFF, 0xA5, 0x00, 0x0): 'orange',
    (0xF0, 0xF8, 0xFF, 0x0): 'aliceblue',
    (0xFA, 0xEB, 0xD7, 0x0): 'antiquewhite',
    (0x7F, 0xFF, 0xD4, 0x0): 'aquamarine',
    (0xF0, 0xFF, 0xFF, 0x0): 'azure',
    (0xF5, 0xF5, 0xDC, 0x0): 'beige',
    (0xFF, 0xE4, 0xC4, 0x0): 'bisque',
    (0xFF, 0xEB, 0xCD, 0x0): 'blanchedalmond',
    (0x8A, 0x2B, 0xE2, 0x0): 'blueviolet',
    (0xA5, 0x2A, 0x2A, 0x0): 'brown',
    (0xDE, 0xB8, 0x87, 0x0): 'burlywood',
    (0x5F, 0x9E, 0xA0, 0x0): 'cadetblue',
    (0x7F, 0xFF, 0x00, 0x0): 'chartreuse',
    (0xD2, 0x69, 0x1E, 0x0): 'chocolate',
    (0xFF, 0x7F, 0x50, 0x0): 'coral',
    (0x64, 0x95, 0xED, 0x0): 'cornflowerblue',
    (0xFF, 0xF8, 0xDC, 0x0): 'cornsilk',
    (0xDC, 0x14, 0x3C, 0x0): 'crimson',
    (0x00, 0x00, 0x8B, 0x0): 'darkblue',
    (0x00, 0x8B, 0x8B, 0x0): 'darkcyan',
    (0xB8, 0x86, 0x0B, 0x0): 'darkgoldenrod',
    (0xA9, 0xA9, 0xA9, 0x0): 'darkgrey',
    (0x00, 0x64, 0x00, 0x0): 'darkgreen',
    (0xBD, 0xB7, 0x6B, 0x0): 'darkkhaki',
    (0x8B, 0x00, 0x8B, 0x0): 'darkmagenta',
    (0x55, 0x6B, 0x2F, 0x0): 'darkolivegreen',
    (0xFF, 0x8C, 0x00, 0x0): 'darkorange',
    (0x99, 0x32, 0xCC, 0x0): 'darkorchid',
    (0x8B, 0x00, 0x00, 0x0): 'darkred',
    (0xE9, 0x96, 0x7A, 0x0): 'darksalmon',
    (0x8F, 0xBC, 0x8F, 0x0): 'darkseagreen',
    (0x48, 0x3D, 0x8B, 0x0): 'darkslateblue',
    (0x2F, 0x4F, 0x4F, 0x0): 'darkslategrey',
    (0x00, 0xCE, 0xD1, 0x0): 'darkturquoise',
    (0x94, 0x00, 0xD3, 0x0): 'darkviolet',
    (0xFF, 0x14, 0x93, 0x0): 'deeppink',
    (0x00, 0xBF, 0xFF, 0x0): 'deepskyblue',
    (0x69, 0x69, 0x69, 0x0): 'dimgrey',
    (0x1E, 0x90, 0xFF, 0x0): 'dodgerblue',
    (0xB2, 0x22, 0x22, 0x0): 'firebrick',
    (0xFF, 0xFA, 0xF0, 0x0): 'floralwhite',
    (0x22, 0x8B, 0x22, 0x0): 'forestgreen',
    (0xDC, 0xDC, 0xDC, 0x0): 'gainsboro',
    (0xF8, 0xF8, 0xFF, 0x0): 'ghostwhite',
    (0xFF, 0xD7, 0x00, 0x0): 'gold',
    (0xDA, 0xA5, 0x20, 0x0): 'goldenrod',
    (0xAD, 0xFF, 0x2F, 0x0): 'greenyellow',
    (0xF0, 0xFF, 0xF0, 0x0): 'honeydew',
    (0xFF, 0x69, 0xB4, 0x0): 'hotpink',
    (0xCD, 0x5C, 0x5C, 0x0): 'indianred',
    (0x4B, 0x00, 0x82, 0x0): 'indigo',
    (0xFF, 0xFF, 0xF0, 0x0): 'ivory',
    (0xF0, 0xE6, 0x8C, 0x0): 'khaki',
    (0xE6, 0xE6, 0xFA, 0x0): 'lavender',
    (0xFF, 0xF0, 0xF5, 0x0): 'lavenderblush',
    (0x7C, 0xFC, 0x00, 0x0): 'lawngreen',
    (0xFF, 0xFA, 0xCD, 0x0): 'lemonchiffon',
    (0xAD, 0xD8, 0xE6, 0x0): 'lightblue',
    (0xF0, 0x80, 0x80, 0x0): 'lightcoral',
    (0xE0, 0xFF, 0xFF, 0x0): 'lightcyan',
    (0xFA, 0xFA, 0xD2, 0x0): 'lightgoldenrodyellow',
    (0xD3, 0xD3, 0xD3, 0x0): 'lightgrey',
    (0x90, 0xEE, 0x90, 0x0): 'lightgreen',
    (0xFF, 0xB6, 0xC1, 0x0): 'lightpink',
    (0xFF, 0xA0, 0x7A, 0x0): 'lightsalmon',
    (0x20, 0xB2, 0xAA, 0x0): 'lightseagreen',
    (0x87, 0xCE, 0xFA, 0x0): 'lightskyblue',
    (0x77, 0x88, 0x99, 0x0): 'lightslategrey',
    (0xB0, 0xC4, 0xDE, 0x0): 'lightsteelblue',
    (0xFF, 0xFF, 0xE0, 0x0): 'lightyellow',
    (0x32, 0xCD, 0x32, 0x0): 'limegreen',
    (0xFA, 0xF0, 0xE6, 0x0): 'linen',
    (0x66, 0xCD, 0xAA, 0x0): 'mediumaquamarine',
    (0x00, 0x00, 0xCD, 0x0): 'mediumblue',
    (0xBA, 0x55, 0xD3, 0x0): 'mediumorchid',
    (0x93, 0x70, 0xDB, 0x0): 'mediumpurple',
    (0x3C, 0xB3, 0x71, 0x0): 'mediumseagreen',
    (0x7B, 0x68, 0xEE, 0x0): 'mediumslateblue',
    (0x00, 0xFA, 0x9A, 0x0): 'mediumspringgreen',
    (0x48, 0xD1, 0xCC, 0x0): 'mediumturquoise',
    (0xC7, 0x15, 0x85, 0x0): 'mediumvioletred',
    (0x19, 0x19, 0x70, 0x0): 'midnightblue',
    (0xF5, 0xFF, 0xFA, 0x0): 'mintcream',
    (0xFF, 0xE4, 0xE1, 0x0): 'mistyrose',
    (0xFF, 0xE4, 0xB5, 0x0): 'moccasin',
    (0xFF, 0xDE, 0xAD, 0x0): 'navajowhite',
    (0xFD, 0xF5, 0xE6, 0x0): 'oldlace',
    (0x6B, 0x8E, 0x23, 0x0): 'olivedrab',
    (0xFF, 0x45, 0x00, 0x0): 'orangered',
    (0xDA, 0x70, 0xD6, 0x0): 'orchid',
    (0xEE, 0xE8, 0xAA, 0x0): 'palegoldenrod',
    (0x98, 0xFB, 0x98, 0x0): 'palegreen',
    (0xAF, 0xEE, 0xEE, 0x0): 'paleturquoise',
    (0xDB, 0x70, 0x93, 0x0): 'palevioletred',
    (0xFF, 0xEF, 0xD5, 0x0): 'papayawhip',
    (0xFF, 0xDA, 0xB9, 0x0): 'peachpuff',
    (0xCD, 0x85, 0x3F, 0x0): 'peru',
    (0xFF, 0xC0, 0xCB, 0x0): 'pink',
    (0xDD, 0xA0, 0xDD, 0x0): 'plum',
    (0xB0, 0xE0, 0xE6, 0x0): 'powderblue',
    (0xBC, 0x8F, 0x8F, 0x0): 'rosybrown',
    (0x41, 0x69, 0xE1, 0x0): 'royalblue',
    (0x8B, 0x45, 0x13, 0x0): 'saddlebrown',
    (0xFA, 0x80, 0x72, 0x0): 'salmon',
    (0xF4, 0xA4, 0x60, 0x0): 'sandybrown',
    (0x2E, 0x8B, 0x57, 0x0): 'seagreen',
    (0xFF, 0xF5, 0xEE, 0x0): 'seashell',
    (0xA0, 0x52, 0x2D, 0x0): 'sienna',
    (0x87, 0xCE, 0xEB, 0x0): 'skyblue',
    (0x6A, 0x5A, 0xCD, 0x0): 'slateblue',
    (0x70, 0x80, 0x90, 0x0): 'slategrey',
    (0xFF, 0xFA, 0xFA, 0x0): 'snow',
    (0x00, 0xFF, 0x7F, 0x0): 'springgreen',
    (0x46, 0x82, 0xB4, 0x0): 'steelblue',
    (0xD2, 0xB4, 0x8C, 0x0): 'tan',
    (0xD8, 0xBF, 0xD8, 0x0): 'thistle',
    (0xFF, 0x63, 0x47, 0x0): 'tomato',
    (0x40, 0xE0, 0xD0, 0x0): 'turquoise',
    (0xEE, 0x82, 0xEE, 0x0): 'violet',
    (0xF5, 0xDE, 0xB3, 0x0): 'wheat',
    (0xF5, 0xF5, 0xF5, 0x0): 'whitesmoke',
    (0x9A, 0xCD, 0x32, 0x0): 'yellowgreen',
    (0x66, 0x33, 0x99, 0x0): 'rebeccapurple',
    }