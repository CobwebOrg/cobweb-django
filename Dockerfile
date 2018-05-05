FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN ['pipenv', 'install', '--system', '--ignore-pipfile']
COPY . /code/
RUN ["python3", "manage.py", "collectstatic"]
CMD ["/code/start-production.sh"]
