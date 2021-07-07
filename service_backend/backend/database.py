"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import uuid

import flask
from sqlalchemy import Column
from sqlalchemy.exc import *
from sqlalchemy_utils import UUIDType as UUID

from backend.extensions import db

Table = db.Table


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD 
    (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                flask.abort(409)
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class BaseModel(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    @classmethod
    def filter_by(cls, **filters):
        """Get record by filtering."""
        filters = {k: v for k, v in filters.items() if v}
        return cls.query.filter_by(**filters)


class PkModel(BaseModel):
    """Base model class that includes CRUD convenience methods, 
    plus adds a 'primary key' column named ``id``."""
    __abstract__ = True
    id = Column(UUID(binary=False), primary_key=True)

    def __init__(self, id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = id if id else uuid.uuid4()

    @classmethod
    def get_by_id(cls, id):
        """Get record by ID."""
        return cls.query.get_or_404(id)
