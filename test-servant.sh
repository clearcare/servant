#!/bin/bash

pip install -r test_requirements.txt

echo "WORKING DIR $(pwd)"

git fetch

pytest

