"""This module exposes the function to create the Flask app object.
"""

from flask import Flask
import sys
from .configuration import configuration
from .controller.authenticator import configure_authenticator
from .controller.io_controller import controller
from .model.database import configure_database
from .model.sandbox import add_demo
from .view.ajax import ajax_blueprint
from .view.pages.authenticator import authenticator_blueprint
from .view.pages.basic_pages import basic_pages
from .view.pages.review.report_result import result_report_blueprint
from .view.pages.review.benchmark import benchmark_review_blueprint
from .view.pages.search.benchmarks import benchmark_search_blueprint
from .view.pages.review.site import site_review_blueprint
from .view.pages.review.result import view_report_blueprint
from .view.pages.submission.benchmarks import add_benchmark_blueprint
from .view.pages.submission.results import upload_json_blueprint
from .view.pages.search.results import result_search_blueprint
from .view.pages.site_editor import site_editor_blueprint


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

    if configuration.get('debug'):
        # flask_application.config['DEBUG'] = True
        # app.config['SQLALCHEMY_ECHO'] = True
        print("Running in debug mode")
    else:
        print("Running in production mode")

    flask_application.app_context().push()
    configure_database(flask_application)
    configure_authenticator(flask_application)
    
    controller.load_mailer()

    if configuration.get('debug') and configuration.get('debug-db-demo-items'):
        add_demo()

    flask_application.register_blueprint(ajax_blueprint)
    flask_application.register_blueprint(basic_pages)
    flask_application.register_blueprint(result_report_blueprint)
    flask_application.register_blueprint(benchmark_review_blueprint)
    flask_application.register_blueprint(site_review_blueprint)
    flask_application.register_blueprint(view_report_blueprint)
    flask_application.register_blueprint(add_benchmark_blueprint)
    flask_application.register_blueprint(benchmark_search_blueprint)
    flask_application.register_blueprint(authenticator_blueprint)
    flask_application.register_blueprint(upload_json_blueprint)
    flask_application.register_blueprint(result_search_blueprint)
    flask_application.register_blueprint(site_editor_blueprint)

    return flask_application
