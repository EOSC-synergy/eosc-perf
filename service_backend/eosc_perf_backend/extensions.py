# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flaat import Flaat
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

flaat = Flaat()
bcrypt = Bcrypt()
cache = Cache()
migrate = Migrate()
api = Api()
db = SQLAlchemy()
