"""Benchmark schemas."""
from marshmallow import Schema, fields


class Create(Schema):
    docker_image = fields.String(required=True)
    docker_tag = fields.String(required=True)
    description = fields.String()
    json_template = fields.Dict()


class Edit(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()
    description = fields.String()
    json_template = fields.Dict()


class FilterArgs(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
