#!/bin/bash

pip3 freeze > requirements-frozen.txt
coverage run manage.py test
coverage html -d code_analysis/htmlcov
python3 manage.py graph_models core projects archives webresources datasources -X AbstractUser -g -o code_analysis/datamodel.png
python3 manage.py graph_models -a -g -o code_analysis/datamodel-full.png
python3 manage.py graph_models core projects archives datasources -X Resource -g -o code_analysis/datamodel-simple.png
