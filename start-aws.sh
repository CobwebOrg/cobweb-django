#!/bin/bash

pip install -r requirements.txt

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

python3 manage.py build_solr_schema -c data/solr/cobweb/conf -r cobweb
python3 manage.py update_index

exec uwsgi uwsgi.ini
