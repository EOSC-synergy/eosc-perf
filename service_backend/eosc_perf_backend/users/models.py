# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime as dt

from eosc_perf_backend.database import Model, db


class User(Model):
    """A user of the app."""

    sub = db.Column(db.Text(), primary_key=True, nullable=False)
    iss = db.Column(db.Text(), primary_key=True, nullable=False)
    email = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    benchmarks = db.relationship("Benchmark")

    @classmethod
    def get_by_subiss(cls, sub, iss):
        return cls.query.get_or_404((sub, iss))

    @classmethod
    def get_by_subiss_or_create(cls, sub, iss, **kwargs):
        user = cls.query.get((sub, iss))
        if user:
            return user
        else:
            return cls.create(sub=sub, iss=iss, **kwargs)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)
