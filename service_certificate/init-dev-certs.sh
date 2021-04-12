#!/usr/bin/env bash

source ../.env

domain="${DOMAIN}"
mkdir -p "conf/live/${domain}"
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > conf/options-ssl-nginx.conf
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > conf/ssl-dhparams.pem
openssl req -x509  -out "conf/live/${domain}/fullchain.pem" \
  -keyout "conf/live/${domain}/privkey.pem"\
   -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT \
   -config <(  printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")