#!/usr/bin/env bash

# API service that reloads nginx on request
htpasswd -bc /tmp/.htpasswd "${NGINX_API_USER}" "${NGINX_API_PASS}" > /dev/null 2>&1
(
  while true
  do
    { echo -e "HTTP/1.1 200 OK\n\nNGINX reload requested at: $(date)"; nginx -s reload & } | nc -l -p 9000 -q 1
  done
) &

exec /nginx-entrypoint.sh "$@"
