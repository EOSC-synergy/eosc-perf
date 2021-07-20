"""Tag schemas."""
from marshmallow import Schema, fields

__all__ = [
    "Tag", "TagsIds", "TagCreate", "TagEdit",
    "SearchQueryArgs", "TagsQueryArgs"
]


class Tag(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class TagsIds(Schema):
    tags_ids = fields.List(fields.UUID)


class TagCreate(Schema):
    name = fields.String(required=True)
    description = fields.String()


class TagEdit(Schema):
    name = fields.String()
    description = fields.String()


class TagsQueryArgs(Schema):
    name = fields.String()


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
