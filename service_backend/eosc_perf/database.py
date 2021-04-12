# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import uuid

from flask import abort

from eosc_perf.extensions import db


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

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


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = db.Column(db.String(40), primary_key=True)

    def __init__(cls, id=str(uuid.uuid4()), **kwargs):
        super().__init__(**kwargs)
        cls.id = id

    @classmethod
    def get_by_id(cls, record_id=None):
        """Get record by ID."""
        if record_id:
            return cls.query.get_or_404(record_id)
        else:
            abort(400)

    @classmethod
    def get(cls, filters):
        """Get record by filtering."""
        return cls.query.filter_by(**filters)
