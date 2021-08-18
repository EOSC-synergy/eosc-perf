"""Models module package for main models definition."""
from flask_smorest import abort
from sqlalchemy import Column, ForeignKeyConstraint, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from ..core import TokenModel
from . import HasCreationDate

from flaat import tokentools
from flask import request


class User(HasCreationDate, TokenModel):
    """The User model represents the users of the application. Users are
    build over a OIDC token model, therefore are identified based on the
    'Subject' and 'issuer' identifications provided by the OIDC provider.

    Also an email is collected which is expected to match the one provided
    by the ODIC introspection endpoint.

    **Properties**:
    """
    #: (Email) Electronic mail collected from OIDC access token
    email = Column(Text, unique=True, nullable=False)

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.name)


class HasCreationUser(object):
    """Mixin that adds an User as creation details to any model."""

    #: (Text) OIDC subject of the user that created the model instance,
    #: *conflicts with created_by*
    creator_sub = Column(Text, nullable=False)

    #: (Text) OIDC issuer of the user that created the model instance,
    #: *conflicts with created_by*
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
        """(User class) User that created the model instance"""
        return relationship("User", backref=backref(
            f'_{cls.__name__.lower()}s', cascade="all, delete-orphan"
        ))

    def ownership(self):
        access_token = tokentools.get_access_token_from_request(request)
        return self.created_by == User.get(token=access_token)

    def update(self, param, force=False, **kwargs):
        if force or self.ownership():
            super().update(param, **kwargs)
        else:
            abort(403)
