"""Backend package for models definition."""
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
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                abort(409)
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class PkModel(BaseModel):
    """Base model class that includes CRUD convenience methods,
    plus adds a 'primary key' column named `id`."""
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @classmethod
    def get(cls, id):
        """Get record by ID."""
        return cls.query.get_or_404(id)


class TokenModel(BaseModel):
    """Base model class that includes CRUD convenience methods,
    plus adds 'primary keys' columns for token `sub` and `iss`."""
    __abstract__ = True
    sub = Column(Text, primary_key=True, nullable=False)
    iss = Column(Text, primary_key=True, nullable=False)
    __table_args__ = (UniqueConstraint('sub', 'iss'),)

    @classmethod
    def create(cls, token, **kwargs):
        token_info = tokentools.get_accesstoken_info(token)
        return super().create(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss'],
            **kwargs
        )

    @classmethod
    def get(cls, token):
        token_info = tokentools.get_accesstoken_info(token)
        sub = token_info['body']['sub'],
        iss = token_info['body']['iss'],
        return cls.query.get_or_404((sub, iss))
