"""Tag schemas."""
from marshmallow import Schema, fields


class Ids(Schema):
    tags_ids = fields.List(fields.UUID)


class Create(Schema):
    name = fields.String(required=True)
    description = fields.String()


class Edit(Schema):
    name = fields.String()
    description = fields.String()


class FilterArgs(Schema):
    name = fields.String()


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
