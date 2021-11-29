# EOSC-PERF

[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Feosc-perf%2Fbackend)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/eosc-perf/job/backend/)
[![Documentation Status](https://readthedocs.org/projects/perf/badge/?version=latest)](https://perf.readthedocs.io/en/latest/?badge=latest)

## Intro

![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university
server clusters.

You can build it up by running

## Instructions

To deploy the application:

1. Set up a `.env` file: `cp .env-example .env`, configure it following the comments
1. Set up a `.env.local` file for frontend-js: `cp .env .env.local` and fill in the blanks
1. Configure your EGI-AAI OIDC client secret `oidc_secret.txt`
1. Configure flask cookie encryption key `cookie_secret.txt`
1. Configure NGINX API credentials `nginx_api_credentials.txt`:

```
USERNAME
PASSWORD
```

5. Set up a `upload_license.txt`: `cp upload_license.txt.placeholder upload_license.txt`, write content
6. To generate HTTPS certs & nginx configuration: #TODO
    * If you want to deploy to production: Run `bash init-lentsencrypt.sh`
    * If you want to develop locally (on `localhost`): Run `bash init-dev-certs.sh`
7. Run `docker-compose build`
8. Run backend build steps in a venv
9. Run `docker-compose up`

To set up a development environment:

1. Set up a virtual environment: `python -m venv venv`
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
    * The requirements will only be installed within the virtual environment.

To build the backend:

```bash
docker-compose build  # Build services (including backend)
docker-compose up  # Brings up the services (including backend)
docker-compose run flask db migrate  # Creates a migration for the db from code
docker-compose run flask db upgrade  # Upgrades/Creates tables on the db (using port)
```

To restore a database backup:

1. Uncomment `- ./backups:/backups` in docker-compose.yaml
1. Reset the database: `bash help_scripts/reset-database.sh`
1. Start database container: `docker-compose up database`
1. Connect to database container and run `pg_restore -d ${POSTGRES_DB} -F t <path to your backup tar> -c -U db_user`

