"""This module exposes a singleton instance for import by wsgi applications like uwsgi.
"""

from .flask_factory import create_app

flask_app = create_app()
