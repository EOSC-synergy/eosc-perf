from flask_sqlalchemy import SQLAlchemy
import os.path

DATABASE_PATH: str = 'test.db'

db = SQLAlchemy()

def configure_database(app):
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
        