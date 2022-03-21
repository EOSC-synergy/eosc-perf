# EOSC-PERF

[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Feosc-perf%2Fbackend)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/eosc-perf/job/backend/)
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
2. Set up a `service_frontend/.env.local` file containing `NEXT_PUBLIC_OIDC_REDIRECT_HOST=<your server host>`
3. Configure your EGI-AAI OIDC client secret in `oidc_secret.txt`
4. Configure flask cookie encryption key in `cookie_secret.txt`
5. Configure NGINX API credentials in `nginx_api_credentials.txt` in the following format:

```
USERNAME
PASSWORD
```

7. Run `docker-compose  -f docker-compose.yaml -f docker-compose.prod.yaml build`
8. Run backend build steps in a venv
9. Run `docker-compose  -f docker-compose.yaml -f docker-compose.prod.yaml up`

#### To reset your database

1. Run `./scripts/reset-database.sh` (Linux)
    or `./scripts/reset-database.ps1` (Windows)

#### To restore a database backup:

1. Uncomment `- ./backups:/backups` in docker-compose.yaml
2. Reset the database: `bash help_scripts/reset-database.sh`
3. Start database container: `docker-compose up database`
4. Connect to database container and run `pg_restore -d ${POSTGRES_DB} -F t <path to your backup tar> -c -U ${POSTGRES_USER}`
