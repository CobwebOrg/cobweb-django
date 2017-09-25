#!/bin/bash


coverage run manage.py test
coverage report
coverage html
python3 manage.py graph_models core projects archives webresources datasources -X Group,Permission,AbstractUser -g -o datamodel.png
