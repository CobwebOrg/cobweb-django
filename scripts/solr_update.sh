pipenv run python3 manage.py build_solr_schema --configure-directory solr_conf/
docker-compose up --build --force-recreate --detach solr 
sleep 15
pipenv run python3 manage.py rebuild_index --noinput
