## Build stage 0: Compule using a base python image
FROM python:3.8.4

# Set working directory
RUN mkdir /buildroot
WORKDIR /buildroot

# Copy our python application
COPY . .

# And build the release
RUN python3 setup.py sdist


## Build stage 1: Clean installation
FROM python:3.8.4 

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

# Set workdirectory
ENV APP /app
RUN mkdir $APP
WORKDIR $APP

# Copy the released application
COPY --from=0 /buildroot/dist dist
COPY ./templates /app/templates
COPY ./uwsgi.ini .
# Install python application
RUN pip install --upgrade pip && \ 
    pip3 install --no-cache-dir ./dist/*.tar.gz && \
# Clean up
    rm -rf /root/.cache/pip/* && \
    rm -rf /tmp/*

# set launch command
EXPOSE 5000
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]

