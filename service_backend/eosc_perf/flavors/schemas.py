# -*- coding: utf-8 -*-
"""Flavors schemas."""
from eosc_perf.extensions import ma

from . import models


class Flavor(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.Flavor

    id = ma.UUID(dump_only=True)


class FlavorEdit(Flavor):
    name = ma.auto_field(required=False)


class FlavorQuery(Flavor):
    name = ma.auto_field(required=False)


class Flavor_names(ma.List):
    """Field that serializes and deserializes flavor_name from flavors.
    Fix for https://github.com/marshmallow-code/apispec/issues/459
    """

    def __init__(self, **kwargs):
        super().__init__(ma.String(), **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return [x.name for x in obj.flavors]

    def _deserialize(self, value, attr, data, **kwargs):
        flavors_query = models.Flavor.name.in_(value)
        return models.Flavor.query.filter(flavors_query).all()
