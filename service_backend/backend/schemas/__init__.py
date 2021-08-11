"""Backend package for schemas definition."""
from marshmallow import Schema
from marshmallow.validate import Range

from . import fields


class BaseSchema(Schema):
    class Meta:
        ordered = True


class Pagination(BaseSchema):
    has_next = fields.Boolean(
        description="True if a next page exists",
        required=True, dump_only=True)
    has_prev = fields.Boolean(
        description="True if a previous page exists",
        required=True, dump_only=True)
    next_num = fields.Integer(
        description="Number of the next page",
        required=True, dump_only=True)
    prev_num = fields.Integer(
        description="Number of the previous page",
        required=True, dump_only=True)
    pages = fields.Integer(
        description="The total number of pages",
        required=True, dump_only=True)
    per_page = fields.Integer(
        description="The number of items to be displayed on a page",
        validate=Range(min=1, max=100), missing=100)
    page = fields.Integer(
        description="The return page number (1 indexed)",
        validate=Range(min=1), missing=1)
    total = fields.Integer(
        description="The total number of items matching the query",
        required=True, dump_only=True)
