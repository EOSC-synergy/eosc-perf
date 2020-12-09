#!/usr/bin/env bash

source .env

domain="${DOMAIN}"
mkdir -p "certbot/conf/live/${domain}"
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > certbot/conf/options-ssl-nginx.conf
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > certbot/conf/ssl-dhparams.pem
openssl req -x509  -out "certbot/conf/live/${domain}/fullchain.pem" \
  -keyout "certbot/conf/live/${domain}/privkey.pem"\
   -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT \
   -config <(  printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")