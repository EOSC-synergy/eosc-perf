"""User schemas."""
from marshmallow import Schema, fields


class ListQueryArgs(Schema):
    iss = fields.String()
    email = fields.String()


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
