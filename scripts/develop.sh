#!/usr/bin/env bash

docker-compose up db solr &
npx webpack --config webpack.config.js --watch &
pipenv run python manage.py runserver 127.0.0.1:8000
