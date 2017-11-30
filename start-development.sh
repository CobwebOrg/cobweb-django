#!/bin/bash
set -e

pip3 freeze > requirements-frozen.txt
python3 manage.py runserver 0.0.0.0:8000
