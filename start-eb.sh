#!/bin/bash
set -e

python3 manage.py migrate --noinput
# python3 manage.py collectstatic --noinput
python3 manage.py archive-it&

exec uwsgi uwsgi.ini
