#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Fill import Fill
from .Options import Options, Version
from .Shape import Circle, Ellipse, Line, Path, Rect
from .Stroke import Stroke


class Mixin:

    Circle = Circle
    Ellipse = Ellipse
    Fill = Fill
    Line = Line
    Options = Options
    Path = Path
    Rect = Rect
    Stroke = Stroke
    Version = Version
