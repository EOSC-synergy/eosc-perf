# -*- coding: utf-8 -*-
"""User schemas."""
import marshmallow as ma


class User(ma.Schema):
    id = ma.fields.String()
    email = ma.fields.String()
    created_at = ma.fields.String()


class Uploader(User):
    pass


class UsersQueryId(ma.Schema):
    record_id = ma.fields.String()


class UsersQueryArgs(ma.Schema):
    email = ma.fields.String()
