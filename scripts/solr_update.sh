docker-compose run web pipenv run python3 manage.py build_solr_schema --configure-directory solr_conf/
docker-compose build solr
docker-compose restart solr
docker-compose run web pipenv run python3 manage.py rebuild_index