FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
ADD Pipfile.lock /code/
RUN pipenv install
ADD . /code/
