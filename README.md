# EOSC-PERF

[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Feosc-perf%2Fbackend)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/eosc-perf/job/backend/)
[![Documentation Status](https://readthedocs.org/projects/perf/badge/?version=latest)](https://perf.readthedocs.io/en/latest/?badge=latest)

## Intro

![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university
server clusters.

## Instructions

#### To deploy the application:

1. Set up a `.env` file: `cp .env-example .env`, configure it following the comments
1. Set up a `service_frontend/.env.local` file containing `NEXT_PUBLIC_OIDC_REDIRECT_HOST=<your server host>`
1. Configure your EGI-AAI OIDC client secret in `oidc_secret.txt`
1. Configure flask cookie encryption key in `cookie_secret.txt`
1. Configure NGINX API credentials in `nginx_api_credentials.txt` in the following format:

```
USERNAME
PASSWORD
```

7. Run `docker-compose build`
8. Run backend build steps in a venv
9. Run `docker-compose up`

#### To reset your database

Run `./scripts/reset-database.sh` (Linux) or `./scripts/reset-database.ps1` (Windows)

#### To restore a database backup:

1. Uncomment `- ./backups:/backups` in docker-compose.yaml
1. Reset the database: `bash help_scripts/reset-database.sh`
1. Start database container: `docker-compose up database`
1. Connect to database container and run `pg_restore -d ${POSTGRES_DB} -F t <path to your backup tar> -c -U db_user`

