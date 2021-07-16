"""Application configuration.
For local development, use a .env file to set environment variables.
"""
import os

from environs import Env, EnvError

env = Env()
env.read_env()


ENV = env.str("FLASK_ENV", default="production")

available_environments = ["production", "development"]
if ENV not in available_environments:
    raise Exception(
        f"""Wrong FLASK_ENV configuration as {ENV}
        Use only {available_environments}"""
    )


# Base configuration
if ENV == 'production':
    try:
        SECRET_KEY = env.str("SECRET_KEY")
    except EnvError:
        SECRET_KEY_FILE = env.str("SECRET_KEY_FILE")
        SECRET_KEY = open(SECRET_KEY_FILE).read().rstrip('\n')
else:
    DEBUG = env.bool("DEBUG", default=True)
    SECRET_KEY_FILE = env.str("SECRET_KEY_FILE", "")
    if SECRET_KEY_FILE == "":
        SECRET_KEY = env.str("SECRET_KEY", default="not-so-secret")
    else:
        SECRET_KEY = open(SECRET_KEY_FILE).read().rstrip('\n')


# Database configuration
if ENV == 'production':
    DB_ENGINE = env.str("DB_ENGINE")
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")
    DB_HOST = env.str("DB_HOST")
    DB_PORT = env.str("DB_PORT")
    DB_NAME = env.str("DB_NAME")
else:
    DB_ENGINE = env.str("DB_ENGINE", default="not-defined")
    DB_USER = env.str("DB_USER", default="not-defined")
    DB_PASSWORD = env.str("DB_PASSWORD", default="not-defined")
    DB_HOST = env.str("DB_HOST", default="not-defined")
    DB_PORT = env.str("DB_PORT", default="not-defined")
    DB_NAME = env.str("DB_NAME", default="not-defined")

DB_CONNECTION = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
SQLALCHEMY_DATABASE_URI = f'{DB_CONNECTION}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Cache and crypt configuration
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


# Authorization configuration.
if ENV == 'production':
    EGI_CLIENT_ID = env.str("OIDC_CLIENT_ID")
    DISABLE_AUTHENTICATION = False
    DISABLE_ADMIN_PROTECTION = False
    ADMIN_ENTITLEMENTS = env.str("ADMIN_ENTITLEMENTS")
    try:
        EGI_CLIENT_SECRET = env.str("OIDC_CLIENT_SECRET")
    except EnvError:
        EGI_CLIENT_SECRET_FILE = env.str("OIDC_CLIENT_SECRET_FILE")
        EGI_CLIENT_SECRET = open(EGI_CLIENT_SECRET_FILE).read().rstrip('\n')
else:
    EGI_CLIENT_ID = env.str("OIDC_CLIENT_ID", default="not-defined")
    DISABLE_AUTHENTICATION = env.bool("DISABLE_AUTHENTICATION", default=True)
    DISABLE_ADMIN_PROTECTION = env.bool("DISABLE_ADMIN_PROTECTION", default=True)
    ADMIN_ENTITLEMENTS = env.str("ADMIN_ENTITLEMENTS", default=[])
    EGI_CLIENT_SECRET_FILE = env.str("OIDC_CLIENT_SECRET_FILE", "")
    if EGI_CLIENT_SECRET_FILE == "":
        EGI_CLIENT_SECRET = env.str("OIDC_CLIENT_SECRET", default="not-defined")
    else:
        EGI_CLIENT_SECRET = open(EGI_CLIENT_SECRET_FILE).read().rstrip('\n')


# API specs configuration
BACKEND_URL = env.str("BACKEND_URL", default="/")
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
    }
}
