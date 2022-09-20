#!/bin/bash

CURRENT_VERSION=`python -c "import pyteamtv; print(pyteamtv.__version__)"`

python setup.py sdist
python setup.py bdist_wheel

twine upload dist/pyteamtv-$CURRENT_VERSION*