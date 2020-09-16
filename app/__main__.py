"""Launch code in case the module is ran directly."""
from .flask_app import flask_app

if __name__ == '__main__':
    flask_app.run()
