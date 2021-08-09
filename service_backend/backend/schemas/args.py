"""Module to define query arguments."""
from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf
from . import Pagination

verdict_values = ["true", "false", "null"]
resource_types = ["benchmark", "result", "site", "flavor"]


class UserFilter(Pagination, Schema):
    email = fields.String()


class UserSearch(Pagination, Schema):
    terms = fields.List(fields.String(), missing=[])


class ReportFilter(Pagination, Schema):
    verdict = fields.String(validate=OneOf(verdict_values))
    resource_type = fields.String(validate=OneOf(resource_types))
    created_before = fields.Date(attribute="before")
    created_after = fields.Date(attribute="after")

    @post_load
    def process_input(self, data, **kwargs):
        if 'verdict' in data and data['verdict'] == "null":
            data['verdict'] = None
        return data


class BenchmarkFilter(Pagination, Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class BenchmarkSearch(Pagination, Schema):
    terms = fields.List(fields.String(), missing=[])


class SiteFilter(Pagination, Schema):
    name = fields.String()
    address = fields.String()


class SiteSearch(Pagination, Schema):
    terms = fields.List(fields.String(), missing=[])


class FlavorFilter(Pagination, Schema):
    name = fields.String()


class TagFilter(Pagination, Schema):
    name = fields.String()


class TagSearch(Pagination, Schema):
    terms = fields.List(fields.String(), missing=[])


class ResultFilter(Pagination, Schema):
    docker_image = fields.String()
    docker_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String(), missing=None)
    upload_before = fields.Date(attribute="before", missing=None)
    upload_after = fields.Date(attribute="after", missing=None)
    filters = fields.List(
        fields.String(example="machine.cpu.count > 4"),
        missing=[]
    )


class ResultContext(Schema):
    benchmark_id = fields.UUID(required=True)
    site_id = fields.UUID(required=True)
    flavor_id = fields.UUID(required=True)
    tags_ids = fields.List(fields.UUID, missing=[])


class ResultSearch(Pagination, Schema):
    terms = fields.List(fields.String(), missing=[])
