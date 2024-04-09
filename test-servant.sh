#!/bin/bash

python --version
pip --version
pip install pytest
pip install -r test_requirements.txt

echo "WORKING DIR $(pwd)"

git fetch

pytest


