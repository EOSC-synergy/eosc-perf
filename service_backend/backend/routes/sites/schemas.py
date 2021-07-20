"""Site schemas."""
from marshmallow import Schema, fields


__all__ = [
    "Site", "SiteCreate", "SiteEdit", "SiteQueryArgs", "SearchArgs",
    "Flavor", "FlavorCreate", "FlavorEdit", "FlavorQueryArgs"
]


class Site(Schema):
    id = fields.UUID()
    name = fields.String()
    address = fields.String()
    description = fields.String()


class SiteCreate(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String()


class SiteEdit(Schema):
    name = fields.String()
    address = fields.String()
    description = fields.String()


class Flavor(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class FlavorCreate(Schema):
    name = fields.String(required=True)
    description = fields.String()


class FlavorEdit(Schema):
    name = fields.String()
    description = fields.String()


class SiteQueryArgs(Schema):
    name = fields.String()
    address = fields.String()


class FlavorQueryArgs(Schema):
    name = fields.String()


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
