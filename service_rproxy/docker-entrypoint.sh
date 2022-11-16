#!/usr/bin/env bash
# vim:sw=2:ts=2:et

set -ueo pipefail
# DEBUG
# set -x

# convert space-delimited string from the ENV to array
#domains=(${domains:-example.org})
domains=(${DOMAINS})
if (( ${#domains[@]} )); then
  primary_domain="${domains[0]}"
else
  primary_domain="localhost"
fi

export nginx_domain="${primary_domain}"

data_path="/etc/letsencrypt"
path="$data_path/live/$primary_domain"

rsa_key_size=${CERT_KEY_SIZE:-4096}

wait_certbot(){
  (
    echo "### Waiting for certbot container"

    retries="${1:-180}"

    set +e
    until ping -c 1 certificate > /dev/null 2>&1 || [ "$retries" -eq 0 ]; do
      : $((retries--))
      echo "### certbot is not up yet!"
      sleep 1s
    done
    set -e

    [ "${retries}" -ne 0 ] || (echo "### certbot service did not get up"; exit 1)

    #echo "### Removing self-signed SSL from $path"
    #rm -rf "$path"
  ) &
}

if [ ! -f "$path/privkey.pem" ]; then
  sleep 5
  echo "### Creating dummy certificate for $primary_domain ..."

  mkdir -p "$path"

  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
    -keyout "$path/privkey.pem" \
    -out "$path/fullchain.pem" \
    -subj '/CN=localhost'

  touch "$path/is-selfsigned"

  if (( ${#domains[@]} )); then
    wait_certbot
  fi
fi

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

# original entrypoint for nginx
exec /nginx-entrypoint.sh "$@"
