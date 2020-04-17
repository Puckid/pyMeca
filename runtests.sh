#!/bin/bash

python -m unittest -v pyMec/tests/test_geometry.py
pylint -v pyMec/geometry.py
pylint -v pyMec/tests/test_geometry.py