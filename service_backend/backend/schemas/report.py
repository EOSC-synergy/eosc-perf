"""Tag schemas."""
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

resource_types = [
    "benchmark_report",
    "result_report",
    "site_report",
    "flavor_report"
]


class Create(Schema):
    message = fields.String(required=True)


class FilterArgs(Schema):
    verdict = fields.Boolean()
    resource_type = fields.String(validate=OneOf(resource_types))
    created_before = fields.Date(attribute="before")
    created_after = fields.Date(attribute="after")
