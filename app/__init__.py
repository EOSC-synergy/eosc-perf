"""This module presents the app creation function exposed when importing the
module."""
import os
import code
from flask import Flask, request
from .controller.authenticator import authenticator
from .model.database import db, DATABASE_PATH, configure_database
from .model.facade import facade
from .model.sandbox import add_dummies_if_not_exist
from .view.ajax import ajax_blueprint
from .view.pages.diagram import diagram_blueprint
from .view.pages.information_page import info_blueprint
from .view.pages.error_page import error_blueprint
import os
import code


def create_app(debug: bool):
    """Create the flask app object.

    Args:
            debug (bool): Whether to start in debug mode."""
    app = Flask(__name__)
    if debug:
        app.config['DEBUG'] = True
        #app.config['SQLALCHEMY_ECHO'] = True
    configure_database(app)

    authenticator(app)

    if debug:
        add_dummies_if_not_exist(app)

    @app.route('/')
    def root():
        return 'hello'

    app.register_blueprint(ajax_blueprint)
    app.register_blueprint(diagram_blueprint)
    app.register_blueprint(info_blueprint)
    app.register_blueprint(error_blueprint)

    return app
