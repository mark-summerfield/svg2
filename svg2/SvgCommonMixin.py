#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

from .Error import Error
from .Fill import Fill
from .Options import Options, Version
from .Shape import Circle, Ellipse, Line, Path, Polygon, Polyline, Rect
from .Stroke import Stroke


class Mixin:

    Circle = Circle
    Ellipse = Ellipse
    Error = Error
    Fill = Fill
    Line = Line
    Options = Options
    Path = Path
    Polygon = Polygon
    Polyline = Polyline
    Rect = Rect
    Stroke = Stroke
    Version = Version
