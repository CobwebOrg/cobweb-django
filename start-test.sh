#!/bin/bash


coverage run manage.py test
coverage html
python3 manage.py graph_models core projects archives webresources datasources -X AbstractUser -g -o datamodel.png
python3 manage.py graph_models -a -g -o datamodel-full.png
