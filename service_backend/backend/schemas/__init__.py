"""Backend package for schemas definition."""
from marshmallow import Schema, fields

from . import benchmark, report, tag, user


class Benchmark(Schema):
    id = fields.UUID()
    docker_image = fields.String()
    docker_tag = fields.String()
    description = fields.String()
    json_template = fields.Dict()


class Report(Schema):
    id = fields.UUID()
    creation_date = fields.DateTime()
    verdict = fields.Boolean()
    message = fields.String()
    resource_type = fields.String()
    resource_id = fields.UUID()


class Tag(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class User(Schema):
    sub = fields.String()
    iss = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()
