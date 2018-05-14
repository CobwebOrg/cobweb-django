#!/bin/bash
set -e

pipenv install --dev --system --ignore-pipfile
python3 manage.py runserver 0.0.0.0:8000
