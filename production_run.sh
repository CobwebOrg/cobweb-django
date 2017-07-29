#!/bin/bash

cd /code
python3 manage.py collectstatic --noinput
python3 manage.py migrate
uwsgi --ini uwsgi.ini