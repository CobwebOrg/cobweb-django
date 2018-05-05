#!/bin/bash

python3 /code/manage.py migrate --noinput

python3 /code/manage.py archive-it

python3 /code/manage.py update_index
