# -*- coding: utf-8 -*-
"""Sites schemas."""
import marshmallow as ma


class Flavor(ma.Schema):
    name = ma.fields.String()
    custom_text = ma.fields.String()


class Site(ma.Schema):
    name = ma.fields.String()
    address = ma.fields.String()
    description = ma.fields.String()
    hidden = ma.fields.Boolean()
    flavors = ma.fields.List(ma.fields.Nested(Flavor))


class SitesQueryArgs(ma.Schema):
    name = ma.fields.String()
    address = ma.fields.String()
    description = ma.fields.String()
    hidden = ma.fields.Boolean()
    flavors = ma.fields.List(ma.fields.Nested(Flavor))
