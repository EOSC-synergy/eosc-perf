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


class FlavorFilter(Pagination, Schema):

    #: (Text):
    #: Text with virtual hardware template identification
    name = fields.FlavorName()


class ReportFilter(Pagination, Schema):

    #: (Bool):
    #: Contains the status information of the report
    verdict = fields.Verdict()

    #: (String):
    #:Resource discriminator
    resource_type = fields.Resource()

    #: (ISO8601, attribute="created_at", missing=None):
    #: Upload datetime of the report before a specific date
    upload_before = fields.UploadBefore(attribute="before", missing=None)

    #: (ISO8601, attribute="created_at", missing=None):
    #: Upload datetime of the report after a specific date
    upload_after = fields.UploadAfter(attribute="after", missing=None)

    @post_load
    def process_input(self, data, **kwargs):
        if 'verdict' in data and data['verdict'] == "null":
            data['verdict'] = None
        return data


class ResultFilter(Pagination, Schema):

    #: (Text):
    #: Docker image version/tag referenced by the benchmark
    docker_image = fields.DockerImage()

    #: (Text):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.DockerTag()

    #: (Text):
    #: Name of the site where the benchmar was executed
    site_name = fields.SiteName()

    #: (Text):
    #: Text with virtual hardware template identification
    flavor_name = fields.FlavorName()

    #: ([Tag.name]):
    #: List of tag names the returned results should be associated with
    tag_names = fields.TagNames()

    #: (ISO8601, attribute="created_at", missing=None):
    #: Upload datetime of the report before a specific date
    upload_before = fields.UploadBefore(attribute="before", missing=None)

    #: (ISO8601, attribute="created_at", missing=None):
    #: Upload datetime of the report after a specific date
    upload_after = fields.UploadAfter(attribute="after", missing=None)

    #: (String; <json.path> <operation> <value>)
    #: Expression to condition the returned results on JSON field
    filters = fields.Filters()


class ResultContext(Schema):

    #: (ISO8601, required, attribute="executed_at") :
    #: Benchmark execution **START**
    execution_datetime = fields.ExecDT(required=True, attribute="executed_at")

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


class TagFilter(Pagination, Schema):

    #: (Text):
    #: Human readable feature identification
    name = fields.TagName()


class UserFilter(Pagination, Schema):

    #: (Text):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.Sub()

    #: (Text):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.Iss()

    #: (Email) Electronic mail collected from OIDC access token
    email = fields.Email()


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
