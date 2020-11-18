# EOSC-PERF

## Intro
![](docs/source/eosc%20synergy%20logo.png)

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university server clusters.

## Instructions

To launch the webapp entirely:
1. Create a 'config.yaml': `cp config.yaml.example config.yaml`
    * Setup debug and production admin entitlements: `debug_admin_entitlements`, `admin_entitlements`
    * Add OIDC client secret: `oidc_client_secret`
    * Set your domain in `oidc_redirect_hostname`
    * Set `secret_key` to something long with much entropy
    * Set `infrastructure_href` to the website of your infrastructure manager
1. Write a license for uploaded results to `upload_license.txt` or copy `uploading_license.txt.placeholder` for testing
1. Move your SSL certificate and key to nginx/certs/ (Make sure they are called `certificate.crt` and `private_key.key`)
1. Run `docker-compose build`
1. Run `docker-compose up`

To generate the documentation:
1. Go to `docs/`
2. (Optional) Run `make clean`
3. Run `make html`

Tips:
- To enable debug mode, set `debug: true` in the config.yaml
- To generate a certificate and key for your localhost, use:
`openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")`
- To run the included unit tests, the unittest package can be used:
  `python -m unittest discover eosc_perf "*_test.py"`
