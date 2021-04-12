# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from eosc_perf.database import PkModel, db


class User(PkModel):
    """A user of the app."""
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)


class Uploader(PkModel):
    """A user with upload options in the app."""
    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User)
