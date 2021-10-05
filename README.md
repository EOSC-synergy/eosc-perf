# EOSC-PERF

[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Feosc-perf%2Fci-cd)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/eosc-perf/job/ci-cd/)
[![Documentation Status](https://readthedocs.org/projects/perf/badge/?version=latest)](https://perf.readthedocs.io/en/latest/?badge=latest)

## Intro

![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university
server clusters.

You can build it up by running

## Instructions

To deploy the application:

1. Set up a `.env` file: `cp .env-example .env`, configure it following the comments
1. Configure your EGI-AAI OIDC client secret `oidc_secret.txt`
1. Configure flask cookie encryption key `cookie_secret.txt`
1. Configure NGINX API credentials `nginx_api_credentials.txt`:

```
USERNAME
PASSWORD
```

6. Configure email credentials `email_credentials.ini`:

```
[Mail]
Username = YOUR_USERNAME
Password = YOUR_PASSWORD
```

7. Set up a `upload_license.txt`: `cp upload_license.txt.placeholder upload_license.txt`, write content
8. To generate HTTPS certs & nginx configuration: #TODO
    * If you want to deploy to production: Run `bash init-lentsencrypt.sh`
    * If you want to develop locally (on `localhost`): Run `bash init-dev-certs.sh`
9. Generate the backend .whl file:

```bash
cd service_backend
pip install --upgrade build # TODO: venv?
python -m build
```

10. Copy the .whl file to the frontend: `cp service_backend/dist/*.whl service_frontend/`
11. Run `docker-compose build`
12. Run `docker-compose up`

To set up a development environment:

1. Set up a virtual environment: `python -m venv venv`
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
    * The requirements will only be installed within the virtual environment.
1. Install backend wheel: # TODO: reliable steps

To build the backend:

```bash
docker-compose build  # Build services (including backend)
docker-compose up  # Brings up the services (including backend)
docker-compose run flask db migrate  # Creates a migration for the db from code
docker-compose run flask db upgrade  # Upgrades/Creates tables on the db (using port)
```
