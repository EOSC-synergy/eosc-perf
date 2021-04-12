#!/usr/bin/env bash

NGINX_CREDENTIALS=/run/secrets/nginx_api_credentials

exec 5< ${NGINX_CREDENTIALS}
read -r NGINX_API_USER <&5
read -r NGINX_API_PASS <&5

while :; do
  certbot renew
  curl --fail --silent --user "${NGINX_API_USER}:${NGINX_API_PASS}" http://nginx/nginx/reload
  sleep 12h & wait ${!}
done
