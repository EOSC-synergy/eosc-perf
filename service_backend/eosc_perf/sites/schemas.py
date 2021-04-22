# -*- coding: utf-8 -*-
"""Sites schemas."""
from eosc_perf.extensions import ma

from eosc_perf.flavors.schemas import Flavor, Flavor_names
from . import models


class Base(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Site

    id = ma.UUID(dump_only=True)
    hidden = ma.Boolean(dump_only=True)

class Site(Base):
    # https://github.com/marshmallow-code/apispec/issues/459
    # flavor_names = ma.Pluck(Flavor, 'name', many=True)
    flavors = Flavor_names()


class SiteEdit(Site):
    name = ma.auto_field(required=False)
    address = ma.auto_field(required=False)
    hidden = ma.Boolean(dump_only=False)


class SiteQuery(Base):
    name = ma.auto_field(required=False)
    address = ma.auto_field(required=False)
    hidden = ma.Boolean(dump_only=False)
