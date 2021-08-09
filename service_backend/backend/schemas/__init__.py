"""Backend package for schemas definition."""
from marshmallow import Schema, fields
from marshmallow.validate import Range


class Pagination(Schema):
    has_next = fields.Boolean(required=True, dump_only=True)
    has_prev = fields.Boolean(required=True, dump_only=True)
    next_num = fields.Integer(required=True, dump_only=True)
    prev_num = fields.Integer(required=True, dump_only=True)
    pages = fields.Integer(required=True, dump_only=True)
    per_page = fields.Integer(validate=Range(min=1, max=100))
    page = fields.Integer(validate=Range(min=1))
    total = fields.Integer(required=True, dump_only=True)
