"""Module to define query arguments."""
from marshmallow import post_load

from . import BaseSchema as Schema
from . import Pagination, fields


class BenchmarkFilter(Pagination, Schema):

    #: (Text):
    #: Docker image referenced by the benchmark
    docker_image = fields.DockerImage()

    #: (Text):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.DockerTag()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+docker_image,-docker_tag", missing="+docker_image")


class FlavorFilter(Pagination, Schema):

    #: (Text):
    #: Text with virtual hardware template identification
    name = fields.FlavorName()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+name", missing="+name")


class ReportFilter(Pagination, Schema):

    #: (Bool):
    #: Contains the status information of the report
    verdict = fields.Verdict()

    #: (String):
    #:Resource discriminator
    resource_type = fields.Resource()

    #: (ISO8601, attribute="upload_datetime", missing=None):
    #: Upload datetime of the report before a specific date
    upload_before = fields.UploadBefore(attribute="before", missing=None)

    #: (ISO8601, attribute="upload_datetime", missing=None):
    #: Upload datetime of the report after a specific date
    upload_after = fields.UploadAfter(attribute="after", missing=None)

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+upload_datetime", missing="+verdict,+id")

    @post_load
    def process_input(self, data, **kwargs):
        if 'verdict' in data and data['verdict'] == "null":
            data['verdict'] = None
        return data


class ResultFilter(Pagination, Schema):

    #: (Benchmark.id):
    #: Unique Identifier for result associated benchmark
    benchmark_id = fields.Id()

    #: (Site.id):
    #: Unique Identifier for result associated site
    site_id = fields.Id()

    #: (Flavor.id):
    #: Unique Identifier for result associated flavor
    flavor_id = fields.Id()

    #: ([Tag.id], required):
    #: Unique Identifiers for result associated tags
    tags_ids = fields.Ids()

    #: (ISO8601, attribute="upload_datetime", missing=None):
    #: Upload datetime of the report before a specific date
    upload_before = fields.UploadBefore(attribute="before", missing=None)

    #: (ISO8601, attribute="upload_datetime", missing=None):
    #: Upload datetime of the report after a specific date
    upload_after = fields.UploadAfter(attribute="after", missing=None)

    #: (String; <json.path> <operation> <value>)
    #: Expression to condition the returned results on JSON field
    filters = fields.Filters()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+execution_datetime", missing="+execution_datetime")


class ResultContext(Schema):

    #: (ISO8601, required") :
    #: Benchmark execution **START**
    execution_datetime = fields.ExecDT(required=True)

    #: (Benchmark.id, required):
    #: Unique Identifier for result associated benchmark
    benchmark_id = fields.Id(required=True)

    #: (Site.id, required):
    #: Unique Identifier for result associated site
    site_id = fields.Id(required=True)

    #: (Flavor.id, required):
    #: Unique Identifier for result associated flavor
    flavor_id = fields.Id(required=True)

    #: ([Tag.id], required):
    #: Unique Identifiers for result associated tags
    tags_ids = fields.Ids()


class SiteFilter(Pagination, Schema):

    #: (Text):
    #: Human readable institution identification
    name = fields.SiteName()

    #: (Text):
    #: Place where a site is physically located
    address = fields.Address()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+name,+address", missing="+name")


class TagFilter(Pagination, Schema):

    #: (Text):
    #: Human readable feature identification
    name = fields.TagName()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+name", missing="+name")


class UserFilter(Pagination, Schema):

    #: (Text):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.Sub()

    #: (Text):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.Iss()

    #: (Email) Electronic mail collected from OIDC access token
    email = fields.Email()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+email", missing="+iss,+sub")


class UserDelete(Schema):

    #: (Text):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.Sub()

    #: (Text):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.Iss()

    #: (Email) Electronic mail collected from OIDC access token
    email = fields.Email()


class Search(Pagination, Schema):

    #: ([Text]):
    #: Group of strings to use as general search on model instances
    terms = fields.Terms()

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+upload_datetime", missing="")
