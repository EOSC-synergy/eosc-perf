# -*- coding: utf-8 -*-
"""User schemas."""
from marshmallow import Schema, fields
from eosc_perf.users.schemas import Uploader


class Benchmark(Schema):
    docker_name = fields.String()
    hidden = fields.Boolean()
    uploader = fields.Pluck(Uploader, 'email')
    description = fields.String()
    template = fields.String()


class BenchmarksCreateArgs(Schema):
    docker_name = fields.String(required=True)
    uploader_id = fields.UUID(required=True)
    description = fields.String()
    template = fields.String()


class BenchmarksQueryArgs(Schema):
    docker_name = fields.String()
    hidden = fields.Boolean()
    uploader_id = fields.UUID()
    description = fields.String()
    template = fields.String()
