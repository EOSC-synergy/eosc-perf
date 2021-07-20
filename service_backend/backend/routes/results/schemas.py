"""Result schemas."""
from backend.routes.benchmarks.schemas import Benchmark
from backend.routes.reports.schemas import Report, ReportCreate
from backend.routes.sites.schemas import Site, Flavor
from backend.schemas import User, Tag
from backend.schemas.tag import Ids as TagsIds
from marshmallow import Schema, fields, INCLUDE


__all__ = [
    "Result", "TagsIds", "Json", "User", "Report", "ReportCreate",
    "FilterQueryArgs", "CreateQueryArgs", "SearchQueryArgs"
]


class Json(Schema):
    class Meta:
        unknown = INCLUDE


class Result(Schema):
    id = fields.UUID()
    upload_date = fields.DateTime()
    json = fields.Dict()
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
