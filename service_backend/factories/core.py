"""Factories package to offer utils to fill the backend database."""
from datetime import datetime

from backend.extensions import db
from factory.fuzzy import FuzzyNaiveDateTime

fdt = FuzzyNaiveDateTime(datetime(2000, 1, 1))


class BaseMeta:
    """Factory configuration to extend to all factory objects."""
    # Use the not-so-global scoped_session
    # Warning: DO NOT USE common.Session()!

    #: Use the application session
    sqlalchemy_session = db.session
