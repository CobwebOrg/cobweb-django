FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y graphviz
RUN apt-get clean
RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

RUN pip freeze > requirements-frozen.txt

COPY . /code/
EXPOSE 8000
CMD ["/code/start-eb.sh"]
