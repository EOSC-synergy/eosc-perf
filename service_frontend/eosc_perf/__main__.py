"""This module contains a main clause so you can run the application as a module directly.

TODO: determine if this can be removed, e.g. if we only support deploying by docker-compose
"""
from .flask_factory import create_app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
