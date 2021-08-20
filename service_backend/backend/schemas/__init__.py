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
from marshmallow import Schema
from marshmallow.validate import Range

from . import fields


class BaseSchema(Schema):
    """Base schema to control common schema features."""
    class Meta:
        """`marshmallow` options object for BaseSchema."""        
        #: Enforce Order in OpenAPI Specification File
        ordered = True


class Pagination(BaseSchema):
    """Pagination schema to limit the amount of results provided by a method"""

    #: (Bool, required, dump_only):
    #: True if a next page exists.
    has_next = fields.Boolean(
        description="True if a next page exists",
        required=True, dump_only=True)

    #: (Bool, required, dump_only):
    #: True if a previous page exists.
    has_prev = fields.Boolean(
        description="True if a previous page exists",
        required=True, dump_only=True)

    #: (Int, required, dump_only):
    #: Number of the next page.
    next_num = fields.Integer(
        description="Number of the next page",
        required=True, dump_only=True)

    #: (Int, required, dump_only):
    #: Number of the previous page.
    prev_num = fields.Integer(
        description="Number of the previous page",
        required=True, dump_only=True)

    #: (Int, required, dump_only):
    #: The total number of pages
    pages = fields.Integer(
        description="The total number of pages",
        required=True, dump_only=True)

    #: (Int, required, dump_only):
    #: The number of items to be displayed on a page.
    per_page = fields.Integer(
        description="The number of items to be displayed on a page",
        validate=Range(min=1, max=100), missing=100)

    #: (Int, required, dump_only):
    #: The return page number (1 indexed).
    page = fields.Integer(
        description="The return page number (1 indexed)",
        validate=Range(min=1), missing=1)
        
    #: (Int, required, dump_only):
    #: The total number of items matching the query.
    total = fields.Integer(
        description="The total number of items matching the query",
        required=True, dump_only=True)
