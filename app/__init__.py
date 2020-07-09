# package root
from flask import Flask, request
from .model.database import db, DATABASE_PATH, configure_database
from .model.facade import facade
from .model.sandbox import add_dummy_objects
from .view.ajax import ajax_blueprint
import os
import code

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    configure_database(app)

    # delete while developing
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    add_dummy_objects(app)

    @app.route('/')
    def root():
        return 'hello'

    app.register_blueprint(ajax_blueprint)

    return app
    
def run_app():
    app = create_app()
    app.run()
