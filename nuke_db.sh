./manage.py reset_db
rm */migrations/*.py
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser --noinput --username andy --password cobweb123
./manage.py createinitialrevisions
