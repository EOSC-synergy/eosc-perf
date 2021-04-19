# -*- coding: utf-8 -*-
"""Application configuration.
For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

class BaseConfig(object):
    """Base config, with default values."""
    SECRET_KEY = env.str("SECRET_KEY")


class DbConfig(object):
    """Database configuration."""
    DB_ENGINE = env.str("DB_ENGINE")
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")
    DB_HOST = env.str("DB_HOST")
    DB_PORT = env.str("DB_PORT")
    DB_NAME = env.str("DB_NAME")
    DB_CONNECTION = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
    SQLALCHEMY_DATABASE_URI = f'{DB_CONNECTION}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class BCryptConfig(object):
    """BCrypt configuration."""
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)

class CacheConfig(object):
    """Cache configuration."""
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.

class AuthConfig(object):
    """Authorization configuration."""
    EGI_CLIENT_ID = env.str("OIDC_CLIENT_ID")
    EGI_CLIENT_SECRET = env.str("OIDC_CLIENT_SECRET")
    ADMIN_ASSURANCE = env.str("ADMIN_ASSURANCE")

class ApiConfig(object):
    """Api specs configuration."""
    API_TITLE = 'My API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        'security': [{"bearerAuth": []}],
        'components': {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }


class ProductionConfig(
    BaseConfig, DbConfig, BCryptConfig, CacheConfig, AuthConfig, ApiConfig
):
    """Uses production configuration server."""
    ENV = 'production'


class DevelopmentConfig(ProductionConfig):
    """Uses development configuration server."""
    ENV = 'development'


class TestingConfig(DevelopmentConfig):
    """Configuration used for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'{DbConfig.DB_CONNECTION}/tests'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "not-so-secret-in-tests"
    BCRYPT_LOG_ROUNDS = (4)  # For faster tests; 4 to avoid "Invalid rounds"
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


FLASK_ENV = env.str("FLASK_ENV", default="production")
if FLASK_ENV == 'development':
    class Configuration(DevelopmentConfig):
        pass
elif FLASK_ENV == 'testing':
    class TestingConfig(TestingConfig):
        pass
else:
    class Configuration(ProductionConfig):
        pass
