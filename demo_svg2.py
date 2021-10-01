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
    print(svg2.__version__)
    # svg = svg2.Svg(..., svg2.SOME_CONST) # API usage
    

if __name__ == '__main__':
    main()
