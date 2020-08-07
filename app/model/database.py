"""This module exposes the database object (db) and the setup function."""
import os.path
from flask_sqlalchemy import SQLAlchemy

DATABASE_PATH: str = 'test.db'

db = SQLAlchemy()

def configure_database(app):
    """Set up the database with the given flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # delete database on debug launch
    if app.config['DEBUG']:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)

    # setup sqlalchemy for flask
    db.init_app(app)

    # create database if it does not exist
    if not os.path.exists(DATABASE_PATH):
        with app.app_context():
            db.create_all()
        