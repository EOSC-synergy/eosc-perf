"""This is the application configuration module. It is used to load
from the system environment and files the configuration to use
when deploying an application instance.

For local development, it is recommended to use a .env file
containing the environment variables definitions. Sensible information
can be loaded directly from the environment or from a configuration/secret
file. In the last case, ensure the application has access to read such files.
"""
import functools

from environs import Env, EnvError
from marshmallow.validate import OneOf


env = Env()
env.read_env()

# Application environment
ENV = env.str("FLASK_ENV", "production", validate=OneOf(
    ["production", "development"],
    error="FLASK_ENV must be one of: {choices}"
))
""" Defines in which mode the application is launched.
There are 2 options:

- `production`: Normal functionality including all security and
  performance checks. Do not use it with `flask.run()`.
- `development`: Bypass authentication and other modules which
  might slow down the development process. Do not use it when
  deployed into the open world.

By default it is set to `production`.

:meta hide-value:
"""


# Overload of environs functions with dev_default
def development_defaults(func):
    """Decoration function to add "dev_default" input.
    If ENV == 'development' and dev_default, default is replaced
    """
    @functools.wraps(func)
    def decorated(*args, dev_default=None, **kwargs):
        if ENV == 'development' and dev_default:
            kwargs['default'] = dev_default
        return func(*args, **kwargs)
    return decorated


bool = development_defaults(env.bool)
int = development_defaults(env.int)
str = development_defaults(env.str)


# Secret key for security and cookie encryption
SECRET_KEY = str("SECRET_KEY", default="", dev_default="not-so-secret")
"""| Secret key to use on flask configuration.

| When ENV is set to `production`, a configuration value is required.
| When ENV is `development`, the default value stands to: "not-so-secret".
| See: https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY

:meta hide-value:
"""

SECRET_KEY_FILE = str("SECRET_KEY_FILE", default="")
"""| Path to a secret file to define `SECRET_KEY`.

| The secret inside the file overwrites the environment SECRET_KEY therefore
| the configuration requirement `SECRET_KEY` does not apply.

:meta hide-value:
"""
if SECRET_KEY_FILE:
    SECRET_KEY = open(SECRET_KEY_FILE).read().rstrip('\n')
if not SECRET_KEY:
    raise EnvError("Environment variable 'SECRET_KEY' empty")


# Database configuration
DB_USER = str("DB_USER", dev_default="not-defined")
"""| Username to use on the database connection.

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: "not-defined".

:meta hide-value:
"""

DB_PASSWORD = str("DB_PASSWORD", dev_default="not-defined")
"""| Password to use on the database connection.

| When ENV is set to `production`, a configuration value is required.
| When ENV is `development`, the default value stands to: "not-so-secret".

:meta hide-value:
"""

DB_HOST = str("DB_HOST", dev_default="not-defined")
"""| Database host where to stablish the connection.

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: "not-defined".

:meta hide-value:
"""

DB_PORT = str("DB_PORT", dev_default="not-defined")
"""| Port where to stablish the connection with the database host.

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: "not-defined".

:meta hide-value:
"""

DB_NAME = str("DB_NAME", dev_default="not-defined")
"""| Name of the database to use located on the host.

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: "not-defined".

:meta hide-value:
"""

DB_CONNECTION = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
SQLALCHEMY_DATABASE_URI = f'{DB_CONNECTION}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Crypt configuration
BCRYPT_LOG_ROUNDS = int("BCRYPT_LOG_ROUNDS", default=12)
"""| Value to determine the complexity of the encryption.
| See bcrypt for more details; default value is 12.

:meta hide-value:
"""


# Authorization configuration.
OIDC_CLIENT_ID = str("OIDC_CLIENT_ID", dev_default="not-defined")
"""| OIDC Client Identifier valid at the Authorization Server.
| See https://openid.net/specs/openid-connect-core-1_0.html

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: "not-defined".

:meta hide-value:
"""

OIDC_CLIENT_SECRET = str("OIDC_CLIENT_SECRET", default="", dev_default=".")
"""| Secret to validate the application identify on the Authorization Server.
| See https://openid.net/specs/openid-connect-core-1_0.html

| When ENV is set to `production`, a configuration value is required.
| When ENV is set to `development`, the default value stands to: ".".

:meta hide-value:
"""

OIDC_CLIENT_SECRET_FILE = str("OIDC_CLIENT_SECRET_FILE", default="")
"""| Path to a secret file to define `OIDC_CLIENT_SECRET`.

| The secret inside the file overwrites the environment SECRET_KEY therefore
| the configuration requirement `OIDC_CLIENT_SECRET` does not apply.

:meta hide-value:
"""
if OIDC_CLIENT_SECRET_FILE:
    OIDC_CLIENT_SECRET = open(OIDC_CLIENT_SECRET_FILE).read().rstrip('\n')
if not OIDC_CLIENT_SECRET:
    raise EnvError("Environment variable 'OIDC_CLIENT_SECRET' empty")

ADMIN_ENTITLEMENTS = str("ADMIN_ENTITLEMENTS", default="")
"""| OIDC Entitlements to grant administrator rights to users.
| By default no entitlements are defined to grant administrator rights,
  default=[].

:meta hide-value:
"""

DISABLE_ADMIN_PROTECTION = bool(
    "DISABLE_ADMIN_PROTECTION", default=False, dev_default=True
)
"""| Administrator methods can be acceed by any user.
| **Warning**: Users information is collected using OIDC.
| OIDC configuration is still needed in order to create new valid users.

| When ENV is set to `production`, the default value stands to: "False".
| When ENV is set to `development`, the default value stands to: "True".

:meta hide-value:
"""


# Email and notification configuration.
MAIL_SUPPORT = str("MAIL_SUPPORT", default="")
""" Email list for application support. This email receives administration
notifications such 'reports'.

:meta hide-value:
"""

MAIL_FROM = str("MAIL_FROM", default="")
""" Email to display on 'from' from notification emails.

:meta hide-value:
"""

MAIL_SERVER = str("MAIL_SERVER", default="")
""" SMTP server where to send the email notification requests.

:meta hide-value:
"""

MAIL_PORT = int("MAIL_PORT", default=25)
""" SMTP server port.

:meta hide-value:
"""

if MAIL_SERVER == "":  # Mail into console
    MAIL_BACKEND = 'console'


# API specs configuration
BACKEND_URL = str("BACKEND_URL", default="/")
API_TITLE = 'EOSC Performance API'
API_VERSION = 'v1'
OPENAPI_VERSION = "3.0.2"
OPENAPI_JSON_PATH = "api-spec.json"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

API_SPEC_OPTIONS = {}
API_SPEC_OPTIONS['security'] = [{"bearerAuth": []}]
API_SPEC_OPTIONS['servers'] = [{"url": BACKEND_URL}]
API_SPEC_OPTIONS['components'] = {
    "securitySchemes": {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    },
    "servers": [
        {"url": "/api"}
    ]
}
