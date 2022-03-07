"""Module to define query arguments."""
from uuid import uuid4

from marshmallow import fields
from marshmallow.validate import OneOf, Range

from . import BaseSchema as Schema
from . import Search, Status, UploadFilter


class Pagination(Schema):

    #: (Int, required, dump_only):
    #: The number of items to be displayed on a page.
    per_page = fields.Integer(
        description="The number of items to be displayed on a page",
        validate=Range(min=1, max=100), load_default=100
    )

    #: (Int, required, dump_only):
    #: The return page number (1 indexed).
    page = fields.Integer(
        description="The return page number (1 indexed)",
        validate=Range(min=1), load_default=1
    )


class UserFilter(Pagination, Schema):

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC subject the model instance
    sub = fields.String(
        description="String containing an OIDC subject",
        example="NzbLsXh8uDCcd-6MNwXF4W_7noWXFZAfHkxZsRGC9Xs",
    )

    #: (Text, required, dump_only):
    #: Primary key containing the OIDC issuer of the model instance
    iss = fields.String(
        description="String containing an OIDC issuer",
        example="https://self-issued.me",

    )

    #: (Email, required):
    #: Electronic mail collected from OIDC access token
    email = fields.String(
        description="Email of user collected by the OIDC token",
        example="simple_email@gmail.com",
    )

    #: (Str):
    #: Order to return the results separated by coma
    # TODO: Check https://github.com/marshmallow-code/flask-smorest/issues/302
    sort_by = fields.String(
        description="{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Specific fields: [sub,iss,email,registration_datetime]",
        ),
        example="+registration_datetime", load_default="+iss,+sub"
    )


class UserDelete(UserFilter):
    class Meta:
        fields = ("sub", "iss", "email")


class UserSearch(Pagination, Search, Schema):
    pass


class SubmitFilter(Pagination, UploadFilter, Schema):

    #: (String):
    #: Resource discriminator
    resource_type = fields.String(
        description="Resource type discriminator",
        example="benchmark",
        validate=OneOf(["benchmark", "claim", "site", "flavor"])
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,upload_datetime]",
            "Specific fields: [resource_type]",
        ),
        example="+resource_type", load_default="+resource_type"
    )


class ClaimFilter(Pagination, UploadFilter, Status, Schema):

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,status,upload_datetime]",
            "Specific fields: [resource_type]",
        ),
        example="+upload_datetime", load_default="+upload_datetime"
    )


class TagFilter(Pagination, Schema):

    #: (Text):
    #: Human readable feature identification
    name = fields.String(
        description="String with short feature identification",
        example="python",
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,upload_datetime]",
            "Specific fields: [name]",
        ),
        example="+name", load_default="+name"
    )


class TagSearch(Pagination, Search, Schema):
    pass


class BenchmarkFilter(Pagination, UploadFilter, Status, Schema):

    #: (Text, required):
    #: Docker image referenced by the benchmark
    docker_image = fields.String(
        description="String with a docker hub container name",
        example="deephdc/deep-oc-benchmarks_cnn",
    )

    #: (Text, required):
    #: Docker image version/tag referenced by the benchmark
    docker_tag = fields.String(
        description="String with a docker hub container tag",
        example="1.0.2-gpu",
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,upload_datetime]",
            "Specific fields: [docker_image,docker_tag]",
        ),
        example="+docker_image,-docker_tag", load_default="+docker_image"
    )


class BenchmarkSearch(Pagination, UploadFilter, Status, Search, Schema):
    pass


class SiteFilter(Pagination, UploadFilter, Status, Schema):

    #: (Text):
    #: Human readable institution identification
    name = fields.String(
        description="String with human readable institution identification",
        example="Karlsruhe Institute of Technology",
    )

    #: (Text):
    #: Place where a site is physically located
    address = fields.String(
        description="String with place where a site is located",
        example="76131 Karlsruhe, Germany",
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,upload_datetime]",
            "Specific fields: [name,address]",
        ),
        example="+name,+address", load_default="+name"
    )


class SiteSearch(Pagination, UploadFilter, Status, Search, Schema):
    pass


class FlavorFilter(Pagination, UploadFilter, Status, Schema):

    #: (Text):
    #: Text with virtual hardware template identification
    name = fields.String(
        description="String with virtual hardware template identification",
        example="c6g.medium",
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,upload_datetime]",
            "Specific fields: [name]",
        ),
        example="+name", load_default="+name"
    )


class FlavorSearch(Pagination, UploadFilter, Status, Search, Schema):
    pass


class ResultFilter(Pagination, UploadFilter, Schema):

    #: (ISO8601):
    #: Execution datetime of the instance before a specific date
    execution_before = fields.Date(
        description="Results executed before date (ISO8601)",
        example="2059-03-10",
    )

    #: (ISO8601):
    #: Execution datetime of the instance after a specific date
    execution_after = fields.Date(
        description="Results executed after date (ISO8601)",
        example="2019-09-07",
    )

    #: (Benchmark.id):
    #: Unique Identifier for result associated benchmark
    benchmark_id = fields.UUID(
        description="UUID benchmark unique identification",
        example=str(uuid4()),
    )

    #: (Site.id):
    #: Unique Identifier for result associated site
    site_id = fields.UUID(
        description="UUID site unique identification",
        example=str(uuid4()),
    )

    #: (Flavor.id):
    #: Unique Identifier for result associated flavor
    flavor_id = fields.UUID(
        description="UUID flavor unique identification",
        example=str(uuid4()),
    )

    #: ([Tag.id], required):
    #: Unique Identifiers for result associated tags
    tags_ids = fields.List(
        fields.UUID(
            description="UUID tag unique identification",
            example=str(uuid4()), required=True,
        ),
        description="UUID tags unique identifications",
        example=[str(uuid4()) for _ in range(2)],
    )

    #: (String; <json.path> <operation> <value>)
    #: Expression to condition the returned results on JSON field
    filters = fields.List(
        fields.String(
            description="JSON filter condition (space sparated)",
            example="machine.cpu.count > 4", required=True,
        ),
        description="List of filter conditions (space separated)",
        example=["cpu.count > 4", "cpu.count < 80"], load_default=[]
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="{}<br>{}<br>{}<br>{}<br>{}<br>{}".format(
            "Order to return the results (coma separated).",
            "Generic fields: [id,execution_datetime,upload_datetime].",
            "Benchmark fields: [benchmark_id,benchmark_name].",
            "Site fields: [site_id,site_name,site_address].",
            "Flavor fields: [flavor_id,flavor_name].",
            "Custom json fields using 'json' and '.' as json field delimiter."
        ),
        example="+execution_datetime", load_default="+execution_datetime"
    )


class ResultContext(Schema):

    #: (ISO8601, required) :
    #: Benchmark execution **START**
    execution_datetime = fields.DateTime(
        description="START execution datetime and timezone of the result",
        example='2020-05-21T10:31:00.000+01:00', required=True,
    )

    #: (Benchmark.id, required):
    #: Unique Identifier for result associated benchmark
    benchmark_id = fields.UUID(
        description="UUID benchmark unique identification",
        example=str(uuid4()), required=True,
    )

    #: (Flavor.id, required):
    #: Unique Identifier for result associated flavor
    flavor_id = fields.UUID(
        description="UUID flavor unique identification",
        example=str(uuid4()), required=True,
    )

    #: ([Tag.id], default=[]):
    #: Unique Identifiers for result associated tags
    tags_ids = fields.List(
        fields.UUID(
            description="UUID tag unique identification",
            example=str(uuid4()), required=True,
        ),
        description="UUID tags unique identifications",
        example=[str(uuid4()) for _ in range(2)], load_default=[],
    )


class ResultSearch(Pagination, UploadFilter, Search, Schema):
    pass
