FROM python:3.6 as base
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN ["pipenv", "install", "--system", "--ignore-pipfile"]
COPY . /code/

FROM base as production
RUN ["python3", "manage.py", "collectstatic"]
CMD ["python3", "scripts/start-production.py"]

FROM base as dev
RUN ["pipenv", "install", "--dev", "--system", "--ignore-pipfile"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

FROM ruby as sass
RUN gem install sass
