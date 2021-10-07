#!/usr/bin/env bash
# This script will reset the database on docker-compose
# Not it does not create a migrations so service_backend/migrations
# folder should be up to date.

docker-compose down
docker volume rm eosc-perf_postgres
docker-compose up -d database
docker-compose run --rm backend_v1 flask db upgrade
