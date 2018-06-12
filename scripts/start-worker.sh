#!/bin/bash

python3 /code/manage.py migrate --noinput
sleep 1m
python3 /code/manage.py update_index
# python3 /code/manage.py archive-it

