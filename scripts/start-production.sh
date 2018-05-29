#!/bin/bash

python3 manage.py migrate --noinput
# python3 manage.py collectstatic --noinput

uwsgi uwsgi.ini
