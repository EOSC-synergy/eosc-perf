"""User models."""
from datetime import datetime as dt

from backend.database import BaseModel
from marshmallow.fields import DateTime
from sqlalchemy import Column, DateTime, Text, UniqueConstraint
from sqlalchemy.sql.schema import UniqueConstraint


class User(BaseModel):
    """A user of the app."""

    sub = Column(Text, primary_key=True, nullable=False)
    iss = Column(Text, primary_key=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow)

    __table_args__ = (
        UniqueConstraint('sub', 'iss'),
    )

    @classmethod
    def get_by_subiss(cls, sub, iss):
        return cls.query.get_or_404((sub, iss))

    @classmethod
    def updt_or_add(cls, sub, iss, **kwargs):
        user = cls.query.get((sub, iss))
        if user:
            # Update user, for example: email, vo, ...
            return user.update(**kwargs)
        else:
            return cls.create(sub=sub, iss=iss, **kwargs)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)
