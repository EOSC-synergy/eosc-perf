"""Main application package."""
import logging
import sys

import marshmallow as ma
from flask import Flask
from webargs.flaskparser import FlaskParser

from .routes import benchmarks, reports, results, sites, tags, users
from .extensions import api         # Api interface module
from .extensions import bcrypt      # Encrypt passwords and others
from .extensions import cache       # Caches responses
from .extensions import db          # SQLAlchemy instance
from .extensions import migrate     # Alembic ext. manage db migrations
from .extensions import auth        # flaat ext. manage db migrations

# Raise ValidationError when unknown fields in query
FlaskParser.DEFAULT_UNKNOWN_BY_LOCATION["query"] = ma.RAISE


# Sourced from:
# https://web.archive.org/web/20131129080707/http://flask.pocoo.org/snippets/35
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app(
        config_base="backend.settings",
        **settings_override
):
    """Create application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_base)
    app.config.update(**settings_override)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    api.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    auth.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    api.register_blueprint(benchmarks.blueprint, url_prefix='/benchmarks')
    api.register_blueprint(reports.blp, url_prefix='/reports')
    api.register_blueprint(results.blueprint, url_prefix='/results')
    api.register_blueprint(sites.blueprint, url_prefix='/sites')
    api.register_blueprint(tags.blp, url_prefix='/tags')
    api.register_blueprint(users.blp, url_prefix='/users')


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
