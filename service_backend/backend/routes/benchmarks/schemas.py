"""Benchmark schemas."""
from marshmallow import Schema, fields


__all__ = [
    "Benchmark", "BenchmarkCreate", "BenchmarkEdit",
    "BenchmarkQueryArgs", "SearchQueryArgs"
]


class Benchmark(Schema):
    id = fields.UUID()
    docker_image = fields.String()
    docker_tag = fields.String()
    description = fields.String()
    json_template = fields.Dict()


class BenchmarkCreate(Schema):
    docker_image = fields.String(required=True)
    docker_tag = fields.String(required=True)
    description = fields.String()
    json_template = fields.Dict()


class BenchmarkEdit(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()
    description = fields.String()
    json_template = fields.Dict()


class BenchmarkQueryArgs(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
