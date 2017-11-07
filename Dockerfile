FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN apt-get purge -y git 		# to prevent accidentally using git w/in container
RUN apt-get clean
RUN apt-get update
run apt-get install -y graphviz
RUN mkdir /code
WORKDIR /code

RUN pip install Django~=1.11.4
RUN pip install psycopg2~=2.7.3
RUN pip install whitenoise~=3.3.0
RUN pip install django-crispy-forms~=1.6.1
RUN pip install django_guardian~=1.4.9
RUN pip install django-reversion~=2.0.10
RUN pip install django_ajax_selects~=1.6.1
RUN pip install django_json_widget
RUN pip install django-tables2
RUN pip install Sickle~=0.6.2
RUN pip install surt~=0.3.0
RUN pip install django-extensions~=1.8.1
RUN pip install factory-boy~=2.9.2
RUN pip install coverage~=4.4.1
RUN pip install django-extensions~=1.8.1
RUN pip install pygraphviz~=1.3.1
RUN pip install ipdb
RUN pip install django-debug-toolbar
RUN pip install uWSGI~=2.0.15
RUN pip install django-mptt
RUN pip install django-autocomplete-light

RUN pip freeze > requirements-frozen.txt

ADD . /code/
EXPOSE 8000
CMD ["/code/start-eb.sh"]