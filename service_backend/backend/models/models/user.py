"""Models module package for main models definition."""
from backend.extensions import auth
from flask.helpers import NotFound
from flask_smorest import abort
from sqlalchemy import Column, ForeignKeyConstraint, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from ..core import TokenModel
from ..utils import HasCreationDate


class User(HasCreationDate, TokenModel):
    """A user of the app."""
    email = Column(Text, unique=True, nullable=False)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)

    @classmethod
    def create(cls, token):
        user_info = auth.get_info_from_introspection_endpoints(token)
        if not user_info:
            abort(500, messages={'introspection endpoint': "No user info"})
        elif 'email' not in user_info:
            abort(422, messages={'token': "No scope for email"})
        else:
            return super().create(token, email=user_info['email'])

    @classmethod
    def get(cls, token):
        try:
            return super().get(token)
        except NotFound:
            abort(403, messages={'user': "Not registered"})

    def update(self, token):
        user_info = auth.get_info_from_introspection_endpoints(token)
        return super().update(email=user_info['email'])

    @classmethod
    def search(cls, terms):
        results = cls.query
        for keyword in terms:
            results = results.filter(
                User.email.contains(keyword)
            )
        return results


class HasCreationUser(object):
    """Mixin that adds creation details utils."""
    creator_iss = Column(Text, nullable=False)
    creator_sub = Column(Text, nullable=False)

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
