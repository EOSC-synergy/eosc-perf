"""This module declares the database object that internal components of the model will interact with, and exposes a
function to set it up at program start.
"""
import os.path
from flask_sqlalchemy import SQLAlchemy
from ..configuration import configuration

db = SQLAlchemy()


def configure_database(flask_app):
    """Set up the database with the given flask app."""
    if len(configuration.get('database-path')) > 0:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = configuration.get('database-path')
    else:
        # in memory sqlite as fallback
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setup sqlalchemy for flask
    db.init_app(flask_app)

    # delete database on debug launch
    if configuration.get('debug') and configuration.get('debug-db-reset'):
        if len(configuration.get('database-path')) > 0 \
                and os.path.exists(configuration.get('database-path')):
            os.remove(configuration.get('database-path'))
        # drop everything
        with flask_app.app_context():
            db.drop_all()

    # create database tables if they do not exist
    with flask_app.app_context():
        db.create_all()
