"""Schemas module for schemas definition."""
from marshmallow import INCLUDE

from . import BaseSchema as Schema
from . import Pagination, fields


# ---------------------------------------------------------------------
# Definition of benchmark schemas

class Benchmark(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (Text, required):
    #: Docker image referenced by the benchmark
    docker_image = fields.DockerImage(required=True)

    #: (Text, required):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.DockerTag(required=True)

    #: (JSON, required):
    #: Schema used to validate benchmark results before upload
    json_schema = fields.Json_schema(required=True)

    #: (Text, required):
    #: Short text describing the main benchmark features
    description = fields.Description(required=True)


class Benchmarks(Pagination, Schema):

    #: ([Benchmark], required):
    #: List of benchmark items for the pagination object
    items = fields.Nested("Benchmark", required=True, many=True)


class BenchmarkCreate(Schema):

    #: (Text, required):
    #: Docker image referenced by the benchmark
    docker_image = fields.DockerImage(required=True)

    #: (Text, required):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.DockerTag(required=True)

    #: (JSON, required):
    #: Schema used to validate benchmark results before upload
    json_schema = fields.Json_schema(required=True)

    #: (Text):
    #: Short text describing the main benchmark features
    description = fields.Description()


class BenchmarkEdit(Schema):

    #: (Text):
    #: Docker image referenced by the benchmark
    docker_image = fields.DockerImage()

    #: (Text):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.DockerTag()

    #: (JSON):
    #: Schema used to validate benchmark results before upload
    json_schema = fields.Json_schema()

    #: (Text):
    #: Short text describing the main benchmark features
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Flavor schemas

class Flavor(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (Text, required):
    #: Text with virtual hardware template identification
    name = fields.FlavorName(required=True)

    #: (Text, required):
    #: Text with useful information for users
    description = fields.Description(required=True)


class Flavors(Pagination, Schema):

    #: ([Flavor], required):
    #: List of flavor items for the pagination object
    items = fields.Nested(Flavor, required=True, many=True)


class FlavorCreate(Schema):

    #: (Text, required):
    #: Text with virtual hardware template identification
    name = fields.FlavorName(required=True)

    #: (Text):
    #: Text with useful information for users
    description = fields.Description()


class FlavorEdit(Schema):

    #: (Text):
    #: Text with virtual hardware template identification
    name = fields.FlavorName()

    #: (Text):
    #: Text with useful information for users
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Report schemas

class Report(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (ISO8601, required, attribute="created_at"):
    #: Upload datetime of the report
    upload_datetime = fields.UploadDT(required=True, attribute="created_at")

    #: (Bool, required):
    #: Contains the status information of the report
    verdict = fields.Boolean(required=True)

    #: (Text, required):
    #: Information created by user to describe the issue
    message = fields.Message(required=True)

    #: (String, required):
    #:Resource discriminator
    resource_type = fields.Resource(required=True)

    #: (UUID, required):
    #: Resource unique identification
    resource_id = fields.Id(required=True)


class Reports(Pagination, Schema):

    #: ([Reports], required):
    #: List of report items for the pagination object
    items = fields.Nested(Report, required=True, many=True)


class ReportCreate(Schema):

    #: (Text, required):
    #: Information created by user to describe the issue
    message = fields.Message(required=True)


# ---------------------------------------------------------------------
# Definition of Result schemas

class Result(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (JSON, required):
    #: Benchmark execution results
    json = fields.Dict(required=True)

    #: (ISO8601, required, attribute="created_at"):
    #: Upload datetime of the report
    upload_datetime = fields.UploadDT(required=True, attribute="created_at")

    #: (ISO8601, required, attribute="executed_at"):
    #: Benchmark execution **START**
    execution_datetime = fields.ExecDT(required=True, attribute="executed_at")

    #: (Benchmark, required):
    #: Benchmark used to provide the results
    benchmark = fields.Nested("Benchmark", required=True)

    #: (Site, required):
    #: Site where the benchmark was executed
    site = fields.Nested("Site", required=True)

    #: (Flavor, required):
    #: Flavor used to executed the benchmark
    flavor = fields.Nested("Flavor", required=True)

    #: ([Tag], required):
    #: List of associated tags to the model
    tags = fields.Nested("Tag", many=True, required=True)


class Results(Pagination, Schema):

    #: ([Results], required):
    #: List of results items for the pagination object
    items = fields.Nested(Result, many=True)


class Json(Schema):
    """Special schema to allow free JSON property"""
    class Meta:
        """`marshmallow` options object for JSON properties"""
        #: Accept and include the unknown fields
        unknown = INCLUDE


# ---------------------------------------------------------------------
# Definition of Site schemas

class Site(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (Text, required):
    #: Human readable institution identification
    name = fields.SiteName(required=True)

    #: (Text, required):
    #: Place where a site is physically located
    address = fields.Address(required=True)

    #: (Text, required):
    #: Useful site information to help users
    description = fields.Description(required=True)


class Sites(Pagination, Schema):

    #: ([Site], required):
    #: List of site items for the pagination object
    items = fields.Nested(Site, required=True, many=True)


class SiteCreate(Schema):

    #: (Text, required):
    #: Human readable institution identification
    name = fields.SiteName(required=True)

    #: (Text, required):
    #: Place where a site is physically located
    address = fields.Address(required=True)

    #: (Text):
    #: Useful site information to help users
    description = fields.Description()


class SiteEdit(Schema):

    #: (Text):
    #: Human readable institution identification
    name = fields.SiteName()

    #: (Text):
    #: Place where a site is physically located
    address = fields.Address()

    #: (Text):
    #: Useful site information to help users
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of Tag schemas

class Tag(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.Id(required=True, dump_only=True)

    #: (Text, required):
    #: Human readable feature identification
    name = fields.TagName(required=True)

    #: (Text, required):
    #: Useful information to help users to understand the label context
    description = fields.Description(required=True)


class Tags(Pagination, Schema):

    #: ([Tag], required):
    #: List of tag items for the pagination object
    items = fields.Nested(Tag, required=True, many=True)


class TagsIds(Schema):

    #: ([UUID]):
    #: List of tag ids
    tags_ids = fields.List(fields.UUID)


class TagCreate(Schema):

    #: (Text, required):
    #: Human readable feature identification
    name = fields.TagName(required=True)

    #: (Text):
    #: Useful information to help users to understand the label context
    description = fields.Description()


class TagEdit(Schema):

    #: (Text):
    #: Human readable feature identification
    name = fields.TagName()

    #: (Text):
    #: Useful information to help users to understand the label context
    description = fields.Description()


# ---------------------------------------------------------------------
# Definition of User schemas

class User(Schema):

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.Sub(required=True, dump_only=True)

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.Iss(required=True, dump_only=True)

    #: (Email, required):
    #: Electronic mail collected from OIDC access token
    email = fields.Email(required=True)

    #: (ISO8601, required):
    #: Creation datetime of the model instance
    created_at = fields.CreationDT(required=True)


class Users(Pagination, Schema):

    #: ([User], required):
    #: List of site items for the pagination object
    items = fields.Nested(User, required=True, many=True)
