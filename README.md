# EOSC-PERF
[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Feosc-perf%2Fmaster)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/eosc-perf/job/master/)
[![Documentation Status](https://readthedocs.org/projects/perf/badge/?version=latest)](https://perf.readthedocs.io/en/latest/?badge=latest)

## Intro

![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university
server clusters.

## Instructions

#### If you do not have an up-to-date version of docker-compose (e.g. Ubuntu)

1. Create a python venv `python -m venv venv`
2. Activate it `. ./venv/bin/activate`
3. Install docker-compose `python -m pip install docker-compose`
4. Whenever you need to use docker-compose, run `./venv/bin/docker-compose` instead

#### To deploy the application:

1. Set up a `.env` file: `cp .env-example .env`, configure it following the comments
2. Configure a database user password in `database_secret.txt`
3. Configure flask cookie encryption key in `cookie_secret.txt`
4. Configure NGINX API credentials in `nginx_api_credentials.txt` in the following format:

```
<USERNAME>
<PASSWORD>
```

5. Run `docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml build`
6. Run `docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up`

#### To reset your database

Run `./scripts/reset-database.sh` (Linux) or `./scripts/reset-database.ps1` (Windows)

#### To restore a database backup:

1. Uncomment `- ./backups:/backups` in docker-compose.yaml
1. Reset the database: `bash scripts/reset-database.sh`
1. Start database container: `docker-compose up database`
1. Connect to database container and run `pg_restore -d ${POSTGRES_DB} -F t <path to your backup tar> -c -U ${POSTGRES_USER}`

