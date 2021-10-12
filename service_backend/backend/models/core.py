"""Models core for models parent classes."""
import uuid

from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean
from flask_sqlalchemy import BaseQuery

from ..extensions import db


class BaseCRUD(db.Model):
    """Base model that adds CRUD methods to the model.
    """
    __abstract__ = True

    @classmethod
    def create(cls, properties):
        """ Creates and saves a new record into the database.

        :param properties: Values to set on the model properties
        :type properties: dict
        :return: The record instance
        :rtype: :class:`MixinCRUD`
        """
        record = cls(**properties)
        db.session.add(record)
        return record

    @classmethod
    def read(cls, primary_key):
        """ Returns the record from the database matching the id.

        :param primary_key: Record with primary_key to retrieve
        :type primary_key: any
        :return: Record to retrieve or None
        :rtype: :class:`BaseModel` or None
        """
        with db.session.no_autoflush:
            return cls.query.get(primary_key)

    def update(self, properties):
        """Updates specific fields from a record in the database.

        :param properties: Values to set on the model properties
        :type properties: dict
        """
        for attr, value in properties.items():
            setattr(self, attr, value)
        db.session.add(self)

    def delete(self):
        """Deletes a specific record from the database.
        """
        if self in db.session.new:
            db.session.expunge(self)
        else:
            db.session.delete(self)


class QueryWithSoftDelete(BaseQuery):
    """Custom query to exclude soft delete items from model query.
    See https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy
    """  # noqa
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted\
                else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(
            self._only_full_mapper_zero('get'),
            session=db.session(), _with_deleted=True
        )

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None\
            or self._with_deleted\
            or not obj.deleted else None


class SoftDelete(BaseCRUD):
    """Mixin  model class with 'primary keys' columns for token `sub` and `iss`.
    """

    __abstract__ = True
    query_class = QueryWithSoftDelete

    #: (Bool) Flag to hide the item from normal queries
    deleted = Column(Boolean, nullable=False, default=False)

    @classmethod
    def read(cls, primary_key, with_deleted=False):
        if with_deleted:
            return cls.query.with_deleted().get(primary_key)
        else:
            return super().read(primary_key)

    def undelete(cls, primary_key):
        """Undeletes the indicated item (delete->False)
        """
        item = cls.query.get(primary_key)
        if item:
            item.deleted = False
            db.session.add(item)
        return item

    def delete(self, hard=False):
        """Deletes a specific record from the database.
        """
        if not hard:
            self.deleted = True
            db.session.add(self)
        else:
            return super().delete()


class PkModel(BaseCRUD):
    """Mixin class with 'primary key' column named `id`.
    """
    __abstract__ = True

    #: (UUID) Primary key with an Unique Identifier for the model instance
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TokenModel(BaseCRUD):
    """Mixin class with 'primary keys' columns for token `sub` and `iss`.
    """
    __abstract__ = True

    #: (Text) Primary key containing the OIDC subject the model instance
    sub = Column(Text, primary_key=True, nullable=False)

    #: (Text) Primary key containing the OIDC issuer of the model instance
    iss = Column(Text, primary_key=True, nullable=False)

    __table_args__ = (UniqueConstraint('sub', 'iss'),)
