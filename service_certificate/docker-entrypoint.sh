#!/usr/bin/env bash
# vim:sw=2:ts=2:et

set -ueo pipefail
# DEBUG
# set -x

# convert space-delimited string from the ENV to array
#domains=(${domains:-example.org})
domains=(${DOMAINS})

NGINX_CREDENTIALS=/run/secrets/nginx_api_credentials
exec 5< ${NGINX_CREDENTIALS}
read -r NGINX_API_USER <&5
read -r NGINX_API_PASS <&5

# if domains are provided
if (( ${#domains[@]} )); then
  primary_domain=${domains[0]}

  data_path="/etc/letsencrypt"
  path="$data_path/live/$primary_domain"

  rsa_key_size=${CERT_KEY_SIZE:-4096}

  trap exit TERM

  echo "### Let nginx bootstrap"
  while ! curl --fail --silent --max-time 3 http://reverse_proxy
  do
    echo "nginx not up yet..."
    sleep 3
  done

  # Select appropriate email arg
  case "$LETSENCRYPT_EMAIL" in
    "") email_arg="--register-unsafely-without-email" ;;
    *) email_arg="--email $LETSENCRYPT_EMAIL" ;;
  esac

  if [ -f "$path/is-selfsigned" ]; then
    echo "### Deleting self-signed cert..."
    rm -r "$path"

    echo "### Requesting Let's Encrypt certificate for $domains ..."

    # join $domains to -d args
    domain_args=""
    for domain in "${domains[@]}"; do
      domain_args="$domain_args -d $domain"
    done

    # Enable staging mode if needed
    if [ $LETSENCRYPT_STAGING != "0" ]; then
      staging_arg="--staging"
    else
      staging_arg=""
    fi

    certbot certonly \
      --webroot -w /var/www/certbot \
      $staging_arg \
      $email_arg \
      $domain_args \
      --rsa-key-size $rsa_key_size \
      --agree-tos \
      --force-renewal

      echo "### Reloading nginx ..."
      curl --fail --silent --user ${NGINX_API_USER}:${NGINX_API_PASS} http://reverse_proxy/nginx/reload
  fi

  while :; do
    certbot renew \
      --webroot -w /var/www/certbot \
      $email_arg \
      --rsa-key-size $rsa_key_size \
      --agree-tos

    curl --fail --silent --user ${NGINX_API_USER}:${NGINX_API_PASS} http://reverse_proxy/nginx/reload
    sleep 12h & wait ${!}
  done
else
  echo "No domains provided, doing nothing."
  while :; do
    sleep 24h
  done
fi