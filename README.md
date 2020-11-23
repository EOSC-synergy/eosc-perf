# EOSC-PERF

## Intro
![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university server clusters.

## Instructions

To deploy the application:
1. Create a 'config.yaml': `cp config.yaml.example config.yaml`
    * Setup debug and production admin entitlements: `debug_admin_entitlements`, `admin_entitlements`
    * Add OIDC client secret: `oidc_client_secret`
    * Set your domain in `oidc_redirect_hostname`
    * Set `secret_key` to something long with much entropy
    * Set `infrastructure_href` to the website of your infrastructure manager
    * Set `oidc_client_id` to your EGI-AAI OIDC client id
1. Write a license for uploaded results to `upload_license.txt` or copy `uploading_license.txt.placeholder` for testing
1. To generate HTTPS certs & nginx configuration:
    * If you want to deploy to production: Run `bash init-lentsencrypt.sh`
    * If you want to develop locally (on `localhost`): Run `bash init-dev-certs.sh`
1. Run `docker-compose build`
1. Run `docker-compose up`

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

To run tests (requires environment):
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Run `python -m unittest discover eosc_perf "*_test.py"`

Tips:
- To enable debug mode, set `debug: true` in the config.yaml

