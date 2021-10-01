#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

try:
    import svg2
except ImportError:
    import pathlib
    import sys
    sys.path.append(pathlib.Path(__file__).resolve().parent)
    import svg2


def main():
    print(svg2.__name__, svg2.__version__)
    svg1 = svg2.Svg1() # SVG 1.1 2nd ed
    print(svg1.standard)
    svg = svg2.Svg2() # SVG 2
    print(svg.standard)


if __name__ == '__main__':
    main()
