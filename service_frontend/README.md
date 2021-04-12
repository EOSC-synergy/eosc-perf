# EOSC-PERF

## Intro
![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university server clusters.

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
1. Run `docker-compose build`
1. Run `docker-compose up`

To install the application locally:
1. Run `pip install .`

To set up a development environment:
1. Set up a virtual environment: `python -m venv venv`
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
    * The requirements will only be installed within the virtual environment.

To generate the documentation:
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Go to `docs/`
1. (Optional) Run `make clean`
1. Run `make html`

Steps to regenerate documentation:
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Go to `docs/`
1. (Optional) Run `make clean`
1. Run `sphinx-apidoc -fo source ../eosc_perf`
1. Move 'Module contents' to the top of the .rst files, under title and main description   
1. Run `make html`

To run tests (requires virtual environment):
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Run `pip install tox`
1. Run `tox` (it should install test requirements automatically)

Tips:
- To enable debug mode, set `EOSC_PERF_DEBUG=true` in the `.env`

