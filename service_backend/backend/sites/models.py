"""Site models."""
from backend.database import PkModel
from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType as UUID


class Site(PkModel):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """

    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    flavors = relationship(
        "Flavor",
        cascade="all, save-update, delete-orphan")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)


class Flavor(PkModel):
    """The Flavor class represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.
    """

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    site_id = Column(ForeignKey('site.id'))

    __table_args__ = (
        UniqueConstraint('site_id', 'name'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site flavor.

        Returns:
            str: A human-readable representation string of the site flavor.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)
