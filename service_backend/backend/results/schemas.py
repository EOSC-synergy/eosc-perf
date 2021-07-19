"""Result schemas."""
from backend.benchmarks.schemas import Benchmark
from backend.reports.schemas import Report
from backend.sites.schemas import Site, Flavor
from backend.tags.schemas import Tag, TagsIds
from backend.users.schemas import User
from marshmallow import Schema, fields, INCLUDE


class Json(Schema):
    class Meta:
        unknown = INCLUDE


class Result(Schema):
    id = fields.UUID(dump_only=True)
    upload_date = fields.DateTime(dump_only=True)
    json = fields.Dict(required=True)
    benchmark = fields.Nested(Benchmark)
    site = fields.Nested(Site)
    flavor = fields.Nested(Flavor)
    tags = fields.Nested(Tag, many=True)


class FilterQueryArgs(Schema):
    #TODO: json = fields.Dict()
    docker_image = fields.String()
    docker_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String())
    upload_before = fields.Date(attribute="before")
    upload_after = fields.Date(attribute="after")


class CreateQueryArgs(Schema):
    benchmark_id = fields.UUID(required=True)
    site_id = fields.UUID(required=True)
    flavor_id = fields.UUID(required=True)
    tags_ids = fields.List(fields.UUID, missing=[])


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
