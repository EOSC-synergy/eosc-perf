#!/usr/bin/env bash

while :; do
  certbot renew
  #curl --fail --silent --user ${NGINX_API_USER}:${NGINX_API_PASS} http://nginx/nginx/reload
  sleep 12h & wait ${!}
done
