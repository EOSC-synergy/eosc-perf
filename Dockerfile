# use base python image
FROM python:3.8.4
# keep all webapp data in /app
ENV APP /app
# set up file structure
RUN mkdir $APP
WORKDIR $APP
# open port 5000 for nginx
EXPOSE 5000
# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# copy the whole webapp
COPY ./app/. .
COPY ./templates/. .
COPY ./config.yaml .
COPY ./uwsgi.ini .
# set launch command
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
