"""Sites module."""
import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from ..core import PkModel
from ..utils import HasCreationDate
from .report import HasReports
from .user import HasCreationUser


class Site(HasReports, HasCreationDate, HasCreationUser, PkModel):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    flavors = relationship("Flavor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def search(cls, terms):
        """Query all sites containing all keywords in the columns.

        Args:
            terms (List[str]): A list of all keywords that need to be matched.
        Returns:
            List[Result]: A list containing all matching query sites in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                sa.or_(
                    Site.name.contains(keyword),
                    Site.address.contains(keyword),
                    Site.description.contains(keyword)
                ))

        return results
