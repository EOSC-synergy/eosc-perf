# -*- coding: utf-8 -*-
"""Sites schemas."""
from marshmallow import Schema, fields


class Flavor(Schema):
    id = fields.UUID()
    name = fields.String()
    custom_text = fields.String()


class FlavorsCreateArgs(Schema):
    name = fields.String(required=True)
    custom_text = fields.String()
