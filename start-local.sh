#!/usr/bin/env bash

docker-compose up db solr node &
pipenv run python manage.py runserver 127.0.0.1:8000
