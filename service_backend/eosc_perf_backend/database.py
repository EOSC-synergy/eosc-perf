# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import uuid

import sqlalchemy_utils

from eosc_perf_backend.extensions import db

# Extend db types
db.UUID = sqlalchemy_utils.UUIDType


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
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    @classmethod
    def filter_by(cls, **filters):
        """Get record by filtering."""
        return cls.query.filter_by(**filters)


class PkModel(Model):
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
