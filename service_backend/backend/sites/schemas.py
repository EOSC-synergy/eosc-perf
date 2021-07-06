"""Site schemas."""
from marshmallow import Schema, fields


class Site(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String()
    flavors = fields.Nested("Flavor", many=True)


class Site_simple(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String()


class Flavor(Schema):
    name = fields.String(required=True)
    description = fields.String()


class Flavor_simple(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String()


class EditSite(Schema):
    name = fields.String()
    address = fields.String()


class EditFlavor(Schema):
    name = fields.String()
    description = fields.String()


class SiteQueryArgs(Schema):
    name = fields.String()
    address = fields.String()


class FlavorQueryArgs(Schema):
    name = fields.String()
