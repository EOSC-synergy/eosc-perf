# -*- coding: utf-8 -*-
"""Sites models."""
from eosc_perf.database import PkModel, db


class Flavor(PkModel):
    """The SiteFlavor class represents a flavor of virtual machines available
    for usage on a Site. Flavours can be pre-existing options filled in by 
    administrators or a custom configuration by the user. Custom flavors' names
    should be set to SiteFlavor.CUSTOM_FLAVOR and can be distinguished from the
    pre-filled flavors with SiteFlavor.is_unique().
    """
    name = db.Column(db.Text(), unique=True, nullable=False)
    custom_text = db.Column(db.Text(), nullable=True, default=None)
