#!/bin/bash

pip3 freeze > requirements-frozen.txt
coverage run manage.py test
coverage html
python3 manage.py graph_models core projects archives webresources datasources -X AbstractUser -g -o datamodel.png
python3 manage.py graph_models -a -g -o datamodel-full.png
python3 manage.py graph_models core projects archives datasources -X Resource -g -o datamodel-simple.png
