"""Tag schemas."""
from marshmallow import Schema, fields


class Tag(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


class TagsQueryArgs(Schema):
    name = fields.String()


class EditTag(Schema):
    name = fields.String()
    description = fields.String()
