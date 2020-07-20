# package root
from flask import Flask, request
from .model.database import db, DATABASE_PATH, configure_database
from .model.facade import facade
from .model.sandbox import add_dummies_if_not_exist
from .view.ajax import ajax_blueprint
from .view.diagram_factory import diagram_blueprint
import os
import code


def create_app(debug: bool):
    app = Flask(__name__)
    if debug:
        app.config['DEBUG'] = True
    configure_database(app)

    if debug:
        add_dummies_if_not_exist(app)

    @app.route('/')
    def root():
        return 'hello'

    app.register_blueprint(ajax_blueprint)
    app.register_blueprint(diagram_blueprint)

    return app
