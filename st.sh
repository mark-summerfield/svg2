#!/bin/bash
tokei -f -tPython
unrecognized.py -q demo_svg2.py svg2/*.py
python3 -m flake8 demo_svg2.py svg2/*.py \
    | grep -v __init__.py.*imported.but.unused
python3 -m vulture demo_svg2.py svg2/*.py 
git st
