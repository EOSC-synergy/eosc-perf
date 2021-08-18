"""Package with models definitions in modules."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime


class HasCreationDate(object):
    """Mixin that adds creation date."""
    #: (ISO8601) Creation datetime of the model instance
    created_at = Column(DateTime, nullable=False, default=dt.now)
