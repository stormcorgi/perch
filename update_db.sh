#!/bin/bash

cd /home/pirate/git/perch
rm -f ./perch.db
source ./venv/bin/activate
python ./perchdb.py