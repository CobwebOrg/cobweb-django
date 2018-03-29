#!/usr/bin/env bash

docker-compose up db solr &
npx webpack --config webpack.config.js &
pipenv run python manage.py runserver 127.0.0.1:8000
