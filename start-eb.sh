#!/bin/bash
set -e

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

python3 manage.py build_solr_schema -c data/solr/cobweb/conf -r cobweb

exec uwsgi uwsgi.ini
