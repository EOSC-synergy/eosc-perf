# -*- coding: utf-8 -*-
"""Sites schemas."""
from marshmallow import Schema, fields


class Flavor(Schema):
    name = fields.String()
    custom_text = fields.String()


class Site(Schema):
    name = fields.String()
    address = fields.String()
    description = fields.String()
    hidden = fields.Boolean()
    # flavors = fields.List(fields.Nested(Flavor))


class SitesCreateArgs(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String()
    # flavors = fields.List(fields.Nested(Flavor))


class SitesQueryArgs(Schema):
    name = fields.String()
    address = fields.String()
    description = fields.String()
    hidden = fields.Boolean()
    # flavors = fields.List(fields.Nested(Flavor))
