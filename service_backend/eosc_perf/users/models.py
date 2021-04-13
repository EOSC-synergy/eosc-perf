# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from eosc_perf.database import PkModel, db


class User(PkModel):
    """A user of the app."""
    email = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
