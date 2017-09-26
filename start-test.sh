#!/bin/bash


coverage run manage.py test
coverage html
python3 manage.py graph_models core projects archives webresources datasources -X Group,Permission,AbstractUser -g -o datamodel.png
