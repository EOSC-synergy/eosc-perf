"""Package with models definitions in modules."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime


class HasCreationDate(object):
    """Mixin that adds creation date."""
    created_at = Column(DateTime, nullable=False, default=dt.now)
