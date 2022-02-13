"""Models module package for main models definition."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from ...extensions import auth
from ..core import TokenModel


class User(TokenModel):
    """The User model represents the users of the application. Users are
    build over a OIDC token model, therefore are identified based on the
    'Subject' and 'issuer' identifications provided by the OIDC provider.

    Also an email is collected which is expected to match the one provided
    by the ODIC introspection endpoint.

    Note an user might have multiple accounts with different ODIC providers
    and on each of them use the same email. Therefore the email cannot be
    a unique entity.

    **Properties**:
    """

    #: (Email) Electronic mail collected from OIDC access token
    # Should not be unique -> User can use multiple OIDC providers
    email = Column(Text, unique=False, nullable=False)

    #: (DateTime) Time when the user was registered
    registration_datetime = Column(DateTime, nullable=False, default=dt.now())

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.email)

    @classmethod
    def current_user(cls):
        tokeninfo = auth.current_tokeninfo()
        return cls.read((tokeninfo['sub'], tokeninfo['iss']))


class HasUploader(object):
    """Mixin that adds an User as upload details to any model."""
    __abstract__ = True

    #: (Text) OIDC subject of the user that created the model instance,
    #: *conflicts with uploader*
    uploader_sub = Column(Text, nullable=False)

    #: (Text) OIDC issuer of the user that created the model instance,
    #: *conflicts with uploader*
    uploader_iss = Column(Text, nullable=False)

    #: (ISO8601) Upload datetime of the model instance
    upload_datetime = Column(DateTime, nullable=False, default=dt.now)

    def __init__(self, **properties):
        super().__init__(**properties)
        if self.uploader is None:
            self.uploader = User.current_user()

    @declared_attr
    def uploader(cls):
        """(User class) User that uploaded the model instance"""
        return relationship("User", backref=backref(
            f'_{cls.__name__.lower()}s', cascade="all, delete-orphan"
        ))

    def update(self, *args, force=False, **kwargs):
        """Decorates super() that only owner can edit unless force=True.
        """
        if force or self.ownership():
            super().update(*args, **kwargs)
        else:
            raise PermissionError

    def ownership(self):
        return self.uploader == User.current_user()
