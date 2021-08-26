"""Flavor module."""
from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr

from ..core import PkModel
from . import HasUploadDatetime
from .report import HasReports
from .user import HasUploader


class Flavor(HasReports, HasUploadDatetime, HasUploader, PkModel):
    """The Flavor model represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.

    **Properties**:
    """
    #: (Text, required) Text with virtual hardware template identification
    name = Column(Text, nullable=False)
    
    #: (Text) Text with useful information for users
    description = Column(Text, nullable=True, default="")

    #: (Site.id, required) Id of the Site the flavor belongs to
    site_id = Column(ForeignKey('site.id'), nullable=False)

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasUploader.__table_args__))
        mixin_indexes.extend([
            UniqueConstraint('site_id', 'name')
        ])
        return tuple(mixin_indexes)

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.name)
