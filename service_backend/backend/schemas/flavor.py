"""Flavor schemas."""
from marshmallow import Schema, fields


class Create(Schema):
    name = fields.String(required=True)
    description = fields.String()


class Edit(Schema):
    name = fields.String()
    description = fields.String()


class ListArgs(Schema):
    name = fields.String()
