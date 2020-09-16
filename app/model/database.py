"""This module exposes the database object (db) and the setup function."""
import os.path
from flask_sqlalchemy import SQLAlchemy
from ..configuration import configuration

db = SQLAlchemy()

def configure_database(app):
    """Set up the database with the given flask app."""
    if len(configuration.get('database-path')) > 0:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + configuration.get('database-path')
    else:
        # in memory
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setup sqlalchemy for flask
    db.init_app(app)

    # delete database on debug launch
    if configuration.get('debug') and configuration.get('debug-db-reset'):
        if len(configuration.get('database-path')) > 0 \
            and os.path.exists(configuration.get('database-path')):
            os.remove(configuration.get('database-path'))
        # drop everything
        with app.app_context():
            db.drop_all()

    # create database if it does not exist
    if len(configuration.get('database-path')) == 0 \
        or not os.path.exists(configuration.get('database-path')):
        with app.app_context():
            db.create_all()
        