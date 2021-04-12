# use base python image
FROM python:3.8.4
# keep all webapp data in /app
ENV APP /app
WORKDIR $APP
# open port 5000 for nginx
EXPOSE 5000
# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt pip
# set launch command
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
# copy the whole webapp
COPY ./templates/ templates/
COPY ./eosc_perf/ eosc_perf/
COPY uwsgi.ini upload_license.txt ./
# set up user, files and permissions
RUN groupadd uwsgi && useradd -g uwsgi uwsgi && mkdir -p $APP $APP/data && chown -R uwsgi $APP
USER uwsgi
