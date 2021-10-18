#!/usr/bin/env bash

export PGHOST=${DB_HOST}
export PGPORT=${DB_PORT}
export PGUSER=${DB_USER}
export PGPASSWORD=${DB_PASSWORD}
pg_dump -d "${DB_DATABASE}" -F t -f /workdir/${DB_DATABASE}."$(date +'%Y-%m-%d_%H-%M-%S')".sql.tar
