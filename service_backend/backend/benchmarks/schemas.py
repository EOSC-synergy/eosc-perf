"""Benchmark schemas."""
from marshmallow import Schema, fields


class Benchmark(Schema):
    id = fields.UUID(dump_only=True)
    docker_image = fields.String(required=True)
    docker_tag = fields.String(required=True)
    description = fields.String()
    json_template = fields.Dict()


class Benchmark_simple(Schema):
    id = fields.UUID(dump_only=True)
    docker_image = fields.String()
    docker_tag = fields.String()


class EditBenchmark(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()
    description = fields.String()
    json_template = fields.Dict()


class BenchmarkQueryArgs(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String())
