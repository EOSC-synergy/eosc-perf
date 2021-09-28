docker-compose down
docker volume rm eosc-perf_postgres
docker-compose up -d database
docker-compose run --rm backend_v1 flask db upgrade
