#!/bin/bash
set -e

pip3 freeze > requirements-frozen.txt
DJANGO_SETTINGS_MODULE=cobweb.settings.debug python3 manage.py runserver 0.0.0.0:8000
