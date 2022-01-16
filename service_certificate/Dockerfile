FROM certbot/certbot

RUN set -x \
&&  apk add --no-cache \
      curl \
      bash \
&&  rm -rf /var/cache/apk/* \
           /tmp/* \
           /var/tmp/*

COPY docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]
