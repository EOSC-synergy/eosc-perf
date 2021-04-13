# -*- coding: utf-8 -*-
"""Sites models."""
from eosc_perf.database import PkModel, db


flavor_association = db.Table(
    'site_flavor',
    db.Column('site_id', db.UUID, db.ForeignKey('site.id'), primary_key=True),
    db.Column('flavor_id', db.UUID, db.ForeignKey('flavor.id'), primary_key=True)
)


class Site(PkModel):
    """The Site class represents a location where a benchmark can be executed.
    This generally refers to the different virtual machine providers.
    """
    name = db.Column(db.Text(), unique=True, nullable=True)
    address = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    hidden = db.Column(db.Boolean, nullable=False, default=True)
    flavors = db.relationship("Flavor", secondary=flavor_association)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)


class Flavor(PkModel):
    """The SiteFlavor class represents a flavor of virtual machines available
    for usage on a Site. Flavours can be pre-existing options filled in by 
    administrators or a custom configuration by the user. Custom flavors' names
    should be set to SiteFlavor.CUSTOM_FLAVOR and can be distinguished from the
    pre-filled flavors with SiteFlavor.is_unique().
    """
    name = db.Column(db.Text(), unique=True, nullable=False)
    custom_text = db.Column(db.Text(), nullable=True, default=None)
