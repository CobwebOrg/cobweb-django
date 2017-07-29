FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y upgrade
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
CMD ["/code/production_.sh"]