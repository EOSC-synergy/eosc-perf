# -*- coding: utf-8 -*-
"""User schemas."""
from marshmallow import Schema, fields
from backend.users.schemas import Uploader


class Benchmark(Schema):
    id = fields.UUID(dump_only=True)
    docker_name = fields.String(required=True)
    template = fields.String()
    hidden = fields.Boolean(dump_only=True)
    description = fields.String()
    uploader = fields.Pluck(Uploader, 'email')


class BenchmarkEdit(Benchmark):
    docker_name = fields.String()  # required=False
    hidden = fields.Boolean()      # dump_only=False
    uploader_id = fields.UUID()    # required=False


class BenchmarkQuery(Benchmark):
    docker_name = fields.String()  # required=False
    hidden = fields.Boolean()      # dump_only=False
    uploader_id = fields.UUID()    # required=False
