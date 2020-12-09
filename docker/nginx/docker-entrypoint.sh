#!/usr/bin/env bash

NGINX_CREDENTIALS=/run/secrets/nginx_api_credentials

exec 5< ${NGINX_CREDENTIALS}
read -r NGINX_API_USER <&5
read -r NGINX_API_PASS <&5

# API service that reloads nginx on request
htpasswd -bc /tmp/.htpasswd "${NGINX_API_USER}" "${NGINX_API_PASS}" > /dev/null 2>&1
(
  while true
  do
    { echo -e "HTTP/1.1 200 OK\n\nNGINX reload requested at: $(date)"; nginx -s reload & } | nc -l -p 9000 -q 1
  done
) &

exec /nginx-entrypoint.sh "$@"
