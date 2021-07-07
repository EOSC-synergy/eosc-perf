"""Result schemas."""
from backend.benchmarks.schemas import Benchmark_simple
from backend.sites.schemas import Site_simple, Flavor_simple
from backend.tags.schemas import Tag_simple
from marshmallow import Schema, fields, INCLUDE


class Json(Schema):
    class Meta:
        unknown = INCLUDE


class Result(Schema):
    id = fields.UUID(dump_only=True)
    upload_date = fields.Date(dump_only=True)
    json = fields.Dict(required=True)
    benchmark = fields.Nested(Benchmark_simple)
    site = fields.Nested(Site_simple)
    flavor = fields.Nested(Flavor_simple)
    tags = fields.Nested(Tag_simple, many=True)


class EditResult(Schema):
    json = fields.Dict()
    benchmark_id = fields.UUID(load_only=True)
    site_id = fields.UUID(load_only=True)
    flavor_id = fields.UUID(load_only=True)
    tags_ids = fields.List(fields.UUID, load_only=True)


class FilterQueryArgs(Schema):
    #TODO: json = fields.Dict()
    docker_image = fields.String()
    docker_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String())


class CreateQueryArgs(Schema):
    benchmark_id = fields.UUID(required=True)
    site_id = fields.UUID(required=True)
    flavor_id = fields.UUID(required=True)
    tags_ids = fields.List(fields.UUID, missing=[])


class SearchQueryArgs(Schema):
    terms = fields.List(fields.String(), missing=[])
