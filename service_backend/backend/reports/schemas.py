"""Report schemas."""
from flask.json import dump
from marshmallow import Schema, fields
from sqlalchemy.orm import load_only


class Report(Schema):
    id = fields.UUID(dump_only=True)
    date = fields.Date(dump_only=True)
    verified = fields.Boolean()
    verdict = fields.Boolean()
    message = fields.String(required=True)


class EditReport(Schema):
    verified = fields.Boolean()
    verdict = fields.Boolean()
    message = fields.String()


class ReportQueryArgs(Schema):
    date = fields.Date()
    verified = fields.Boolean()
    verdict = fields.Boolean()


# Benchmark report schemas -----------

class ReportForBenchmark(Report):
    benchmark = fields.Nested("Benchmark", dump_only=True)


class BReportQueryArgs(ReportQueryArgs):
    benchmark_image = fields.String()
    benchmark_tag = fields.String()


class BenchmarkQueryArgs(Schema):
    benchmark_image = fields.String()
    benchmark_tag = fields.String()


# Result report schemas --------------

class ReportForResult(Report):
    result = fields.Nested("Result", dump_only=True)


class RReportQueryArgs(ReportQueryArgs):
    benchmark_image = fields.String()
    benchmark_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()


class ResultQueryArgs(Schema):
    benchmark_image = fields.String()
    benchmark_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()


# Site report schemas ----------------

class ReportForSite(Report):
    site = fields.Nested("Site", dump_only=True)


class SReportQueryArgs(ReportQueryArgs):
    site_name = fields.String()


class SiteQueryArgs(Schema):
    site_name = fields.String()


# Flavor report schemas ----------------

class ReportForFlavor(Report):
    site = fields.Nested("Site", dump_only=True)
    flavor = fields.Nested("Flavor", dump_only=True)


class FReportQueryArgs(ReportQueryArgs):
    site_name = fields.String()
    flavor_name = fields.String()


class FlavorQueryArgs(Schema):
    site_name = fields.String()
    flavor_name = fields.String()
