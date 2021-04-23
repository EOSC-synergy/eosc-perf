# EOSC Perf -- Backend

EOSC Performance API service. 

# Running on docker as production


# Running locally as development

You can run the software locally so you can use your IDE debug functionalities.

Install the development requirements:
```bash
pip install -r requirements/dev.txt
```

Prepare your `.env` file with the following variables:
```ini
# General configuation
FLASK_APP=autoapp.py
FLASK_ENV=development

# Database configuration
DB_ENGINE=postgresql
DB_USER=mynonsuperuser
DB_PASSWORD=test123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eosc_perf

# Backend configuration
GUNICORN_WORKERS=1
LOG_LEVEL=debug
SECRET_KEY=not-so-secret
OIDC_CLIENT_ID=eosc-perf
OIDC_CLIENT_SECRET=your-oidc-secret
ADMIN_ASSURANCE=https://refeds.org/assurance/IAP/low
```

Run a local development server.:
```bash
flask run
```

>Use this command on your **IDE debugger** so you can apply breakpoints to debug your code.


## Manage database

The commands you would use to work with your database:

```bash
flask db migrate
flask db upgrade
```

### Database Initialization

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration. Ensure `FLASK_APP` is 
defined in your environment.

```bash
flask db init  # Not needed as the migrations folder already exists 
flask db migrate  # Create a new models version on "migrations" 
flask db upgrade  # Upgrade the db with last "migration" version
```

### Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
flask db migrate  # Create a new models version on "migrations" 
```

This will generate a new migration script. Then run

```bash
flask db upgrade  # Upgrade the db with last "migration" version
```

To apply the migration.

For a full migration command reference, run `flask db --help`.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations/versions` folder to version control. Make sure folder 
`migrations/versions` is not empty.


# Running Tests
