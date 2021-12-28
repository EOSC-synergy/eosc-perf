#!/usr/bin/env  bash
#
# Copyright (c) 2018 - 2020 Karlsruhe Institute of Technology - Steinbuch Centre for Computing
# This code is distributed under the MIT License
# Please, see the LICENSE file
#
# @author: vykozlov
#
# script to start postfix in docker container:
#  - setups the environment
#  - starts postfix

set -e

### USAGEMESSAGE ###
USAGEMESSAGE="Usage: $0 \n
Script to configure and start postfix to work inside docker container\n"

### PARSE SCRIPT FLAGS ###
if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    shopt -s xpg_echo
    echo $USAGEMESSAGE
    exit 1
fi
###

domains=(${DOMAINS})
if (( ${#domains[@]} )); then
    PERF_HOSTNAME="${domains[0]}"
else
    PERF_HOSTNAME="localhost"
fi

echo "$PERF_HOSTNAME" > /etc/mailname
echo "$PERF_HOSTNAME" > /etc/hostname

# place to keep log, maillog
# http://www.postfix.org/MAILLOG_README.html
#postconf -e maillog_file="/var/log/postfix.log"
# Logging to stdout is useful when Postfix runs in a container, as it eliminates a syslogd dependency.
postconf -e maillog_file="/dev/stdout"
# Following works for postfix>=3.4.
# Hmm, next line seems to hang server, comment. It is already in master.cf (Ubuntu 20.04)
#postconf -M postlog/unix-dgram="postlog unix-dgram n - n - 1 postlog"

# set myhostname and mynetworks
postconf -e myhostname="$PERF_HOSTNAME"
postconf -e mydestination="\$myhostname, localhost"
postconf -e mynetworks="127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128 172.16.0.0/12 172.17.0.0/16 10.0.0.0/8"

# TLS parameters
postconf -e smtpd_use_tls=yes
# we use Letsencrypt certificates obtained via certbot (other container)
postconf -e smtpd_tls_cert_file=/etc/letsencrypt/live/\$myhostname/fullchain.pem
postconf -e smtpd_tls_key_file=/etc/letsencrypt/live/\$myhostname/privkey.pem
postconf -e smtpd_tls_CApath=/etc/ssl/certs
postconf -e smtpd_tls_security_level=may
postconf -e smtpd_tls_loglevel=1

postconf -e smtp_tls_CApath=/etc/ssl/certs
postconf -e smtp_tls_security_level=encrypt
postconf -e smtp_tls_mandatory_ciphers=high
postconf -e smtp_tls_loglevel=1

postconf -e smtpd_relay_restrictions="permit_mynetworks permit_sasl_authenticated defer_unauth_destination"
postconf -e inet_interfaces="all"
postconf -e inet_protocols="all"

postconf -e masquerade_domains="\$myhostname"

# delay emails to the same domain to avoid blocking
# http://www.postfix.org/postconf.5.html#default_destination_rate_delay
postconf -e default_destination_rate_delay="2m"
postconf -e default_destination_concurrency_failed_cohort_limit="10"

# switch chroot off for smtp
postconf -F smtp/*/chroot=n

# start postfix in foreground for running in a contianer
/usr/sbin/postfix start-fg
