"""Schemas module for schemas definition."""
from marshmallow import INCLUDE, Schema, fields

# ---------------------------------------------------------------------
# Definition of User schemas


class User(Schema):
    sub = fields.String(required=True, dump_only=True)
    iss = fields.String(required=True, dump_only=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True)


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
    id = fields.UUID(required=True, dump_only=True)
    docker_image = fields.String(required=True)
    docker_tag = fields.String(required=True)
    description = fields.String(required=True)
    json_template = fields.Dict(required=True)


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
    id = fields.UUID(required=True, dump_only=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    description = fields.String(required=True)


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
    id = fields.UUID(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


class FlavorCreate(Schema):
    name = fields.String(required=True)
    description = fields.String()


class FlavorEdit(Schema):
    name = fields.String()
    description = fields.String()


# ---------------------------------------------------------------------
# Definition of Tag schemas

class Tag(Schema):
    id = fields.UUID(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


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
    id = fields.UUID(required=True, dump_only=True)
    upload_date = fields.DateTime(attribute="created_at", required=True)
    json = fields.Dict(required=True)
    benchmark = fields.Nested(Benchmark, required=True)
    site = fields.Nested(Site, required=True)
    flavor = fields.Nested(Flavor, required=True)
    tags = fields.Nested(Tag, many=True, required=True)


class Json(Schema):
    class Meta:
        unknown = INCLUDE
