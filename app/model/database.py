from flask_sqlalchemy import SQLAlchemy
import os.path

DATABASE_PATH: str = 'test.db'

db = SQLAlchemy()

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' # + DATABASE_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
