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
    # svg1 = svg2.Svg1(..., svg2.SOME_CONST) # API usage for SVG 1.1 2nd ed
    # svg = svg2.Svg(..., svg2.SOME_CONST) # API usage for SVG 2
    

if __name__ == '__main__':
    main()
