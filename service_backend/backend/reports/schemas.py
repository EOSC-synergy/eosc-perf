"""Report schemas."""
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


__all__ = [
    "Report", "ReportCreate",
    "FilterQueryArgs"
]

resource_types = [
    "benchmark_report",
    "result_report",
    "site_report",
    "flavor_report"
]


class Report(Schema):
    id = fields.UUID()
    creation_date = fields.DateTime()
    verdict = fields.Boolean()
    message = fields.String()
    resource_type = fields.String()
    resource_id = fields.UUID()


class ReportCreate(Schema):
    message = fields.String(required=True)


class FilterQueryArgs(Schema):
    verdict = fields.Boolean()
    resource_type = fields.String(validate=OneOf(resource_types))
    created_before = fields.Date(attribute="before")
    created_after = fields.Date(attribute="after")
