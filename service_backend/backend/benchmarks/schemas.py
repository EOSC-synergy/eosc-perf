"""Benchmark schemas."""
from marshmallow import Schema, fields


class Benchmark(Schema):
    id = fields.UUID(dump_only=True)
    docker_image = fields.String(required=True)
    docker_tag = fields.String(required=True)


class EditBenchmark(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class BenchmarkQueryArgs(Schema):
    docker_image = fields.String()
