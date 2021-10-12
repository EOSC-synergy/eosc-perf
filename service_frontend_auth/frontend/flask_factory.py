"""This module exposes the function to create the Flask app object.
"""

import sys

from flask import Flask

from .configuration import configuration
from .controller.io_controller import controller
from .view.pages.authenticator import authenticator_blueprint


# sourced from: https://web.archive.org/web/20131129080707/http://flask.pocoo.org/snippets/35/
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


def create_app(custom_configuration: dict = None):
    """Create the flask app object."""
    flask_application = Flask(__name__)

    if 'sphinx' in sys.modules:
        return flask_application

    if custom_configuration is None:
        configuration.reload()
    else:
        configuration.reset()
        for key, value in custom_configuration.items():
            configuration.set(key, value)

    flask_application.wsgi_app = ReverseProxied(flask_application.wsgi_app)

    if configuration.get('debug'):
        print("Running in debug mode")
    else:
        print("Running in production mode")

    flask_application.app_context().push()

    controller.load_authenticator(flask_application)

    flask_application.register_blueprint(authenticator_blueprint)

    return flask_application
