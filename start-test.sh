#!/bin/bash


coverage run manage.py test
coverage html
python3 manage.py graph_models core projects archives webresources datasources metadata -X AbstractUser -g -o datamodel.png
python3 manage.py graph_models -a -g -o datamodel-full.png
python3 manage.py graph_models core projects archives datasources -X Resource,Metadatum -g -o datamodel-simple.png
python3 manage.py graph_models metadata -g -o datamodel-metadata.png