#!/bin/bash

sudo add-apt-repository universe
sudo apt update
sudo apt-get install -y python3.11
#sudo apt-get install -y python3.11-pip
#curl https://bootstrap.pypa.io/pip/get-pip.py --output get-pip.py
#sudo python3.11 get-pip.py

python3.11 -m ensurepip

ls /usr/bin/python*
ls /usr/bin/pip*

python3.11 --version
pip3.11 --version

pip3.11 install pytest
pip3.11 install -r test_requirements.txt

echo "WORKING DIR $(pwd)"

git fetch

ls /usr/bin/*pytest*
ls /usr/local/bin/*pytest*

pytest --version
pytest

