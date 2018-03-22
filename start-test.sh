#!/bin/bash
set -e

DJANGO_SETTINGS_MODULE=cobweb.settings.test python3 manage.py runserver 0.0.0.0:8000
