#!/bin/bash
cd svg2
tokei -slines -f -tPython
cd ..
unrecognized.py -q demo_svg2.py svg2/*.py
python3 -m flake8 \
    --ignore=E261,E303,W504 \
    demo_svg2.py svg2/*.py \
    | grep -v __init__.py.*imported.but.unused
python3 -m vulture demo_svg2.py svg2/*.py 
./t.py $@
git st
