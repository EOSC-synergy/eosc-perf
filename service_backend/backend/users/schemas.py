"""User schemas."""
from marshmallow import Schema, fields


__all__ = [
    "User", "SearchQueryArgs", "UserQueryArgs"
]


class User(Schema):
    sub = fields.String()
    iss = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class UserQueryArgs(User):
    iss = fields.String()
    email = fields.String()


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
