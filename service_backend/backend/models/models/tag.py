"""Tags module with mixin that provides a generic association
via a individually generated association tables for each parent class.
The associated objects themselves are persisted in a single table
shared among all parents.

See examples/generic_associations/table_per_association at the sqlalchemy
documentation.
"""
from sqlalchemy import Column, ForeignKey, Table, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from ..core import PkModel


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


class HasTags(object):
    """Mixin that creates a new tag_association table for each parent.
    """

    @declared_attr
    def tags(cls):
        name = cls.__tablename__
        tag_association = Table(
            f"{name}_tags", cls.metadata,
            Column(
                f"{name}_id", ForeignKey(f"{name}.id"),
                primary_key=True),
            Column(
                "tag_id", ForeignKey("tag.id", ondelete="CASCADE"),
                primary_key=True)
        )
        return relationship(Tag, secondary=tag_association)

    @declared_attr
    def tag_names(cls):
        return association_proxy('tags', 'name')
