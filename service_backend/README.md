# EOSC Perf -- Backend

EOSC Performance API service.

# Prepare your environment
Prepare your environment with the following variables:
```ini
FLASK_ENV=<production-or-development>
FLASK_APP=autoapp.py
GUNICORN_WORKERS=1
SECRET_KEY=<desired-cookie-encryption-key>
OIDC_CLIENT_ID=<your-odic-client-secret>
OIDC_CLIENT_SECRET=<your-odic-client-secret>
ADMIN_ENTITLEMENTS=<only-used-in-production>
DB_HOST=localhost
DB_PORT=5432
DB_USER=<my-non-super-user>
DB_PASSWORD=<my-db-password>
DB_NAME=<my-db-name>
```


# Running on docker as production
To run the application on production, container technologies is the recommended way (docker, kubernetes, etc).

## Environment details
To run the application on production the following environment variables and secrets need to be set:
```ini
FLASK_ENV=production
ADMIN_ENTITLEMENTS=[<entitlements-for-admin>]
...
```

> To simplify the container configuration, you can save your environment into a file and pass it later using the option `--env-file`. For instance `docker run --env-file ./env backend`

## Load data as secrets
Secrets are sensitive data which are not generally safe as environment variables. If you are using a docker compose configuration or similar technology which supports the usage of secrets, you can configure the following environment variables to indicate the location of the secret configuration file:
```ini
SECRET_KEY_FILE=<path/to/cookie-secret/file>
OIDC_CLIENT_SECRET_FILE=<path/to/OIDC-secret/file>
```

> Note when the `_FILE` version of the environment variable is set, the direct version of the environment variable is ignored.

## Start the backend service
You can deploy the backend service on the port 8080 with the following example command:
```bash
docker run -it --env-file .env -p 8080:5000 backend
```


# Running locally as development
You can run the software locally in order to use your IDE testing and debug functionalities.

## Environment details
To run the application on production the following environment variables and secrets need to be set:
```ini
FLASK_ENV=development
...
```

## Tools installation
To run the application locally you need to install at least the production requirements, however, in order to run tests or other development tools, development requirements are also needed.
```bash
pip install -r requirements/dev.txt
```

## Run development server
Run a local development server.:
```bash
flask run
```

>Use this command on your **IDE debugger** so you can apply breakpoints to debug your code.


# Run your database
The application needs a [PostgreSQL](https://www.postgresql.org/) database where to store the persistent data in secured and efficient manner. We recommend deploy this database using container technologies (docker, kubernetes, etc).

Here is a docker run example to deploy a postgres database service on the port 5432.
```bash
docker run -p 5432:5432 -v `pwd`/data:/data \
    -e POSTGRES_USER=<defined-env-non-super-user> \
    -e POSTGRES_PASSWORD=<my-db-password> \
    -e POSTGRES_DB=<my-db-name> \
    -e PGDATA=/data \
    postgres
```

## New database migration
You can create a new migration with:
```bash
docker run --rm --env-file .env \
    --volume `pwd`:/app \
    --network="host" \
    backend flask db migrate
```

If you will deploy your application remotely you should add the `migrations/versions` folder to version control. Make sure folder `migrations/versions` is not empty.

## Upgrade your database
You can upgrade your database with the last migration with:
```bash
docker run --rm --env-file .env \
    --volume `pwd`:/app \
    --network="host" \
    backend flask db upgrade
```

>For a full migration command reference, run with `flask db --help`.

## Backup your database
You can backup your [PostgreSQL](https://www.postgresql.org/) database operating over the `data` folder if `PGDATA` was specified and mounted with `--volume` at the postgres container creation.

> Although backup by coping the /data folder or volume container is simple, there are other [alternatives](https://www.postgresql.org/about/news/postgresql-14-beta-2-released-2249/) more correct advanced solutions with advantages.


# Build documentation
Documentation is build using [Sphinx](https://www.sphinx-doc.org). To build the documentation form sources you have to change directory to `docs` and execute `make html`:
```bash
cd docs
make html
```

You can open the documentation with your browser using the `index.html` file at `docs/build/html`.


# Running Tests
Tests are automated to run with [tox](https://tox.readthedocs.io), although as are based in pytest you can directly discover, call and debug them with your pytest IDE extension.

To execute tests using tox run:
```bash
tox  # Run tests using tox (includes coverage, style and security)
```

To execute tests using pytest, ensure you have the `requirements/dev.txt` dependencies installed and run:
```bash
pytest  # Run tests using pytest
```


# Autostart database
The file `autoapp.py` is a script which automatically generates an 
app from factory function `create_app` and upgrades the database with
the last migration version.

To use it, make sure that the `FLASK_APP` env variable points to it.
For example, if using docker-compose file:
```yaml
services:
  ...
  backend_service_name:
    ...
    environment:
      FLASK_APP: autoapp.py
      ...
```

