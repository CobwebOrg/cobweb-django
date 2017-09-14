#!/bin/bash
set -e

python3 manage.py migrate --noinput
# python3 manage.py collectstatic --noinput
python3 manage.py archive-it
python3 manage.py ait-resources.py &

exec uwsgi uwsgi.ini
