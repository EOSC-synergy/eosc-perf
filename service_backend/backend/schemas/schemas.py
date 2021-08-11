"""Schemas module for schemas definition."""
from marshmallow import INCLUDE

from . import BaseSchema as Schema
from . import Pagination, fields

# ---------------------------------------------------------------------
# Definition of User schemas

class User(Schema):
    sub = fields.Sub(required=True, dump_only=True)
    iss = fields.Iss(required=True, dump_only=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True)


class Users(Pagination, Schema):
    items = fields.Nested(User, many=True)


# ---------------------------------------------------------------------
# Definition of Report schemas

class Report(Schema):
    id = fields.Id(required=True, dump_only=True)
    upload_date = fields.DateTime(attribute="created_at", required=True)
    verdict = fields.Boolean(required=True)
    message = fields.Message(required=True)
    resource_type = fields.Resource(required=True)
    resource_id = fields.Id(required=True)


class Reports(Pagination, Schema):
    items = fields.Nested(Report, many=True)


class ReportCreate(Schema):
    message = fields.Message(required=True)


# ---------------------------------------------------------------------
# Definition of benchmark schemas

class Benchmark(Schema):
    id = fields.Id(required=True, dump_only=True)
    docker_image = fields.DockerImage(required=True)
    docker_tag = fields.DockerTag(required=True)
    description = fields.Description(required=True)
    json_template = fields.JsonTemplate(required=True)


class Benchmarks(Pagination, Schema):
    items = fields.Nested(Benchmark, many=True)


class BenchmarkCreate(Schema):
    docker_image = fields.DockerImage(required=True)
    docker_tag = fields.DockerTag(required=True)
    description = fields.Description()
    json_template = fields.JsonTemplate()


class BenchmarkEdit(Schema):
    docker_image = fields.DockerImage()
    docker_tag = fields.DockerTag()
    description = fields.Description()
    json_template = fields.JsonTemplate()


# ---------------------------------------------------------------------
# Definition of Site schemas

class Site(Schema):
    id = fields.Id(required=True, dump_only=True)
    name = fields.SiteName(required=True)
    address = fields.Address(required=True)
    description = fields.Description(required=True)


class Sites(Pagination, Schema):
    items = fields.Nested(Site, many=True)


class SiteCreate(Schema):
    name = fields.SiteName(required=True)
    address = fields.Address(required=True)
    description = fields.Description()


class SiteEdit(Schema):
    name = fields.SiteName()
    address = fields.Address()
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Flavor schemas

class Flavor(Schema):
    id = fields.Id(required=True, dump_only=True)
    name = fields.FlavorName(required=True)
    description = fields.Description(required=True)


class Flavors(Pagination, Schema):
    items = fields.Nested(Flavor, many=True)


class FlavorCreate(Schema):
    name = fields.FlavorName(required=True)
    description = fields.Description()


class FlavorEdit(Schema):
    name = fields.FlavorName()
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Tag schemas

class Tag(Schema):
    id = fields.Id(required=True, dump_only=True)
    name = fields.TagName(required=True)
    description = fields.Description(required=True)


class Tags(Pagination, Schema):
    items = fields.Nested(Tag, many=True)


class TagsIds(Schema):
    tags_ids = fields.List(fields.UUID)


class TagCreate(Schema):
    name = fields.TagName(required=True)
    description = fields.Description()


class TagEdit(Schema):
    name = fields.TagName()
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Result schemas

class Result(Schema):
    id = fields.Id(required=True, dump_only=True)
    upload_date = fields.DateTime(attribute="created_at", required=True)
    json = fields.Dict(required=True)
    benchmark = fields.Nested(Benchmark, required=True)
    site = fields.Nested(Site, required=True)
    flavor = fields.Nested(Flavor, required=True)
    tags = fields.Nested(Tag, many=True, required=True)


class Results(Pagination, Schema):
    items = fields.Nested(Result, many=True)


class Json(Schema):
    class Meta:
        unknown = INCLUDE
