#!/bin/bash

pipenv run manage.py migrate --noinput
# pipenv run manage.py collectstatic --noinput

pipenv run manage.py build_solr_schema -c /solr_data/cobweb/conf -r cobweb
# pipenv run manage.py update_index

pipenv run manage.py archive-it

pipenv run manage.py update_index
