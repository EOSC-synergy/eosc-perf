# -*- coding: utf-8 -*-
"""Flavors schemas."""
from marshmallow import Schema, fields
from . import models


class Flavor(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    custom_text = fields.String()


class FlavorEdit(Flavor):
    name = fields.String(required=False)


class FlavorQuery(Flavor):
    name = fields.String(required=False)


class FlavorNames(fields.List):
    """Field that serializes and deserializes flavor_name from flavors.
    Fix for https://github.com/marshmallow-code/apispec/issues/459
    """

    def __init__(self, **kwargs):
        super().__init__(fields.String(), **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return [x.name for x in obj.flavors]

    def _deserialize(self, value, attr, data, **kwargs):
        flavors_query = models.Flavor.name.in_(value)
        return models.Flavor.query.filter(flavors_query).all()
