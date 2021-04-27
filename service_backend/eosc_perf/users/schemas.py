# -*- coding: utf-8 -*-
"""User schemas."""
from marshmallow import Schema, fields


class User(Schema):
    sub = fields.String(required=True)
    iss = fields.String(required=True)
    email = fields.Email(required=True)
    created_at = fields.String(dump_only=True)


class UserEdit(User):
    email = fields.String()  # required=False

    class Meta:
        exclude = ('sub', 'iss', 'created_at')


class UserQuery(User):
    sub = fields.String()    # required=False
    iss = fields.String()    # required=False
    email = fields.String()  # required=False


class Uploader(User):
    pass
