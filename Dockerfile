# use base python image
FROM python:3.8.4

# keep all webapp data in /app
ENV APP /app

# Install system updates and tools
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
# Install system updates and tools
    apt-get install -y --no-install-recommends \
        && \
# Clean up & back to dialog front end
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

# Install application & set up file structure
RUN mkdir $APP
WORKDIR $APP
COPY ./eosc_perf ./eosc_perf
COPY ./templates ./templates
COPY ./setup.py .
COPY ./setup.cfg .
COPY ./uwsgi.ini .
# Install python application
RUN pip install --upgrade pip && \ 
    pip3 install --no-cache-dir -e . && \
# Clean up
    rm -rf /root/.cache/pip/* && \
    rm -rf /tmp/*

# set launch command
EXPOSE 5000
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]

