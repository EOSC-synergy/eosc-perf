"""Module to define query arguments."""
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


resource_types = [
    "benchmark_report",
    "result_report",
    "site_report",
    "flavor_report"
]


class UserFilter(Schema):
    iss = fields.String()
    email = fields.String()


class UserSearch(Schema):
    terms = fields.List(fields.String(), missing=[])


class ReportFilter(Schema):
    verdict = fields.Boolean()
    resource_type = fields.String(validate=OneOf(resource_types))
    created_before = fields.Date(attribute="before")
    created_after = fields.Date(attribute="after")


class BenchmarkFilter(Schema):
    docker_image = fields.String()
    docker_tag = fields.String()


class BenchmarkSearch(Schema):
    terms = fields.List(fields.String(), missing=[])


class SiteFilter(Schema):
    name = fields.String()
    address = fields.String()


class SiteSearch(Schema):
    terms = fields.List(fields.String(), missing=[])


class FlavorFilter(Schema):
    name = fields.String()


class TagFilter(Schema):
    name = fields.String()


class TagSearch(Schema):
    terms = fields.List(fields.String(), missing=[])


class ResultFilter(Schema):
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


class ResultSearch(Schema):
    terms = fields.List(fields.String(), missing=[])
