"""Report schemas."""
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


resource_types = [
    "benchmark_report",
    "result_report",
    "site_report",
    "flavor_report"
]


class Report(Schema):
    id = fields.UUID(dump_only=True)
    creation_date = fields.Date(dump_only=True)
    verdict = fields.Boolean(dump_only=True)
    message = fields.String(required=True)
    resource_type = fields.String(dump_only=True)
    resource_id = fields.UUID(dump_only=True)


class FilterQueryArgs(Schema):
    verdict = fields.Boolean()
    resource_type = fields.String(validate=OneOf(resource_types))
    created_before = fields.Date(attribute="before")
    created_after = fields.Date(attribute="after")
