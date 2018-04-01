FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install
COPY . /code/
RUN ["pipenv", "run", "python3", "manage.py", "collectstatic"]
# ENTRYPOINT ["pipenv", "run"]
# CMD ["/code/start-production.sh"]
