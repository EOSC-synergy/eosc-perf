"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import uuid

import flask
import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext import associationproxy

from backend.extensions import db

# Extend db types
db.UUID = sqlalchemy_utils.UUIDType
db.Json = sqlalchemy.dialects.postgresql.JSON
db.Jsonb = sqlalchemy.dialects.postgresql.JSONB
db.exc = sqlalchemy.exc
db.association_proxy = associationproxy.association_proxy


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
            except db.exc.IntegrityError:
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
    id = db.Column(db.UUID(binary=False), primary_key=True)

    def __init__(self, id=None, **kwargs):
        super().__init__(**kwargs)
        self.id = id if id else uuid.uuid4()

    @classmethod
    def get_by_id(cls, id):
        """Get record by ID."""
        return cls.query.get_or_404(id)
