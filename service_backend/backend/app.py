"""Application module where to define the flask application and
extensions to build the backend package.
"""
import logging
import sys

import marshmallow as ma
from flask import Flask
from webargs.flaskparser import FlaskParser

from . import routes
from .extensions import api         # Api interface module
from .extensions import auth        # flaat ext. manage db migrations
from .extensions import bcrypt      # Encrypt passwords and others
from .extensions import db          # SQLAlchemy instance
from .extensions import migrate     # Alembic ext. manage db migrations
from .extensions import mail        # Mail ext. to send notifications

#: Raise ValidationError when unknown fields in query
FlaskParser.DEFAULT_UNKNOWN_BY_LOCATION["query"] = ma.RAISE


# Sourced from:
# https://web.archive.org/web/20131129080707/http://flask.pocoo.org/snippets/35
class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:

    .. code-block:: nginx

        location /myprefix {
            proxy_pass http://192.168.0.1:5001;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Script-Name /myprefix;
            }

    :param app: the WSGI application
    :type app: flask.Flask application
    """

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


def create_app(config_base="backend.settings", **settings_override):
    """Create application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories

    :param config_base: Configuration object, defaults to "backend.settings"
    :type config_base: str, optional
    :return: EOSC Performance API instance
    :rtype: :class:`flask.app.Flask`
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
    db.init_app(app)
    migrate.init_app(app, db)
    auth.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    api.register_blueprint(routes.benchmarks.blp, url_prefix='/benchmarks')
    api.register_blueprint(routes.reports.blp, url_prefix='/reports')
    api.register_blueprint(routes.results.blp, url_prefix='/results')
    api.register_blueprint(routes.sites.blp, url_prefix='/sites')
    api.register_blueprint(routes.flavors.blp, url_prefix='/flavors')
    api.register_blueprint(routes.tags.blp, url_prefix='/tags')
    api.register_blueprint(routes.users.blp, url_prefix='/users')


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
