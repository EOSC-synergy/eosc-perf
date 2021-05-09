# EOSC-PERF

## Intro
![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university server clusters.

#### ****************** EDIT FROM SERVICE BACKEND *******************
This is an example of env configuration to run backend with a database service based in postgres container image using the current docker-compose.yaml file.

```ini
# General configuation
FLASK_APP=service_backend/autoapp.py

# Database configuration
DB_NAME=eosc_perf
DB_USER=mynonsuperuser
DB_PASSWORD=test123
DB_HOST=localhost

# Backend configuration
BACKEND_ENV=development
BACKEND_WORKERS=1
BACKEND_LOG_LEVEL=debug
SECRET_KEY=not-so-secret
OIDC_CLIENT_ID=your-oidc-client
OIDC_CLIENT_SECRET=your-oidc-secret
ADMIN_ASSURANCE=https://refeds.org/assurance/IAP/low
```

You can build it up by running

```bash
docker-compose up database  # Brings up the database service
flask db migrate  # Creates a migration for the db from code
flask db upgrade  # Upgrades/Creates tables on the db (using port)
docker-compose build backend  # Build backend on desired target env
docker-compose up backend  # Brings up the backend service
```
#### *****************************************************************

## Instructions

To deploy the application:
1. Set up a `.env` file: `cp .env-example .env`, configure it following the comments
1. Configure your EGI-AAI OIDC client secret:
   * create a file `oidc_secret.txt` with the secret as contents
1. Configure flask cookie encryption key:
   * create a file `cookie_secret.txt` with the key as contents
1. Configure NGINX API credentials:
   * create a file `nginx_api_credentials.txt` with:
     * one line: username (example: nginx)
     * one line: password (example: correct-horse-battery-staple)
1. Set up a `upload_license.txt`: `cp upload_license.txt.placeholder upload_license.txt`
   * Write a license for uploaded results
1. To generate HTTPS certs & nginx configuration:
   * If you want to deploy to production: Run `bash init-lentsencrypt.sh`
   * If you want to develop locally (on `localhost`): Run `bash init-dev-certs.sh`
1. Generate the backend .whl file:
   * `cd service_backend`
   * `pip install --upgrade build` # TODO: venv?
   * `python -m build`
1. Copy the .whl file to the frontend: `cp service_backend/dist/*.whl service_frontend/`
1. Run `docker-compose build`
1. Run `docker-compose up`

To set up a development environment:
1. Set up a virtual environment: `python -m venv venv`
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
    * The requirements will only be installed within the virtual environment.
1. Install backend wheel: # TODO: reliable steps
