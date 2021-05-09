# -*- coding: utf-8 -*-
"""Sites schemas."""
from eosc_perf_backend.flavors.schemas import FlavorNames
from marshmallow import Schema, fields


class Site(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    hidden = fields.Boolean(dump_only=True)
    description = fields.String()
    flavors = FlavorNames()


class SiteEdit(Site):
    name = fields.String()     # required=False
    address = fields.String()  # required=False
    hidden = fields.Boolean()  # dump_only=False


class SiteQuery(Site):
    name = fields.String()     # required=False
    address = fields.String()  # required=False
    hidden = fields.Boolean()  # dump_only=False

    class Meta:
        exclude = ('flavors',)
