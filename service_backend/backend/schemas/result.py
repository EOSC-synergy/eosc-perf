"""Result schemas."""
from marshmallow import Schema, fields, INCLUDE


class Json(Schema):
    class Meta:
        unknown = INCLUDE


class ListArgs(Schema):
    #TODO: json = fields.Dict()
    docker_image = fields.String()
    docker_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String())
    upload_before = fields.Date(attribute="before")
    upload_after = fields.Date(attribute="after")


class CreateArgs(Schema):
    benchmark_id = fields.UUID(required=True)
    site_id = fields.UUID(required=True)
    flavor_id = fields.UUID(required=True)
    tags_ids = fields.List(fields.UUID, missing=[])


class SearchArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
