# -*- coding: utf-8 -*-
"""User schemas."""
from marshmallow import Schema, fields


class User(Schema):
    id = fields.UUID()
    email = fields.Email()
    created_at = fields.String()


class UsersCreateArgs(Schema):
    email = fields.String(required=True)


class UsersQueryArgs(Schema):
    email = fields.String()


class Uploader(User):
    pass
