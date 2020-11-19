"""This exposes the flask app singleton and creation function."""

from flask import Flask
import sys
from .configuration import configuration
from .controller.authenticator import (configure_authenticator,
                                       authenticator_blueprint)
from .model.database import configure_database
from .model.sandbox import add_demo, add_filler
from .view.ajax import ajax_blueprint
from .view.pages.diagram import diagram_blueprint
from .view.pages.information_page import info_blueprint
from .view.pages.report_result import result_report_blueprint
from .view.pages.benchmark_review import benchmark_review_blueprint
from .view.pages.benchmark_search import benchmark_search_blueprint
from .view.pages.site_review import site_review_blueprint
from .view.pages.view_report import view_report_blueprint
from .view.pages.add_benchmark import add_benchmark_blueprint
from .view.pages.upload_json import upload_json_blueprint
from .view.pages.search_result import result_search_blueprint
from .view.pages.privacy_policy import privacy_blueprint
from .view.pages.json_display import display_json_blueprint


def create_app():
    """Create the flask app object."""
    flask_application = Flask(__name__)

    if 'sphinx' in sys.modules:
        return flask_application

    configuration.reload()

    if configuration.get('debug'):
        flask_application.config['DEBUG'] = True
        # app.config['SQLALCHEMY_ECHO'] = True
        print("Running in debug mode")
    else:
        print("Running in production mode")

    flask_application.app_context().push()
    configure_database(flask_application)
    configure_authenticator(flask_application)

    if configuration.get('debug') and configuration.get('debug-db-demo-items'):
        add_demo()
    if configuration.get('debug') and configuration.get('debug-db-filler-items'):
        add_filler()

    flask_application.register_blueprint(ajax_blueprint)
    flask_application.register_blueprint(diagram_blueprint)
    flask_application.register_blueprint(info_blueprint)
    flask_application.register_blueprint(result_report_blueprint)
    flask_application.register_blueprint(benchmark_review_blueprint)
    flask_application.register_blueprint(site_review_blueprint)
    flask_application.register_blueprint(view_report_blueprint)
    flask_application.register_blueprint(add_benchmark_blueprint)
    flask_application.register_blueprint(benchmark_search_blueprint)
    flask_application.register_blueprint(authenticator_blueprint)
    flask_application.register_blueprint(upload_json_blueprint)
    flask_application.register_blueprint(result_search_blueprint)
    flask_application.register_blueprint(privacy_blueprint)
    flask_application.register_blueprint(display_json_blueprint)

    return flask_application


flask_app: Flask = create_app()
