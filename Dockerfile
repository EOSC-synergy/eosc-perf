# use base python image
FROM python:3.8.4
# keep all webapp data in /app
ENV APP /app
# set up file structure
WORKDIR $APP
# open port 5000 for nginx
EXPOSE 5000
# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# set up user
RUN groupadd uwsgi && useradd -g uwsgi uwsgi
RUN mkdir -p $APP $APP/data && chown -R uwsgi $APP
USER uwsgi
# copy the whole webapp
COPY ./uwsgi.ini upload_license.txt config.yaml ./
COPY ./templates/ templates/
COPY ./eosc_perf/ eosc_perf/
# set launch command
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
