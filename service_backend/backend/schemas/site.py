"""Site schemas."""
from marshmallow import Schema, fields


class Create(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String()


class Edit(Schema):
    name = fields.String()
    address = fields.String()
    description = fields.String()


class ListArgs(Schema):
    name = fields.String()
    address = fields.String()


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
