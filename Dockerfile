FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN apt-get purge -y git 		# to prevent accidentally using git w/in container
RUN apt-get clean
RUN apt-get update
run apt-get install -y graphviz
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip freeze > requirements-frozen.txt
ADD . /code/
EXPOSE 8000
CMD ["/code/start-eb.sh"]