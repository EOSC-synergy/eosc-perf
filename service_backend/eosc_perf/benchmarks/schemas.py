# -*- coding: utf-8 -*-
"""User schemas."""
import marshmallow as ma
from eosc_perf.users.schemas import Uploader


class Benchmark(ma.Schema):
    id = ma.fields.String()
    docker_name = ma.fields.String()
    hidden = ma.fields.Boolean()
    uploader = ma.fields.Nested(Uploader)
    description = ma.fields.String()
    template = ma.fields.String()


class BenchmarksQueryArgs(ma.Schema):
    docker_name = ma.fields.String()
    hidden = ma.fields.Boolean()
    description = ma.fields.String()
    template = ma.fields.String()


class BenchmarksQueryId(ma.Schema):
    record_id = ma.fields.String()
