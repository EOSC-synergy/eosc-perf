"""Flavor module."""
from sqlalchemy import (Column, ForeignKey, ForeignKeyConstraint, Text,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from ..core import PkModel
from .reports import NeedsApprove
from .user import HasUploader


class Flavor(NeedsApprove, HasUploader, PkModel):
    """The Flavor model represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.

    **Properties**:
    """
    #: (Text, required) Text with virtual hardware template identification
    name = Column(Text, nullable=False)

    #: (Text) Text with useful information for users
    description = Column(Text, nullable=True)

    #: (Site.id, required) Id of the Site the flavor belongs to
    site_id = Column(ForeignKey('site.id'), nullable=False)

    #: (Site, required) Id of the Site the flavor belongs to
    site = relationship("Site", back_populates="flavors")

    __table_args__ = (
        UniqueConstraint('site_id', 'name'),
        ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                             ['user.iss', 'user.sub']),
    )

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.name)
