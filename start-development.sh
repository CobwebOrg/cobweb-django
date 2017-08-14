#!/bin/bash

python3 manage.py graph_models registry > 'dataModel.dot'
python3 manage.py runserver 0.0.0.0:8000