FROM python:3.7 as base
ENV PYTHONUNBUFFERED 1
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN ["pipenv", "install", "--system", "--ignore-pipfile"]
COPY . /code/

FROM base as production
ENV DJANGO_SETTINGS_MODULE cobweb.settings
CMD ["python3", "scripts/start-production.py"]

FROM base as dev
RUN ["pipenv", "install", "--dev", "--system", "--ignore-pipfile"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

FROM ruby as sass
RUN gem install sass

FROM production as static
RUN DJANGO_STATIC_ROOT='/static' COBWEB_SECRET_KEY='abcdefghijklmnopqrstuvwxyz' \
    python3 manage.py collectstatic

FROM nginx as nginx
COPY --from=static /static /data/www/static
COPY ./nginx_conf /etc/nginx/conf.d