# -*- coding: utf-8 -*-
"""Sites models."""
from backend.database import PkModel, db
from backend.flavors.models import Flavor


flavor_association = db.Table(
    'site_flavor',
    db.Column('site_id', db.UUID, db.ForeignKey('site.id'), primary_key=True),
    db.Column('flavor_id', db.UUID, db.ForeignKey('flavor.id'), primary_key=True)
)


class Site(PkModel):
    """The Site class represents a location where a benchmark can be executed.
    This generally refers to the different virtual machine providers.
    """
    name = db.Column(db.Text(), unique=True, nullable=False)
    address = db.Column(db.Text(), nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.Text(), nullable=True)
    flavors = db.relationship("Flavor", secondary=flavor_association)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)