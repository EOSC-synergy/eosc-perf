"""Site models."""
from enum import unique
from backend.database import PkModel, db


class Site(PkModel):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """

    name = db.Column(db.Text(), unique=True, nullable=False)
    address = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True, default="")
    flavors = db.relationship(
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

    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True, default="")
    site_id = db.Column(db.UUID, db.ForeignKey('site.id'))

    __table_args__ = (
        db.UniqueConstraint('site_id', 'name'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site flavor.

        Returns:
            str: A human-readable representation string of the site flavor.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)
