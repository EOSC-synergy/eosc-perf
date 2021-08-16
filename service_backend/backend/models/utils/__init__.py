"""Utils subpackage with mixins and tools to extend models."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime

from . import dockerhub

__all__ = [
    "dockerhub",
    "HasCreationDate"
]


class HasCreationDate(object):
    """Mixin that adds creation date."""
    created_at = Column(DateTime, nullable=False, default=dt.now)
