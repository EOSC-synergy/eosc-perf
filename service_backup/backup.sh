#!/usr/bin/env bash

export PGHOST=${POSTGRES_HOST}
export PGPORT=${POSTGRES_PORT}
export PGUSER=${POSTGRES_USER}
export PGPASSWORD=$(cat ${POSTGRES_PASSWORD_FILE})

pg_dump -d "${POSTGRES_DB}" -F t -f /workdir/${POSTGRES_DB}."$(date +'%Y-%m-%d_%H-%M-%S')".sql.tar
