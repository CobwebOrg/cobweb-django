#!/bin/bash
set -e

pipenv install --dev
pipenv run python3 manage.py runserver 0.0.0.0:8000
