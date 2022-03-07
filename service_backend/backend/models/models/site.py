"""Sites module."""
from sqlalchemy import Column, ForeignKeyConstraint, Text
from sqlalchemy.orm import relationship

from ..core import PkModel
from .reports import NeedsApprove
from .user import HasUploader


class Site(NeedsApprove, HasUploader, PkModel):
    """The Site model represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers and
    should include a human readable name and physical location.
    """
    #: (Text, required) Human readable institution identification
    name = Column(Text, unique=True, nullable=False)

    #: (Text, required) Place where a site is physically located
    address = Column(Text, nullable=False)

    #: (Text) Useful site information to help users
    description = Column(Text, nullable=True)

    #: ([Flavor], read_only) List of flavors available at the site
    flavors = relationship(
        "Flavor", back_populates="site",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                             ['user.iss', 'user.sub']),
    )

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.name)
