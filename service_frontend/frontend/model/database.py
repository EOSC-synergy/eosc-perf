"""This module declares the database object that internal components of the model will interact with, and exposes a
function to set it up at program start. Modules outside the model subpackage should not make use of the database object
directly.
"""

from flask_sqlalchemy import SQLAlchemy

from ..configuration import configuration

db = SQLAlchemy()


def configure_database(flask_app):
    """Set up the database with the given flask app."""
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = configuration.database.determine_sqlalchemy_url()
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setup sqlalchemy for flask
    db.init_app(flask_app)

    # delete database on debug launch
    if configuration.get('debug') and configuration.get('debug-db-reset'):
        # drop everything
        with flask_app.app_context():
            db.drop_all()

    # create database tables if they do not exist
    with flask_app.app_context():
        db.create_all()
