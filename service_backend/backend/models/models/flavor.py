"""Flavor module."""
from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr

from ..core import PkModel
from . import HasCreationDate
from .report import HasReports
from .user import HasCreationUser


class Flavor(HasReports, HasCreationDate, HasCreationUser, PkModel):
    """The Flavor class represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.
    """
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    site_id = Column(ForeignKey('site.id'), nullable=False)

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasCreationUser.__table_args__))
        mixin_indexes.extend([
            UniqueConstraint('site_id', 'name')
        ])
        return tuple(mixin_indexes)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site flavor.

        Returns:
            str: A human-readable representation string of the site flavor.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)
