FROM alpine:3.13.1


COPY /backup.sh /
RUN mkdir /workdir && chmod +x /backup.sh && apk add --no-cache bash

# copy crontabs for root user
COPY cronjobs /etc/crontabs/root

# start crond with log level 8 in foreground, output to stderr
CMD ["crond", "-f", "-d", "8"]
