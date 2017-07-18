#!/bin/sh
python3 manage.py makemigrations registry
python3 manage.py migrate
exec "$@"