"""Schemas module for schemas definition."""
import uuid

from marshmallow import INCLUDE, post_dump
from marshmallow.validate import OneOf

from . import BaseSchema as Schema
from . import Id, Pagination, UploadDatetime, fields


# ---------------------------------------------------------------------
# Definition of User schemas

class User(Schema):

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.String(
        description="String containing an OIDC subject",
        example="NzbLsXh8uDCcd-6MNwXF4W_7noWXFZAfHkxZsRGC9Xs",
        required=True,
    )

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.String(
        description="String containing an OIDC issuer",
        example="https://self-issued.me", required=True,

    )

    #: (Email, required):
    #: Electronic mail collected from OIDC access token
    email = fields.String(
        description="Email of user collected by the OIDC token",
        example="simple_email@gmail.com", required=True
    )

    #: (Email) Electronic mail collected from OIDC access token
    registration_datetime = fields.DateTime(
        description="Time when the user was registered",
        example="2021-09-11 10:16:11.732268", required=True
    )


class Users(Pagination, Schema):

    #: ([User], required):
    #: List of site items for the pagination object
    items = fields.Nested(User, required=True, many=True)


# ---------------------------------------------------------------------
# Definition of Report schemas

class Submit(UploadDatetime, Schema):

    #: (String, required):
    #: Resource discriminator
    resource_type = fields.String(
        description="Resource type discriminator",
        example="benchmark", required=True,
        validate=OneOf(["benchmark", "claim", "site", "flavor"])
    )

    #: (UUID, required):
    #: Resource unique identification
    resource_id = fields.UUID(
        description="UUID resource unique identification",
        example=str(uuid.uuid4()), required=True
    )

    #: (User, required):
    #: Resource uploader/creator
    uploader = fields.Nested(
        User, attribute="resource.uploader",
        required=True, dump_only=True,
    )

    @post_dump
    def aggregate_claims(self, data, **kwargs):
        data = super().remove_skip_values(data, **kwargs)
        if 'resource_type' in data:
            if "claim" in data['resource_type']:
                data['resource_type'] = "claim"
        return data


class Submits(Pagination, Schema):

    #: ([Submit], required):
    #: List of submit items for the pagination object
    items = fields.Nested(Submit, required=True, many=True)


class CreateClaim(Schema):

    #: (String, required):
    #: Claim text describing the resource issue
    message = fields.String(
        description="Resource type discriminator",
        example="The resource uses negative time", required=True
    )


class Claim(Id, UploadDatetime, CreateClaim):

    #: (UUID, required):
    #: Resource unique identification
    resource_type = fields.String(
        description="Resource type discriminator",
        example="result", required=True,
        validate=OneOf(["result"]),
    )

    #: (UUID, required):
    #: Resource unique identification
    resource_id = fields.UUID(
        description="UUID resource unique identification",
        example=str(uuid.uuid4()), required=True, dump_only=True,
    )

    #: (User, required):
    #: Claim uploader/creator
    uploader = fields.Nested(User, required=True, dump_only=True)


class Claims(Pagination, Schema):

    #: ([Claim], required):
    #: List of claim items for the pagination object
    items = fields.Nested(Claim, required=True, many=True)


# ---------------------------------------------------------------------
# Definition of Tag schemas

class CreateTag(Schema):

    #: (Text, required):
    #: Human readable feature identification
    name = fields.String(
        description="String with short feature identification",
        example="python", required=True
    )

    #: (Text):
    #: Useful information to help users to understand the label context
    description = fields.String(
        description="String with an statement about the object",
        example="This is a simple description example",
    )


class Tag(Id, CreateTag):
    pass


class Tags(Pagination, Schema):

    #: ([Tag], required):
    #: List of tag items for the pagination object
    items = fields.Nested(Tag, required=True, many=True)


class TagsIds(Schema):

    #: ([UUID]):
    #: List of tag ids
    tags_ids = fields.List(fields.UUID)


# ---------------------------------------------------------------------
# Definition of benchmark schemas

class CreateBenchmark(Schema):

    #: (Text, required):
    #: Docker image referenced by the benchmark
    docker_image = fields.String(
        description="String with a docker hub container name",
        example="deephdc/deep-oc-benchmarks_cnn", required=True,
    )

    #: (Text, required):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.String(
        description="String with a docker hub container tag",
        example="1.0.2-gpu", required=True,
    )

    #: (JSON, required):
    #: Schema used to validate benchmark results before upload
    json_schema = fields.Dict(
        # description="JSON Schema for result validation",
        required=True,
        example={
            "$id": "https://example.com/benchmark.schema.json",
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "type": "object",
            "properties": {
                "start_datetime": {
                    "description": "The benchmark start datetime.",
                    "type": "string",
                    "format": "date-time"
                },
                "end_datetime": {
                    "description": "The benchmark end datetime.",
                    "type": "string",
                    "format": "date-time"
                },
                "machine": {
                    "description": "Execution machine details.",
                    "type": "object",
                    "properties": {
                        "cpus": {
                            "description": "Number of CPU.",
                            "type": "integer"
                        },
                        "ram": {
                            "description": "Available RAM in MB.",
                            "type": "integer"
                        },
                    },
                    "required": ["cpus", "ram"]
                }
            },
            "required": ["start_datetime", "end_datetime", "machine"]
        }
    )

    #: (Text):
    #: Short text describing the main benchmark features
    description = fields.String(
        description="String with an statement about the object",
        example="This is a simple description example",
    )


class Benchmark(Id, UploadDatetime, CreateBenchmark):
    pass


class Benchmarks(Pagination, Schema):

    #: ([Benchmark], required):
    #: List of benchmark items for the pagination object
    items = fields.Nested("Benchmark", required=True, many=True)


# ---------------------------------------------------------------------
# Definition of Site schemas

class CreateSite(Schema):

    #: (Text, required):
    #: Human readable institution identification
    name = fields.String(
        description="String with human readable institution identification",
        example="Karlsruhe Institute of Technology", required=True,
    )

    #: (Text, required):
    #: Place where a site is physically located
    address = fields.String(
        description="String with place where a site is located",
        example="76131 Karlsruhe, Germany", required=True,
    )

    #: (Text, required):
    #: Useful site information to help users
    description = fields.String(
        description="String with an statement about the object",
        example="This is a simple description example",
    )


class Site(Id, UploadDatetime, CreateSite):
    pass


class Sites(Pagination, Schema):

    #: ([Site], required):
    #: List of site items for the pagination object
    items = fields.Nested(Site, required=True, many=True)


# ---------------------------------------------------------------------
# Definition of Flavor schemas

class CreateFlavor(Schema):

    #: (Text, required):
    #: Text with virtual hardware template identification
    name = fields.String(
        description="String with virtual hardware template identification",
        example="c6g.medium", required=True,
    )

    #: (Text, required):
    #: Text with useful information for users
    description = fields.String(
        description="String with an statement about the object",
        example="This is a simple description example",
    )


class Flavor(Id, UploadDatetime, CreateFlavor):
    pass


class Flavors(Pagination, Schema):

    #: ([Flavor], required):
    #: List of flavor items for the pagination object
    items = fields.Nested(Flavor, required=True, many=True)


# ---------------------------------------------------------------------
# Definition of Result schemas

class Result(Id, UploadDatetime, Schema):

    #: (ISO8601, required) :
    #: Benchmark execution **START**
    execution_datetime = fields.DateTime(
        description="START execution datetime of the result",
        example="2021-09-08 20:37:10.192459", required=True,
    )

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

    #: (JSON, required):
    #: Benchmark execution results
    json = fields.Dict(required=True)


class Results(Pagination, Schema):

    #: ([Result], required):
    #: List of results items for the pagination object
    items = fields.Nested(Result, required=True, many=True)


class Json(Schema):
    """Special schema to allow free JSON property"""
    class Meta:
        """`marshmallow` options object for JSON properties"""
        #: Accept and include the unknown fields
        unknown = INCLUDE
