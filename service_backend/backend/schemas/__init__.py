"""Backend package for schemas definition."""
from marshmallow import Schema, fields

from . import tag, user


class Tag(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class User(Schema):
    sub = fields.String()
    iss = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
