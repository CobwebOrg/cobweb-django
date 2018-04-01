#!/bin/bash

# python3 manage.py migrate --noinput
# python3 manage.py collectstatic --noinput

pipenv run uwsgi uwsgi.ini
