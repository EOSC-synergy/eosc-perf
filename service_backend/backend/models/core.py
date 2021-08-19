"""Models core for models parent classes."""
import uuid

from backend.extensions import db
from flaat import tokentools
from flask_smorest import abort
from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError


class BaseModel(db.Model):
    """Base model class that includes CRUD convenience methods
    create, read, update & delete operations."""
    __abstract__ = True

    @classmethod
    def create(cls, param):
        """Creates a new record and save it the database.

        :param param: Values to set on the model properties
        :type param: dict
        :raises Conflict: Database conflict on new instance
        :return: The new created database model instance
        :rtype: :class:`BaseModel`
        """
        instance = cls(**param)
        return instance.save()

    def update(self, param, commit=True):
        """Updates specific fields of a record.

        :param param: Values to set on the model properties
        :type param: dict
        :param commit: Commit changes, defaults to True
        :type commit: bool, optional
        :return: True, or instance if commit flag is False
        :rtype: True or :class:`BaseModel`
        """
        for attr, value in param.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Adds the record to the session.

        :param commit: Commit changes, defaults to True
        :type commit: bool, optional
        :return: Saved instance 
        :rtype: :class:`BaseModel`
        """
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                abort(409)
        return self

    def delete(self, commit=True):
        """Adds a record remove request to the session.
        
        :param commit: Commit changes, defaults to True
        :type commit: bool, optional
        :return: True, or session commit result if commit flag is False
        :rtype: bool
        """
        db.session.delete(self)
        return commit and db.session.commit()


class PkModel(BaseModel):
    """Base model class that includes CRUD convenience methods,
    plus adds a 'primary key' column named `id`."""
    __abstract__ = True

    #: (UUID) Primary key with an Unique Identifier for the model instance
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @classmethod
    def get(cls, id):
        """Get record by ID."""
        return cls.query.get_or_404(id)


class TokenModel(BaseModel):
    """Base model class that includes CRUD convenience methods,
    plus adds 'primary keys' columns for token `sub` and `iss`."""
    __abstract__ = True

    #: (Text) Primary key containing the OIDC subject the model instance 
    sub = Column(Text, primary_key=True, nullable=False)

    #: (Text) Primary key containing the OIDC issuer of the model instance
    iss = Column(Text, primary_key=True, nullable=False)

    __table_args__ = (UniqueConstraint('sub', 'iss'),)

    @classmethod
    def create(cls, token, param):
        token_info = tokentools.get_accesstoken_info(token)
        return super().create(dict(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss'],
            **param
        ))

    @classmethod
    def get(cls, token):
        token_info = tokentools.get_accesstoken_info(token)
        sub = token_info['body']['sub'],
        iss = token_info['body']['iss'],
        return cls.query.get_or_404((sub, iss))

