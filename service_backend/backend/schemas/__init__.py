"""Backend package for schemas definition."""
from marshmallow import Schema, fields
from . import user


class User(Schema):
    sub = fields.String()
    iss = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
