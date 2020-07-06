from ..app import app

from flask_sqlalchemy import SQLAlchemy

import os
try:
    os.remove('app/test.db')
except:
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
