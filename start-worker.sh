#!/bin/bash

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

# python3 manage.py build_solr_schema -c /solr_data/cobweb/conf -r cobweb
# python3 manage.py update_index

python3 manage.py archive-it

python3 manage.py update_index
