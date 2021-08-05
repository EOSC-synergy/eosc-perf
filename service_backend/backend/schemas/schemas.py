"""Schemas module for schemas definition."""
from backend.models import models
from marshmallow import INCLUDE, Schema, fields, post_load

# ---------------------------------------------------------------------
# Definition of User schemas


class User(Schema):
    sub = fields.String()
    iss = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


# ---------------------------------------------------------------------
# Definition of Report schemas

class Report(Schema):
    id = fields.UUID(required=True, dump_only=True)
    created_at = fields.DateTime(required=True)
    verdict = fields.Boolean(required=True)
    message = fields.String(required=True)
    resource_type = fields.String(required=True)
    resource_id = fields.UUID(required=True)


class ReportCreate(Schema):
    message = fields.String(required=True)


# ---------------------------------------------------------------------
# Definition of benchmark schemas

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


# ---------------------------------------------------------------------
# Definition of Site schemas

class Site(Schema):
    id = fields.UUID()
    name = fields.String()
    address = fields.String()
    description = fields.String()


class SiteCreate(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String()


class SiteEdit(Schema):
    name = fields.String()
    address = fields.String()
    description = fields.String()


# ---------------------------------------------------------------------
# Definition of Flavor schemas

class Flavor(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class FlavorCreate(Schema):
    name = fields.String(required=True)
    description = fields.String()


class FlavorEdit(Schema):
    name = fields.String()
    description = fields.String()


# ---------------------------------------------------------------------
# Definition of Tag schemas

class Tag(Schema):
    id = fields.UUID()
    name = fields.String()
    description = fields.String()


class TagsIds(Schema):
    tags_ids = fields.List(fields.UUID)


class TagCreate(Schema):
    name = fields.String(required=True)
    description = fields.String()


class TagEdit(Schema):
    name = fields.String()
    description = fields.String()


# ---------------------------------------------------------------------
# Definition of Result schemas

class Result(Schema):
    id = fields.UUID()
    upload_date = fields.DateTime(attribute="created_at")
    json = fields.Dict()
    benchmark = fields.Nested(Benchmark)
    site = fields.Nested(Site)
    flavor = fields.Nested(Flavor)
    tags = fields.Nested(Tag, many=True)


class Json(Schema):
    class Meta:
        unknown = INCLUDE
