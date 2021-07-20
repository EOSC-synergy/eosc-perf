"""Backend package for models definition."""
from datetime import datetime as dt

from backend.database import BaseModel, PkModel
from backend.extensions import auth
from flaat import tokentools
from flask_smorest import abort
from sqlalchemy import Column, DateTime, Text, UniqueConstraint, or_


class Tag(PkModel):
    """The Tag class represents a user-created label that can be used for
    filtering a list of results.

    These are entirely created by users and may not necessarily be related to
    any benchmark output data. These may be used to indicate if, for example, a
    benchmark is used to measure CPU or GPU performance, since some benchmarks
    may be used to test both.
    """

    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False, default="")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the tag.

        Returns:
            str: A human-readable representation string of the tag.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def query_with(cls, terms):
        """Query all tags containing all keywords.

        Args:
            terms (List[str]): A list of all keywords to match on the search.
        Returns:
            List[Tag]: A list containing all matching tags in the database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                or_(
                    Tag.name.contains(keyword),
                    Tag.description.contains(keyword)
                ))

        return results


class User(BaseModel):
    """A user of the app."""

    sub = Column(Text, primary_key=True, nullable=False)
    iss = Column(Text, primary_key=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow)

    __table_args__ = (
        UniqueConstraint('sub', 'iss'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)

    @classmethod
    def create(cls, token):
        token_info = tokentools.get_accesstoken_info(token)
        user_info = auth.get_info_from_introspection_endpoints(token)

        if not user_info:
            abort(500, messages={'introspection endpoint': "No user info"})

        elif 'email' not in user_info:
            abort(422, messages={'token': "No scope for email"})

        return super().create(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss'],
            email=user_info['email']
        )

    @classmethod
    def get(cls, sub=None, iss=None, token=None):

        if not sub and not iss and not token:
            raise TypeError("Missing sub & iss or token")

        elif not sub and not iss:
            token_info = tokentools.get_accesstoken_info(token)
            sub = token_info['body']['sub'],
            iss = token_info['body']['iss'],

        user = cls.query.get((sub, iss))
        if user:
            return user
        else:
            abort(404, messages={'user': "Not registered"})

    @classmethod
    def query_emails_with(cls, terms):
        results = cls.query
        for keyword in terms:
            results = results.filter(
                User.email.contains(keyword)
            )
        return results

    def update_info(self, token):
        user_info = auth.get_info_from_introspection_endpoints(token)
        return super().update(
            email=user_info['email']
        )
