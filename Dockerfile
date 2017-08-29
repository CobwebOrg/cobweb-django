FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN apt-get clean
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip freeze > requirements-frozen.txt
ADD . /code/
EXPOSE 8000
CMD ["/code/start-eb.sh"]