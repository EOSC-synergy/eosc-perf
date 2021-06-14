"""User schemas."""
from json import dump
from marshmallow import Schema, fields


class User(Schema):
    sub = fields.String(dump_only=True)
    iss = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.String(dump_only=True)


class UserEdit(User):
    email = fields.Email()


class UserQuery(User):
    iss = fields.String()
    email = fields.String()
