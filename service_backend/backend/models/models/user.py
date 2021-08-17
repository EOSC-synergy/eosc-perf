"""Models module package for main models definition."""
from backend.extensions import auth
from flask.helpers import NotFound
from flask_smorest import abort
from sqlalchemy import Column, ForeignKeyConstraint, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from ..core import TokenModel
from . import HasCreationDate

from flaat import tokentools
from flask import request


class User(HasCreationDate, TokenModel):
    """A user of the app."""
    email = Column(Text, unique=True, nullable=False)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)


class HasCreationUser(object):
    """Mixin that adds creation details utils."""

    #: OIDC Subject of the creator user
    creator_sub = Column(Text, nullable=False)

    #: OIDC Issuer of the creator user
    creator_iss = Column(Text, nullable=False)

    def __init__(self, *args, created_by=None, **kwargs):
        if not created_by:
            access_token = tokentools.get_access_token_from_request(request)
            created_by = User.get(token=access_token)
        return super().__init__(*args, created_by=created_by, **kwargs)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(['creator_iss', 'creator_sub'],
                                 ['user.iss', 'user.sub']),
        )

    @declared_attr
    def created_by(cls):
        return relationship("User", backref=backref(
            f'{cls.__name__.lower()}s', cascade="all, delete-orphan"
        ))

    def ownership(self):
        access_token = tokentools.get_access_token_from_request(request)
        return self.created_by == User.get(token=access_token)

    def update(self, param, force=False, **kwargs):
        if force or self.ownership():
            super().update(param, **kwargs)
        else:
            abort(403)
