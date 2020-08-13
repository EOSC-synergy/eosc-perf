"""This module presents the app creation function exposed when importing the
module."""
import os
import code
from flask import Flask, redirect
from .configuration import configuration
from .controller.authenticator import (configure_authenticator,
                                       authenticator_blueprint)
from .model.database import db, configure_database
from .model.sandbox import add_dummies_if_not_exist
from .view.ajax import ajax_blueprint
from .view.pages.diagram import diagram_blueprint
from .view.pages.information_page import info_blueprint
from .view.pages.error_page import error_blueprint
from .view.pages.report_result import result_report_blueprint
from .view.pages.benchmark_review import benchmark_review_blueprint
from .view.pages.benchmark_search import benchmark_search_blueprint
from .view.pages.site_review import site_review_blueprint
from .view.pages.view_report import view_report_blueprint
from .view.pages.add_benchmark import add_benchmark_blueprint
from .view.pages.upload_json import upload_json_blueprint
from .view.pages.search_result import result_search_blueprint


def create_app(config):
    """Create the flask app object.

    Args:
        config (dict): A dictionary containing the configuration values."""
    flask_app = Flask(__name__)
    if config['debug']:
        flask_app.config['DEBUG'] = True
        #app.config['SQLALCHEMY_ECHO'] = True
        print("Running in debug mode")
    else:
        print("Running in production mode")

    flask_app.app_context().push()
    configure_database(flask_app, config)
    configure_authenticator(flask_app, config)

    if config['debug']:
        add_dummies_if_not_exist()

    flask_app.register_blueprint(ajax_blueprint)
    flask_app.register_blueprint(diagram_blueprint)
    flask_app.register_blueprint(info_blueprint)
    flask_app.register_blueprint(error_blueprint)
    flask_app.register_blueprint(result_report_blueprint)
    flask_app.register_blueprint(benchmark_review_blueprint)
    flask_app.register_blueprint(site_review_blueprint)
    flask_app.register_blueprint(view_report_blueprint)
    flask_app.register_blueprint(add_benchmark_blueprint)
    flask_app.register_blueprint(benchmark_search_blueprint)
    flask_app.register_blueprint(authenticator_blueprint)
    flask_app.register_blueprint(upload_json_blueprint)
    flask_app.register_blueprint(result_search_blueprint)

    return flask_app

app: Flask = create_app(configuration)
