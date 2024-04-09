#!/bin/bash

ls /usr/bin/python*
ls /usr/bin/pip*

python --version
pip --version

pip install pytest
pip install -r test_requirements.txt

echo "WORKING DIR $(pwd)"

git fetch

pytest


