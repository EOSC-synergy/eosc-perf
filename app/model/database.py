"""This module exposes the database object (db) and the setup function."""
import os.path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure_database(app, config):
    """Set up the database with the given flask app."""
    if len(config['database-path']) > 0:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + config['database-path']
    else:
        # in memory
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setup sqlalchemy for flask
    db.init_app(app)

    # delete database on debug launch
    if config['debug'] and config['debug-db-reset']:
        if len(config['database-path']) > 0 and os.path.exists(config['database-path']):
            os.remove(config['database-path'])
        # drop everything
        with app.app_context():
            db.drop_all()

    # create database if it does not exist
    if len(config['database-path']) == 0 or not os.path.exists(config['database-path']):
        with app.app_context():
            db.create_all()
        