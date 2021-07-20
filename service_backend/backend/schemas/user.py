"""User schemas."""
from marshmallow import Schema, fields


class FilterArgs(Schema):
    iss = fields.String()
    email = fields.String()


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
