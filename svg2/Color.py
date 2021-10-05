#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import re


class Color(int):
    '''Holds an RGBA color with each component 0-255 in a single int.'''

    __slots__ = ()

    def __new__(Class, color_or_red, green=0, blue=0, alpha=255):
        '''Returns a Color or raises a ColorError.

        The color is specified as a single string, e.g.,
            color = Svg.Color('#E4C')
            color = Svg.Color('#00F0073')
            color = Svg.Color('rgb(255, 0, 0)')
            color = Svg.Color('rgb(38, 180, 0, 220)')
            color = Svg.Color('rgb(100%, 33.33%, 66.67%)')
            color = Svg.Color('orange')
        or as 1-3 RGB numbers, or 4 RGBA numbers (all 0-255), e.g.,
            color = Svg.Color(255) # green and blue default to 0;
                                   # alpha to 255
            color = Svg.Color(0, 0x7F, 0, 0x7F)
        or raises a ColorError.

        For convenience all named colors are predefined, e.g.:
            Svg.Color('blue') == Svg.Color.BLUE
        '''
        if isinstance(color_or_red, int):
            if (0 <= color_or_red < 256 and 0 <= green < 256 and
                    0 <= blue < 256 and 0 <= alpha < 256):
                return super().__new__(
                    Class, _int_for_rgba(color_or_red, green, blue, alpha))
            raise ColorError(f'out of range color value: ({color_or_red!r},'
                             f'{green!r},{blue!r},{alpha!r})')
        color_rx = re.compile(
            r'#(?P<hex>[\da-fA-F]{3,8})|'
            r'rgb\s*\((?P<rgb>\d{1,3}(:?(:?\.\d+)?%)?,'
            r'\s*\d{1,3}(:?(:?\.\d+)?%)?,\s*\d{1,3}(:?(:?\.\d+)?%)?\s*'
            r'(?:,\s*\d{1,3}(:?(:?\.\d+)?%)?)?\s*)\)')
        match = color_rx.fullmatch(color_or_red)
        if match is None:
            t = _color_for_name(color_or_red)
            if t is not None:
                return super().__new__(Class, _int_for_rgba(*t))
        else:
            h = match.group('hex')
            if h:
                if len(h) == 3:
                    h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}'
                elif len(h) == 4:
                    h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}{h[3]}{h[3]}'
                if len(h) == 6:
                    return super().__new__(
                        Class,
                        _int_for_rgba(int(h[:2], 16), int(h[2:4], 16),
                                      int(h[4:6], 16)))
                return super().__new__(
                    Class, _int_for_rgba(int(h[:2], 16), int(h[2:4], 16),
                                         int(h[4:6], 16), int(h[6:8], 16)))
            else:
                rgb = match.group('rgb')
                percents = '%' in rgb
                factor = (255 / 100.0) if percents else 1
                parts = []
                for v in rgb.split(',', 3):
                    if percents and '%' not in v:
                        raise ColorError(
                            'rgb colors must be all values or all '
                            f'percentages: {color_or_red!r}')
                    n = round(float(v.strip(' %')) * factor)
                    if not (0 <= n < 256):
                        raise ColorError(
                            f'out of range color value: {color_or_red!r}')
                    parts.append(n)
                return super().__new__(Class, _int_for_rgba(*parts))
        raise ColorError(f'invalid color: {color_or_red!r}')


    def __repr__(self):
        h = self.rgb_html() if self.alpha == 255 else self.rgba_html()
        return f'Color({h!r})'


    def __str__(self):
        if self.alpha != 255:
            return self.rgba_html()
        name = _NAME_FOR_COLOR.get((self.red, self.green, self.blue))
        return name or self.rgba_html()


    @property
    def red(self):
        return (self & 0xFF000000) >> 24


    @property
    def green(self):
        return (self & 0x00FF0000) >> 16


    @property
    def blue(self):
        return (self & 0x0000FF00) >> 8


    @property
    def alpha(self):
        return self & 0x000000FF


    @property
    def rgb(self):
        return Rgb(self.red, self.green, self.blue)


    @property
    def rgba(self):
        return Rgba(self.red, self.green, self.blue, self.alpha)


    def rgb_html(self, *, minimize=True):
        '''Use minimize=True (the default) to produce 3 hex digits when
        possible; use minimize=False to guarantee 6 hex digits in all
        cases.'''
        r = f'{self.red:02X}'
        g = f'{self.green:02X}'
        b = f'{self.blue:02X}'
        if (minimize and (r[0] == r[1]) and (g[0] == g[1]) and
                (b[0] == b[1])):
            return f'#{r[0]}{g[0]}{b[0]}'
        return f'#{r}{g}{b}'


    def rgba_html(self, *, minimize=True):
        '''Use minimize=True (the default) to produce 4 hex digits when
        possible; use minimize=False to guarantee 8 hex digits in all
        cases.'''
        r = f'{self.red:02X}'
        g = f'{self.green:02X}'
        b = f'{self.blue:02X}'
        a = f'{self.alpha:02X}'
        if (minimize and (r[0] == r[1]) and (g[0] == g[1]) and
                (b[0] == b[1]) and (a[0] == a[1])):
            return f'#{r[0]}{g[0]}{b[0]}{a[0]}'
        return f'#{r}{g}{b}{a}'


    def rgb_css(self, *, sep=','):
        '''Use sep=', ' for a pretty-printing string.'''
        return (f'rgb({self.red}{sep}{self.green}{sep}{self.blue})')


    def rgba_css(self, *, sep=','):
        '''Use sep=', ' for a pretty-printing string.'''
        return (f'rgb({self.red}{sep}{self.green}{sep}{self.blue}{sep}'
                f'{self.alpha})')


Rgb = collections.namedtuple('Rgb', 'red green blue')
Rgba = collections.namedtuple('Rgba', 'red green blue alpha')


class ColorError(Exception):
    pass


def _int_for_rgba(red, green, blue, alpha=255):
    return (red << 24) + (green << 16) + (blue << 8) + alpha


def _color_for_name(name):
    if _color_for_name.d is None:
        _color_for_name.d = {v: k for k, v in _NAME_FOR_COLOR.items()}
        _color_for_name.d['aqua'] = (0x00, 0xFF, 0xFF) # synonyms
        _color_for_name.d['fuchsia'] = (0xFF, 0x00, 0xFF)
        _color_for_name.d['gray'] = (0x80, 0x80, 0x80)
        _color_for_name.d['darkgray'] = (0xA9, 0xA9, 0xA9)
        _color_for_name.d['darkslategray'] = (0x2F, 0x4F, 0x4F)
        _color_for_name.d['dimgray'] = (0x69, 0x69, 0x69)
        _color_for_name.d['lightgray'] = (0xD3, 0xD3, 0xD3)
        _color_for_name.d['lightslategray'] = (0x77, 0x88, 0x99)
        _color_for_name.d['slategray'] = (0x70, 0x80, 0x90)
    return _color_for_name.d.get(name.strip().replace(' ', '').lower(),
                                 None)
_color_for_name.d = None # noqa: E305


_NAME_FOR_COLOR = {
    (0x00, 0x00, 0x00): 'black',
    (0xC0, 0xC0, 0xC0): 'silver',
    (0x80, 0x80, 0x80): 'grey',
    (0xFF, 0xFF, 0xFF): 'white',
    (0x80, 0x00, 0x00): 'maroon',
    (0xFF, 0x00, 0x00): 'red',
    (0x80, 0x00, 0x80): 'purple',
    (0xFF, 0x00, 0xFF): 'magenta',
    (0x00, 0x80, 0x00): 'green',
    (0x00, 0xFF, 0x00): 'lime',
    (0x80, 0x80, 0x00): 'olive',
    (0xFF, 0xFF, 0x00): 'yellow',
    (0x00, 0x00, 0x80): 'navy',
    (0x00, 0x00, 0xFF): 'blue',
    (0x00, 0x80, 0x80): 'teal',
    (0x00, 0xFF, 0xFF): 'cyan',
    (0xFF, 0xA5, 0x00): 'orange',
    (0xF0, 0xF8, 0xFF): 'aliceblue',
    (0xFA, 0xEB, 0xD7): 'antiquewhite',
    (0x7F, 0xFF, 0xD4): 'aquamarine',
    (0xF0, 0xFF, 0xFF): 'azure',
    (0xF5, 0xF5, 0xDC): 'beige',
    (0xFF, 0xE4, 0xC4): 'bisque',
    (0xFF, 0xEB, 0xCD): 'blanchedalmond',
    (0x8A, 0x2B, 0xE2): 'blueviolet',
    (0xA5, 0x2A, 0x2A): 'brown',
    (0xDE, 0xB8, 0x87): 'burlywood',
    (0x5F, 0x9E, 0xA0): 'cadetblue',
    (0x7F, 0xFF, 0x00): 'chartreuse',
    (0xD2, 0x69, 0x1E): 'chocolate',
    (0xFF, 0x7F, 0x50): 'coral',
    (0x64, 0x95, 0xED): 'cornflowerblue',
    (0xFF, 0xF8, 0xDC): 'cornsilk',
    (0xDC, 0x14, 0x3C): 'crimson',
    (0x00, 0x00, 0x8B): 'darkblue',
    (0x00, 0x8B, 0x8B): 'darkcyan',
    (0xB8, 0x86, 0x0B): 'darkgoldenrod',
    (0xA9, 0xA9, 0xA9): 'darkgrey',
    (0x00, 0x64, 0x00): 'darkgreen',
    (0xBD, 0xB7, 0x6B): 'darkkhaki',
    (0x8B, 0x00, 0x8B): 'darkmagenta',
    (0x55, 0x6B, 0x2F): 'darkolivegreen',
    (0xFF, 0x8C, 0x00): 'darkorange',
    (0x99, 0x32, 0xCC): 'darkorchid',
    (0x8B, 0x00, 0x00): 'darkred',
    (0xE9, 0x96, 0x7A): 'darksalmon',
    (0x8F, 0xBC, 0x8F): 'darkseagreen',
    (0x48, 0x3D, 0x8B): 'darkslateblue',
    (0x2F, 0x4F, 0x4F): 'darkslategrey',
    (0x00, 0xCE, 0xD1): 'darkturquoise',
    (0x94, 0x00, 0xD3): 'darkviolet',
    (0xFF, 0x14, 0x93): 'deeppink',
    (0x00, 0xBF, 0xFF): 'deepskyblue',
    (0x69, 0x69, 0x69): 'dimgrey',
    (0x1E, 0x90, 0xFF): 'dodgerblue',
    (0xB2, 0x22, 0x22): 'firebrick',
    (0xFF, 0xFA, 0xF0): 'floralwhite',
    (0x22, 0x8B, 0x22): 'forestgreen',
    (0xDC, 0xDC, 0xDC): 'gainsboro',
    (0xF8, 0xF8, 0xFF): 'ghostwhite',
    (0xFF, 0xD7, 0x00): 'gold',
    (0xDA, 0xA5, 0x20): 'goldenrod',
    (0xAD, 0xFF, 0x2F): 'greenyellow',
    (0xF0, 0xFF, 0xF0): 'honeydew',
    (0xFF, 0x69, 0xB4): 'hotpink',
    (0xCD, 0x5C, 0x5C): 'indianred',
    (0x4B, 0x00, 0x82): 'indigo',
    (0xFF, 0xFF, 0xF0): 'ivory',
    (0xF0, 0xE6, 0x8C): 'khaki',
    (0xE6, 0xE6, 0xFA): 'lavender',
    (0xFF, 0xF0, 0xF5): 'lavenderblush',
    (0x7C, 0xFC, 0x00): 'lawngreen',
    (0xFF, 0xFA, 0xCD): 'lemonchiffon',
    (0xAD, 0xD8, 0xE6): 'lightblue',
    (0xF0, 0x80, 0x80): 'lightcoral',
    (0xE0, 0xFF, 0xFF): 'lightcyan',
    (0xFA, 0xFA, 0xD2): 'lightgoldenrodyellow',
    (0xD3, 0xD3, 0xD3): 'lightgrey',
    (0x90, 0xEE, 0x90): 'lightgreen',
    (0xFF, 0xB6, 0xC1): 'lightpink',
    (0xFF, 0xA0, 0x7A): 'lightsalmon',
    (0x20, 0xB2, 0xAA): 'lightseagreen',
    (0x87, 0xCE, 0xFA): 'lightskyblue',
    (0x77, 0x88, 0x99): 'lightslategrey',
    (0xB0, 0xC4, 0xDE): 'lightsteelblue',
    (0xFF, 0xFF, 0xE0): 'lightyellow',
    (0x32, 0xCD, 0x32): 'limegreen',
    (0xFA, 0xF0, 0xE6): 'linen',
    (0x66, 0xCD, 0xAA): 'mediumaquamarine',
    (0x00, 0x00, 0xCD): 'mediumblue',
    (0xBA, 0x55, 0xD3): 'mediumorchid',
    (0x93, 0x70, 0xDB): 'mediumpurple',
    (0x3C, 0xB3, 0x71): 'mediumseagreen',
    (0x7B, 0x68, 0xEE): 'mediumslateblue',
    (0x00, 0xFA, 0x9A): 'mediumspringgreen',
    (0x48, 0xD1, 0xCC): 'mediumturquoise',
    (0xC7, 0x15, 0x85): 'mediumvioletred',
    (0x19, 0x19, 0x70): 'midnightblue',
    (0xF5, 0xFF, 0xFA): 'mintcream',
    (0xFF, 0xE4, 0xE1): 'mistyrose',
    (0xFF, 0xE4, 0xB5): 'moccasin',
    (0xFF, 0xDE, 0xAD): 'navajowhite',
    (0xFD, 0xF5, 0xE6): 'oldlace',
    (0x6B, 0x8E, 0x23): 'olivedrab',
    (0xFF, 0x45, 0x00): 'orangered',
    (0xDA, 0x70, 0xD6): 'orchid',
    (0xEE, 0xE8, 0xAA): 'palegoldenrod',
    (0x98, 0xFB, 0x98): 'palegreen',
    (0xAF, 0xEE, 0xEE): 'paleturquoise',
    (0xDB, 0x70, 0x93): 'palevioletred',
    (0xFF, 0xEF, 0xD5): 'papayawhip',
    (0xFF, 0xDA, 0xB9): 'peachpuff',
    (0xCD, 0x85, 0x3F): 'peru',
    (0xFF, 0xC0, 0xCB): 'pink',
    (0xDD, 0xA0, 0xDD): 'plum',
    (0xB0, 0xE0, 0xE6): 'powderblue',
    (0xBC, 0x8F, 0x8F): 'rosybrown',
    (0x41, 0x69, 0xE1): 'royalblue',
    (0x8B, 0x45, 0x13): 'saddlebrown',
    (0xFA, 0x80, 0x72): 'salmon',
    (0xF4, 0xA4, 0x60): 'sandybrown',
    (0x2E, 0x8B, 0x57): 'seagreen',
    (0xFF, 0xF5, 0xEE): 'seashell',
    (0xA0, 0x52, 0x2D): 'sienna',
    (0x87, 0xCE, 0xEB): 'skyblue',
    (0x6A, 0x5A, 0xCD): 'slateblue',
    (0x70, 0x80, 0x90): 'slategrey',
    (0xFF, 0xFA, 0xFA): 'snow',
    (0x00, 0xFF, 0x7F): 'springgreen',
    (0x46, 0x82, 0xB4): 'steelblue',
    (0xD2, 0xB4, 0x8C): 'tan',
    (0xD8, 0xBF, 0xD8): 'thistle',
    (0xFF, 0x63, 0x47): 'tomato',
    (0x40, 0xE0, 0xD0): 'turquoise',
    (0xEE, 0x82, 0xEE): 'violet',
    (0xF5, 0xDE, 0xB3): 'wheat',
    (0xF5, 0xF5, 0xF5): 'whitesmoke',
    (0x9A, 0xCD, 0x32): 'yellowgreen',
    (0x66, 0x33, 0x99): 'rebeccapurple',
    }

for _value, _name in _NAME_FOR_COLOR.items():
    setattr(Color, _name.upper(), Color(*_value))
for _name, _value in (('AQUA', (0x00, 0xFF, 0xFF)), # synonyms
                      ('FUCHSIA', (0xFF, 0x00, 0xFF)),
                      ('GRAY', (0x80, 0x80, 0x80)),
                      ('DARKGRAY', (0xA9, 0xA9, 0xA9)),
                      ('DARKSLATEGRAY', (0x2F, 0x4F, 0x4F)),
                      ('DIMGRAY', (0x69, 0x69, 0x69)),
                      ('LIGHTGRAY', (0xD3, 0xD3, 0xD3)),
                      ('LIGHTSLATEGRAY', (0x77, 0x88, 0x99)),
                      ('SLATEGRAY', (0x70, 0x80, 0x90))):
    setattr(Color, _name, Color(*_value))
del _value, _name
