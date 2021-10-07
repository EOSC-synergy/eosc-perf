"""Backend package for schemas definition. This module is based on the
group of python framework **marshmallow**, an ORM/ODM/framework-agnostic
library for converting complex datatypes, such as objects, to and from
native Python datatypes.

Combined with the flask extension flask_smorest, it allows to generate
the OpenAPI specification schemas based on python class objects.

This objects come into 2 types:
 - Schemas: JSON structures used to operate model instances
 - Arguments: Query arguments to control route method parameters
"""
from uuid import uuid4

from marshmallow import Schema, fields, pre_load, post_dump
from marshmallow.validate import OneOf, Range
from werkzeug.datastructures import ImmutableMultiDict

from ..models.models.reports.submit import ResourceStatus


class BaseSchema(Schema):
    """Base schema to control common schema features."""
    class Meta:
        """`marshmallow` options object for BaseSchema."""
        #: Enforce Order in OpenAPI Specification File
        ordered = True

    @pre_load   # Support PHP and axios query framework
    def process_input(self, data, **kwargs):
        if hasattr(data, 'data'):  # flask_smorest query
            args = data.data._iter_hashitems()
            fixed_args = [(x.replace('[]', ''), y) for x, y in args]
            data.data = ImmutableMultiDict(fixed_args)
        return data

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value is not None
        }


class Pagination(Schema):
    """Pagination schema to limit the amount of results provided by a method"""

    #: (Bool, required, dump_only):
    #: True if a next page exists.
    has_next = fields.Boolean(
        description="True if a next page exists",
        required=True, dump_only=True
    )

    #: (Bool, required, dump_only):
    #: True if a previous page exists.
    has_prev = fields.Boolean(
        description="True if a previous page exists",
        required=True, dump_only=True
    )

    #: (Int, required, dump_only):
    #: Number of the next page.
    next_num = fields.Integer(
        description="Number of the next page",
        required=True, dump_only=True
    )

    #: (Int, required, dump_only):
    #: Number of the previous page.
    prev_num = fields.Integer(
        description="Number of the previous page",
        required=True, dump_only=True
    )

    #: (Int, required, dump_only):
    #: The total number of pages
    pages = fields.Integer(
        description="The total number of pages",
        required=True, dump_only=True
    )

    #: (Int, required, dump_only):
    #: The number of items to be displayed on a page.
    per_page = fields.Integer(
        description="The number of items to be displayed on a page",
        validate=Range(min=1, max=100), required=True,
    )

    #: (Int, required, dump_only):
    #: The return page number (1 indexed).
    page = fields.Integer(
        description="The return page number (1 indexed)",
        validate=Range(min=1), required=True,
    )

    #: (Int, required, dump_only):
    #: The total number of items matching the query.
    total = fields.Integer(
        description="The total number of items matching the query",
        required=True, dump_only=True
    )


class Id(Schema):

    #: (UUID, required, dump_only):
    #: Primary key with an Unique Identifier for the model instance
    id = fields.UUID(
        description="UUID resource unique identification",
        example=str(uuid4()), required=True, dump_only=True,
    )


class Status(Schema):

    #: (Str):
    #: Resource current state (approved, on_review, etc.)
    status = fields.String(
        description="Resource current state",
        validate=OneOf(list(ResourceStatus.__members__)),
        load_default=ResourceStatus.approved.name
    )


class Search(Schema):

    #: ([Text]):
    #: Group of strings to use as general search on model instances
    terms = fields.List(
        fields.String(
            description="Subset expression of a string",
            example="search_term"
        ),
        description="List of terms (string subsets)",
        example=["search_term 1", "search_term 2"],
        load_default=[]
    )

    #: (Str):
    #: Order to return the results separated by coma
    sort_by = fields.String(
        description="Order to return the results (coma separated)",
        example="+upload_datetime", load_default="")


class UploadDatetime(Schema):

    #: (ISO8601):
    #: Upload datetime of the model instance
    upload_datetime = fields.DateTime(
        description="Upload datetime of the referred resource",
        example="2021-09-08 20:37:10.192459",
        required=True, dump_only=True,
    )


class UploadFilter(Schema):

    #: (ISO8601, attribute="upload_datetime"):
    #: Upload datetime of the instance before a specific date
    upload_before = fields.Date(
        description="Results with upload before date (ISO8601)",
        example="2059-03-10",
    )

    #: (ISO8601, attribute="upload_datetime"):
    #: Upload datetime of the instance after a specific date
    upload_after = fields.Date(
        description="Results with upload after date (ISO8601)",
        example="2019-09-07",
    )
