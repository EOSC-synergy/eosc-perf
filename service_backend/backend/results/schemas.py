"""Result schemas."""
from marshmallow import Schema, fields, INCLUDE


class Json(Schema):
    class Meta:
        unknown = INCLUDE


class Result(Schema):
    id = fields.UUID(dump_only=True)
    json = fields.Dict(required=True)
    # uploader_email: Never open to public (GDPR)
    benchmark_image = fields.Function(lambda x: x.benchmark.docker_image)
    benchmark_tag = fields.Function(lambda x: x.benchmark.docker_tag)
    site_name = fields.Function(lambda x: x.site.name)
    flavor_name = fields.Function(lambda x: x.flavor.name)
    tag_names = fields.Function(lambda x: [tag.name for tag in x.tags])


class EditResult(Schema):
    json = fields.Dict()
    benchmark_image = fields.String()
    benchmark_tag = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String())


class FilterQueryArgs(Schema):
    # json = fields.Dict()
    # uploader_email: Never open to public (GDPR)
    benchmark_image = fields.String()
    site_name = fields.String()
    flavor_name = fields.String()
    tag_names = fields.List(fields.String())


class CreateQueryArgs(Schema):
    benchmark_image = fields.String(required=True)
    benchmark_tag = fields.String(required=True)
    site_name = fields.String(required=True)
    flavor_name = fields.String(required=True)
    tag_names = fields.List(fields.String())
